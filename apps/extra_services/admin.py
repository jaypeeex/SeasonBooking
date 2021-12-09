from django.contrib import admin

from .models import ExtraService
from .models import ExtraServiceCategory

admin.site.register(ExtraService)
admin.site.register(ExtraServiceCategory)
