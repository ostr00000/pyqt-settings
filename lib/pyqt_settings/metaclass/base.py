from typing import Type


class BaseMeta(type):
    @classmethod
    def wrap(mcs, otherClass: Type):
        class Wrapper(mcs, type(otherClass)):
            pass

        return Wrapper
