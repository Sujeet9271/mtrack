from django.contrib import admin
from .models import Profile

# Register your models here.
admin.site.register(Profile)

admin.site.site_header="Mtrack"
admin.site.site_title="Mtrack"