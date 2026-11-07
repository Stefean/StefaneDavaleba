from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    prep_time = models.IntegerField()

    def __str__(self):
        return self.title