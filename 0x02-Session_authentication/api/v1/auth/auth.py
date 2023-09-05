#!/usr/bin/env python3
"""Auth module"""
from flask import request
from typing import List


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth method"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        n_path = len(path)
        if not n_path:
            return True

        s_path = True if path[n_path - 1] == '/' else False
        tmp = s_path

        if not s_path:
            tmp += '/'

        for i in excluded_paths:
            k = len(i)
            if not k:
                continue

            if i[k - 1] != '*':
                if tmp == i:
                    return False
            else:
                if i[:-1] == path[:k - 1]:
                    return False
        return True

def authorization_header(self, request=None) -> str:
    """Auth header method"""
    if request is None:
        return None
    return request.headers.get("Authorization", None)

def current_user(self, request=None):
    """Current user metod"""
    return None
