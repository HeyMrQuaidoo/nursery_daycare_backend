from asyncio import Lock
from functools import lru_cache
from typing import Dict, Any, Union
from dogpile.cache import make_region
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.collections import InstrumentedList

from app.core.config import settings
from app.modules.common.models.model_registry import registry
from app.modules.common.models.model_association import AssociationProcessor


cache_region = make_region().configure(
    "dogpile.cache.dbm",
    expiration_time=300,
    arguments={"filename": f"{settings.CACHE_PATH}cachefile.dbm"},
)


class BaseModelCollection(InstrumentedList):
    commit_lock = Lock()

    def __init__(self, *args, **kwargs):
        self._config_cache = {}
        self._is_processing = False
        self._parent = kwargs.pop("parent", None)
        self._cache_enabled = kwargs.pop("cache_enabled", True)

        super().__init__(*args, **kwargs)

    def set_parent(self, parent):
        """Method to set or reset the parent dynamically."""
        self._parent = parent

        return self

    def _get_child_config(self, item) -> Dict[str, Union[Any, Dict[str, Any]]]:
        """Retrieve the appropriate configuration for the child item."""
        if not self._parent:
            return {}

        parent_type = getattr(self._parent, "__tablename__", None)
        child_type = getattr(item, "__tablename__", None)

        if not parent_type or not child_type:
            raise ValueError("Cannot determine parent or child type")

        if child_type not in self._config_cache:
            config = registry.get_config().get(parent_type, {}).get(child_type, None)

            if not config:
                raise ValueError(
                    f"No configuration found for parent: {parent_type}, child: {child_type}"
                )

            self._config_cache[child_type] = config

        return self._config_cache[child_type]

    @lru_cache(maxsize=1024)
    def _cached_items(self):
        """Returns the cached items in the collection."""
        return list(self)

    def _generate_cache_key(self):
        """Generate a unique cache key based on parent and relationship."""
        parent_type = "unknown"
        parent_id = "__default__"
        print(f"\t\t\t_generate_cache_key {self._parent} {isinstance(self, list)}")

        # handle case when there's no parent and self is a list
        if not self._parent and isinstance(self, list):
            first_item = self.__getitem__(0) if len(self) > 0 else None
            print(
                f"\t\t\t\t {first_item} {self} {first_item.__class__.__name__.lower()}"
            )
            if first_item:
                parent_type = first_item.__class__.__name__.lower()

        if not self._parent and parent_id != "__default__" and not parent_type:
            print(f"\t\t\treturning {self._parent}")
            return

        # if there's a parent, use the parent's table name and ID
        if self._parent:
            parent_type = getattr(self._parent, "__tablename__", "unknown")
            parent_id = getattr(
                self._parent, f"{self._parent.__tablename__}_id", "__default__"
            )

        # return the formatted cache key
        return f"{parent_type}:{parent_id}"

    def _get_cached_items(self):
        """Get the items from cache, or load and cache them if not present."""
        cache_key = self._generate_cache_key()

        if cache_key:
            print(f"\t\t\tcache key: {cache_key}")
            return cache_region.get_or_create(
                cache_key, lambda: list(InstrumentedList.__iter__(self))
            )
        else:
            print(f"\t\t\telse cache key {cache_key} {self}")
            return list(InstrumentedList.__iter__(self))

    def _invalidate_cache(self):
        """Invalidate the cache when the collection changes."""
        # self._cached_items.cache_clear()
        cache_key = self._generate_cache_key()
        cache_region.delete(cache_key)

    # TODO (DQ): Fix caching issue
    def __iter__(self):
        """Override the iterator to return cached items if enabled."""
        # if self._cache_enabled:
        # return iter(self._cached_items())
        # return iter(self._get_cached_items())
        return super().__iter__()

    def __getitem__(self, index):
        """Override the item getter to use caching."""
        return super().__getitem__(index)

    def remove(self, item):
        """Override remove to clear the cache when an item is removed."""
        self._invalidate_cache()
        super().remove(item)

    def pop(self, index=-1):
        """Override pop to clear the cache when an item is popped from the list."""
        self._invalidate_cache()
        return super().pop(index)

    def clear(self):
        """Override clear to clear the cache when the list is cleared."""
        self._invalidate_cache()
        super().clear()

    def append(self, object) -> None:
        super().append(object)

    async def append_item(self, item, session: AsyncSession = None):
        """Override append to clear the cache when an item is added."""
        self._invalidate_cache()

        # process the item asynchronously
        processor = AssociationProcessor(self._parent, self._get_child_config)
        item = await processor.process_item(item, session)

        # commit the session and refresh the parent to ensure consistency
        await session.commit()
        # await session.refresh(self._parent) # Caused issue with saving child items

        # flush the session to ensure the collection is persisted
        await session.flush()

        return item
