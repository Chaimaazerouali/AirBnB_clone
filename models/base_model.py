#!/usr/bin/python3
"""Base Model"""


import uuid
from datetime import datetime
import json
from models.__init__ import storage


class BaseModel():
"""Class BaseModel creation"""
def __init__(self, *args, **kwargs):
"""Initializes instance attributes

Args:
- *args: list of arguments
- **kwargs: dict of key-values arguments
"""

if kwargs is not None and kwargs != {}:
for key in kwargs:
if key == "created_at":
self.__dict__["created_at"] = datetime.strptime(
kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
elif key == "updated_at":
self.__dict__["updated_at"] = datetime.strptime(
kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
else:
self.__dict__[key] = kwargs[key]
else:
self.id = str(uuid.uuid4())
self.created_at = datetime.now()
self.updated_at = datetime.now()
storage.new(self)
def __str__(self):
"""Returns official string representation"""
self.id and self.__dict__

n_dic = {}

c_name = "[" + self.__class__.__name__ + "]"
id = " (" + self.id + ")"
dic = " " + str(self.__dict__)
return c_name + id + dic


def save(self):
"""updates the public instance attribute updated_at"""
self.updated_at = datetime.now()
storage.new(self)
storage.save()


def to_dict(self):
"""returns a dictionary containing all keys/values of __dict__"""
n_dic = {}
ms = [attr for attr in dir(self)
if not callable(getattr(self, attr)) and not
attr.startswith("__")]
n_dic["__class__"] = self.__class__.__name__

for key in self.__dict__:
if key == "created_at" or key == "updated_at":
n_dic[key] = self.__dict__[key].isoformat()
else:
n_dic[key] = self.__dict__[key]

for key in self.__class__.__dict__:
if key in ms:
n_dic[key] = self.__class__.__dict__[key]
return n_dic

