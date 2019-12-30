
"""
String hash functions
"""


class FNV:
    """
    A callable interface for FNV hash function
    """

    def __init__(self, offset: int = 0x811c9dc5) -> None:
        self.offset = offset
        self.fnvprime = 0x01000193
        self.fnvsize = 2**32

    def __call__(self, substring) -> int:  # __call__() is basically Scala's apply() method
        if not isinstance(substring, bytes):
            substring = substring.encode("UTF-8", "ignore")

        hval = self.offset

        for byte in substring:
            hval = (hval * self.fnvprime) % self.fnvsize
            hval = hval ^ byte

        return hval


class DJB2:
    """
    A callable interface for DJB2 hash function
    """

    def __init__(self, offset: int = 5381) -> None:
        self.offset = offset

    def __call__(self, substring: str) -> int:

        hval = self.offset

        for character in substring:
            hval = ((hval << 5) + hval) + ord(character)

        return hval & 0xFFFFFFFF


class Jenkins:
    """
    A callable interface for Jenkins hash function
    """

    def __init__(self, offset: int = 2654435769) -> None:
        self.offset = offset

    def __call__(self, substring: str) -> int:
        initial = 0

        length = lenpos = len(substring)

        if length is 0:
            return 0

        a = self.offset
        b = self.offset
        c = initial
        p = 0

        while lenpos >= 12:
            a += (ord(substring[p+0]) + (ord(substring[p+1]) << 8) +
                  (ord(substring[p+2]) << 16) + (ord(substring[p+3]) << 24))
            b += (ord(substring[p+4]) + (ord(substring[p+5]) << 8) +
                  (ord(substring[p+6]) << 16) + (ord(substring[p+7]) << 24))
            c += (ord(substring[p+8]) + (ord(substring[p+9]) << 8) +
                  (ord(substring[p+10]) << 16) + (ord(substring[p+11]) << 24))
            a, b, c = self._mix(a, b, c)
            p += 12
            lenpos -= 12

        c += length
        if lenpos >= 11:
            c += ord(substring[p+10]) << 24
        if lenpos >= 10:
            c += ord(substring[p+9]) << 16
        if lenpos >= 9:
            c += ord(substring[p+8]) << 8

        if lenpos >= 8:
            b += ord(substring[p+7]) << 24
        if lenpos >= 7:
            b += ord(substring[p+6]) << 16
        if lenpos >= 6:
            b += ord(substring[p+5]) << 8
        if lenpos >= 5:
            b += ord(substring[p+4])
        if lenpos >= 4:
            a += ord(substring[p+3]) << 24
        if lenpos >= 3:
            a += ord(substring[p+2]) << 16
        if lenpos >= 2:
            a += ord(substring[p+1]) << 8
        if lenpos >= 1:
            a += ord(substring[p+0])
        a, b, c = self._mix(a, b, c)

        return c

    def _mix(self, a, b, c):
        a &= 0xffffffff
        b &= 0xffffffff
        c &= 0xffffffff
        a -= b
        a -= c
        a ^= (c >> 13)
        a &= 0xffffffff
        b -= c
        b -= a
        b ^= (a << 8)
        b &= 0xffffffff
        c -= a
        c -= b
        c ^= (b >> 13)
        c &= 0xffffffff
        a -= b
        a -= c
        a ^= (c >> 12)
        a &= 0xffffffff
        b -= c
        b -= a
        b ^= (a << 16)
        b &= 0xffffffff
        c -= a
        c -= b
        c ^= (b >> 5)
        c &= 0xffffffff
        a -= b
        a -= c
        a ^= (c >> 3)
        a &= 0xffffffff
        b -= c
        b -= a
        b ^= (a << 10)
        b &= 0xffffffff
        c -= a
        c -= b
        c ^= (b >> 15)
        c &= 0xffffffff

        return a, b, c


"""
Integer hash functions
"""


class Knuth:
    """
    A callable interface for Knuth multiplicative method
    """

    def __init__(self, offset: int = 2654435769) -> None:
        self.offset = offset

    def __call__(self, number: int) -> int:
        return (number*self.offset) % 2**32


class Hmod:
    """
    A callable interface for mod function
    """

    def __init__(self, offset: int = 997) -> None:
        self.offset = offset

    def __call__(self, number: int) -> int:
        return number % self.offset


def normal_hash(number: int) -> int:
    """
    Just an easter egg
    Works like a charm though

    As a side note, this is the hash() function
    implementation of built-in int class

    class int:
        def __hash__(self):
            value = self
            if value == -1:
                value == -2
            return value
    """
    return number
