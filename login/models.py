from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserProfileManager(BaseUserManager):
    def create_user(self, numero, username, email, password=None):
        if not numero:
            raise ValueError('Users must have a document number')

        user = self.model(
            numero=numero,
            username=username,
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser):
    tipo_choices = (
        (1, 'T.I'),
        (2, 'C.C'),
        (3, 'C.E'),
        (4, 'C.I'),
    )

    tipo = models.PositiveSmallIntegerField(choices=tipo_choices)
    numero = models.PositiveIntegerField(unique=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    objects = UserProfileManager()

    USERNAME_FIELD = 'numero'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return str(self.numero)