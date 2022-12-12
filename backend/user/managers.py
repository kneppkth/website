from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        firstname: str,
        lastname: str,
        password: str,
        is_staff: bool = False,
        is_superuser: bool = False
    ):
        user = self.model(
            email=email, firstname=firstname, lastname=lastname, is_staff=is_staff, is_superuser=is_superuser
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, firstname: str, lastname: str, password: str
    ):
        user = self.create_user(
            email=email,
            firstname=firstname,
            lastname=lastname,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        user.save(using=self._db)
        return user
