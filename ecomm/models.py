from django.db import models

class Contact(models.Model):  # Capitalized
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    CATEGORY_CHOICE = (
        (1, 'mobile'),
        (2, 'shoes'),
        (3, 'cloths'),
    )
    
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.IntegerField(max_length=20, verbose_name='category', choices=CATEGORY_CHOICE)
    pdetails = models.CharField(max_length=100, verbose_name='product details')
    is_active = models.BooleanField(default=True)
    pimage = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.name} - {self.pdetails}"

class Cart(models.Model):
    uid = models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid = models.ForeignKey('Product',on_delete= models.CASCADE,db_column = 'pid')
    qty = models.IntegerField(default=1)

class Order(models.Model):
    uid = models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid = models.ForeignKey('Product',on_delete= models.CASCADE,db_column = 'pid')
    qty = models.IntegerField(default=1)
    amt=models.IntegerField()