import os, django

import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'houseMercere.settings')
django.setup()
from characterSheets.models import Ability, VF

Ability.objects.all().delete()
VF.objects.all().delete()
