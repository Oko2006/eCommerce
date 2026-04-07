from django.db import models
# Create your models here.
class Order(models.Model):
    address=models.ForeignKey('users.Address',on_delete=models.PROTECT,related_name='orders')
    user=models.ForeignKey('users.User',related_name='orders',on_delete=models.PROTECT)
    cart=models.OneToOneField('cart.Cart',on_delete=models.PROTECT)
    placed_at=models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)

class OrderItem(models.Model):
    order=models.ForeignKey('Order',on_delete=models.CASCADE,related_name='order_item')
    product=models.ForeignKey('products.Product',on_delete=models.PROTECT,related_name='product')
    product_name=models.CharField(max_length=255)
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)

    def save(self,*args,**kwargs):
        self.total_price=self.price*self.quantity
        super().save(*args,**kwargs)
