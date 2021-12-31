from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    def create_user(self, email,phone, fullname,image=None, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            fullname=fullname,image=image
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email,phone,fullname, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            phone=phone,
            fullname=fullname,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email,phone,fullname, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            phone=phone,
            fullname=fullname,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    phone = PhoneNumberField(unique=True)
    fullname = models.CharField(max_length=30, null=False)
    image = models.ImageField(
        upload_to='uploads',default='../static/img/anonymous.jpg')
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname','phone']# Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()

class Account(models.Model):
    name = models.CharField(unique=True, max_length=30)
    currency_categories = (
        ('RWF', 'RWF'),
        ('$', '$'),
    )
    currency=models.CharField(max_length=25, choices=currency_categories)

class Category(models.Model):
    name = models.CharField(unique=True, max_length=30)
    cate_types = (
        ('income', 'income'),
        ('expense', 'expense'),
    )
    type=models.CharField(max_length=25, choices=cate_types)

class Expense(models.Model):
    amount=models.DecimalField(max_digits=12, decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField(max_length=200)

class Income(models.Model):
    amount=models.DecimalField(max_digits=12, decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField(max_length=200)