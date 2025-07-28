from django.db import models

# Create your models here.
class VisitType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Visit(models.Model):
    visit_type = models.ForeignKey(VisitType, on_delete=models.CASCADE)
    date = models.DateField()
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.visit_type.name} on {self.date}: {self.count}"