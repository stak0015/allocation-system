from ctypes import py_object
from typing import TypeVar, Generic

T = TypeVar('T')

class ArrayR(Generic[T]):
    """
    Array implementation imported from FIT1008 Ed Applied Week 3
    """
    def __init__(self, length: int) -> None:
        """ Creates an array of references to objects of the given length
        :complexity: O(length) for best/worst case to initialise to None
        :pre: length > 0
        """
        if length <= 0:
            raise ValueError("Array length should be larger than 0.")
        self.array = (length * py_object)() # initialises the space 
        self.array[:] =  [None for _ in range(length)]

    def __len__(self) -> int:
        """ Returns the length of the array
        :complexity: O(1) 
        """
        return len(self.array)

    def __getitem__(self, index: int) -> T:
        """ Returns the object in position index.
        :complexity: O(1) 
        :pre: index in between 0 and length - self.array[] checks it
        """
        return self.array[index]

    def __setitem__(self, index: int, value: T) -> None:
        """ Sets the object in position index to value
        :complexity: O(1) 
        :pre: index in between 0 and length - self.array[] checks it
        """
        self.array[index] = value