#!/usr/bin/env python3
"""Encrypt passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """is valid passwd"""
    valid = False
    if bcrypt.checkpw(password.encode(), hashed_password):
        vaild = True
    return valid
