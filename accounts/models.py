from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class MyUserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError('لطفا نام کاربری را وارد کنید')
        
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, verbose_name='نام کاربری')

    is_active = models.BooleanField(default=True, verbose_name='کاربر فعال باشد؟')
    is_admin = models.BooleanField(default=False, verbose_name='کاربر ادمین سایت باشد؟')

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
    
    def __str__(self) -> str:
        return self.username

    def has_perm(self, perm, obj=None) -> bool:
        return True

    def has_module_perms(self, app_label: str) -> bool:
        return True

    @property
    def is_staff(self):
        return self.is_admin
 