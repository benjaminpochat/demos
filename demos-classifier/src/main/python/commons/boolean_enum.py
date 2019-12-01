from enum import Enum


class Boolean(Enum):
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    UNKNOWN = 'UNKNOWN'

    def to_int(self):
        if self is Boolean.TRUE:
            return 1
        elif self is Boolean.FALSE:
            return 0
        else:
            return -1