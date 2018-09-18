class Base(object):
    def __repr__(self):
        return '%r' % self.__dict__

    def __eq__(self, other):
        """
        override __eq__ to support == operator for object comparison
        :param other:
        :return:
        """
        if not isinstance(other, self.__class__):
            return False

        for key, value in self.__dict__.items():
            if value != other.__getattribute__(key):
                return False

        return True

    def __ne__(self, other):
        """
        override __ne__ to support != operator for object comparison
        :param other:
        :return:
        """
        return not self == other


class Container(Base):
    """Class to contain runtime attributes"""
    pass


Cache = Container()


class AppInfo(Base):
    app_env = None
    app_product = None
    app_project = None
    app_version = None
    _app_platform = None

    @property
    def app_platform(self):
        return self._app_platform

    @app_platform.setter
    def app_platform(self, value):
        if equals_ignore_case(value, Platform.IOS):
            self._app_platform = Platform.IOS
        elif equals_ignore_case(value, Platform.ANDROID):
            self._app_platform = Platform.ANDROID
        else:
            raise ValueError("Platform '{}' is not supported".format(value))