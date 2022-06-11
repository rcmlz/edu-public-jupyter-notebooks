#!/usr/bin/env python
# -*- coding: utf-8 -*-

def nord(x, y):
    """
    Berechnet Koordinaten in Nord

    >>> nord(2, 7)
    (2, 5)
    >>> nord(3, 7)
    (3, 5)
    >>> nord(4, 6)
    (4, 4)
    >>> nord(3, 8)
    (3, 6)

    """
    if isinstance(x, int) and isinstance(y, int):
        return (x, y-2)

def sued(x, y):
    """
    Berechnet Koordinaten in Sued

    >>> sued(2, 7)
    (2, 9)
    >>> sued(3, 7)
    (3, 9)
    >>> sued(4, 6)
    (4, 8)
    >>> sued(3, 8)
    (3, 10)


    """
    if isinstance(x, int) and isinstance(y, int):
        return (x, y+2)

def nord_west(x, y):
    """
    Berechnet Koordinaten in Nord-West

    >>> nord_west(2, 7)
    (2, 6)
    >>> nord_west(3, 7)
    (3, 6)
    >>> nord_west(3, 8)
    (2, 7)
    >>> nord_west(4, 6)
    (3, 5)
    >>> nord_west(4, 2)
    (3, 1)

    """
    if isinstance(x, int) and isinstance(y, int):
        sum_is_even = (x + y) % 2
        x_is_even = x % 2
        if (x_is_even and sum_is_even) or (not x_is_even and not sum_is_even):
            return (x-1, y-1)
        else:
            return (x, y-1)

def sued_west(x, y):
    """
    Berechnet Koordinaten in Sued-West

    >>> sued_west(2, 7)
    (2, 8)
    >>> sued_west(3, 7)
    (3, 8)
    >>> sued_west(3, 8)
    (2, 9)
    >>> sued_west(4, 6)
    (3, 7)
    >>> sued_west(4, 2)
    (3, 3)

    """
    if isinstance(x, int) and isinstance(y, int):
        sum_is_even = (x + y) % 2
        x_is_even = x % 2
        if (x_is_even and sum_is_even) or (not x_is_even and not sum_is_even):
            return (x-1, y+1)
        else:
            return (x, y+1)

def nord_ost(x, y):
    """
    Berechnet Koordinaten in Sued-West

    >>> nord_ost(2, 7)
    (3, 6)
    >>> nord_ost(3, 7)
    (4, 6)
    >>> nord_ost(3, 8)
    (3, 7)
    >>> nord_ost(4, 6)
    (4, 5)
    >>> nord_ost(4, 2)
    (4, 1)

    """
    if isinstance(x, int) and isinstance(y, int):
        sum_is_even = (x + y) % 2
        x_is_even = x % 2
        if (x_is_even and sum_is_even) or (not x_is_even and not sum_is_even):
            return (x, y-1)
        else:
            return (x+1, y-1)

def sued_ost(x, y):
    """
    Berechnet Koordinaten in Sued-West

    >>> sued_ost(2, 7)
    (3, 8)
    >>> sued_ost(4, 6)
    (4, 7)
    >>> sued_ost(3, 8)
    (3, 9)
    >>> sued_ost(3, 7)
    (4, 8)

    """
    if isinstance(x, int) and isinstance(y, int):
        sum_is_even = (x + y) % 2
        x_is_even = x % 2
        if (x_is_even and sum_is_even) or (not x_is_even and not sum_is_even):
            return (x, y+1)
        else:
            return (x+1, y+1)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
