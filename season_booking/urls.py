"""season_booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.items.views import create_item
from apps.accounts.views import user_register, user_login, user_logout
from apps.bookings.views import index, check_availability, book_apartment, booking_confirm, redirect_to_payment, dashboard, webpay_return, historical_booking, payment_success, payment_failed
from apps.apartments.views import register_apartment, edit_apartment, apartment_list, apartment_extra_services, apartment_inventory, delete_inventory_item, create_inventory_item
from apps.extra_services.views import register_extra_service, extra_services_list, edit_extra_service
from apps.bookings.views import check_in
from apps.reports.views import bookings_report
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('apartment/register', register_apartment, name='register_apartment'),
    path('extra_services/register', register_extra_service, name='register_extra_service'),
    path('extra_service/edit/<int:extra_service_id>/', edit_extra_service, name='edit_extra_service'),
    path('extra_services/list', extra_services_list, name='extra_services_list'),
    path('apartment/extra-services/<int:apartment_id>/', apartment_extra_services, name="apartment_extra_services"),
    path('book/apartment/<int:apartment_id>/', book_apartment, name="book_apartment"),
    path('booking/confirm/<int:apartment_id>/', booking_confirm, name="booking_confirm"),
    path('redirect-to-payment/', redirect_to_payment, name="redirect_to_payment"),
    path('apartment/edit/<int:apartment_id>/', edit_apartment, name="edit_apartment"),
    path('apartment/list/', apartment_list, name="apartment_list"),
    path('check-availability/', check_availability, name='check_availability'),
    path('webpay-return/', webpay_return, name="webpay_return"),
    path('create-item/', create_item, name='create-item'),
    path('apartment/<int:apartment_id>/inventory', apartment_inventory, name='apartment_inventory'),
    path('delete-inventory-item/<int:apartment_id>/<int:inventory_item_id>', delete_inventory_item, name='delete_inventory_item'),
    path('inventory/item/<int:inventory_id>/', create_inventory_item, name='create_inventory_item'),
    path('check-in/', check_in, name='check_in'),
    path('reports/bookings', bookings_report, name='bookings_report'),
    path('historical-booking/', historical_booking, name='historical_booking'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/failed/', payment_failed, name='payment_failed'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
