from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import getUserCard
from .views import getCardAPI
from .views import getCardTagAPI
from .views import makeFavCard


urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('getUserCard/#/?q=card', getUserCard, name='getUserCard'),
    path('getCardAPI/<str:card_name>/', getCardAPI, name='getCardAPI'),
    path('getCardTagAPI/<str:print_tag>/', getCardTagAPI, name='getCardTagAPI'),
    path('makeFavCard/', makeFavCard, name='makeFavCard')
    
    #add url for view of favorite cards

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
