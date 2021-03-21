from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from characterSheets.models import Character, Ability, VF, Saga
from characterSheets.forms import editCharacter, changeSaga, changeCharacter


class SagaDetailView(generic.DetailView):
    model = Saga


class SagaListView(generic.ListView):
    model = Saga


class CharacterDetailView(generic.DetailView):
    model = Character


class CharactersByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic view for listing characters owned by a user."""
    model = Character
    template_name = 'characterSheets/character_list_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Character.objects.filter(player=self.request.user)



def createSaga(request):
    if request.method == 'POST':
        form = changeSaga(request.POST)

        if form.is_valid():
            saga = form.save()
            saga.save()
            return HttpResponseRedirect(saga.get_absolute_url())
    else:
        form = changeSaga(initial={'storyGuide': request.user})

    context = {
        'form': form,
    }

    return render(request, 'characterSheets/saga_form.html', context)


def SagaUpdate(request,pk):
    saga = get_object_or_404(Saga,pk=pk)
    form = changeSaga(request.POST or None, instance=saga)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(saga.get_absolute_url())
    context = {
        'form': form,
        'saga': saga,
    }

    return render(request, 'characterSheets/saga_form.html', context)


class SagaDelete(DeleteView):
    model = Saga
    success_url = reverse_lazy('sagas')



def createCharacter(request):
    form = changeCharacter(request.POST or None, initial={'player': request.user})
    if form.is_valid():
        character = form.save()
        character.save()
        return HttpResponseRedirect(character.get_absolute_url())
    context = {
        'form': form,
    }

    return render(request, 'characterSheets/character_form.html', context)


def editCharacter(request,pk):
    character = get_object_or_404(Character,pk=pk)
    form = changeCharacter(request.POST or None, instance=character)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(character.get_absolute_url())
    context = {
        'form': form,
        'character': character,
    }

    return render(request, 'characterSheets/character_form.html', context)
