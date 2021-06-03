from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Order(models.Model):
    user= models.ForeignKey(User,  on_delete=models.CASCADE)
    order_date= models.DateTimeField()
    details= models.ManyToManyField(Product, through='OrderDetails')
    is_finished= models.BooleanField()
    

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return 'User: ' + self.user.username + ', Order id:' + str(self.id)

class OrderDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    

    def __str__(self):
        return 'User: ' + self.order.username + ', Product: ' + self.product.name + ', Order id: ' + str(self. order.id)

    
    class Meta:
        ordering=['id']