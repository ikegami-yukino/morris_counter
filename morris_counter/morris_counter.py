"""Morris Counter

This package provides Morris Counter, which based on the following paper:

Robert Morris. Counting large numbers of events in small registers.
Communications of the ACM, vol. 21, issue 10, pp. 840-842, 1978.
"""
import random
import struct
import sys

try:
    import numpy as np
    USE_NUMPY = True
except ImportError:
    import array
    USE_NUMPY = False
    DTYPE_CONVERT_TABLE = {
        'uint8': 'B',
        'uint16': 'H',
        'uint32': 'I',
        'uint64': 'L',
    }
try:
    import mmh3

    def hashing(item):
        return mmh3.hash(item, signed=False)
except ImportError:
    import hashlib

    def hashing(item):
        return int(hashlib.md5(item).hexdigest(), 16)

MAXIMUM_VALUES = {
    'uint8': 255,
    'uint16': 65535,
    'uint32': 4294967295,
    'uint64': 18446744073709551615,
    'B': 255,
    'H': 65535,
    'I': 4294967295,
    'L': 18446744073709551615
}
STR_FORMAT = '<MorrisCounter; size=%d, radix=%d, max_exponent=%d>'
byteorder = sys.byteorder


class MorrisCounter(object):
    def __init__(self, size=1000000, dtype='uint8', radix=2, seed=3282):
        """MorrisCounter

        Parameters
        ----------
        size : int
            the maximum number of kind of items (n_items > 0)
            (default=1000000)
        dtype : str
            counter's data type ('uint8' is recomended)
            you can use in {'uint8', 'uint16', 'uint32', 'uint64'}
            (default='uint8')
        radix : int
            counter's radix (radix > 1)
            (default=2)
        seed : int
            random seed
            (default=3282)
        """
        if USE_NUMPY:
            self.exponents = np.zeros(size, dtype=dtype)
        else:
            self.exponents = array.array(
                DTYPE_CONVERT_TABLE.get(dtype, dtype), [0]*size)
        self.radix = radix
        self.size = size
        self.max_exponent = MAXIMUM_VALUES[dtype]
        random.seed(seed)

    def __str__(self):
        """Define string format

        Examples
        --------
        >>> mc = MorrisCounter(size=10, dtype='uint8', radix=2)
        >>> print(mc)
        <MorrisCounter; size=10, radix=2, max_exponent=255>
        """
        return STR_FORMAT % (self.size, self.radix, self.max_exponent)

    def _delta(self, idx):
        """Compute delta

        Parameters
        ----------
        idx : int
            index of interest item

        Examples
        --------
        >>> mc = MorrisCounter()
        >>> mc._delta(0)
        1
        """
        if USE_NUMPY:
            return self.radix**-int(self.exponents[idx])
        return self.radix**-self.exponents[idx]

    def _get_idx(self, item):
        """Get index of given item by hashing

        Parameters
        ----------
        item : str, int, float, and so on.
            interest item

        Return
        --------
        idx : int
        """
        if isinstance(item, str):
            item = item.encode()
        elif isinstance(item, int):
            item = item.to_bytes((item.bit_length() + 7) // 8, byteorder)
        elif isinstance(item, float):
            item = struct.pack('d', item)
        elif not isinstance(item, bytes):
            item = bytes(item)
        return hashing(item) % self.size

    def increment(self, item):
        """Increment exponent of given item stochastically

        Parameters
        ----------
        item : str, int, float, and so on.
            interest item

        Examples
        --------
        >>> mc = MorrisCounter(radix=2, seed=3282)
        >>> _ = [mc.increment('ZOC') for _ in range(2000)]
        >>> mc.exponents[mc._get_idx('ZOC')]
        11
        """
        idx = self._get_idx(item)
        self.exponents[idx] += (self.exponents[idx] < self.max_exponent and
                                random.random() < self._delta(idx))

    def count(self, item):
        """Compute estimate count value of given item

        Parameters
        ----------
        item : str, int, float, and so on.
            interest item

        Return
        --------
        estimate_value : int

        Examples
        --------
        >>> mc = MorrisCounter(radix=2, seed=3282)
        >>> _ = [mc.increment('ZOC') for _ in range(2000)]
        >>> mc.count('ZOC')
        2048
        >>> _ = [mc.increment(909) for _ in range(2000)]
        >>> mc.count(909)
        2048
        >>> _ = [mc.increment(0.0909) for _ in range(2000)]
        >>> mc.count(0.0909)
        4096
        >>> _ = [mc.increment({}) for _ in range(2000)]
        >>> mc.count({})
        2048
        """
        idx = self._get_idx(item)
        return self.radix**self.exponents[idx] // (self.radix - 1)
