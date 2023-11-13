#!/usr/bin/python3
"""
   This is the module that implements the cmd
   for the console interface
"""

import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parsingTokenizer(arg):
    curlyBraces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curlyBraces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curlyBraces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curlyBraces.group())
        return retl


class HBNBCommand(cmd.Cmd):

    """Defines the HBNB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            """
            "count": self.do_count,
            """
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        """Usage: create <class> <key 1>=<value 2> <key 2>=<value 2>
        Create a new instance of BaseModel and save it to the JSON file"""

        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")

            kwargs = {}
            for i in range(1, len(my_list)):
                key, value = tuple(my_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                obj = eval(my_list[0])()
            else:
                obj = eval(my_list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Usage: show BaseModel 1234-1234-1234
        Display the string representation of a class instance of a given id.
        """
        argList = parsingTokenizer(arg)
        objDictionary = storage.all()
        if len(argList) == 0:
            print("** class name missing **")
        elif argList[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argList) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argList[0], argList[1]) not in objDictionary:
            print("** no instance found **")
        else:
            print(objDictionary["{}.{}".format(argList[0], argList[1])])

    """
    def do_destroy(self, arg):
        Usage: destroy BaseModel 1234-1234-1234 i.e <id>
            Delete a class instance of a given id.
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in storage.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            obj_key = "{}.{}".format(args[0], args[1])
            if obj_key in objects:
                objects.pop(obj_key)
                storage.save()
            else:
                print("** no instance found **")
    """

    def do_destroy(self, arg):
        """Usage: destroy BaseModel 1234-1234-1234 i.e <id>
            Delete a class instance of a given id."""
        argList = parsingTokenizer(arg)
        objDictionary = storage.all()
        if len(argList) == 0:
            print("** class name missing **")
        elif argList[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argList) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argList[0],
                            argList[1]) not in objDictionary.keys():
            print("** no instance found **")
        else:
            del objDictionary["{}.{}".format(argList[0], argList[1])]
            storage.save()

    """
    def do_all(self, arg):
        Prints string representation of all instances
        args = arg.split()
        objects = storage.all()
        obj_list = []
        if not arg:
            for obj_key in objects:
                obj_list.append(str(objects[obj_key]))
            print(obj_list)
        elif args[0] not in models.storage.all().keys():
            print("** class doesn't exist **")
        else:
            for obj_key in objects:
                if obj_key.startswith(args[0] + "."):
                    obj_list.append(str(objects[obj_key]))
            print(obj_list)
    """

    def do_all(self, arg):
        """Prints string representation of all instances"""
        argList = parsingTokenizer(arg)
        if len(argList) > 0 and argList[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argList) > 0 and argList[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argList) == 0:
                    objl.append(obj.__str__())
            print(objl)

    """
    def do_count(self, arg):
        Usage: <class name>.count().
        Update to be able to retrieve the number of instances of a given class
        argList = parsingTokenizer(arg)
        count = 0
        for obj in storage.all().values():
            if argList[0] == obj.__class__.__name__:
                count += 1
        print(count)
    """

    """
    def do_update(self, arg):

        Usage: update <class> <id> <attribute_name>
        <attribute_value> For example:
        update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.

        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in storage.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            objects = storage.all()
            obj_key = "{}.{}".format(args[0], args[1])
            if obj_key in objects:
                setattr(objects[obj_key], args[2], args[3])
                objects[obj_key].save()
            else:
                print("** no instance found **")
    """

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name>
        <attribute_value> For example:
        update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        """
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""

        argList = parsingTokenizer(arg)
        objdict = storage.all()

        if len(argList) == 0:
            print("** class name missing **")
            return False
        if argList[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argList) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argList[0], argList[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argList) == 2:
            print("** attribute name missing **")
            return False
        if len(argList) == 3:
            try:
                type(eval(argList[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argList) == 4:
            obj = objdict["{}.{}".format(argList[0], argList[1])]
            if argList[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argList[2]])
                obj.__dict__[argList[2]] = valtype(argList[3])
            else:
                obj.__dict__[argList[2]] = argList[3]
        elif type(eval(argList[2])) == dict:
            obj = objdict["{}.{}".format(argList[0], argList[1])]
            for k, v in eval(argList[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
