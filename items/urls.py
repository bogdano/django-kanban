from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('boards/', views.board_view, name='board_view'),
    path('create-item/', views.create_item, name='create_item'),
    path('delete-item/<int:pk>/', views.delete_item, name='delete_item'),
    path('update-item-position/<int:pk>/', views.update_item_position, name='update_item_position'),
    path('update-item-position-checked/<int:pk>/', views.update_item_position_checked, name='update_item_position_checked'),
    # Add more paths as needed for other views
]
