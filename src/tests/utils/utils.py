import random
import string

username = "tywfamvyczuoqcvetzzvlzvxfqpcijco"
password = "baxpmyntxcclbiblrxtpersdfublkkor"

new_username = "rfzmehwlzifvlbdiyhvksedcghhllnsh"
new_password = "ddnvbdeublblxnbwrgbazksjnbynmxix"


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))
