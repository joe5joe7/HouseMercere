from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import Character, Ability, Saga, VF, SourceSet

admin.site.register(Character)


@admin.register(VF)
class VFAdmin(admin.ModelAdmin):
    list_filter = ['virtueOrFlaw', 'type']


admin.site.register(Saga)


class sourcesetAdmin(GuardedModelAdmin):
    pass


admin.site.register(SourceSet, sourcesetAdmin)
