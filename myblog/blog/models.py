import datetime

from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.title
