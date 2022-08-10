insert_profile_validator = {
    'name': {
        'type': 'string',
        'required': True
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