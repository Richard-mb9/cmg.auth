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
    'profile': {
        'type': 'string',
        'required': True,
        'allowed': [profile.value for profile in ProfilesEnum]
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