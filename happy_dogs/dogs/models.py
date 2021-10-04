from django.db import models


# TODO: Add admin
# TODO: Add fields attributes
class Dog(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Visit(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    # TODO: Improve string
    def __str__(self):
        return f"{self.dog.name} Visit"
