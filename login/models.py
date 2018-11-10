from django.db import models

class userData(models.Model):
    cID = models.CharField(max_length = 12, null= False)
    cName = models.CharField(max_length= 10, null= False, blank=True)
    cPassword = models.CharField(max_length = 30, null=False)
    cCurrAccID = models.CharField(max_length = 30, null=False, blank=True)#就是因為這個東西我他媽的我要用資料庫FU

    def __str__(self):
        return self.cID