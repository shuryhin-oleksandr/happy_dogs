from django.db import models


# TODO: Add admin
# TODO: Add fields attributes
class Dog(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, blank=True)

    @property
    def full_name(self):
        if self.first_name and not self.last_name:
            return self.first_name
        elif self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

    class Meta:
        unique_together = ['first_name', 'last_name']

    def __str__(self):
        return self.full_name


class BoardingVisit(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    # TODO: Improve string
    def __str__(self):
        return f"{self.dog.full_name} Visit"
