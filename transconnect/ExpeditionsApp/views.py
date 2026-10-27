from django.shortcuts import render
from .models import Expedition
def liste_expeditions(request):
    expeditions = (
      Expedition.objects
          .filter(statut='publiee')
          .select_related('entreprise')
            .order_by('-created_at')
)
    return render(request, 'expeditions/liste.html', {'expeditions': expeditions})
