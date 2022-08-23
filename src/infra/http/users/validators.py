from src.utils.enums.profiles import ProfilesEnum


insert_user_validator = {
    'email': {
        'type': 'string',
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        'required': True
    },
    'password': {
        'type': 'string',
        'required': True
    },
    'profiles': {
        'type': 'list',
        'schema': {
            'type': 'string',
        },
        'required': True,
        'allowed': [profile.value for profile in ProfilesEnum]
    }
}

filter_users_validator = {
    'profile': {
        'type': 'string'
    },
    'email': {
        'type': 'string'
    },
    'id': {
        'type': 'string'
    },
    'enable': {
        'type': 'string',
        'allowed': ['false', 'true', 'all']
    },
    'page_size': {
        'type': 'string'
    },
    'page': {
        'type': 'string'
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

update_user_profiles_validator = {

    'profiles': {
        'type': 'list',
        'schema': {
            'type': 'string',
        },
        'allowed': [profile.value for profile in ProfilesEnum]
    }
}


update_user_validator = {
    'enable': {
        'type': 'boolean'
    },
}
