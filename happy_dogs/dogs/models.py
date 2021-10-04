from django.db import models


# TODO: Add admin
# TODO: Add fields attributes
class Dog(models.Model):
    name = models.CharField(max_length=128)


class Visit(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
