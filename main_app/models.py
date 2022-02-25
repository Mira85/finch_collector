from django.db import models
from django.urls import reverse

class Finch(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    habitat = models.CharField(max_length=200)
    lifespan = models.CharField(max_length=100)
    sound = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})