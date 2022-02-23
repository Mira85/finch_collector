from django.db import models

class Finch(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    habitat = models.CharField(max_length=200)
    lifespan = models.CharField(max_length=100)
    sound = models.CharField(max_length=100)

    def __str__(self):
        return self.name