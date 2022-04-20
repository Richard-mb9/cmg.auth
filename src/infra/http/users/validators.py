insert_user_validator = {
    'email': {
        'type': 'string',
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        'required': True
    },
    'password': {
        'type': 'string',
        'required': True
    }
}

update_password_validator = {
    'old_password': {
        'type': 'string',
        'required': True
    },
    'new_password': {
        'type': 'string',
        'required': True
    }
}


insert_rule_validator = {
    'name': {
        'type': 'string',
        'required': True
    },
}

assign_to_groups_validator = {
    'groups_ids': {
        'type': 'list',
        'schema': {
            'type': 'number'
        },
        'required': True
    },
}