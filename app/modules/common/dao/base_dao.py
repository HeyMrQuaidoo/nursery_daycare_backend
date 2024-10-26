import asyncio
from pydantic import BaseModel
from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Generic, Union

from app.core.lifespan import get_db
from app.db.dbCrud import DBOperations
from app.core.response import DAOResponse
from app.core.errors import RecordNotFoundException

DBModelType = TypeVar("DBModelType")


class BaseDAO(DBOperations, Generic[DBModelType]):
    def __init__(
        self,
        model: Type[DBModelType],
        excludes: Optional[List[str]] = [],
        detail_mappings: Optional[Dict[str, Any]] = {},
        model_entity_params: Optional[Dict[str, Any]] = {},
        *args,
        **kwargs,
    ):
        self.model = model
        self.excludes = excludes
        self.detail_mappings = detail_mappings

        super().__init__(
            self.model,
            excludes=excludes,
            detail_mappings=detail_mappings,
            model_entity_params=model_entity_params,
            *args,
            **kwargs,
        )
        self.primary_key = kwargs.get("primary_key")

    def extract_model_data(
        self, data: dict, schema: Type[BaseModel], nested_key: Optional[str] = None
    ) -> Union[List[dict] | dict]:
        """
        Extracts model data from a dictionary based on the provided schema.

        Args:
            data (dict): The dictionary containing the data to be extracted.
            schema (Type[BaseModel]): The schema class to use for extracting the data.
            nested_key (Optional[str], optional): The key in the dictionary representing nested data.

        Returns:
            Union[List[dict], dict]: The extracted data.
        """
        data = data.get(nested_key, {}) if nested_key else data

        if not data:
            return None

        if isinstance(data, list):
            return [
                {key: item[key] for key in item if key in schema.model_fields}
                for item in data
            ]

        return {key: data[key] for key in data if key in schema.model_fields}

    def exclude_keys(self, original_dict: Dict, keys_to_exclude: List[str]):
        return {k: v for k, v in original_dict.items() if k not in keys_to_exclude}

    async def validate_ids(
        self,
        db_session: AsyncSession,
        validations: List[Tuple[DBOperations, Dict]],
    ) -> Union[None, DAOResponse]:
        """not used: validate ids"""
        queries = [
            dao.query(db_session, filters=filters, single=True)
            for dao, filters in validations
        ]
        results = await asyncio.gather(*queries)

        for result, (dao, filters) in zip(results, validations):
            if not result:
                key = list(filters.keys())[0]

                raise RecordNotFoundException(dao.model.__name__, key)

        return None

    async def build_pagination_meta(
        self,
        request: Request,
        limit: int,
        offset: int,
        db_session: AsyncSession = Depends(get_db),
    ) -> Dict[str, Any]:
        base_url = request.url.path
        total = await self.query_count(db_session=db_session)

        next_offset = offset + limit
        previous_offset = max(0, offset - limit)

        meta = {
            "total": total,
            "limit": limit,
            "offset": offset,
            "next": f"{base_url}?limit={limit}&offset={next_offset}"
            if next_offset < total
            else None,
            "previous": f"{base_url}?limit={limit}&offset={previous_offset}"
            if offset > 0
            else None,
        }

        return meta
