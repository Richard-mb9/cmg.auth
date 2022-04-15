from sqlalchemy import inspect

def object_as_dict(obj):
    if isinstance(obj, list):
        items = []
        for item in obj:
            items.append(object_as_dict(item))
        return items
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}