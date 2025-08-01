from django.shortcuts import render,get_object_or_404
from Real_Estate_App.models import PropertyCategory, Location, Property, Developer
from django.db.models import Avg, Q
from django.http import HttpResponse

# Create your views here.

def BASE(request):
    return render(request, 'base.html')

# def HOME(request):
#     return render(request, 'main/home.html')

def ABOUT(request):
    return render(request, 'main/about.html')

def CONTACT(request):
    return render(request, 'main/contact.html')

def PRIVACY(request):
    return render(request, 'main/privacy.html')

def aljada(request):
    return render(request, 'main/aljada.html')
def propertydetail(request):
    return render(request, 'main/propertydetail.html')
def burjazizi(request):
    return render(request, 'main/burjazizilanding.html')

def COMING(request):
    return render(request, 'main/coming.html')
# views.py

from django.shortcuts import render
from django.db.models import Avg
from .models import Location, Property, PropertyCategory

def HOME2(request):
    location = Location.objects.all()
    property_category = PropertyCategory.objects.all()
    developer = Developer.objects.all()

    # Get all properties
    properties = Property.objects.all()


    latest_properties = Property.objects.order_by('-created_at')[:9]


    # Fetch properties in the top three attractive areas
    attractive_properties = Property.objects.order_by('-price')[:3]
    context = {
        'location': location,
        'property_category': property_category,
        'developer' : developer,
        'properties': properties,
        'latest_properties': latest_properties,
        'attractive_properties': attractive_properties,
    }

    return render(request, 'main/home2.html', context)

from django.shortcuts import render
from .models import Property, Location, PropertyCategory

def PROPERTIES(request):
    location = Location.objects.all()
    property_category = PropertyCategory.objects.all()
    developer = Developer.objects.all()


    # Check if 'status' parameter is present in the URL
    status_param = request.GET.get('status', None)

    # Filter properties based on status parameter
    if status_param == 'offplan':
        properties = Property.objects.filter(status='OFF PLAN').order_by('-created_at')
    elif status_param == 'ready_to_move':
        properties = Property.objects.filter(status='FOR SALE').order_by('-created_at')
    else:
        # If no status parameter is provided, show all properties
        properties = Property.objects.order_by('-created_at')

    context = {
        'location': location,
        'property_category': property_category,
        'developer' : developer,
        'properties': properties,
    }

    return render(request, 'main/properties.html', context)


def SINGLEPAGE(request, pk):
    location = Location.objects.all()
    property_category = PropertyCategory.objects.all()
    developer = Developer.objects.all()
    property_instance = get_object_or_404(Property, pk=pk)
    images = property_instance.images.all()

    context = {
        'location' : location,
        'property_category' : property_category,
        'developer' : developer,
        'property' : property_instance,
        'images' : images,
    }

    return render(request, 'main/singlepage.html', context)

def property_search(request):
    if request.method == 'GET':
        developer_id = request.GET.get('developer', '')
        location_id = request.GET.get('location', '')
        category_id = request.GET.get('category', '')

        # Filter properties based on the search criteria
        properties = Property.objects.filter(
            Q(developer__id=developer_id) if developer_id else Q(),
            Q(location__id=location_id) if location_id else Q(),
            Q(category__id=category_id) if category_id else Q(),
        )

        # Get all available locations and property categories
        all_developers = Developer.objects.all()
        all_locations = Location.objects.all()
        all_categories = PropertyCategory.objects.all()

        if properties.exists():
            return render(request, 'main/properties.html', {'properties': properties, 'developer': all_developers, 'location': all_locations, 'property_category': all_categories})
        else:
            message = "Properties not available in the specified criteria."
            return render(request, 'main/properties.html', {'message': message, 'developer': all_developers, 'location': all_locations, 'property_category': all_categories})

    return HttpResponse("Invalid Request")




def Filter_Search(request):
    location = Location.objects.all()
    property_category = PropertyCategory.objects.all()
    developer = Developer.objects.all()

    # Get the parameters from the request
    developer_id = request.GET.get('developer', '')
    location_id = request.GET.get('location', '')
    category_id = request.GET.get('category', '')
    status = request.GET.get('status', '')
    sort_by = request.GET.get('sort_by', '')

    # Filter properties based on the selected criteria
    properties = Property.objects.all()

    if developer_id:
        properties = properties.filter(developer__id=developer_id)

    if location_id:
        properties = properties.filter(location__id=location_id)

    if category_id:
        properties = properties.filter(category__id=category_id)

    if status:
        properties = properties.filter(status=status)

    # Sort properties based on the selected sorting option
    if sort_by == 'low_to_high':
        properties = properties.order_by('price')
    elif sort_by == 'high_to_low':
        properties = properties.order_by('-price')
    elif sort_by == 'newest':
        properties = properties.order_by('-id')
    elif sort_by == 'oldest':
        properties = properties.order_by('id')

    # Check if no properties match the criteria
    if not properties.exists():
        message = "Properties not available in the specified criteria."
        context = {
            'developer': developer,
            'location': location,
            'property_category': property_category,
            'message': message,
        }
        return render(request, 'main/properties.html', context)

    context = {
        'location': location,
        'property_category': property_category,
        'developer' : developer,
        'properties': properties,
        'selected_location': int(location_id) if location_id else None,
        'selected_category': int(category_id) if category_id else None,
        'selected_status': status,
        'selected_sort_by': sort_by,
    }

    return render(request, 'main/properties.html', context)

def COMPARE(request):
    property_ids = request.GET.get('property_ids', '').split(',')
    properties = Property.objects.filter(pk__in=property_ids)
    return render(request, 'main/compare.html', {'properties': properties})



import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def add_property_to_bayut(request, property_id):
    if request.method == 'POST':
        try:
            # Retrieve the property using the provided ID
            property_instance = Property.objects.get(id=property_id)

            # Your RapidAPI key
            rapidapi_key = 'ae8ddbc530mshb9150192c5bec43p124d2bjsndcf2bd88af9e'

            # The endpoint URL for the Bayut API
            url = "https://bayut.p.rapidapi.com/properties/list"

            # Headers required by RapidAPI
            headers = {
                'x-rapidapi-host': "bayut.p.rapidapi.com",
                'x-rapidapi-key': rapidapi_key,
                'content-type': "application/json"
            }

            # Data to be sent to Bayut API
            data = {
                'title': property_instance.title,
                'description': property_instance.description,
                'price': property_instance.price,
                'bedrooms': property_instance.bedrooms,
                'bathrooms': property_instance.bathrooms,
                'area': property_instance.area,
                'type': property_instance.property_type,
                'status': property_instance.status,
                # Add any other fields required by Bayut's API
            }

            # Make the POST request to the Bayut API
            response = requests.post(url, json=data, headers=headers)

            # Handle the response
            if response.ok:
                return JsonResponse(response.json(), safe=False)
            else:
                return JsonResponse({'error': 'Failed to add property to Bayut'}, status=response.status_code)

        except Property.DoesNotExist:
            return JsonResponse({'error': 'Property does not exist'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



# views.py
from django.http import JsonResponse
from django.shortcuts import render
import requests
from .models import Properties

def add_property(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')

        # Save property in the real estate website
        property_obj = Properties.objects.create(
            title=title,
            description=description,
            price=price,
        )

        # Send property data to the CRM website
        url = 'http://leadloom.pythonanywhere.com/api/add_property/'
        data = {
            'title': title,
            'description': description,
            'price': price,
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to add property to CRM'})
    else:
        return render(request, 'main/properties.html')


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PropertiesSerializer

class AddProperty(APIView):
    def post(self, request, format=None):
        # Deserialize the incoming JSON data using PropertiesSerializer
        serializer = PropertiesSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            # If data is valid, save the property
            serializer.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            # If data is invalid, return error response with serializer errors
            return Response({'status': 'error', 'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# views.py in Real Estate Website project
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Property
from .serializers import PropertySerializer
import requests

class SyncPropertiesFromCRM(APIView):
    def post(self, request):
        # Make a GET request to CRM API to fetch properties
        crm_api_url = 'https://leadloom.pythonanywhere.com//propertiesapi/'
        response = requests.get(crm_api_url)
        if response.status_code == 200:
            # Deserialize and save properties in real estate website
            properties_data = response.json()
            for property_data in properties_data:
                serializer = PropertySerializer(data=property_data)
                if serializer.is_valid():
                    serializer.save()
            return Response({"message": "Properties synced from CRM"})
        return Response({"error": "Failed to fetch properties from CRM"}, status=response.status_code)
