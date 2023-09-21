from django.db import models

# Create your models here.

class Information(models.Model):
    Information_name = models.CharField(max_length=50,null=True,blank=True,default='Anonymous')
    Information_password = models.CharField(max_length=150,null=True,blank=True)
    Information_phone = models.IntegerField(null=False,unique=True)
    Information_email = models.EmailField(null=True,blank=True)
    Information_used = models.BooleanField(null=True,default=False)
    Information_spam = models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return self.Information_name

