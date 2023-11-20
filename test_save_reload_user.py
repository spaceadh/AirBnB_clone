#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.user import User

all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new User --")
my_user = User()
my_user.first_name = "Betty"
my_user.last_name = "Bar"
my_user.email = "airbnb@mail.com"
my_user.password = "root"
my_user.save()
print(my_user)

print("-- Create a new User 2 --")
my_user2 = User()
my_user2.first_name = "John"
my_user2.email = "airbnb2@mail.com"
my_user2.password = "root"
my_user2.save()
print(my_user2)

print("-- Create a new User 3 --")
my_user3 = User()
my_user3.first_name = "Alvin Wachira"
my_user3.email = "alvinvictor023@gmail.com"
my_user3.password = "Not giving My Password 😑"
my_user3.save()
print(my_user3)

print("-- Create a new User 4 --")
my_user4 = User()
my_user4.first_name = "Layi"
my_user4.last_name = "Wasabi"
my_user4.email = "layiwasabi24@hotmail.com"
my_user4.password = "info_leyan_finfo"
my_user4.save()
print(my_user4)

print("-- Create a new User 5 --")
my_user5 = User()
my_user5.first_name = "Lionel"
my_user5.last_name = "Messi"
my_user5.email = "leomessi@livemail.com"
my_user5.password = "messi_is_infinity_8"
my_user5.save()
print(my_user5)
