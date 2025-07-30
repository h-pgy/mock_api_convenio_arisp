import random
from typing import Optional


def random_int_string(lengths: list[int], separator: str = '.', final_separator:Optional[str]=None) -> str:

    if final_separator is not None:
        final_length = lengths[-1]
        lengths = lengths[:-1]
        generated_string = separator.join(str(random.randint(0, length*10-1)).zfill(length) for length in lengths)
        generated_string += final_separator + str(random.randint(0, final_length*10-1)).zfill(final_length)
    else:
        generated_string = separator.join(str(random.randint(0, length*10-1)).zfill(length) for length in lengths)

    return generated_string