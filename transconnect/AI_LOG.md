## Entrée 05/10/2026

- Outil IA utilisé : ChatGPT

- Prompt :
  Analyse le modèle Offre fourni dans l'exercice « Bug Hunt tracé »
  et identifie les anomalies par rapport au cahier des charges.

- Sortie obtenue (résumé) :
  L'IA a identifié 4 anomalies dans le modèle Offre :
  1. prix utilise CharField au lieu de DecimalField.
  2. delai_jours utilise IntegerField au lieu de PositiveIntegerField.
  3. date_proposition utilise auto_now au lieu de auto_now_add.
  4. vehicule autorise une valeur NULL avec null=True.

- Écarts identifiés vs cahier des charges :
  - prix doit être un DecimalField.
  - delai_jours doit être un PositiveIntegerField.
  - date_proposition doit utiliser auto_now_add=True.
  - vehicule ne doit pas autoriser NULL.

- Correction apportée et justification :
  - Remplacement de CharField par DecimalField pour représenter correctement un prix décimal.
  - Remplacement de IntegerField par PositiveIntegerField afin d'empêcher les valeurs négatives pour le délai.
  - Remplacement de auto_now=True par auto_now_add=True afin que la date corresponde à la création de l'offre.
  - Suppression de null=True afin que chaque offre soit obligatoirement associée à un véhicule.