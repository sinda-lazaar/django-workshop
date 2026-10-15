from django.contrib import admin
from.models import Expedition
from django.contrib.auth.admin import UserAdmin
# Register your models here.
@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'chargeur', 'date_creation', 'statut')
    list_filter = ('statut', 'date_creation')
    search_fields = ('id', 'chargeur__user_id')
    ordering = ('-date_creation',)
    date_hierarchy = 'date_creation'
    list_per_page = 10
admin.site.register(Expedition)