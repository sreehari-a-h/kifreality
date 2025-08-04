# serializers.py
from rest_framework import serializers


class PropertiesSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

from rest_framework import serializers
from .models import PropertyCategory, Developer, Property, PropertyImage

class PropertyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyCategory
        fields = '__all__'

# class LocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Location
#         fields = '__all__'

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = '__all__'

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ('id', 'image')

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = '__all__'

class PropertiesExampleSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ['status', 'category', 'property_type', 'title', 'description', 'price', 'bedrooms', 'bathrooms', 'area', 'location', 'developer', 'created_at', 'image', 'brochure', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None
