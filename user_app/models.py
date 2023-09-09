from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class EntityChoices(models.TextChoices):
        STUDENT = ("STUDENT", "STUDENT")
        LIBRARIAN = ("LIBRARIAN", "LIBRARIAN")

class User(AbstractUser):

    entity = models.CharField(max_length=9, choices=EntityChoices.choices)

    def save(self, *args, **kwargs):
        if not self.id: 
            if not self.entity and self.is_superuser == True:
                self.entity = EntityChoices.LIBRARIAN
            if self.entity == EntityChoices.LIBRARIAN:
                self.is_superadmin = True
        super().save(*args, **kwargs)
