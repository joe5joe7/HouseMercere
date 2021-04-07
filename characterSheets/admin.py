from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import Character, Ability, Saga, VF, SourceSet, DefaultSpeciality, Weapon, WeaponInstance

admin.site.register(Character)


@admin.register(VF)
class VFAdmin(admin.ModelAdmin):
    list_filter = ['virtueOrFlaw', 'type']


admin.site.register(Saga)


class sourcesetAdmin(GuardedModelAdmin):
    pass


admin.site.register(SourceSet, sourcesetAdmin)
admin.site.register(Weapon)
admin.site.register(WeaponInstance)

admin.site.register(DefaultSpeciality)
