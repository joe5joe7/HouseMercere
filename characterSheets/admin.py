from django.contrib import admin
from .models import Character, Ability, Saga, VF, Speciality

admin.site.register(Character)


class SpecialityInline(admin.TabularInline):
    model = Speciality

@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_filter = ['type']
    inlines = [SpecialityInline]

@admin.register(VF)
class VFAdmin(admin.ModelAdmin):
    list_filter = ['virtueOrFlaw','type']



admin.site.register(Saga)
