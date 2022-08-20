from sqlalchemy import inspect
from flask import request


def object_as_dict(obj):
    if isinstance(obj, list):
        items = []
        for item in obj:
            items.append(object_as_dict(item))
        return items
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def get_items_to_querys_from_request():
    object = {}
    for key in request.args:
        object[key] = request.args[key]
    return object