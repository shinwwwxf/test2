from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('salary/', views.salary_calculator, name='salary_calculator'),
    path('chatbot/salary/', views.salary_chatbot, name='salary_chatbot'),
    path('chatbot/absence/', views.absence_chatbot, name='absence_chatbot'),
    path('chatbot/entry/', views.entry_chatbot, name='entry_chatbot'),
]
