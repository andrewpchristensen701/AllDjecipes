from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser



class ChefUser(AbstractUser):
    pass

    def __str__(self):
        return f'{self.username}'
    
