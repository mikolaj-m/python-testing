import argparse
import json
import tempfile
import os
from typing import List, Union

current_dir = os.path.dirname(__file__)

def take_from_list(li: list, indices: Union[int, List[int]]):
    """
    This function returns list of elements for given indices.

    :param li: list of elements
    :param indices: single index or list of indices
    :return: list of elements selected using indices
    
    >>> [ take_from_list([0, 1, 2, 3, 4], i) for i in range(5)]
    [[0], [1], [2], [3], [4]]
    
    >>> take_from_list(['a', 'b', 'c', 'd'], [0, 1, 2, 3])
    ['a', 'b', 'c', 'd']

    >>> take_from_list(['a', 'b', 'c', 'd'], [1, 2])
    ['b', 'c']

    >>> take_from_list(['a', 'b', 'c', 'd'], [0, 3])
    ['a', 'd']

    >>> take_from_list(['a', 'b', 'c', 'd'], 2.5)
    Traceback (most recent call last):
    ...
    ValueError: Indices should be integer or list of integers, not <class 'float'>

    >>> take_from_list(['a', 'b', 'c', 'd'], [2.5])
    Traceback (most recent call last):
    ...
    ValueError: Indices should be integer or list of integers, not <class 'list'>

    >>> take_from_list(['a', 'b', 'c', 'd'], 'a')
    Traceback (most recent call last):
    ...
    ValueError: Indices should be integer or list of integers, not <class 'str'>

    >>> take_from_list([], 0)
    Traceback (most recent call last):
    ...
    IndexError: Index 0 is to big for list of length 0

    >>> take_from_list([1, 2, 3], 3)
    Traceback (most recent call last):
    ...
    IndexError: Index 3 is to big for list of length 3

    >>> take_from_list([1, 2, 3], 42)
    Traceback (most recent call last):
    ...
    IndexError: Index 42 is to big for list of length 3
    """
    if isinstance(indices, int):
        indices = [indices]
    if not isinstance(indices, list) or not all(isinstance(i, int) for i in indices):
        raise ValueError(f"Indices should be integer or list of integers, not {type(indices)}")
    for index in indices:
        if index >= len(li):
            raise IndexError(f"Index {index} is to big for list of length {len(li)}")

    return [li[i] for i in indices]


def calculate(in_file: str, out_file: str):
    """
    >>> with tempfile.NamedTemporaryFile() as tmpfile1, tempfile.NamedTemporaryFile() as tmpfile2:
    ...     tmpfile1.write(b'{"list": [0, 1, 2, 3, 4, 5, 6, 7], "indices": [5]}') and True
    ...     tmpfile1.flush()
    ...     calculate(tmpfile1.name, tmpfile2.name)
    ...     line = tmpfile2.readline()
    ...     line == b'[5]'
    True
    True
    >>> with tempfile.NamedTemporaryFile() as tmpfile1, tempfile.NamedTemporaryFile() as tmpfile2:
    ...     tmpfile1.write(b'{"list": [0, 1, 2, 3, 4, 5, 6, 7], "indices": [5]}') and True
    ...     tmpfile1.flush()
    ...     calculate(tmpfile1.name, tmpfile2.name)
    ...     line = tmpfile2.readline()
    ...     line == b'[6]'
    True
    False
    >>> with tempfile.NamedTemporaryFile() as tmpfile:
    ...     calculate("input.json", tmpfile.name)
    ...     line = tmpfile.readline()
    ...     line == b'[81, 62, 78, 67, 89, 33, 106, 126, 112, 20, 56, 128, 106, 3, 107]'
    True
    """
    with open(in_file, 'r') as f_p:
        data = json.load(f_p)

    result = take_from_list(data["list"], data["indices"])

    with open(out_file, 'w') as f_p:
        json.dump(result, f_p)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", default=os.path.join(current_dir, "input.json"), nargs="?")
    parser.add_argument("output_file", default=os.path.join(current_dir, "output.json"), nargs="?")
    args = parser.parse_args()

    calculate(args.input_file, args.output_file)