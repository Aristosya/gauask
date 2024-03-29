# This file is held models(tables) that is related with users.
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Profile model that keeps name and image of a user
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(default='default.png', upload_to='images')
    teacher = models.BooleanField(default=False,)
    description = models.TextField(default='', max_length=255,)


    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.img.path)
        if image.height > 256 or image.width > 256:
            resize = (256, 256)
            image.thumbnail(resize)
            image.save(self.img.path)
