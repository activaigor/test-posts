from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name="posts")
    body = models.TextField(default="")
    date = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ("-date",)
        get_latest_by = "created"

    def __unicode__(self):
        return u"%s" % self.title