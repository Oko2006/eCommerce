from django.db import models

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField('products.Product', through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.username}'s cart"
    class Meta:
        unique_together = ('cart', 'product')