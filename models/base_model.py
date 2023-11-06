from uuid import uuid4
from datetime import datetime

class BaseModel:
    """Base class for all our classes"""

    def __init__(self, *args, **kwargs):
        """ Deserialize and serialize a class """
        if not kwargs:
            # Initialize if no arguments are passed
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)
        else:
            if 'id' not in kwargs:
                kwargs['id'] = str(uuid4())
            self.id = kwargs['id']

            for key, val in kwargs.items():
                if key == "__class_":
                    continue
                if key == "created_at":
                    self.created_at = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S.%f')
                elif key == "updated_at":
                    self.updated_at = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S.%f')

    def __str__(self):
        """Override the string representation of self"""
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Update the 'updated_at' attribute and save the instance"""
        self.updated_at = datetime.utcnow()
        models.storage.save()  # Assuming you have a save method in your storage module

    def to_dict(self):
        """Return a dictionary representation of self for serialization"""
        temp = {**self.__dict__}
        temp['__class__'] = type(self).__name__
        temp['created_at'] = self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        temp['updated_at'] = self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return temp
