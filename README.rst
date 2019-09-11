Morris Counter
==============
|travis| |pyversion| |version| |license|

Memory-efficient probabilistic counter namely Morris Counter.
This module based on the following paper:

- Robert Morris. Counting large numbers of events in small registers. Communications of the ACM, vol. 21, issue 10, pp. 840-842, 1978.

Currently Morris Counter supports Python 3.5 and higher.

Basic idea of Morris Counter is described as follows:

- https://en.wikipedia.org/wiki/Approximate_counting_algorithm
- http://yukinoi.hatenablog.com/entry/2015/11/19/220721 (written in Japanse)

INSTALLATION
==============

::

 $ pip install morris_counter


While the Morris Counter works builtin modules, using third-party package (numpy and mmh3) leads to improve memory-usage and computation time.

::

 $ pip install numpy mmh3

USAGE
============

.. code:: python

  from morris_counter import MorrisCounter

  mc = MorrisCounter(size=1000000, dtype='uint8', radix=2, seed=3282)
  mc.count('ZOC')
  # => 1
  mc.increment('ZOC')
  mc.count('ZOC')
  # => 2
  _ = [mc.increment('ZOC') for _ in range(2000)]
  mc.count('ZOC')
  # => 2048


.. |travis| image:: https://travis-ci.org/ikegami-yukino/morris_counter.svg?branch=master
    :target: https://travis-ci.org/ikegami-yukino/morris_counter
    :alt: travis-ci.org

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/morris_counter.svg

.. |version| image:: https://img.shields.io/pypi/v/morris_counter.svg
    :target: http://pypi.python.org/pypi/morris_counter/
    :alt: latest version

.. |license| image:: https://img.shields.io/pypi/l/morris_counter.svg
    :target: http://pypi.python.org/pypi/morris_counter/
    :alt: license
