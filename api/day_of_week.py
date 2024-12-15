from django.db import models

class DayOfWeek(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name 