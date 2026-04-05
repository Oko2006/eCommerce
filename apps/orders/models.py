from django.db import models
# Create your models here.
class Order(models.Model):
    address=models.ForeignKey('users.Address',on_delete=models.PROTECT,related_name='orders')
    user=models.ForeignKey('users.User',related_name='orders',on_delete=models.PROTECT)
    cart=models.OneToOneField('cart.Cart',on_delete=models.PROTECT)
    placed_at=models.DateTimeField(auto_now_add=True)
