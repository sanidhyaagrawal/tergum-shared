from django.db import models
from django.conf import settings

# Create your models here.
class invite_links(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    token = models.CharField(max_length=500)
    posted_date =  models.DateTimeField(auto_now_add=True,verbose_name="invite link creation date")

    # TO STRING METHOD
    def __str__(self):
        return self.token
