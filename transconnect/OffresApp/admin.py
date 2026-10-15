from django.contrib import admin
from .models import Offre
from django.contrib.auth.admin import UserAdmin
# Register your models here.    
@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'prix', 'date_proposition', 'delai_jours', 'statut', 'transporteur', 'expedition', 'vehicule')
    list_filter = ('statut', 'date_proposition')
    search_fields = ('id', 'transporteur__nom', 'expedition__id')
    ordering = ('-date_proposition',)
    date_hierarchy = 'date_proposition'
    list_per_page = 10
admin.site.register(Offre)