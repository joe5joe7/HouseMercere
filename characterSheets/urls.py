from django.urls import path, include
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('sagas/', views.SagaListView.as_view(), name='sagas'),
    path('sagas/<str:pk>', views.SagaDetailView.as_view(), name='saga-detail'),
    path('characters/<int:pk>', views.CharacterDetailView, name='character-detail'),
    path('mycharacters/', views.CharactersByUserListView.as_view(), name='my-characters'),
    path('saga/create/', views.createSaga, name='saga-create'),
    path('saga/<str:pk>/update',views.SagaUpdate, name='saga-update'),
    path('saga/<str:pk>/delete',views.SagaDelete.as_view(), name='saga-delete'),
    path('character/create/', views.createCharacter, name='character-create'),
    path('character/<int:pk>/edit/', views.editCharacter, name='edit-character'),
    path('character/create/details/<int:pk>', views.createCharacter_details, name='create-character-details'),
    path('character/create/abilities/<int:pk>', views.createCharacter_abilities, name='create-character-abilities'),
    path('character/create/vf/<int:pk>', views.createCharacter_VF,name='create-character-vf'),
    path('character/<int:pk>/addfatigue', views.add_fatigue, name='add-fatigue'),
    path('character/<int:pk>/subtractfatigue', views.subtract_fatigue, name='subtract-fatigue'),
    path('character/<int:pk>/addwound/<str:wound_type>', views.add_wound, name='add-wound'),
    path('character/<int:pk>/removewound/<str:wound_type>', views.remove_wound, name='remove-wound'),
    path('character/<int:pk>/charactercombat', views.CharacterCombatView, name='character-combat'),
    path('character/<int:pk>/characterequipment', views.CharacterEquipmentView, name='character-equipment'),
    path('equipment/<str:equipType>/<int:pk>/<str:status>', views.changeStatusEquip, name='change-status'),
    path('add_sourceset',views.add_sourceset, name='add-sourceset'),
    path('view_sourceset/<int:pk>', views.view_sourceset, name='view-sourceset'),
    path('import_virtues/<int:pk>', views.import_virtues, name='import-virtues'),
    path('sourceset_virtues/<int:pk>',views.sourceset_virtues, name='sourceset-virtues'),
    path('sourceset_flaws/<int:pk>',views.sourceset_flaws, name='sourceset-flaws'),
    path('sourceset_abilities/<int:pk>',views.sourceset_abilities, name='sourceset-abilities'),
    path('sourceset_equipment/<int:pk>',views.sourceset_equipment, name='sourceset-equipment'),
    path('sourceset_editvirtues/<int:pk>',views.edit_virtues, name='edit-virtues'),
    path('sourceset_exportvirtues/<int:pk>', views.export_virtues, name='export-virtues'),
    path('sourceset_delete/<int:pk>', views.delete_sourceset, name='delete-sourceset'),
    path('sourceset_editflaws/<int:pk>',views.edit_flaws, name='edit-flaws'),
    path('sourceset_exportflaws/<int:pk>', views.export_flaws, name='export-flaws'),
    path('import_flaws/<int:pk>', views.import_flaws, name='import-flaws'),
    path('sourceset_editabilities/<int:pk>',views.edit_abilities, name='edit-abilities'),
    path('sourceset_exportabilities/<int:pk>', views.export_abilities, name='export-abilities'),
    path('import_abilities/<int:pk>', views.import_abilities, name='import-abilities'),
    path('sourceset_subscribe/<int:pk>', views.subscribe_sourceset, name='subscribe-sourceset'),
    path('sourceset_unsubscribe/<int:pk>', views.unsubscribe_sourceset, name='unsubscribe-sourceset'),
    path('sourceset/equipment/delete/weapon/<int:pk>', views.delete_weapon, name='delete-weapon'),
    path('sourceset/equipment/delete/armor/<int:pk>', views.delete_armor, name='delete-armor'),
    path('sourceset/equipment/delete/misc/<int:pk>', views.delete_misc, name='delete-misc'),
]
