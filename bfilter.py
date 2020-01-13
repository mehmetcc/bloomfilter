from typing import List, Callable
import math

"""
TODO implement more concise approach for hash value slicing
"""


class BloomFilter:
    """
    Bloom Filter
    An abstraction based on bfilter.BitArray class for querying and referencing
    """

    def __init__(self, size: int, *hash_functions: List[Callable[[str], int]]) -> None:
        self.bit_array = BitArray(size*10)
        # very, very naughty piece of code
        self.bit_size = len(str(size*10))
        self.hash_functions = hash_functions
        self.slice_size = 1
        self.found = 0

    def add_from_list(self, substring_list: List[str]) -> None:
        for substring in substring_list:
            self.add(substring)

    def add(self, substring) -> None:
        for hash_function in self.hash_functions:
            self._add(hash_function, substring)

    def _add(self, hash_function: Callable[[str], int], substring: str) -> None:
        # some dirty integer slicing
        hval = self._first_n_digits(hash_function(
            substring), self.bit_size-self.slice_size)

        # print('Debug - hval: {}'.format(hval))

        self.bit_array[hval] = True

        # print('Debug - {} with hash value {}'.format(hash_function.__str__(), hval))

    def check_from_list(self, substring_list: List[str]) -> None:
        for substring in substring_list:
            self.check(substring)

    def check(self, substring: str) -> None:
        all_check = True

        for hash_function in self.hash_functions:
            check = self._check(hash_function, substring)

            if check is False:
                all_check = False

        if all_check is True:
            self.found += 1

    def _check(self, hash_function: Callable[[str], int], substring: str) -> bool:
        index = self._first_n_digits(hash_function(
            substring), self.bit_size-self.slice_size)

        return False if self.bit_array[index] is False else True

    def _first_n_digits(self, number, n):
        return number // 10 ** (int(math.log(number, 10)) - n + 1)

    def __len__(self) -> int:
        return len(self.bit_array)

    def __repr__(self) -> str:
        return self.bit_array.__repr__()

    def __str__(self) -> str:
        return self.bit_array.__str__()

    def __iter__(self):
        return self.bit_array.__iter__()


class BitArray:
    """
    Container class for Bit Array
    """

    def __init__(self, size: int) -> None:
        """
        As a general rule, whenever you ask yourself "should I inherit or have a member of that type", 
        choose not to inherit. This rule of thumb is known as "favour composition over inheritance".

        https://stackoverflow.com/questions/25328448/should-i-subclass-python-list-or-create-class-with-list-as-attribute
        """
        self.value = 0
        self.length = self.value.bit_length()
        self.size = size

    def __getitem__(self, index: int) -> bool:
        if index > self.size:
            raise KeyError('{} is not a valid index'.format(index))

        return bool((self.value >> index) & 0b01)

    def __setitem__(self, index: int, value: int) -> None:
        # if max size is reached
        if self.size <= self.length:
            # terminate the operation
            return None

        # if value is not valid
        if not value in {False, True}:
            # raise ValueError
            raise ValueError("{} is not a valid value".format(value))

        # https://en.wikipedia.org/wiki/Bit_array#Inversion
        self.value = self.value | 1 << index if value else self.value & ~(
            1 << index)

        # if value is added to the array, select index+1
        # else select length
        self.length = max(self.length, index+1)

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        return "{} {}".format(type(self).__name__, self.__str__())

    def __str__(self) -> str:
        tmp = ''

        # for some reason, couldn't manage to make this
        # work with ''.join()
        for element in self:
            tmp += str(element) + ','

        return '[' + tmp[:-1] + ']'

    def __iter__(self):  # -> list_iterator
        return (self[byte] for byte in range(self.length))
