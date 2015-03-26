from django.contrib import admin
from .models import Story, Variant, Option, Attribute

admin.site.register(Story)
admin.site.register(Variant)
admin.site.register(Option)
admin.site.register(Attribute)
