"""single class decorator"""


def singleton(class_: object) -> object:
    """Make class_ be singleton object"""

    class Wrapper(class_):
        """Add singleton functionality"""

        _instance = None
        _sealed = False

        def __new__(cls, *args, **kwargs):  # pylint: disable=unused-argument
            """Check if this class is already instantiated"""
            if Wrapper._instance is None:
                Wrapper._instance = super().__new__(cls)
                Wrapper._sealed = False
            return Wrapper._instance

        def __init__(self, *args, **kwargs):
            if self.__class__._sealed:
                return
            super().__init__(*args, **kwargs)
            self.__class__._sealed = True

    Wrapper.__name__ = class_.__name__
    return Wrapper
