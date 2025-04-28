from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path
from app import views


urlpatterns = [

    path('admin', admin.site.urls),

    path('', views.home, name='home'),
    path('order', views.create_order, name='create_order'),
    path('success', views.payment_success, name='payment_success'),
    path('verify', views.verify_signature, name='verify_signature')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
