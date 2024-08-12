from django.db import models


class ContactPage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.CharField(max_length=50,)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# class AboutPage(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     image = models.ImageField(upload_to='about/', null=True, blank=True)
