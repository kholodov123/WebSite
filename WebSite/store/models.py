from django.db import models
from django.contrib.auth.models import User
import uuid


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=1500, null=True)
    price = models.IntegerField()
    picture = models.ImageField(upload_to="images", default="")

    def __str__(self):
        return self.name


class ProductInstance(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    inv_num = models.CharField(max_length=20, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    due_back = models.DateField(null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.inv_num, self.product, self.status)


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    complete = models.BooleanField(default=False)
    session_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        cartitems = self.cartitems.all()
        total = sum([item.price for item in cartitems])
        return total

    @property
    def num_of_items(self):
        cartitems = self.cartitems.all()
        quantity = sum([item.quantity for item in cartitems])
        return quantity


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name

    @property
    def price(self):
        new_price = self.product.price * self.quantity
        return new_price


class WatchedList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'
