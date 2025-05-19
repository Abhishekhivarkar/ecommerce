



# Create your models here.
# class contact(models.Model):
#     name=models.CharField(max_length=100)
#     contact=models.CharField(max_length=15)
#     email=models.EmailField()
#     description=models.TextField()
# models.py
# from django.db import models

# class contact(models.Model):
#     name = models.CharField(max_length=100)
#     contact = models.CharField(max_length=15)
#     email = models.EmailField()
#     description = models.TextField()

#     created_at=models.DateTimeField(auto_now_add=True)

#     def __str__(self):

#         return self.name

# Create your models here.
from django.db import models

class Contact(models.Model):  # Capitalized
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.name

