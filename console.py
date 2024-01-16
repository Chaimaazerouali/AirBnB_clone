#!/usr/bin/python
"""
Module for HBNBCommand console
"""
import cmd
import re
import shlex
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City

class HBNBCommand(cmd.Cmd):
"""
HBNBCommand console class
"""
prompt = "(hbnb) "
valid_classes = ["BaseModel", "User", "Amenity", "Place", "Review", "State", "City"]

def emptyline(self):
"""
Doesn't do anything on ENTER.
"""
pass

def do_EOF(self, arg):
"""
EOF (Ctrl+D) signal to exit the program.
"""
return True

def do_quit(self, arg):
"""
Quit command to exit the program.
"""
return True

def do_create(self, arg):
"""
Create a new instance of BaseModel and save it to the JSON file.
Usage: create <class_name>
"""
commands = shlex.split(arg)

if not commands:
print("** class name missing **")
elif commands[0] not in self.valid_classes:
print("** class doesn't exist **")
else:
new_instance = eval(f"{commands[0]}()")
storage.save()
print(new_instance.id)

def do_show(self, arg):
"""
Show the string representation of an instance.
Usage: show <class_name> <id>
"""
commands = shlex.split(arg)

if not commands:
print("** class name missing **")
elif commands[0] not in self.valid_classes:
print("** class doesn't exist **")
elif len(commands) < 2:
print("** instance id missing **")
else:
objects = storage.all()
key = f"{commands[0]}.{commands[1]}"

if key in objects:
print(objects[key])
else:
print("** no instance found **")

def do_destroy(self, line):
"""Deletes an instance based on the class name and id"""
object_dict = storage.all()
input_list = line.split()
valid_classes = ["User", "State", "City", "Place", "Amenity", "Review", "BaseModel"]

if not input_list:
print("** class name missing **")
elif input_list[0] not in valid_classes:
print("** class doesn't exist **")
elif len(input_list) < 2:
print("** instance id missing **")
else:
instance_key = f"{input_list[0]}.{input_list[1]}"
if instance_key in object_dict:
object_dict.pop(instance_key, None)
with open(storage._FileStorage__file_path, mode="w", encoding='utf-8') as file:
json.dump(object_dict, file)
else:
print("** no instance found **")

def do_all(self, line):
"""Prints all string representation of all instances."""
if line:
words = line.split()
if words[0] not in storage.classes():
print("** class doesn't exist **")
else:
filtered_list = [str(obj) for key, obj in storage.all().items() if type(obj).__name__ == words[0]]
print(filtered_list)
else:
all_instances = [str(obj) for key, obj in storage.all().items()]
print(all_instances)

def do_count(self, arg):
"""
Counts and retrieves the number of instances of a class
usage: <class name>.count()
"""
objects = storage.all()
commands = shlex.split(arg)

if commands:
class_name = commands[0]
count = sum(1 for obj in objects.values() if obj.__class__.__name__ == class_name)
print(count)
else:
print("** class name missing **")

def default(self, line):
"""Catch commands if nothing else matches then."""
self.process_command(line)

def process_command(self, line):
"""Intercepts commands to test for class.syntax()"""
match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
if not match:
return line

class_name = match.group(1)
method = match.group(2)
args = match.group(3)

match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
if match_uid_and_args:
uid = match_uid_and_args.group(1)
attr_or_dict = match_uid_and_args.group(2)
else:
uid = args
attr_or_dict = False

attr_and_value = ""
if method == "update" and attr_or_dict:
match_dict = re.search('^({.*})$', attr_or_dict)
if match_dict:
self.update_dictionary(class_name, uid, match_dict.group(1))
return ""
match_attr_and_value = re.search('^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
if match_attr_and_value:
attr_and_value = (match_attr_and_value.group(1) or "") + " " + (match_attr_and_value.group(2) or "")
command = f"{method} {class_name} {uid} {attr_and_value}"
self.onecmd(command)
return command

def update_dictionary(self, class_name, uid, s_dict):
"""Helper method for update() with a dictionary."""
s = s_dict.replace("'", '"')
dictionary = json.loads(s)
if not class_name:
print("** class name missing **")
elif class_name not in storage.classes():
print("** class doesn't exist **")
elif not uid:
print("** instance id missing **")
else:
key = f"{class_name}.{uid}"
if key not in storage.all():
print("** no instance found **")
else:
attributes = storage.attributes()[class_name]
for attribute, value in dictionary.items():
if attribute in attributes:
value = attributes[attribute](value)
setattr(storage.all()[key], attribute, value)
storage.all()[key].save()

if __name__ == '__main__':
HBNBCommand().cmdloop()

