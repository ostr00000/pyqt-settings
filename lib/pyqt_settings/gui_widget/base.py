from typing import TypeVar, Generic

T = TypeVar('T')


class FieldWidget(Generic[T]):
    def getValue(self) -> T:
        raise NotImplementedError

    def setValue(self, value: T):
        raise NotImplementedError
