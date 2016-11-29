from __future__ import unicode_literals

from django.db import models
from ..login_reg_app.models import User

# Create your models here.

class Quote(models.Model):
    quote = models.CharField(max_length=45)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitter = models.ForeignKey(User)



class Favorite(models.Model):
    user = models.ForeignKey(User)
    quote = models.ForeignKey(Quote)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)