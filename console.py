#!/usr/bin/python3
"""
   This module implements the cmd
   for the console interface
"""

import cmd as c
import re as r
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def Parse_Token(arg):
    curlyBraces = r.search(r"\{(.*?)\}", arg)
    brackets = r.search(r"\[(.*?)\]", arg)
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


class HBNBCommand(c.Cmd):
    """
        Defines the HBnB commandline interpreter.
        Attributes:
            prompt (str): The user command prompt.
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
        """
            Do nothing if an empty line
            is enetered to the prompt.
        """

        pass

    def default(self, arg):
        """
            The Default built-in behavior for cmd module
            when the input entered is invalid
        """

        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = r.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = r.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = F"{(argl[0], command[1])}"
                    return argdict[command[0]](call)
        print(F"*** Unknown syntax: {arg}")
        return False

    def do_quit(self, arg):
        """
            The Quit command exits the program
            when entered into the prompt
        """
        return True

    def do_EOF(self, arg):
        """
            The EOF signal exits the program
            when Ctrl + D is entered into the prompt
        """

        print(" ")
        return True

    def do_create(self, arg):
        """
            Usage: create <class> <key 1>=<value 2>
            <key 2>=<value 2>
            This creates a new instance of BaseModel and save
            it to the JSON file
        """

        try:
            if not arg:
                raise SyntaxError()
            my_list = arg.split(" ")

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
            print(F"** class name missing **")
        except NameError:
            print(F"** class doesn't exist **")

    def do_show(self, arg):
        """
            Usage: show <class> <id> or <class>.show(<id>)
            This displays the string representation of a class
            instance of a given id.
        """
        argList = Parse_Token(arg)
        objDictionary = storage.all()
        if len(argList) == 0:
            print(F"** class name missing **")
        elif argList[0] not in HBNBCommand.__classes:
            print(F"** class doesn't exist **")
        elif len(argList) == 1:
            print(F"** instance id missing **")
        elif F"{argList[0]}.{argList[1]}" not in objDictionary:
            print(F"** no instance found **")
        else:
            print(objDictionary[F"{argList[0]}.{argList[1]}"])

    def do_destroy(self, arg):
        """
            Usage: destroy <class> <id> or <class>.destroy(<id>)
            This deletes a class instance of a given id.
        """
        argList = Parse_Token(arg)
        objDictionary = storage.all()
        if len(argList) == 0:
            print(F"** class name missing **")
        elif argList[0] not in HBNBCommand.__classes:
            print(F"** class doesn't exist **")
        elif len(argList) == 1:
            print(F"** instance id missing **")
        elif F"{argList[0]}.{argList[1]}" not in objDictionary.keys():
            print(F"** no instance found **")
        else:
            del objDictionary[F"{argList[0]}.{argList[1]}"]
            storage.save()

    def do_all(self, arg):
        """
            Usage: all or all <class> or <class>.all()
            Display string representations of all instances
            of a given class.
            If no class is specified, displays all
            instantiated objects
        """
        argList = Parse_Token(arg)
        if len(argList) > 0 and argList[0] not in HBNBCommand.__classes:
            print(F"** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argList) > 0 and argList[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argList) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """
            Usage: <class name>.count().
            This retrieves the number of instances of a
            given class
        """
        argList = Parse_Token(arg)
        count = 0
        for obj in storage.all().values():
            if argList[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """
            Usage: update <class> <id> <attribute_name>
            <attribute_value> or
            <class>.update(<id>, <attribute_name>,
            <attribute_value>) or
            <class>.update(<id>, <dictionary>)
            This updates a class instance of a given id by
            adding or updating a given attribute
            key/value pair or dictionary.
        """

        argList = Parse_Token(arg)
        objdict = storage.all()

        if len(argList) == 0:
            print(F"** class name missing **")
            return False
        if argList[0] not in HBNBCommand.__classes:
            print(F"** class doesn't exist **")
            return False
        if len(argList) == 1:
            print(F"** instance id missing **")
            return False
        if F"{argList[0]}.{argList[1]}" not in objdict.keys():
            print(F"** no instance found **")
            return False
        if len(argList) == 2:
            print(F"** attribute name missing **")
            return False
        if len(argList) == 3:
            try:
                type(eval(argList[2])) != dict
            except NameError:
                print(F"** value missing **")
                return False

        if len(argList) == 4:
            obj = objdict[F"{argList[0]}.{argList[1]}"]
            if argList[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argList[2]])
                obj.__dict__[argList[2]] = valtype(argList[3])
            else:
                obj.__dict__[argList[2]] = argList[3]
        elif type(eval(argList[2])) == dict:
            obj = objdict[F"{argList[0]}.{argList[1]}"]
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
