from django.urls import path, include
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('sagas/', views.SagaListView.as_view(), name='sagas'),
    path('sagas/<str:pk>', views.SagaDetailView.as_view(), name='saga-detail'),
    path('characters/<int:pk>', views.CharacterDetailView.as_view(), name='character-detail'),
    path('mycharacters/', views.CharactersByUserListView.as_view(), name='my-characters'),
    path('saga/create/', views.createSaga, name='saga-create'),
    path('saga/<str:pk>/update',views.SagaUpdate, name='saga-update'),
    path('saga/<str:pk>/delete',views.SagaDelete.as_view(), name='saga-delete'),
    path('characters/create/', views.createCharacter, name='character-create'),
    path('character/<int:pk>/edit/', views.editCharacter, name='edit-character'),
]
