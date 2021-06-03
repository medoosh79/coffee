from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product_favorites= models.ManyToManyField(Product, verbose_name=_("Product Favorites"))
    address = models.CharField(_("Address"), max_length=70)
    address2 = models.CharField(_("Address2"), max_length=70)
    city = models.CharField(_("City"), max_length=20)
    state = models.CharField(_("State"), max_length=20)
    zip = models.CharField(_("ZIP"), max_length=20)
    mobile = models.CharField(_("Mobile"), max_length=15)
    image= models.ImageField(_("Image"), upload_to="user/", height_field=None, width_field=None, max_length=None)
   
    class Meta:
        verbose_name = _("UserProfile")
        verbose_name_plural = _("UserProfiles")

    def __str__(self):
        return str(self.user.username)

    