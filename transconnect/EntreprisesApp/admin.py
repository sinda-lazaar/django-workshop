from django.contrib import admin
from .models import Entreprise, Utilisateur
from VehiculesApp.models import Vehicule
from django.contrib.auth.admin import UserAdmin
admin.site.site_header = "TransConnect -Administration"
admin.site.site_title = "TransConnect"
admin.site.index_title = 'Tableau de bord'
# Register your models here.
@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'role', 'first_name', 'last_name')
    list_filter = ('user_id','created_at')
    search_fields = ('user_id', 'first_name', 'last_name')
    list_editable = ('first_name','last_name')
    ordering=('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 1
#admin.site.register(Utilisateur,UtilisateurAdmin)
class VehiculeInline(admin.StackedInline):
    model = Vehicule
    fields=('immatriculation',)
    extra=1
class EntrepriseAdmin(admin.ModelAdmin):
    inlines = [VehiculeInline]
    list_display = ('raison_social',)
    fieldsets = (
        ('Identite entreprise' , {
            'fields' :('raison_social' , 'matricule_fiscal' , 'type_entreprise')
        }),
        ('contact',{
            'fields' :('adresse' , 'gerant')
        }),
        ('date systeme' , {
            'fields' :('created_at' , 'updated_at')
        })
    )
    readonly_fields=('created_at','updated_at')
admin.site.register(Entreprise, EntrepriseAdmin)
   
