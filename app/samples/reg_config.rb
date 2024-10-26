{
    'users': {
        'roles': {
            'association_class': <class 'app.modules.auth.models.user_role.UserRoles'>,
            'entity_param_key': 'roles',
            'entity_params_attr': {'user_id': 'user_id'},
            'item_params_attr': {'role_id': 'role_id', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'company': {
            'association_class': <class 'app.modules.associations.models.entity_company.EntityCompany'>,
            'entity_param_key': 'company',
            'entity_params_attr': {'entity_id': 'user_id', 'entity_type': 'user'},
            'item_params_attr': {'entity_company_id': 'entity_company_id', 'company_id': 'company_id', 'company_type': 'company_type', 'entity_type': 'entity_type', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'favorites': {
            'association_class': <class 'app.modules.auth.models.user_favorites.FavoriteProperties'>,
            'entity_param_key': 'favorites',
            'entity_params_attr': {'user_id': 'user_id'},
            'item_params_attr': {'favorite_id': 'favorite_id', 'property_unit_assoc_id': 'property_unit_assoc_id', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'interactions_as_user': {
            'association_class': <class 'app.modules.auth.models.user_interactions.UserInteractions'>,
            'entity_param_key': 'interactions_as_user',
            'entity_params_attr': {'user_id': 'user_id', 'employee_id': 'user_id'},
            'item_params_attr': {'user_interaction_id': 'user_interaction_id', 'property_unit_assoc_id': 'property_unit_assoc_id', 'contact_time': 'contact_time', 'contact_details': 'contact_details', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'interactions_as_employee': {
            'association_class': <class 'app.modules.auth.models.user_interactions.UserInteractions'>,
            'entity_param_key': 'interactions_as_employee',
            'entity_params_attr': {'user_id': 'user_id', 'employee_id': 'user_id'},
            'item_params_attr': {'user_interaction_id': 'user_interaction_id', 'property_unit_assoc_id': 'property_unit_assoc_id', 'contact_time': 'contact_time', 'contact_details': 'contact_details', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'address': {
            'association_class': <class 'app.modules.associations.models.entity_address.EntityAddress'>,
            'entity_param_key': 'address',
            'entity_params_attr': {'entity_id': 'user_id', 'entity_type': 'user'},
            'item_params_attr': {'entity_address_id': 'entity_address_id', 'entity_type': 'entity_type', 'address_id': 'address_id', 'emergency_address': 'emergency_address', 'emergency_address_hash': 'emergency_address_hash', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'emergency_addresses': {
            'association_class': <class 'app.modules.associations.models.entity_address.EntityAddress'>,
            'entity_param_key': 'emergency_addresses',
            'entity_params_attr': {'entity_id': 'user_id', 'entity_type': 'user'},
            'item_params_attr': {'entity_address_id': 'entity_address_id', 'entity_type': 'entity_type', 'address_id': 'address_id', 'emergency_address': 'emergency_address', 'emergency_address_hash': 'emergency_address_hash', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'accounts': {
            'association_class': <class 'app.modules.associations.models.entity_accounts.EntityAccount'>,
            'entity_param_key': 'accounts',
            'entity_params_attr': {'entity_id': 'user_id', 'entity_type': 'user'},
            'item_params_attr': {'entity_account_id': 'entity_account_id', 'account_id': 'account_id', 'account_type': 'account_type', 'entity_type': 'entity_type', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'documents': {
            'association_class': <class 'app.modules.resources.models.document.Document'>,
            'entity_param_key': 'documents',
            'entity_params_attr': {'uploaded_by': 'user_id'},
            'item_params_attr': {'document_number': 'document_number', 'name': 'name', 'content_url': 'content_url', 'content_type': 'content_type', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'transaction_as_client_offered': {
            'association_class': <class 'app.modules.billing.models.transaction.Transaction'>,
            'entity_param_key': 'transaction_as_client_offered',
            'entity_params_attr': {'client_offered': 'user_id', 'client_requested': 'user_id'},
            'item_params_attr': {'transaction_id': 'transaction_id', 'transaction_number': 'transaction_number', 'payment_type_id': 'payment_type_id', 'transaction_date': 'transaction_date', 'transaction_details': 'transaction_details', 'transaction_type': 'transaction_type_id', 'transaction_status': 'transaction_status', 'invoice_number': 'invoice_number', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'transaction_as_client_requested': {
            'association_class': <class 'app.modules.billing.models.transaction.Transaction'>,
            'entity_param_key': 'transaction_as_client_requested',
            'entity_params_attr': {'client_offered': 'user_id', 'client_requested': 'user_id'},
            'item_params_attr': {'transaction_id': 'transaction_id', 'transaction_number': 'transaction_number', 'payment_type_id': 'payment_type_id', 'transaction_date': 'transaction_date', 'transaction_details': 'transaction_details', 'transaction_type': 'transaction_type_id', 'transaction_status': 'transaction_status', 'invoice_number': 'invoice_number', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'maintenance_requests': {
            'association_class': <class 'app.modules.communication.models.maintenance_request.MaintenanceRequest'>,
            'entity_param_key': 'maintenance_requests',
            'entity_params_attr': {'requested_by': 'user_id'},
            'item_params_attr': {'id': 'id', 'task_number': 'task_number', 'title': 'title', 'description': 'description', 'status': 'status', 'priority': 'priority', 'property_unit_assoc_id': 'property_unit_assoc_id', 'scheduled_date': 'scheduled_date', 'completed_date': 'completed_date', 'is_emergency': 'is_emergency', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'tours': {
            'association_class': <class 'app.modules.communication.models.tour_bookings.Tour'>,
            'entity_param_key': 'tours',
            'entity_params_attr': {'user_id': 'user_id'},
            'item_params_attr': {'tour_booking_id': 'tour_booking_id', 'name': 'name', 'email': 'email', 'phone_number': 'phone_number', 'tour_type': 'tour_type', 'status': 'status', 'tour_date': 'tour_date', 'property_unit_assoc_id': 'property_unit_assoc_id', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'events': {
            'association_class': <class 'app.modules.communication.models.calendar_event.CalendarEvent'>,
            'entity_param_key': 'events',
            'entity_params_attr': {'organizer_id': 'user_id'},
            'item_params_attr': {'id': 'id', 'event_id': 'event_id', 'title': 'title', 'description': 'description', 'status': 'status', 'event_type': 'event_type', 'event_start_date': 'event_start_date', 'event_end_date': 'event_end_date', 'completed_date': 'completed_date', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'property_assignments': {
            'association_class': <class 'app.modules.properties.models.property_assignment.PropertyAssignment'>,
            'entity_param_key': 'property_assignments',
            'entity_params_attr': {'user_id': 'user_id'},
            'item_params_attr': {'property_assignment_id': 'property_assignment_id', 'property_unit_assoc_id': 'property_unit_assoc_id', 'assignment_type': 'assignment_type', 'date_from': 'date_from', 'date_to': 'date_to', 'notes': 'notes', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'assigned_properties': {
            'association_class': <class 'app.modules.properties.models.property_assignment.PropertyAssignment'>,
            'entity_param_key': 'assigned_properties',
            'entity_params_attr': {'user_id': 'user_id'},
            'item_params_attr': {'property_assignment_id': 'property_assignment_id', 'property_unit_assoc_id': 'property_unit_assoc_id', 'assignment_type': 'assignment_type', 'date_from': 'date_from', 'date_to': 'date_to', 'notes': 'notes', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'assigned_units': {
            'association_class': <class 'app.modules.properties.models.property_assignment.PropertyAssignment'>,
            'entity_param_key': 'assigned_units',
            'entity_params_attr': {'user_id': 'user_id'},
            'item_params_attr': {'property_assignment_id': 'property_assignment_id', 'property_unit_assoc_id': 'property_unit_assoc_id', 'assignment_type': 'assignment_type', 'date_from': 'date_from', 'date_to': 'date_to', 'notes': 'notes', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'owned_properties': {
            'association_class': <class 'app.modules.properties.models.property_assignment.PropertyAssignment'>,
            'entity_param_key': 'owned_properties',
            'entity_params_attr': {'user_id': 'user_id'},
            'item_params_attr': {'property_assignment_id': 'property_assignment_id', 'property_unit_assoc_id': 'property_unit_assoc_id', 'assignment_type': 'assignment_type', 'date_from': 'date_from', 'date_to': 'date_to', 'notes': 'notes', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'sent_messages': {
            'association_class': <class 'app.modules.communication.models.message.Message'>,
            'entity_param_key': 'sent_messages',
            'entity_params_attr': {'sender_id': 'user_id'},
            'item_params_attr': {'message_id': 'message_id', 'subject': 'subject', 'message_body': 'message_body', 'parent_message_id': 'message_id', 'thread_id': 'message_id', 'is_draft': 'is_draft', 'is_notification': 'is_notification', 'is_reminder': 'is_reminder', 'is_scheduled': 'is_scheduled', 'is_read': 'is_read', 'date_created': 'date_created', 'scheduled_date': 'scheduled_date', 'next_remind_date': 'next_remind_date', 'reminder_frequency_id': 'reminder_frequency_id', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'received_messages': {
            'association_class': <class 'app.modules.communication.models.message_recipient.MessageRecipient'>,
            'entity_param_key': 'received_messages',
            'entity_params_attr': {'recipient_id': 'user_id'},
            'item_params_attr': {'id': 'id', 'recipient_group_id': 'property_unit_assoc_id', 'message_id': 'message_id', 'is_read': 'is_read', 'msg_send_date': 'msg_send_date', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'client_under_contract': {
            'association_class': <class 'app.modules.contract.models.under_contract.UnderContract'>,
            'entity_param_key': 'client_under_contract',
            'entity_params_attr': {'client_id': 'user_id', 'employee_id': 'user_id'},
            'item_params_attr': {'under_contract_id': 'under_contract_id', 'property_unit_assoc_id': 'property_unit_assoc_id', 'contract_status': 'contract_status', 'contract_number': 'contract_number', 'start_date': 'start_date', 'end_date': 'end_date', 'next_payment_due': 'next_payment_due', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'employee_under_contract': {
            'association_class': <class 'app.modules.contract.models.under_contract.UnderContract'>,
            'entity_param_key': 'employee_under_contract',
            'entity_params_attr': {'client_id': 'user_id', 'employee_id': 'user_id'},
            'item_params_attr': {'under_contract_id': 'under_contract_id', 'property_unit_assoc_id': 'property_unit_assoc_id', 'contract_status': 'contract_status', 'contract_number': 'contract_number', 'start_date': 'start_date', 'end_date': 'end_date', 'next_payment_due': 'next_payment_due', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'rental_history': {
            'association_class': <class 'app.modules.properties.models.rental_history.PastRentalHistory'>,
            'entity_param_key': 'rental_history',
            'entity_params_attr': {'user_id': 'user_id'},
            'item_params_attr': {'rental_history_id': 'rental_history_id', 'start_date': 'start_date', 'end_date': 'end_date', 'property_owner_name': 'property_owner_name', 'property_owner_email': 'property_owner_email', 'property_owner_mobile': 'property_owner_mobile', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'invoice_as_issued_by_user': {
            'association_class': <class 'app.modules.billing.models.invoice.Invoice'>,
            'entity_param_key': 'invoice_as_issued_by_user',
            'entity_params_attr': {'issued_by': 'user_id', 'issued_to': 'user_id'},
            'item_params_attr': {'id': 'id', 'invoice_number': 'invoice_number', 'invoice_details': 'invoice_details', 'invoice_amount': 'invoice_amount', 'due_date': 'due_date', 'date_paid': 'date_paid', 'invoice_type': 'invoice_type', 'status': 'status', 'transaction_number': 'transaction_number', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'invoice_as_issued_to_user': {
            'association_class': <class 'app.modules.billing.models.invoice.Invoice'>,
            'entity_param_key': 'invoice_as_issued_to_user',
            'entity_params_attr': {'issued_by': 'user_id', 'issued_to': 'user_id'},
            'item_params_attr': {'id': 'id', 'invoice_number': 'invoice_number', 'invoice_details': 'invoice_details', 'invoice_amount': 'invoice_amount', 'due_date': 'due_date', 'date_paid': 'date_paid', 'invoice_type': 'invoice_type', 'status': 'status', 'transaction_number': 'transaction_number', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        }
    },
    'role': {
        'users': {
            'association_class': <class 'app.modules.auth.models.user_role.UserRoles'>,
            'entity_param_key': 'users',
            'entity_params_attr': {'role_id': 'role_id'},
            'item_params_attr': {'user_id': 'user_id', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'permissions': {
            'association_class': <class 'app.modules.auth.models.role_permissions.RolePermissions'>,
            'entity_param_key': 'permissions',
            'entity_params_attr': {'role_id': 'role_id'},
            'item_params_attr': {'permission_id': 'permission_id', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'address': {
            'association_class': <class 'app.modules.associations.models.entity_address.EntityAddress'>,
            'entity_param_key': 'address',
            'entity_params_attr': {'entity_id': 'role_id', 'entity_type': 'role'},
            'item_params_attr': {'entity_address_id': 'entity_address_id', 'entity_type': 'entity_type', 'address_id': 'address_id', 'emergency_address': 'emergency_address', 'emergency_address_hash': 'emergency_address_hash', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        }
    },
    'address': {
        'city': {
            'association_class': <class 'app.modules.address.models.city.City'>,
            'entity_param_key': 'city',
            'entity_params_attr': {},
            'item_params_attr': {'city_id': 'city_id', 'region_id': 'region_id', 'city_name': 'city_name', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'region': {
            'association_class': <class 'app.modules.address.models.region.Region'>,
            'entity_param_key': 'region',
            'entity_params_attr': {},
            'item_params_attr': {'region_id': 'region_id', 'country_id': 'country_id', 'region_name': 'region_name', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'country': {
            'association_class': <class 'app.modules.address.models.country.Country'>,
            'entity_param_key': 'country',
            'entity_params_attr': {},
            'item_params_attr': {'country_id': 'country_id', 'country_name': 'country_name', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'entity_addresses': {
            'association_class': <class 'app.modules.associations.models.entity_address.EntityAddress'>,
            'entity_param_key': 'entity_addresses',
            'entity_params_attr': {'address_id': 'address_id'},
            'item_params_attr': {'entity_address_id': 'entity_address_id', 'entity_type': 'entity_type', 'emergency_address': 'emergency_address', 'emergency_address_hash': 'emergency_address_hash', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'users': {
            'association_class': <class 'app.modules.associations.models.entity_address.EntityAddress'>,
            'entity_param_key': 'users',
            'entity_params_attr': {'address_id': 'address_id'},
            'item_params_attr': {'entity_address_id': 'entity_address_id', 'entity_type': 'entity_type', 'emergency_address': 'emergency_address', 'emergency_address_hash': 'emergency_address_hash', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'roles': {
            'association_class': <class 'app.modules.associations.models.entity_address.EntityAddress'>,
            'entity_param_key': 'roles',
            'entity_params_attr': {'address_id': 'address_id'},
            'item_params_attr': {'entity_address_id': 'entity_address_id', 'entity_type': 'entity_type', 'emergency_address': 'emergency_address', 'emergency_address_hash': 'emergency_address_hash', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'accounts': {
            'association_class': <class 'app.modules.associations.models.entity_address.EntityAddress'>,
            'entity_param_key': 'accounts',
            'entity_params_attr': {'address_id': 'address_id'},
            'item_params_attr': {'entity_address_id': 'entity_address_id', 'entity_type': 'entity_type', 'emergency_address': 'emergency_address', 'emergency_address_hash': 'emergency_address_hash', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'rental_history': {
            'association_class': <class 'app.modules.associations.models.entity_address.EntityAddress'>,
            'entity_param_key': 'rental_history',
            'entity_params_attr': {'address_id': 'address_id'},
            'item_params_attr': {'entity_address_id': 'entity_address_id', 'entity_type': 'entity_type', 'emergency_address': 'emergency_address', 'emergency_address_hash': 'emergency_address_hash', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'properties': {
            'association_class': <class 'app.modules.associations.models.entity_address.EntityAddress'>,
            'entity_param_key': 'properties',
            'entity_params_attr': {'address_id': 'address_id'},
            'item_params_attr': {'entity_address_id': 'entity_address_id', 'entity_type': 'entity_type', 'emergency_address': 'emergency_address', 'emergency_address_hash': 'emergency_address_hash', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        }
    },
    'past_rental_history': {
        'user': {
            'association_class': <class 'app.modules.auth.models.user.User'>,
            'entity_param_key': 'user',
            'entity_params_attr': {},
            'item_params_attr': {'user_id': 'user_id', 'first_name': 'first_name', 'last_name': 'last_name', 'email': 'email', 'phone_number': 'phone_number', 'password': 'password', 'identification_number': 'identification_number', 'photo_url': 'photo_url', 'gender': 'gender', 'date_of_birth': 'date_of_birth', 'login_provider': 'login_provider', 'reset_token': 'reset_token', 'verification_token': 'verification_token', 'is_subscribed_token': 'is_subscribed_token', 'is_disabled': 'is_disabled', 'is_verified': 'is_verified', 'is_subscribed': 'is_subscribed', 'current_login_time': 'current_login_time', 'last_login_time': 'last_login_time', 'employer_name': 'employer_name', 'occupation_status': 'occupation_status', 'occupation_location': 'occupation_location', 'emergency_contact_name': 'emergency_contact_name', 'emergency_contact_email': 'emergency_contact_email', 'emergency_contact_relation': 'emergency_contact_relation', 'emergency_contact_number': 'emergency_contact_number', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        },
        'address': {
            'association_class': <class 'app.modules.associations.models.entity_address.EntityAddress'>,
            'entity_param_key': 'address',
            'entity_params_attr': {'entity_id': 'rental_history_id', 'entity_type': 'pastrentalhistory'},
            'item_params_attr': {'entity_address_id': 'entity_address_id', 'entity_type': 'entity_type', 'address_id': 'address_id', 'emergency_address': 'emergency_address', 'emergency_address_hash': 'emergency_address_hash', 'created_at': 'created_at', 'updated_at': 'updated_at'}
        }
    }
}
