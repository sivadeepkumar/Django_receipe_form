from django.db import models

# Create your models here.


class Receipe(models.Model):
    receipe_name = models.TextField(max_length=100)
    receipe_description = models.TextField()
    receipe_image = models.ImageField()

    def __str__(self) -> str:
        return '{},{},{}'.format(self.receipe_name,self.receipe_description,self.receipe_image)     