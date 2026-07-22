from django.db import models
from companies.models import Company

class Application(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    position = models.CharField(max_length=150)
    status = models.CharField(max_length=20,default='Applied')
    application_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
     return f"{self.company} - {self.position}"