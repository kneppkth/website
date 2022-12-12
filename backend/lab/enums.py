import enum


class ChemicalType(enum.IntEnum):
    DEVELOPER = 0
    STOP = 1
    FIXER = 2
    BLIX = 3
    STABILIZER = 4


class DevelopmentType(enum.IntEnum):
    BN_NEGATIVE = 0
    BN_POSITIVE = 1
    COLOUR_NEGATIVE = 2
    COLOUR_POSITIVE = 3
