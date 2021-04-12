from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import Character, Ability, Saga, VF, SourceSet, DefaultSpeciality, Weapon, WeaponInstance, ArmorInstance, \
    SpellGuideline, SpellGuidelineExample, spellCharacteristic

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
admin.site.register(ArmorInstance)
admin.site.register(SpellGuideline)
admin.site.register(SpellGuidelineExample)
admin.site.register(spellCharacteristic)

admin.site.register(DefaultSpeciality)
