#!/usr/bin/python3
"""
    This is the base class for all classes
    in the AirBnB clone project
"""

from datetime import datetime
from uuid import uuid4
import models


class BaseModel():
    """
        The Parent class for AirBnB clone project
        Methods:
        __init__(self, *args, **kwargs), __str__(self),
        __save(self), __repr__(self), to_dict(self)
    """

    def __init__(self, *args, **kwargs):
        """
            Initialize attributes: uuid4,
            date_created and date_updated
        """

        date_format = '%Y-%m-%dT%H:%M:%S.%f'
        if kwargs:
            for key, value in kwargs.items():
                if "created_at" == key:
                    self.created_at = datetime.strptime(kwargs["created_at"],
                                                        date_format)
                elif "updated_at" == key:
                    self.updated_at = datetime.strptime(kwargs["updated_at"],
                                                        date_format)
                elif "__class__" == key:
                    pass
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """
            Return class name, id, and the dictionary
        """

        return (F"{self.__class__.__name__, self.id, self.__dict__}")

    def __repr__(self):
        """
            Return string representation
        """

        return (self.__str__())

    def save(self):
        """
            Instance method to:
            invoke save() method to a serialized file
        """

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
            Return dictionary of BaseModel with
            string formats of times
        """

        dic = self.__dict__.copy()
        dic["created_at"] = self.created_at.isoformat()
        dic["updated_at"] = self.updated_at.isoformat()
        dic["__class__"] = self.__class__.__name__
        return dic
