import random

from yacut.constans import MAX_LEN_SHORT_AUTOGEN, SYMVOLS


def get_unique_short_id():
    return ''.join(random.choices(SYMVOLS, k=MAX_LEN_SHORT_AUTOGEN))
