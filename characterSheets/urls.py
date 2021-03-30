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
    path('add_sourceset',views.add_sourceset, name='add-sourceset'),
    path('view_sourceset/<int:pk>', views.view_sourceset, name='view-sourceset'),
    path('edit_sourceset/<int:pk>', views.edit_sourceset, name='edit-sourceset'),
    path('import_virtues/<int:pk>', views.import_virtues, name='import-virtues'),
]
