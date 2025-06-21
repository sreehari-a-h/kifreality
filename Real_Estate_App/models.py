from django.db import models
from django.utils.html import mark_safe

# Create your models here.

class PropertyCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Location(models.Model):
    city = models.CharField(max_length=100, null=True, blank=True)
    # latitude = models.FloatField()
    # longitude = models.FloatField()

    def __str__(self):
        return self.city if self.city else "Unknown Location"

class Developer(models.Model):
    name = models.CharField(max_length=100)
    # website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    STATUS_CHOICES = (
        ('FOR SALE', 'For Sale'),
        ('OFF PLAN', 'Off Plan'),
    )

    PROPERTY_TYPE_CHOICES = (
        ('RENTAL', 'Rental'),
        ('SALE', 'Sale'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='FOR SALE')
    category = models.ForeignKey(PropertyCategory, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES, default='SALE')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.CharField(max_length=20)
    bedrooms = models.CharField(max_length=20)
    bathrooms = models.CharField(max_length=20)
    area = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # New field for property brochure PDF
    brochure = models.FileField(upload_to='media/property_brochures/', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("singlepage", kwargs={'pk': self.pk})

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/property_images/')

    def __str__(self):
        return f"Image for {self.property.property_type} - {self.property.title}"

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="100px" height="100px" />' % (self.image.url))
        else:
            return "No Image"

    image_tag.short_description = 'Image'




# models.py
from django.db import models

class Properties(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class PropertiesExample(models.Model):
    STATUS_CHOICES = (
        ('FOR SALE', 'For Sale'),
        ('OFF PLAN', 'Off Plan'),
    )

    PROPERTY_TYPE_CHOICES = (
        ('RENTAL', 'Rental'),
        ('SALE', 'Sale'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='FOR SALE')
    category = models.CharField(max_length=200)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES, default='SALE')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.CharField(max_length=20)
    bathrooms = models.CharField(max_length=20)
    area = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=200)
    developer = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/property_images/')

    # New field for property brochure PDF
    brochure = models.FileField(upload_to='media/property_brochures/', null=True, blank=True)

    def __str__(self):
        return self.title


