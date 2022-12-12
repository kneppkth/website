import os

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from versatileimagefield.fields import VersatileImageField

from knepp.storage import OverwriteStorage
from knepp.db.mixins import Timestamps, StandardModel
from user.enums import GenderType
from user.managers import UserManager


def user_picture_filename(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"user/picture/{instance.id}{ext}"


class User(AbstractBaseUser, StandardModel, Timestamps, PermissionsMixin):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
    )

    email_verified = models.BooleanField(default=False)
    verify_key = models.CharField(max_length=127, blank=True, null=True)
    verify_expiration = models.DateTimeField(default=timezone.now)

    registration_finished = models.BooleanField(default=False)

    # Personal information
    picture = VersatileImageField(
        "Image",
        upload_to=user_picture_filename,
        default="user/picture/profile.png",
        storage=OverwriteStorage(),
    )
    gender = models.PositiveSmallIntegerField(
        choices=((t.value, t.name) for t in GenderType), default=GenderType.NONE
    )
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    # University
    university = models.CharField(max_length=255, blank=True, null=True)
    degree = models.CharField(max_length=255, blank=True, null=True)
    graduation_year = models.PositiveIntegerField(
        default=timezone.now().year, blank=True, null=True
    )

    # Dietary restrictions
    diet = models.CharField(max_length=255, blank=True, null=True)
    diet_other = models.CharField(max_length=255, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ("firstname", "lastname")

    def __str__(self) -> str:
        return self.email

    def get_fullname_or_email(self) -> str:
        return (
            f"{self.firstname} {self.lastname}"
            if (self.firstname and self.lastname)
            else self.email
        )

    def get_full_name(self) -> str:
        return self.email

    def get_short_name(self) -> str:
        return self.email


class THSRegistration(StandardModel, Timestamps):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
