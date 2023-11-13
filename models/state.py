#!/usr/bin/python3
"""This module defines the state class"""

from models.base_model import BaseModel


class State(BaseModel):
    """
    A subclass of BaseModel class
    Public class attribute:
        name: (str)
    """
    name = ""
