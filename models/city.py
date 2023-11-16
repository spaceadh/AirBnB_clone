#!/usr/bin/python3
"""
    This module defines the city class
    in the HBnB project
"""

from models.base_model import BaseModel


class City(BaseModel):
    """
        A subclass of BaseModel class
        Public class attributes:
            state_id: (str) will be State.id
            name: (str)
    """

    state_id = " "
    name = " "
