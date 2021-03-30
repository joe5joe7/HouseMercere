import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from guardian.shortcuts import assign_perm

from characterSheets.models import Character, Saga, AbilityInstance, VirtueInstance, FlawInstance, Personality, \
    Reputation, SourceSet, Ability, VF, Equipment
from characterSheets.forms import changeSaga, createCharacterForm, \
    createCharacter_detailsForm, AbilityFormset, addCharacterToSaga, removeCharacterSaga, \
    confirmationForm, VirtueFormset, FlawFormset, characterBasicForm, characterDetailForm, abilitiesForm, \
    createCharacter_virtueForm, createCharacter_flawForm, personalityForm, reputationForm, addSourceSet, abiLibForm, \
    vfLibForm, equipLibForm, importVirtuesForm

import logging

logger = logging.getLogger(__name__)
logger.debug('Logging active')


class SagaDetailView(generic.DetailView):
    model = Saga


class SagaListView(generic.ListView):
    model = Saga


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


def SagaUpdate(request, pk):
    saga = get_object_or_404(Saga, pk=pk)
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
    form = createCharacterForm(request.POST or None)
    if form.is_valid():
        character = form.save()
        character.player = request.user
        character.save()

        if character.warping > 0 or character.decrepitude > 0:
            return HttpResponseRedirect('details/' + str(character.pk))
        else:
            return redirect('create-character-abilities', character.pk)


    else:
        print('invalid form!')
        print(form.is_bound)
        print(form.errors)
    context = {
        'form': form,
    }

    return render(request, 'characterSheets/create_character.html', context)


def createCharacter_details(request, pk):
    character = get_object_or_404(Character, pk=pk)
    form = createCharacter_detailsForm(request.POST or None, instance=character)
    if form.is_valid():
        form.save()
        return redirect('create-character-abilities', character.pk)
    context = {
        'form': form,
        'character': character,
    }

    return render(request, 'characterSheets/createCharacter_details.html', context)


def createCharacter_abilities(request, pk):
    character = get_object_or_404(Character, pk=pk)
    formset = AbilityFormset(request.POST or None, form_kwargs={'character': character})
    if formset.is_valid():
        print('valid ability form!')
        for form in formset:
            form.save()
        return redirect('create-character-vf', character.pk)
    else:
        print('invalid ability form')
        print('is_bound: ' + str(formset.is_bound))
        print('Errors: ' + str(formset.errors))

    context = {
        'formset': formset,
        'character': character,
    }

    return render(request, 'characterSheets/createCharacter_abilities.html', context)


def createCharacter_VF(request, pk):
    character = get_object_or_404(Character, pk=pk)
    virtueFormset = VirtueFormset(None, form_kwargs={'character': character})
    flawFormset = FlawFormset(None, form_kwargs={'character': character})

    if request.method == 'POST':
        virtueFormset = VirtueFormset(request.POST)
        flawFormset = FlawFormset(request.POST)
        if virtueFormset.is_valid() and flawFormset.is_valid():
            for form in virtueFormset:
                form.save()
            for form in flawFormset:
                form.save()
            return HttpResponseRedirect(character.get_absolute_url())

    context = {
        'virtueFormset': virtueFormset,
        'flawFormset': flawFormset,
    }

    return render(request, 'characterSheets/create_character_vf.html', context)


def CharacterCombatView(request, pk):
    character = get_object_or_404(Character, pk=pk)
    addSaga = addToSaga(request, character)

    context = {
        'character': character,
        'addCharacterToSaga': addSaga,
    }

    return render(request, 'characterSheets/character_combat.html', context)


def addToSaga(request, character):
    addSaga = addCharacterToSaga(None, instance=character)
    if request.method == 'POST':
        print(request.POST)
        if 'add' in request.POST:
            addSaga = addCharacterToSaga(request.POST, instance=character)
            if addSaga.is_valid():
                addSaga.save()
                return HttpResponseRedirect(character.get_absolute_url())
        elif 'remove' in request.POST:
            removeSaga = removeCharacterSaga(request.POST, instance=character)
            if removeSaga.is_valid():
                removeSaga.save()
                return HttpResponseRedirect(character.get_absolute_url())
        elif 'del' in request.POST:
            deleteCharacter = confirmationForm(request.POST)
            if deleteCharacter.is_valid():
                character.delete()
                return redirect('index')

    return addSaga


def CharacterDetailView(request, pk):
    character = get_object_or_404(Character, pk=pk)
    abilityList = AbilityInstance.objects.filter(owner=character)
    virtueList = VirtueInstance.objects.filter(owner=character)
    flawList = FlawInstance.objects.filter(owner=character)
    sagaMemberList = Saga.objects.filter(members=request.user)
    sagaStoryGuideList = Saga.objects.filter(storyGuide=request.user)
    addSaga = addToSaga(request, character)
    removeSaga = removeCharacterSaga(None, instance=character)
    deleteCharacter = confirmationForm(None)
    personalityList = Personality.objects.filter(owner=character)
    reputationList = Reputation.objects.filter(owner=character)

    # if request.method == 'POST':
    #     print(request.POST)
    #     if 'add' in request.POST:
    #         addSaga = addCharacterToSaga(request.POST, instance=character)
    #         if addSaga.is_valid():
    #             addSaga.save()
    #             return HttpResponseRedirect(character.get_absolute_url())
    #     elif 'remove' in request.POST:
    #         removeSaga = removeCharacterSaga(request.POST, instance=character)
    #         if removeSaga.is_valid():
    #             removeSaga.save()
    #             return HttpResponseRedirect(character.get_absolute_url())
    #     elif 'del' in request.POST:
    #         deleteCharacter = confirmationForm(request.POST)
    #         if deleteCharacter.is_valid():
    #             character.delete()
    #             return redirect('index')

    sagaList = list(sagaStoryGuideList) + list(set(sagaMemberList) - set(sagaStoryGuideList))

    context = {
        'character': character,
        'abilityList': abilityList,
        'virtueList': virtueList,
        'flawList': flawList,
        'sagaList': sagaList,
        'addCharacterToSaga': addSaga,
        'removeSaga': removeSaga,
        'deleteCharacter': deleteCharacter,
        'personalityList': personalityList,
        'reputationList': reputationList,
    }
    return render(request, 'characterSheets/character_detail.html', context)


def editCharacter(request, pk):
    character = get_object_or_404(Character, pk=pk)
    basicDetailsForm = characterBasicForm(None, instance=character, prefix='bd-form')
    moreDetailsForm = characterDetailForm(None, instance=character, prefix='md-form')
    abiExtra = 0
    virtExtra = 0
    flawExtra = 0
    personalityExtra = 0
    reputationExtra = 0
    if len(AbilityInstance.objects.filter(owner=character)) == 0:
        abiExtra = 1
    if len(VirtueInstance.objects.filter(owner=character)) == 0:
        virtExtra = 1
    if len(FlawInstance.objects.filter(owner=character)) == 0:
        flawExtra = 1
    if len(Personality.objects.filter(owner=character)) == 0:
        personalityExtra = 1
    if len(Reputation.objects.filter(owner=character)) == 0:
        reputationExtra = 1

    formset = modelformset_factory(AbilityInstance, form=abilitiesForm, extra=abiExtra, can_delete=True)
    abilityForm = formset(
        None,
        queryset=AbilityInstance.objects.filter(owner=character),
        form_kwargs={'character': character},
        prefix='abi-form',
    )
    vFormset = modelformset_factory(VirtueInstance, form=createCharacter_virtueForm, extra=virtExtra, can_delete=True)
    virtueForm = vFormset(
        None,
        queryset=VirtueInstance.objects.filter(owner=character),
        form_kwargs={'character': character},
        prefix='virtue-form',
    )
    fFormset = modelformset_factory(FlawInstance, form=createCharacter_flawForm, extra=flawExtra, can_delete=True)
    flawForm = fFormset(
        None,
        queryset=FlawInstance.objects.filter(owner=character),
        form_kwargs={'character': character},
        prefix='flaw-form',
    )
    pFormset = modelformset_factory(Personality, form=personalityForm, extra=personalityExtra, can_delete=True)
    pForm = pFormset(
        None,
        queryset=Personality.objects.filter(owner=character),
        form_kwargs={'character': character},
        prefix='personality-form'
    )
    rFormset = modelformset_factory(Reputation, form=reputationForm, extra=reputationExtra, can_delete=True)
    rForm = rFormset(
        None,
        queryset=Reputation.objects.filter(owner=character),
        form_kwargs={'character': character},
        prefix='reputation-form'
    )
    # confirm = confirmationForm(None)

    if request.method == 'POST':
        basicDetailsForm = characterBasicForm(request.POST, instance=character, prefix='bd-form')
        moreDetailsForm = characterDetailForm(request.POST, instance=character, prefix='md-form')
        abilityForm = formset(
            request.POST,
            queryset=AbilityInstance.objects.filter(owner=character),
            form_kwargs={'character': character},
            prefix='abi-form',
        )
        virtueForm = vFormset(
            request.POST,
            queryset=VirtueInstance.objects.filter(owner=character),
            form_kwargs={'character': character},
            prefix='virtue-form',
        )
        flawForm = fFormset(
            request.POST,
            queryset=FlawInstance.objects.filter(owner=character),
            form_kwargs={'character': character},
            prefix='flaw-form',
        )
        pForm = pFormset(
            request.POST,
            queryset=Personality.objects.filter(owner=character),
            form_kwargs={'character': character},
            prefix='personality-form'
        )
        rForm = rFormset(
            request.POST,
            queryset=Reputation.objects.filter(owner=character),
            form_kwargs={'character': character},
            prefix='reputation-form'
        )

        if basicDetailsForm.is_valid() and moreDetailsForm.is_valid() and abilityForm.is_valid() and virtueForm.is_valid() and flawForm.is_valid() and pForm.is_valid() and rForm.is_valid():
            basicDetailsForm.save()
            moreDetailsForm.save()
            abilityForm.save()
            virtueForm.save()
            flawForm.save()
            pForm.save()
            rForm.save()
            return HttpResponseRedirect(character.get_absolute_url())
        # elif not abilityForm.is_valid():
        #     print('invalid ability form')
        #     print('is_bound: ' + str(abilityForm.is_bound))
        #     print('Errors: ' + str(abilityForm.errors))
        # elif not basicDetailsForm.is_valid():
        #     print('invalid basic form')
        #     print('is_bound: ' + str(basicDetailsForm.is_bound))
        #     print('Errors: ' + str(basicDetailsForm.errors))
        # elif not moreDetailsForm.is_valid():
        #     print('invalid more form')
        #     print('is_bound: ' + str(moreDetailsForm.is_bound))
        #     print('Errors: ' + str(moreDetailsForm.errors))
        # elif not virtueForm.is_valid():
        #     print('invalid virtue form')
        #     print('is_bound: ' + str(virtueForm.is_bound))
        #     print('Errors: ' + str(virtueForm.errors))

    context = {
        'basicDetailsForm': basicDetailsForm,
        'moreDetailsForm': moreDetailsForm,
        'abilityForm': abilityForm,
        'virtueForm': virtueForm,
        'flawForm': flawForm,
        'character': character,
        'reputationForm': rForm,
        'personalityForm': pForm,
    }

    return render(request, 'characterSheets/edit_character.html', context)


def add_fatigue(request, pk):
    character = get_object_or_404(Character, pk=pk)
    if character.fatigueScore < 5:
        character.fatigueScore = F('fatigueScore') + 1
        character.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def subtract_fatigue(request, pk):
    character = get_object_or_404(Character, pk=pk)
    if character.fatigueScore > 0:
        character.fatigueScore = F('fatigueScore') - 1
        character.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_wound(request, pk, wound_type):
    character = get_object_or_404(Character, pk=pk)
    if wound_type == 'light':
        if character.lightWounds >= 5:
            pass
        else:
            character.lightWounds = F('lightWounds') + 1
    elif wound_type == 'medium':
        if character.mediumWounds >= 5:
            pass
        else:
            character.mediumWounds = F('mediumWounds') + 1
    elif wound_type == 'heavy':
        if character.heavyWounds >= 5:
            pass
        else:
            character.heavyWounds = F('heavyWounds') + 1
    elif wound_type == 'incapacitated':
        character.incapacitated = True
    elif wound_type == 'dead':
        character.dead = True

    character.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_wound(request, pk, wound_type):
    character = get_object_or_404(Character, pk=pk)
    if wound_type == 'light':
        if character.lightWounds <= 0:
            pass
        else:
            character.lightWounds = F('lightWounds') - 1
    elif wound_type == 'medium':
        if character.mediumWounds <= 0:
            pass
        else:
            character.mediumWounds = F('mediumWounds') - 1
    elif wound_type == 'heavy':
        if character.heavyWounds <= 0:
            pass
        else:
            character.heavyWounds = F('heavyWounds') - 1
    elif wound_type == 'incapacitated':
        character.incapacitated = False
    elif wound_type == 'dead':
        character.dead = False

    character.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_sourceset(request):
    sourceset = addSourceSet(request.POST or None)
    if request.POST:
        ss = sourceset.save()
        ss.save()
        assign_perm('characterSheets.source_can_edit', request.user, ss)
        return redirect('profile')

    context = {
        'sourceset': sourceset
    }

    return render(request, 'characterSheets/add_sourceset.html', context)


def view_sourceset(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    ssSagas = ss.saga_set.all()
    ssVirtues = ss.vf_set.filter(virtueOrFlaw='virtue')
    ssFlaws = ss.vf_set.filter(virtueOrFlaw='flaw')

    context = {
        'ss': ss,
        'ssVirtues': ssVirtues,
        'ssFlaws': ssFlaws,
    }

    return render(request, 'characterSheets/view_sourceset.html', context)


def edit_sourceset(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    abiExtra = 0
    virtExtra = 0
    flawExtra = 0
    equipExtra = 0
    if len(ss.ability_set.all()) == 0:
        abiExtra = 1
    if len(ss.vf_set.filter(virtueOrFlaw='virtue')) == 0:
        virtExtra = 1
    if len(ss.vf_set.filter(virtueOrFlaw='flaw')) == 0:
        flawExtra = 1
    if len(ss.equipment_set.all()) == 0:
        equipExtra = 1

    aformset = modelformset_factory(Ability, form=abiLibForm, extra=abiExtra, can_delete=True)
    abilityForm = aformset(
        None,
        queryset=ss.ability_set.all(),
        form_kwargs={'source': ss},
        prefix='abi-form',
    )
    vFormset = modelformset_factory(VF, form=vfLibForm, extra=virtExtra, can_delete=True)
    virtueForm = vFormset(
        None,
        queryset=ss.vf_set.filter(virtueOrFlaw='virtue'),
        form_kwargs={'source': ss, 'vf': 'virtue'},
        prefix='virtue-form',
    )
    fFormset = modelformset_factory(VF, form=vfLibForm, extra=flawExtra, can_delete=True)
    flawForm = fFormset(
        None,
        queryset=ss.vf_set.filter(virtueOrFlaw='flaw'),
        form_kwargs={'source': ss, 'vf': 'flaw'},
        prefix='flaw-form',
    )
    eFormset = modelformset_factory(Equipment, form=equipLibForm, extra=equipExtra, can_delete=True)
    equipForm = eFormset(
        None,
        queryset=ss.equipment_set.all(),
        form_kwargs={'source': ss},
        prefix='equip-form'
    )

    if request.method == 'POST':
        abilityForm = aformset(
            request.POST,
            queryset=ss.ability_set.all(),
            form_kwargs={'source': ss},
            prefix='abi-form',
        )
        virtueForm = vFormset(
            request.POST,
            queryset=ss.vf_set.filter(virtueOrFlaw='virtue'),
            form_kwargs={'source': ss, 'vf': 'virtue'},
            prefix='virtue-form',
        )
        flawForm = fFormset(
            request.POST,
            queryset=ss.vf_set.filter(virtueOrFlaw='flaw'),
            form_kwargs={'source': ss, 'vf': 'flaw'},
            prefix='flaw-form',
        )
        equipForm = eFormset(
            request.POST,
            queryset=ss.equipment_set.all(),
            form_kwargs={'source': ss},
            prefix='equip-form'
        )

        if abilityForm.is_valid() and virtueForm.is_valid() and flawForm.is_valid() and equipForm.is_valid():
            abilityForm.save()
            virtueForm.save()
            flawForm.save()
            equipForm.save()
            return HttpResponseRedirect(ss.get_absolute_url())

    context = {
        'abilityForm': abilityForm,
        'virtueForm': virtueForm,
        'flawForm': flawForm,
        'equipForm': equipForm,
    }

    return render(request, 'characterSheets/edit_sourceset.html', context)


def import_virtues(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    importForm = importVirtuesForm(None)
    if request.method == 'POST':
        importForm = importVirtuesForm(request.POST)
        if importForm.is_valid():
            data = importForm.cleaned_data['iData']
            for virtue in data:
                virtue.source = ss
                virtue.save()
            return HttpResponseRedirect(ss.get_absolute_url())

    context = {
        'importForm': importForm,
    }
    return render(request, 'characterSheets/import_virtues.html', context)


def sourceset_virtues(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    ssVirtues = ss.vf_set.filter(virtueOrFlaw='virtue')

    context = {
        'ssVirtues': ssVirtues,
        'ss': ss,
    }

    return render(request, 'characterSheets/sourceset_virtues.html', context)


def sourceset_flaws(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    ssFlaws = ss.vf_set.filter(virtueOrFlaw='flaw')

    context = {
        'ssFlaws': ssFlaws,
        'ss': ss,
    }

    return render(request, 'characterSheets/sourceset_flaws.html', context)


def sourceset_abilities(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)

    context = {
        'ss': ss,
    }

    return render(request, 'characterSheets/sourceset_abilities.html', context)


def sourceset_equipment(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)

    context = {
        'ss': ss,
    }

    return render(request, 'characterSheets/sourceset_equipment.html', context)


def edit_virtues(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)

    virtExtra = 0
    if len(ss.vf_set.filter(virtueOrFlaw='virtue')) == 0:
        virtExtra = 1

    vFormset = modelformset_factory(VF, form=vfLibForm, extra=virtExtra, can_delete=True)
    virtueForm = vFormset(
        None,
        queryset=ss.vf_set.filter(virtueOrFlaw='virtue'),
        form_kwargs={'source': ss, 'vf': 'virtue'},
        prefix='virtue-form',
    )

    if request.method == 'POST':
        virtueForm = vFormset(
            request.POST,
            queryset=ss.vf_set.filter(virtueOrFlaw='virtue'),
            form_kwargs={'source': ss, 'vf': 'virtue'},
            prefix='virtue-form',
        )

        if virtueForm.is_valid():
            virtueForm.save()
            return HttpResponseRedirect(ss.get_absolute_url())

    context = {
        'virtueForm': virtueForm,
    }

    return render(request, 'characterSheets/edit_virtues.html', context)
