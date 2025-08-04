from django.db import models
from django.utils.html import mark_safe
from django.utils.timezone import now
# Create your models here.



# class Location(models.Model):
#     city = models.CharField(max_length=100, null=True, blank=True)
#     # latitude = models.FloatField()
#     # longitude = models.FloatField()

#     def __str__(self):
#         return self.city if self.city else "Unknown Location"
class City(models.Model):
    name= models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.name
    
class District(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE,related_name='distrcits')
    
class Developer(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

class PropertyCategory(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name
    
class PropertyStatus(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self):
        return self.name

class SalesStatus(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self):
        return self.name
    
class Facility(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self):
        return self.name
    
# class Property(models.Model):
    # STATUS_CHOICES = (
    #     ('FOR SALE', 'For Sale'),
    #     ('OFF PLAN', 'Off Plan'),
    # )

    # PROPERTY_TYPE_CHOICES = (
    #     ('RENTAL', 'Rental'),
    #     ('SALE', 'Sale'),
    # )

    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='FOR SALE')
    # category = models.ForeignKey(PropertyCategory, on_delete=models.CASCADE)
    # property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES, default='SALE')
    # title = models.CharField(max_length=200)
    # description = models.TextField()
    # price = models.CharField(max_length=20)
    # bedrooms = models.CharField(max_length=20)
    # bathrooms = models.CharField(max_length=20)
    # area = models.DecimalField(max_digits=8, decimal_places=2)
    # location = models.ForeignKey(C, on_delete=models.CASCADE)
    # developer = models.ForeignKey(Developer, on_delete=models.CASCADE, null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    # # New field for property brochure PDF
    # brochure = models.FileField(upload_to='media/property_brochures/', null=True, blank=True)
class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover = models.URLField(blank=True, null=True)  # assuming it's a URL
    address = models.CharField(max_length=255, blank=True, null=True)
    address_text = models.TextField(blank=True, null=True)
    delivery_date = models.IntegerField(blank=True, null=True)  # storing YYYYMM as int
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True)
    property_type = models.ForeignKey(PropertyCategory, on_delete=models.SET_NULL, null=True)
    property_status = models.ForeignKey(PropertyStatus, on_delete=models.SET_NULL, null=True)
    sales_status = models.ForeignKey(SalesStatus, on_delete=models.SET_NULL, null=True)
    completion_rate = models.IntegerField(default=0)
    residential_units = models.IntegerField(default=0)
    commercial_units = models.IntegerField(default=0)
    payment_plan = models.IntegerField(default=0)
    post_delivery = models.BooleanField(default=False)
    payment_minimum_down_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    guarantee_rental_guarantee = models.BooleanField(default=False)
    guarantee_rental_guarantee_value = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    downPayment = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    low_price = models.CharField(max_length=10,null=True,blank=True)
    min_area = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True,blank=True)
    updated_at = models.DateTimeField(default=now)

    facilities = models.ManyToManyField(Facility, blank=True, related_name='properties')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("singlepage", kwargs={'pk': self.pk})

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.URLField()

    def __str__(self):
        return f"Image for {self.property.title}"

class PropertyFacility(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_facilities')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.property.title} - {self.facility.name}"
    
class GroupedApartment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='grouped_apartments')
    unit_type = models.CharField(max_length=100, blank=True)
    rooms = models.CharField(max_length=50, blank=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.unit_type} - {self.rooms} rooms"


class PropertyUnit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    unit_number = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Unit {self.unit_number} in {self.property.title}"

class PaymentPlan(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='payment_plans')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.property.title})"


class PaymentPlanValue(models.Model):
    property_payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE, related_name='values')
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f"{self.name}: {self.value}"
    
# models.py
# from django.db import models

# class Properties(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return self.title


# class PropertiesExample(models.Model):
#     STATUS_CHOICES = (
#         ('FOR SALE', 'For Sale'),
#         ('OFF PLAN', 'Off Plan'),
#     )

#     PROPERTY_TYPE_CHOICES = (
#         ('RENTAL', 'Rental'),
#         ('SALE', 'Sale'),
#     )

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='FOR SALE')
#     category = models.CharField(max_length=200)
#     property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES, default='SALE')
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     bedrooms = models.CharField(max_length=20)
#     bathrooms = models.CharField(max_length=20)
#     area = models.DecimalField(max_digits=8, decimal_places=2)
#     location = models.CharField(max_length=200)
#     developer = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     image = models.ImageField(upload_to='media/property_images/')

#     # New field for property brochure PDF
#     brochure = models.FileField(upload_to='media/property_brochures/', null=True, blank=True)

#     def __str__(self):
#         return self.title


