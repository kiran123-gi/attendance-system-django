from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('add/', views.add_student),
    path('mark/', views.mark_attendance),
    path('dashboard/', views.dashboard_data),
    path('upload/', views.upload_excel),
]