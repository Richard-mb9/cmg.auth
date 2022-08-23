from typing import List


class ListUsersResponse(object):
    def __init__(self, object):
        for key in object:
            setattr(self, key, object[key])
    
    id: int
    email: str
    enable: bool
    profiles: List[str]