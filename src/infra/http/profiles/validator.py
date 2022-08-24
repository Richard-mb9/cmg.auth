insert_profile_validator = {
    'name': {
        'type': 'string',
        'required': True
    },
    'role_name': {
        'type': 'string',
    }
}

update_profile_validator = {
    'name': {
        'type': 'string'
    },
    'roles_ids': {
        'type': 'list',
        'schema': {
            'type': 'number'
        }
    },
}

assign_to_rules_validator = {
    'roles_ids': {
        'type': 'list',
        'schema': {
            'type': 'number'
        },
        'required': True
    },
}
