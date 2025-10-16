from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='index'),
    path('toggle/<int:box_id>/', views.toggle_box, name='toggle_box'),
    path('initialize/', views.initialize_boxes_view, name='initialize_boxes'),
]