from django.db import models

class MyUsers(models.Model):
    uname = models.CharField(max_length=250)
    email = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=10)
    verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=250, default="Male")
    city = models.CharField(max_length=250, default="Raipur")
    dob = models.CharField(max_length=50, default="02,Apr 1996")
    pic = models.ImageField(upload_to='pictures/')

    def __str__(self):
        return self.uname + ' - ' + self.email + ' - ' + self.password + ' - ' + str(self.verified) + ' - ' + str(self.gender) + ' - ' + str(self.city) + ' - ' + str(self.dob) + ' - ' + str(self.pic)


class Gallery(models.Model):
    email = models.CharField(max_length=250)
    pic = models.ImageField(upload_to='pictures/Gallery/')

    def __str__(self):
        return self.email + ' - ' + str(self.pic)

