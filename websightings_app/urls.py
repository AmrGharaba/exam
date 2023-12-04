from django.urls import path
from . import views

urlpatterns = [
    path('',views.root),
    path('user_processing',views.user_processing),
    path('dashboard',views.user_dashboard),
    path('sightings/new',views.new_sighting),
    path('sightings/add_sighting', views.add_sighting),
    path('sightings/<id>',views.details),
    path('sightings/edit/<id>',views.edit_form),
    path('sightings/edit_process/<id>', views.edit_process),
    path('logout',views.logout),
    path('skeptic/<id>',views.add_skeptic),
    path('delete/<id>',views.delete)
]