from django.contrib import admin
from .models import Vehicule
from django.contrib.auth.admin import UserAdmin
# Register your models here
@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_vehicule', 'capacite', 'statut', 'transporteur')
    list_filter = ('type_vehicule', 'statut')
    search_fields = ('id', 'transporteur__nom')
    ordering = ('-id',)
    list_per_page = 10
admin.site.register(Vehicule)