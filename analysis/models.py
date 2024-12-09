from django.contrib.auth.models import User
from django.db import models

from PostBox.settings import base


class Analysis(models.Model):
    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE)
    about = models.CharField(max_length=255)
    type = models.CharField(max_length=30)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    description = models.TextField(),
    result_image = models.ImageField(upload_to='analysis/%Y/%m/%d/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.about)
    class Meta:
        db_table = 'analysis'

