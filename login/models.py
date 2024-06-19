from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserProfileManager(BaseUserManager):
    def create_user(self, numero, username, email, password=None, tipo=2):
        if not numero:
            raise ValueError('Users must have a document number')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            numero=numero,
            username=username,
            email=self.normalize_email(email),
            tipo=tipo
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, numero, username, email, password=None, tipo=2):
        user = self.create_user(
            numero=numero,
            username=username,
            email=email,
            password=password,
            tipo=tipo,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    tipo_choices = (
        (1, 'T.I'),
        (2, 'C.C'),
        (3, 'C.E'),
        (4, 'C.I'),
    )

    tipo = models.PositiveSmallIntegerField(choices=tipo_choices, default=2)
    numero = models.PositiveIntegerField(unique=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'numero'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return str(self.numero)

class UserAddress(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username}'s Address"