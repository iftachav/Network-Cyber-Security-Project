
class Service(object):

    def create(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def get_many(self, *args, **kwargs):
        pass

    def get_one(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass


class ServiceClassWrapper(Service):

    def __init__(self, class_type, *args, **kwargs):
        self._class_type = class_type(*args, **kwargs)

    def create(self, *args, **kwargs):
        return self._class_type.create(*args, **kwargs)

    def update(self, *args, **kwargs):
        return self._class_type.update(*args, **kwargs)

    def get_many(self, *args, **kwargs):
        return self._class_type.get_many(*args, **kwargs)

    def get_one(self, *args, **kwargs):
        return self._class_type.get_one(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._class_type.delete(*args, **kwargs)


class UserService(Service):
    pass
