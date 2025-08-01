from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('base', views.BASE, name='base'),
    path('', views.HOME2, name='home2'),
    path('about', views.ABOUT, name='about'),
    path('privacy', views.PRIVACY, name='privacy'),
    path('contact', views.CONTACT, name='contact'),
    path('propertydetail', views.propertydetail, name='propertydetail'),
    path('burjazizi-landing', views.burjazizi, name='burjazizi-landing'),
    path('aljada', views.aljada, name='aljada'),
    path('properties', views.PROPERTIES, name='properties'),
    path('singlepage/<int:pk>', views.SINGLEPAGE, name='singlepage'),
    path('property_search', views.property_search, name='property_search'),
    path('filter_search', views.Filter_Search, name='Filter_Search'),
    path('compare/', views.COMPARE, name='compare'),
    path('coming', views.COMING, name='coming'),
    path('add_property_to_bayut/<int:property_id>/', views.add_property_to_bayut, name='add_property_to_bayut'),
    # path('add_property/',views.add_property, name='add_property'),
    path('api/add_property/',views.AddProperty.as_view(), name='add_property'),
    path('sync-properties-from-crm/',views.SyncPropertiesFromCRM.as_view(), name='sync_properties_from_crm'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
