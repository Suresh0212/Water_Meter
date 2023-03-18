from django.urls import path
from . import views
urlpatterns = [
    path('', views.data),
    # path('test-api', views.get_data),
    path('api', views.ChartData.as_view()),
    # path('', views.home, name="home")
]