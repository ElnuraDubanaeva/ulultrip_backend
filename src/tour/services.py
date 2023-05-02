import random
import string


class TourServices:
    @classmethod
    def make_qr_code(cls):
        strings_upp = string.ascii_uppercase
        strings_low = string.ascii_lowercase
        digits = string.digits
        str_up = "".join(random.choice(strings_upp) for i in range(2))
        str_low = "".join(random.choice(strings_low) for i in range(2))
        dig_ = "".join(random.choice(digits) for i in range(4))
        return str_up + dig_ + str_low