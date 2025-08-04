# # admin.py
# from django.contrib import admin
# from django.utils.safestring import mark_safe
# from .models import PropertyCategory, Developer, Property, PropertyImage 
# import requests
# from django.core.files.base import ContentFile
# import os


# import logging
# from .models import Property


# class PropertyImageInline(admin.TabularInline):
#     model = PropertyImage
#     extra = 1

# class PropertyAdmin(admin.ModelAdmin):
#     inlines = [PropertyImageInline]
#     actions = ['fetch_properties']

#     list_display = ('title', 'download_brochure_link', 'status', 'category', 'property_type', 'price', 'bedrooms', 'bathrooms', 'area', 'location', 'developer', 'created_at')
#     search_fields = ('title', 'status', 'price', 'bedrooms', 'bathrooms', 'area', 'created_at')

#     def download_brochure_link(self, obj):
#         if obj.brochure:
#             return mark_safe(f'<a href="{obj.brochure.url}" download="{obj.brochure.name}">Download Brochure</a>')
#         return "No Brochure"

#     download_brochure_link.short_description = "Brochure"

#     def fetch_properties(self, request, queryset):
#      try:
#         response = requests.get('https://leadloom.pythonanywhere.com/api/property/')  # Adjust URL accordingly
#         response.raise_for_status()  # Raise exception for bad response status
#         data = response.json()
#         for property_data in data:
#             category_id = property_data.get('category')
#             category_instance, _ = PropertyCategory.objects.get_or_create(pk=category_id)


#             location_name = property_data.get('location_name')
#             # location_instance, _ = Location.objects.get_or_create(city=location_name)



#             developer_name = property_data.get('developer_name')  # Assuming 'developer_name' is the correct key
#             developer_instance = None
#             if developer_name:
#               developer_instance, _ = Developer.objects.get_or_create(name=developer_name)

#             property_instance = Property.objects.create(
#                 title=property_data['title'],
#                 status=property_data['status'],
#                 category=category_instance,
#                 property_type=property_data['property_type'],
#                 price=property_data['price'],
#                 description=property_data['description'],
#                 bedrooms=property_data['bedrooms'],
#                 bathrooms=property_data['bathrooms'],
#                 area=property_data['area'],
#                 # location=location_instance,
#                 developer=developer_instance,
#                 created_at=property_data['created_at']
#             )
#             images_data = property_data.get('images', [])
#             for image_data in images_data:
#                 image_url = image_data.get('image')
#                 if image_url:
#                     # Download image and create PropertyImage instance
#                     image_content = requests.get(image_url).content
#                     image_file = ContentFile(image_content)
#                     property_image = PropertyImage(property=property_instance)
#                     property_image.image.save(os.path.basename(image_url), image_file, save=True)




#         self.message_user(request, "Properties fetched successfully.")
#      except requests.exceptions.RequestException as e:
#         self.message_user(request, f"Failed to fetch properties from API: {e}", level='ERROR')

#     fetch_properties.short_description = "Fetch Properties"








# admin.site.register(PropertyCategory)
# # admin.site.register(Location)
# admin.site.register(Developer)  # Add Developer to the admin site
# admin.site.register(Property, PropertyAdmin)


# class PropertyImageAdmin(admin.ModelAdmin):
#     list_display = ('property', 'image_tag', 'images_link',)
#     # search_fields =('property')
#     readonly_fields = ('image_tag',)
#     search_fields = ('property__title',)

#     def images_link(self, obj):
#         if obj.image:  # Assuming 'images' is the field name in your model
#             return mark_safe(f'<a href="{obj.image.url}" download>Download Image</a>')
#         return "No Image"
#     images_link.short_description = "Images"


# admin.site.register(PropertyImage,PropertyImageAdmin)
# # admin.site.register(PropertyImage)


# # project_b/items/admin.py
# from django.contrib import admin
# from django.http import JsonResponse

# logger = logging.getLogger(__name__)


# from django.contrib import admin


# class PropertiesAdmin(admin.ModelAdmin):
#     list_display = ('title', 'description', 'price')
#     actions = ['fetch_properties']

#     def fetch_properties(self, request, queryset):
#         try:
#             response = requests.get('https://leadloom.pythonanywhere.com/api/properties/')  # Adjust URL accordingly
#             response.raise_for_status()  # Raise exception for bad response status
#             data = response.json()
#             for property_data in data:
#                 Property.objects.create(title=property_data['title'], description=property_data['description'], price=property_data['price'])
#             self.message_user(request, "Properties fetched successfully.")
#         except requests.exceptions.RequestException as e:
#             logger.error(f"Failed to fetch properties from API: {e}")
#             self.message_user(request, "Failed to fetch properties from API. Check logs for details.", level='ERROR')


# # Register your models with the admin site
# admin.site.register(Property, PropertiesAdmin)


# class PropertiesExampleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'status', 'category', 'property_type', 'price', 'bedrooms', 'bathrooms', 'area', 'location', 'developer', 'created_at', 'image_thumbnail')
#     actions = ['fetch_properties']

#     def image_thumbnail(self, obj):
#         return '<img src="{url}" width="100" height="100" />'.format(url=obj.image.url) if obj.image else None

#     image_thumbnail.allow_tags = True
#     image_thumbnail.short_description = 'Image'

#     def fetch_properties(self, request, queryset):
#         try:
#             response = requests.get('https://leadloom.pythonanywhere.com/api/property/')  # Adjust URL accordingly
#             response.raise_for_status()  # Raise exception for bad response status
#             data = response.json()
#             for property_data in data:
#                 Property.objects.create(
#                     title=property_data['title'],
#                     status=property_data['status'],
#                     category=property_data['category'],
#                     property_type=property_data['property_type'],
#                     price=property_data['price'],
#                     bedrooms=property_data['bedrooms'],
#                     bathrooms=property_data['bathrooms'],
#                     area=property_data['area'],
#                     location=property_data['location'],
#                     developer=property_data['developer'],
#                     created_at=property_data['created_at']
#                 )
#             self.message_user(request, "Properties fetched successfully.")
#         except requests.exceptions.RequestException as e:
#             self.message_user(request, f"Failed to fetch properties from API: {e}", level='ERROR')

#     fetch_properties.short_description = "Fetch Properties"

# admin.site.register(Property, PropertiesExampleAdmin)
