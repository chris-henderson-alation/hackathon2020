import json
import inspect

class Validate(object):
    @classmethod
    def validate(cls, value):
        pass

class Optional(object):
    pass

class Default(object):
    pass

class Deserialize(Validate):

    @classmethod
    def optional(cls):
        return type("Optional" + cls.__name__, (cls, Optional), {})

    @classmethod
    def default(cls, default):
        cls.deserialize(default)
        return type("Default" + cls.__name__, (cls, Default), {"defaultValue": default})

    @classmethod
    def deserialize(cls, raw):
        if isinstance(raw, str):
            raw = json.loads(raw)
        elif hasattr(raw, 'read') and callable(getattr(raw, 'read')):
            raw = json.load(raw)
        if isinstance(raw, dict):
            return cls.deserialize_dict(raw)
        elif isinstance(raw, list):
            if not issubclass(cls, ArrayOf):
                raise Exception("expected type {}, got an array".format(cls.__name__))
            raw = [cls.Type.deserialize(v) for v in raw]
        for klazz in [klazz for klazz in cls.mro() if issubclass(klazz, Validate)]:
            klazz.validate(raw)
        return raw
        

    @classmethod
    def deserialize_dict(cls, raw):
        obj = cls()
        for k, v in cls.__dict__.items():
            if not inspect.isclass(v) or not issubclass(v, Deserialize):
                continue
            if k in raw:
                obj.__setattr__(k,  v.deserialize(raw[k]))
            elif v.hasDefault():
                obj.__setattr__(k, v.defaultValue)
            elif not v.required():
                obj.__setattr__(k,  None)
            else:
                raise Exception("expected member {}".format(k))
        return obj


    @classmethod
    def required(cls):
        return not issubclass(cls, Optional)

    @classmethod
    def hasDefault(cls):
        return issubclass(cls, Default)



















































class Primitive(Deserialize):

    @classmethod
    def typeCheck(cls, terminal):
        return isinstance(terminal, cls.Type) or not cls.required() and terminal is None

    @classmethod
    def deserialize(cls, terminal):
        terminal = super(Primitive, cls).deserialize(terminal)
        if cls.typeCheck(terminal):
            return terminal
        raise Exception("wrong type: got {} want {}".format(terminal.__class__.__name__, cls.__name__, ))
    
class Integer(Primitive):
    Type = int

class Float(Primitive):
    Type = float

class Unsigned(Integer):

    @classmethod
    def validate(cls, value):
        if value < 0:
            raise Exception("Unsigned integers may not be negative, received {}".format(value))

class u8(Unsigned):
    @classmethod
    def validate(cls, value):
        if value > 255:
            raise Exception("too big")


class i8(Integer):
    @classmethod
    def validate(cls, value):
        if value > 127 or value < -128:
            raise Exception("no")


class u16(Unsigned):
    @classmethod
    def validate(cls, value):
        if value > 65535:
            raise Exception("too big")


class i16(Integer):
    @classmethod
    def validate(cls, value):
        if value > 32767 or value < -32768:
            raise Exception("no")

class u32(Unsigned):
    @classmethod
    def validate(cls, value):
        if value > 4294967295:
            raise Exception("too big")


class i32(Integer):
    @classmethod
    def validate(cls, value):
        if value > 2147483647 or value < -2147483648:
            raise Exception("no")

class u64(Unsigned):
    @classmethod
    def validate(cls, value):
        if value > 18446744073709551615:
            raise Exception("too big")


class i64(Integer):
    @classmethod
    def validate(cls, value):
        if value > 9223372036854775807 or value < -9223372036854775808:
            raise Exception("no")

class String(Primitive):

    @classmethod
    def typeCheck(cls, terminal):
        return isinstance(terminal, unicode) or isinstance(terminal, str)

class Boolean(Primitive):
    Type = bool 

class ArrayOf(object):

    def __new__(self, target, length=None):
        return type(
            "ArrayOf<{}>".format(target.__name__ ), 
            (Deserialize, ArrayOf), 
            {"Type": target, "validate": ArrayOf.newValidator(length)}
        )

    @staticmethod
    def newValidator(length):
        if length is None:
            @classmethod
            def validator(cls, _):
                pass
        else:
            @classmethod
            def validator(cls, arr):
                if len(arr) != length:
                    raise Exception("wrong size")
        return validator
