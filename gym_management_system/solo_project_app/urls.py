from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import trainer_search


urlpatterns = [
    
    path('', views.homepage, name='home'),  
    path('users',views.index),
    path('subscriptions',views.subscriptions),
    path('add_subscription/<int:id>',views.add_subscription),
    path('classes',views.classes),
    path('add_class',views.add_class),
    path('user/<int:id>/profile',views.user_profile),
    path('user/<int:id>/update/', views.update_profile, name='update_profile'),
    path('trainers/view',views.trainers_view),
    path('add_user_to_class',views.add_user_to_class),
    path('members/view',views.members_view),
    path('logout',views.logout),
    path('edit/class/<int:id>',views.edit_class),
    path('aboutus',views.aboutus),

    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
