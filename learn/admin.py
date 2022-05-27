from django.contrib import admin

from .models import English, Dutch, Translation
# Register your models here.

admin.site.register(English)
admin.site.register(Dutch)
admin.site.register(Translation)
