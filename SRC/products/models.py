from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Product(models.Model):
    PrdName = models.CharField(verbose_name=_(' Name'), max_length=100)
    PrdDesc = models.TextField(verbose_name=_(' Description'))
    PrdImage = models.ImageField(verbose_name=_('imge/%y/%m/%d/'), upload_to='media', blank = True,  null= True)
    PrdPrice = models.DecimalField(verbose_name=_(' Price'), max_digits=8, decimal_places=2)
    PrdDescountPrice = models.DecimalField(verbose_name=_('Descount Price'), max_digits=8, decimal_places=2)
    PrdCost = models.DecimalField(verbose_name=_(' Cost'), max_digits=8, decimal_places=2)
    PrdCreated = models.DateTimeField(verbose_name=_(' Created'))
    PrdIsActive = models.BooleanField(default=True)

    

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering =['-PrdCreated']


    def __str__(self):
        return str(self.PrdName)

   

