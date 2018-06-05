from django.db import models

class MyUsers(models.Model):
    uname = models.CharField(max_length=250)
    email = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=10)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.uname + ' - ' + self.email + ' - ' + self.password + ' - ' + str(self.verified)
