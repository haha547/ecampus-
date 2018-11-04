from django.db import models

class student(models.Model):
    entetID = models.CharField(max_length=20,null=False)
    enterPassword = models.CharField(max_length=50,null=False)
    
    def _str_(self):
        return self.enterID
