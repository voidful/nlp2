import time
from random import sample, randint, uniform


def _checkInt(l):
    return all(isinstance(i, int) for i in l)


def _checkStr(l):
    return all(isinstance(i, str) for i in l)


def _checkFloat(l):
    return any(isinstance(i, float) for i in l)


def random_string(length):
    return ''.join(sample('0123456789ABCDEF', length))


def random_string_with_timestamp(length):
    return str(int(time.time())) + random_string(length)


def random_value_in_array_form(input_array):
    if _checkInt(input_array):
        return randint(input_array[0], input_array[1])
    elif _checkFloat(input_array):
        return uniform(input_array[0], input_array[1])
    elif _checkStr(input_array):
        return input_array[randint(0, len(input_array) - 1)]
