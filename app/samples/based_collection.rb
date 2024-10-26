{
    'uselist': True,
    'argument': 'Addresses',
    '_init_args': _RelationshipArgs(
        secondary=_RelationshipArg(
            name='secondary', 
            argument='entity_address', 
            resolved=Table(
                'entity_address', MetaData(),
                Column('entity_address_id', UUID(), table=<entity_address>, primary_key=True, nullable=False, default=CallableColumnDefault(<function uuid4 at 0x10534cf40>)),
                Column('entity_id', UUID(), table=<entity_address>, nullable=False),
                Column('entity_type', Enum('property', 'contract', 'user', 'role', 'amenities', 'account', 'comapany', 'entityamenities', 'pastrentalhistory', name='entitytypeenum'), table=<entity_address>, nullable=False),
                Column('address_id', UUID(), ForeignKey('address.address_id'), table=<entity_address>, nullable=False),
                Column('emergency_address', Boolean(), table=<entity_address>, default=ScalarElementColumnDefault(False)),
                Column('emergency_address_hash', String(length=128), table=<entity_address>, default=ScalarElementColumnDefault('')),
                Column('created_at', DateTime(timezone=True), table=<entity_address>, nullable=False, default=CallableColumnDefault(<function BaseModel.<lambda> at 0x10515c400>)),
                Column('updated_at', DateTime(timezone=True), table=<entity_address>, nullable=False, onupdate=CallableColumnDefault(<function BaseModel.<lambda> at 0x10515cae0>), default=CallableColumnDefault(<function BaseModel.<lambda> at 0x10515ca40>)),
                schema=None
            )
        ),
        primaryjoin=_RelationshipArg(
            name='primaryjoin',
            argument="and_(User.user_id==EntityAddress.entity_id, EntityAddress.entity_type=='user')",
            resolved=<sqlalchemy.sql.elements.BooleanClauseList object at 0x1078bf740>
        ),
        secondaryjoin=_RelationshipArg(
            name='secondaryjoin',
            argument='and_(EntityAddress.address_id==Addresses.address_id, EntityAddress.emergency_address==False)',
            resolved=<sqlalchemy.sql.elements.BooleanClauseList object at 0x1078bf6e0>
        ),
        order_by=_RelationshipArg(
            name='order_by',
            argument=False,
            resolved=False
        ),
        foreign_keys=_RelationshipArg(
            name='foreign_keys',
            argument=None,
            resolved=None
        ),
        remote_side=_RelationshipArg(
            name='remote_side',
            argument=None,
            resolved=None
        )
    ),
    'post_update': False,
    'viewonly': True,
    'sync_backref': None,
    'lazy': 'selectin',
    'single_parent': False,
    'collection_class': <class 'app.modules.common.models.model_base_collection.BaseModelCollection'>,
    'passive_deletes': False,
    'passive_updates': True,
    'enable_typechecks': True,
    'query_class': None,
    'innerjoin': False,
    'distinct_target_key': None,
    'active_history': False,
    '_legacy_inactive_history_style': False,
    'join_depth': None,
    'omit_join': None,
    'local_remote_pairs': [
        (
            Column('user_id', UUID(), table=<users>, primary_key=True, nullable=False, default=CallableColumnDefault(<function uuid4 at 0x1056ac4a0>)),
            Column('entity_id', UUID(), table=<entity_address>, nullable=False)
        ),
        (
            Column('address_id', UUID(), table=<address>, primary_key=True, nullable=False, default=CallableColumnDefault(<function uuid4 at 0x1053f2700>)),
            Column('address_id', UUID(), ForeignKey('address.address_id'), table=<entity_address>, nullable=False)
        )
    ],
    'load_on_pending': False,
    'comparator_factory': <class 'sqlalchemy.orm.relationships.RelationshipProperty.Comparator'>,
    '_creation_order': 1286,
    '_reverse_property': {<_RelationshipDeclared at 0x105528230; users>},
    '_overlaps': {'entity_addresses', 'properties', 'addresses', 'address'},
    '_cascade': CascadeOptions('merge'),
    'back_populates': 'users',
    'backref': None,
    '_clsregistry_resolvers': (
        <function _resolver.<locals>.resolve_name at 0x107657b00>,
        <function _resolver.<locals>.resolve_arg at 0x107657e20>
    ),
    'entity': <Mapper at 0x1053fe480; Addresses>,
    'target': Table(
        'address', MetaData(),
        Column('address_id', UUID(), table=<address>, primary_key=True, nullable=False, default=CallableColumnDefault(<function uuid4 at 0x1053f2700>)),
        Column('address_type', Enum('billing', 'mailing', name='addresstypeenum'), table=<address>, nullable=False),
        Column('primary', Boolean(), table=<address>, nullable=False, default=ScalarElementColumnDefault(True)),
        Column('address_1', String(length=80), table=<address>, nullable=False),
        Column('address_2', String(length=80), table=<address>, nullable=False),
        Column('address_postalcode', String(length=20), table=<address>, nullable=False),
        Column('city_id', UUID(), ForeignKey('city.city_id'), table=<address>, nullable=False),
        Column('region_id', UUID(), ForeignKey('region.region_id'), table=<address>, nullable=False),
        Column('country_id', UUID(), ForeignKey('country.country_id'), table=<address>, nullable=False),
        Column('created_at', DateTime(timezone=True), table=<address>, nullable=False, default=CallableColumnDefault(<function BaseModel.<lambda> at 0x10515c400>)),
        Column('updated_at', DateTime(timezone=True), table=<address>, nullable=False, onupdate=CallableColumnDefault(<function BaseModel.<lambda> at 0x10515cae0>), default=CallableColumnDefault(<function BaseModel.<lambda> at 0x10515ca40>)),
        schema=None
    ),
    'mapper': <Mapper at 0x1053fe480; Addresses>,
    'order_by': False,
    '_user_defined_foreign_keys': set(),
    'remote_side': {
        Column('entity_type', Enum('property', 'contract', 'user', 'role', 'amenities', 'account', 'comapany', 'entityamenities', 'pastrentalhistory', name='entitytypeenum'), table=<entity_address>, nullable=False),
        Column('entity_id', UUID(), table=<entity_address>, nullable=False),
        Column('emergency_address', Boolean(), table=<entity_address>, default=ScalarElementColumnDefault(False)),
        Column('address_id', UUID(), ForeignKey('address.address_id'), table=<entity_address>, nullable=False)
    },
    '_is_self_referential': False,
    '_join_condition': <sqlalchemy.orm.relationships.JoinCondition object at 0x1078bf770>,
    'primaryjoin': <sqlalchemy.sql.elements.BooleanClauseList object at 0x1078fc4d0>,
    'secondaryjoin': <sqlalchemy.sql.elements.BooleanClauseList object at 0x1078fc530>,
    'secondary': Table(
        'entity_address', MetaData(),
        Column('entity_address_id', UUID(), table=<entity_address>, primary_key=True, nullable=False, default=CallableColumnDefault(<function uuid4 at 0x10534cf40>)),
        Column('entity_id', UUID(), table=<entity_address>, nullable=False),
        Column('entity_type', Enum('property', 'contract', 'user', 'role', 'amenities', 'account', 'comapany', 'entityamenities', 'pastrentalhistory', name='entitytypeenum'), table=<entity_address>, nullable=False),
        Column('address_id', UUID(), ForeignKey('address.address_id'), table=<entity_address>, nullable=False),
        Column('emergency_address', Boolean(), table=<entity_address>, default=ScalarElementColumnDefault(False)),
        Column('emergency_address_hash', String(length=128), table=<entity_address>, default=ScalarElementColumnDefault('')),
        Column('created_at', DateTime(timezone=True), table=<entity_address>, nullable=False, default=CallableColumnDefault(<function BaseModel.<lambda> at 0x10515c400>)),
        Column('updated_at', DateTime(timezone=True), table=<entity_address>, nullable=False, onupdate=CallableColumnDefault(<function BaseModel.<lambda> at 0x10515cae0>), default=CallableColumnDefault(<function BaseModel.<lambda> at 0x10515ca40>)),
        schema=None
    ),
    'direction': <RelationshipDirection.MANYTOMANY: 3>,
    'local_columns': {
        Column('user_id', UUID(), table=<users>, primary_key=True, nullable=False, default=CallableColumnDefault(<function uuid4 at 0x1056ac4a0>))
    },
    'synchronize_pairs': [
        (
            Column('user_id', UUID(), table=<users>, primary_key=True, nullable=False, default=CallableColumnDefault(<function uuid4 at 0x1056ac4a0>)),
            Column('entity_id', UUID(), table=<entity_address>, nullable=False)
        )
    ],
   '_calculated_foreign_keys': {
        Column('entity_type', Enum('property', 'contract', 'user', 'role', 'amenities', 'account', 'comapany', 'entityamenities', 'pastrentalhistory', name='entitytypeenum'), table=<entity_address>, nullable=False),
        Column('entity_id', UUID(), table=<entity_address>, nullable=False),
        Column('emergency_address', Boolean(), table=<entity_address>, default=ScalarElementColumnDefault(False)),
        Column('address_id', UUID(), ForeignKey('address.address_id'), table=<entity_address>, nullable=False)
    },
    'secondary_synchronize_pairs': [
        (
            Column('address_id', UUID(), table=<address>, primary_key=True, nullable=False, default=CallableColumnDefault(<function uuid4 at 0x1053f2700>)),
            Column('address_id', UUID(), ForeignKey('address.address_id'), table=<entity_address>, nullable=False)
        )
    ],
    '_lazy_strategy': <sqlalchemy.orm.strategies.LazyLoader object at 0x107901700>
}