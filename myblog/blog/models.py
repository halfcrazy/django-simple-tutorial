import datetime

from django.core.urlresolvers import reverse
from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    body = models.TextField()
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    def get_absolute_url(self):
        return reverse('blog:detail_post', args=[self.title])

    def __str__(self):
        return self.title
