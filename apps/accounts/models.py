from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from mptt.models import MPTTModel, TreeManyToManyField, TreeForeignKey


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(
        max_length=255,
        unique=True
    )
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return str(self.username)

    @property
    def is_staff(self):
        return self.is_admin


class UserWallet(models.Model):
    wallet_id = models.BigAutoField(primary_key=True)
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wallet'
    )  # Link to the User model
    balance_toman = models.IntegerField(
        default=0,
        help_text="Balance in Iranian Toman"
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
    def __str__(self):
        return f"{self.user_id}'s wallet (Balance: {self.balance_toman} IR Toman)"
