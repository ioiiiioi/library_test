from django.db import models
from user_app.models import User

class BaseModels(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created_by')

    class Meta:
        abstract = True