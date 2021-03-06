#!/usr/bin/python3
'''
    Define class FileStorage
'''
import json
import models


class FileStorage:
    '''
        Serializes instances to JSON file and deserializes to JSON file.
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''
            Return the dictionary
        '''
        new_dict = {}
        if cls is None or cls is "":
            return self.__objects
        try:
            if isinstance(cls, str) is True:
                cls = models.classes[cls]
            for k, v in self.__objects.items():
                if isinstance(v, cls):
                    new_dict[k] = v
        except Exception:
            new_dict = {}
        return new_dict

    def new(self, obj):
        '''
            Set in __objects the obj with key <obj class name>.id
            Aguments:
                obj : An instance object.
        '''
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        FileStorage.__objects[key] = value_dict

    def save(self):
        '''
            Serializes __objects attribute to JSON file.
        '''
        objects_dict = {}
        for key, val in FileStorage.__objects.items():
            objects_dict[key] = val.to_dict()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objects_dict, fd)

    def reload(self):
        '''
            Deserializes the JSON file to __objects.
        '''
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                FileStorage.__objects = json.load(fd)
            for key, val in FileStorage.__objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
                FileStorage.__objects[key] = class_name(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''
            Deletes an obj
        '''
        if obj is not None:
            key = str(obj.__class__.__name__) + "." + str(obj.id)
            FileStorage.__objects.pop(key, None)
            self.save()

    def close(self):
        '''
            Deserialize JSON file to objects
        '''
        self.reload()

    def get(self, cls, id):
        '''
            gets a specific 'cls' object with matching 'id'
        '''
        try:
            for value in self.all(cls).values():
                if value.id == id:
                    return value
        except BaseException:
            return None
        return None

    def count(self, cls=None):
        '''
           returns the number of 'cls' object or all the objects
        '''
        if cls is None:
            return len(self.all())
        else:
            return len(self.all(cls))
