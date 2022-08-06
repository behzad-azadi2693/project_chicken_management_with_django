from django.urls import path
from .views import signin, signout

app_name = 'accounts'


urlpatterns = [
    path('', signin, name='signin'),
    path('signout/', signout, name='signout'),
]