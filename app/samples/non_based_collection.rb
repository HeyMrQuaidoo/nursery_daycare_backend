{
    'uselist': False,
    'argument': 'FavoriteProperties',
    '_init_args': _RelationshipArgs(
        secondary=_RelationshipArg(name='secondary', argument=None, resolved=None),
        primaryjoin=_RelationshipArg(name='primaryjoin', argument=None, resolved=None),
        secondaryjoin=_RelationshipArg(name='secondaryjoin', argument=None, resolved=None),
        order_by=_RelationshipArg(name='order_by', argument=False, resolved=False),
        foreign_keys=_RelationshipArg(name='foreign_keys', argument=None, resolved=None),
        remote_side=_RelationshipArg(name='remote_side', argument=None, resolved=None)
    ),
    'post_update': False,
    'viewonly': False,
    'sync_backref': None,
    'lazy': 'selectin',
    'single_parent': False,
    'collection_class': None,
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
            Column('user_id', UUID(), table=<users>, primary_key=True, nullable=False, default=CallableColumnDefault(<function uuid4 at 0x113bac4a0>)),
            Column('user_id', UUID(), ForeignKey('users.user_id'), table=<favorite_properties>, primary_key=True, nullable=False)
        )
    ],
    'load_on_pending': False,
    'comparator_factory': <class 'sqlalchemy.orm.relationships.RelationshipProperty.Comparator'>,
    '_creation_order': 1283,
    '_reverse_property': {<_RelationshipDeclared at 0x113b36d50; users>},
    '_overlaps': (),
    '_cascade': CascadeOptions('merge,save-update'),
    'back_populates': 'users',
    'backref': None,
    '_clsregistry_resolvers': (
        <function _resolver.<locals>.resolve_name at 0x1156093a0>,
        <function _resolver.<locals>.resolve_arg at 0x115609620>
    ),
    'entity': <Mapper at 0x113b1e810; FavoriteProperties>,
    'target': Table(
        'favorite_properties', MetaData(),
        Column('favorite_id', UUID(), table=<favorite_properties>, primary_key=True, nullable=False, default=CallableColumnDefault(<function uuid4 at 0x113b36de0>)),
        Column('user_id', UUID(), ForeignKey('users.user_id'), table=<favorite_properties>, primary_key=True, nullable=False),
        Column('property_unit_assoc_id', UUID(), ForeignKey('property_unit_assoc.property_unit_assoc_id'), table=<favorite_properties>, primary_key=True, nullable=False),
        Column('created_at', DateTime(timezone=True), table=<favorite_properties>, nullable=False, default=CallableColumnDefault(<function BaseModel.<lambda> at 0x1138ac400>)),
        Column('updated_at', DateTime(timezone=True), table=<favorite_properties>, nullable=False, onupdate=CallableColumnDefault(<function BaseModel.<lambda> at 0x1138acae0>), default=CallableColumnDefault(<function BaseModel.<lambda> at 0x1138aca40>)),
        schema=None
    ),
    'mapper': <Mapper at 0x113b1e810; FavoriteProperties>,
    'order_by': False,
    '_user_defined_foreign_keys': set(),
    'remote_side': {
        Column('user_id', UUID(), ForeignKey('users.user_id'), table=<favorite_properties>, primary_key=True, nullable=False)
    },
    '_is_self_referential': False,
    '_join_condition': <sqlalchemy.orm.relationships.JoinCondition object at 0x1156be810>,
    'primaryjoin': <sqlalchemy.sql.elements.BinaryExpression object at 0x1156bec00>,
    'secondaryjoin': None,
    'secondary': None,
    'direction': <RelationshipDirection.ONETOMANY: 1>,
    'local_columns': {
        Column('user_id', UUID(), table=<users>, primary_key=True, nullable=False, default=CallableColumnDefault(<function uuid4 at 0x113bac4a0>))
    },
    'synchronize_pairs': [
        (
            Column('user_id', UUID(), table=<users>, primary_key=True, nullable=False, default=CallableColumnDefault(<function uuid4 at 0x113bac4a0>)),
            Column('user_id', UUID(), ForeignKey('users.user_id'), table=<favorite_properties>, primary_key=True, nullable=False)
        )
    ],
    '_calculated_foreign_keys': {
        Column('user_id', UUID(), ForeignKey('users.user_id'), table=<favorite_properties>, primary_key=True, nullable=False)
    },
    'secondary_synchronize_pairs': [],
    '_dependency_processor': OneToManyDP(User.favorites),
    '_lazy_strategy': <sqlalchemy.orm.strategies.LazyLoader object at 0x11560d0e0>
}
