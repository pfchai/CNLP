# -*- coding: utf-8 -*-

from collections import defaultdict


class Registrable():
    """
    """

    _registry = defaultdict(dict)
    default_implementation = None

    @classmethod
    def register(cls, name, constructor=None, exist_ok=False):
        """
        注册一个类
        """

        registry = Registrable._registry[cls]

        def add_subclass_to_registry(subclass):
            if name in registry:
                if exist_ok:
                    message = (
                        f'{name} 已经被 {registry[name][0].__name__} 注册了，但exist_ok=True'
                        f'所以在这里将会被 {cls.__name__} 覆盖'
                    )
                    print(message)
                else:
                    print(f'{name} 已经被 {registry[name][0].__name__} 注册了')
                    raise
            registry[name] = (subclass, constructor)
            return subclass

        return add_subclass_to_registry

    @classmethod
    def by_name(cls, name):
        subclass, constructor = cls.resolve_class_name(name)
        if not constructor:
            return subclass
        else:
            return getattr(subclass, constructor)

    @classmethod
    def resolve_class_name(cls, name):
        if name in Registrable._registry[cls]:
            subclass, constructor = Registrable._registry[cls][name]
            return subclass, constructor
        else:
            raise

    @classmethod
    def list_available(cls):
        keys = list(Registrable._registry[cls].keys())
        default = cls.default_implementation

        if default is None:
            return keys
        elif default not in keys:
            raise
        else:
            return [default] + [k for k in keys if k != default]



