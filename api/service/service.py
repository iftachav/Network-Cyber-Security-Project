
class Service(object):
    """
    A service that will be implemented by all of our resources implementations.
    """
    def create(self, *args, **kwargs):
        pass

    def check_session(self, *args, **kwargs):
        # print("in service check_session")
        pass

    def attacks(self, *args, **kwargs):
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
    """
    This class is a wrapper to all of our resource implementations in order to support important feature which is
     'duck typing'.

     https://realpython.com/lessons/duck-typing/
    """
    def __init__(self, class_type, *args, **kwargs):
        """
        Args:
            class_type (Service): any concrete class that inherits Service & has the methods below.
        """
        self._class_type = class_type(*args, **kwargs)

    def check_session(self, *args, **kwargs):
        return self._class_type.check_session(*args, **kwargs)

    def attacks(self, *args, **kwargs):
        return self._class_type.attacks(*args, **kwargs)

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


class ClientService(Service):
    pass


class LoginAttemptsService(Service):
    pass
