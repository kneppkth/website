import enum

from django.utils.translation import gettext as _


class GenderType(enum.IntEnum):
    NONE = 0
    FEMALE = 1
    MALE = 2
    NON_BINARY = 3


GenderType.labels = {
    GenderType.NONE: _("prefer not to say"),
    GenderType.FEMALE: _("woman"),
    GenderType.MALE: _("man"),
    GenderType.NON_BINARY: _("non-binary"),
}
GenderTypeDict = GenderType.labels


GenderType.colours = {
    GenderType.NONE: "#3a3a3a",
    GenderType.FEMALE: "#ed1a3e",
    GenderType.MALE: "#ebc934",
    GenderType.NON_BINARY: "#00abe7",
}
GenderTypeColoursDict = GenderType.colours


class DietType(enum.IntEnum):
    LACTOSE = 0
    GLUTEN = 1
    VEGETARIAN = 2
    VEGAN = 3
    OTHER = 4


DietType.labels = {
    DietType.LACTOSE: _("lactose intolerant"),
    DietType.GLUTEN: _("gluten intolerant"),
    DietType.VEGETARIAN: _("vegetarian"),
    DietType.VEGAN: _("vegan"),
    DietType.OTHER: _("other"),
}
DietTypeDict = DietType.labels
