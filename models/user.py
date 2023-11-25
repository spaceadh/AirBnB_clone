#!/usr/bin/python3
"""
    This modeule defines the user class
    in the HBnB project
"""
from models.base_model import BaseModel
import json


class User(BaseModel):
    """
        A subclass of BaseModel class
        Public class attribute:
            email: (str)
            password: (str)
            first_name: (str)
            last_name: (str)
    """

    email = " "
    password = " "
    first_name = " "
    last_name = " "
