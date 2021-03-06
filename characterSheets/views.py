import logging

from django.contrib import messages
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
    Reputation, SourceSet, Ability, VF, DefaultSpeciality, Weapon, Armor, MiscEquip, WeaponInstance, ArmorInstance, \
    MiscEquipInstance, SpellGuideline, SpellGuidelineExample, Spell, spellCharacteristic, Art, SpellInstance
from characterSheets.forms import changeSaga, createCharacterForm, \
    createCharacter_detailsForm, AbilityFormset, addCharacterToSaga, removeCharacterSaga, \
    confirmationForm, VirtueFormset, FlawFormset, characterBasicForm, characterDetailForm, abilitiesForm, \
    createCharacter_virtueForm, createCharacter_flawForm, personalityForm, reputationForm, addSourceSet, abiLibForm, \
    vfLibForm, weaponLibForm, importVirtuesForm, importFlawsForm, importAbilitiesForm, armorLibForm, miscEquipLibForm, \
    weaponInstForm, armorInstForm, miscInstForm, spellGuidelineForm, spellGuidelineExampleForm, \
    importSpellGuidelineExamples, addCharacteristic, spellLibForm, importSpells, characterArt, characterSpell

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

        return redirect('edit-character', character.pk)


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


def CharacterMagicView(request, pk):
    character = get_object_or_404(Character, pk=pk)
    arts = Art.objects.filter(character=character)
    spells = SpellInstance.objects.filter(character=character)
    artsFormset = modelformset_factory(Art, form=characterArt, extra=15 - len(arts), can_delete=True)
    artsForm = artsFormset(
        None,
        queryset=character.art_set.all(),
        form_kwargs={'character': character},
        prefix='arts-form',
    )
    spellForm = characterSpell(request.POST or None, character=character)

    if request.method == 'POST':
        artsForm = artsFormset(
            request.POST,
            queryset=character.art_set.all(),
            form_kwargs={'character': character},
            prefix='arts-form',
        )
        if spellForm.is_valid():
            spellForm.save()
            return redirect('character-magic', pk=pk)
        if artsForm.is_valid():
            artsForm.save()
            return redirect('character-magic', pk=pk)

    context = {
        'character': character,
        'arts': arts,
        'spells': spells,
        'artsForm': artsForm,
        'spellForm': spellForm,
    }

    return render(request, 'characterSheets/character_magic.html', context)


def CharacterEquipmentView(request, pk):
    character = get_object_or_404(Character, pk=pk)
    addSaga = addToSaga(request, character)
    weaponForm = weaponInstForm(user=request.user, owner=character)
    armorForm = armorInstForm(user=request.user, owner=character)
    miscEquipForm = miscInstForm(user=request.user, owner=character)
    if request.method == 'POST':
        if request.POST.get('form-type') == 'weapon':
            weaponForm = weaponInstForm(request.POST, user=request.user, owner=character)
            if weaponForm.is_valid():
                weaponForm.save()
                return redirect('character-equipment', pk=pk)
        elif request.POST.get('form-type') == 'armor':
            armorForm = armorInstForm(request.POST, user=request.user, owner=character)
            if armorForm.is_valid():
                armorForm.save()
                return redirect('character-equipment', pk=pk)
        elif request.POST.get('form-type') == 'misc':
            miscEquipForm = miscInstForm(user=request.user, owner=character)
            if miscEquipForm.is_valid():
                miscEquipForm.save()
                return redirect('character-equipment', pk=pk)

    context = {
        'character': character,
        'addCharacterToSaga': addSaga,
        'weaponForm': weaponForm,
        'armorForm': armorForm,
        'miscEquipForm': miscEquipForm,
    }

    return render(request, 'characterSheets/character_equipment.html', context)


def changeStatusEquip(request, pk, equipType, status):
    if equipType == 'weapon':
        equip = get_object_or_404(WeaponInstance, pk=pk)
        if status == 'e':
            if equip.referenceWeapon.shield:
                numEquipped = WeaponInstance.objects.filter(ownerChar=equip.ownerChar, status='e',
                                                            referenceWeapon__shield=True).count()
                if numEquipped >= 1:
                    messages.error(request, 'Character already has a shield equipped.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                if WeaponInstance.objects.filter(ownerChar=equip.ownerChar, status='e', referenceWeapon__shield=False,
                                                 referenceWeapon__twoHanded=True).first() is not None and equip.referenceWeapon.freeHand is False:
                    messages.error(request, 'Character has a two handed weapon equipped.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                if equip.referenceWeapon.twoHanded:
                    numEquipped = WeaponInstance.objects.filter(ownerChar=equip.ownerChar, status='e').count()
                    if numEquipped >= 1:
                        messages.error(request,
                                       equip.__str__() + ' is a two-handed weapon, character already has another item equipped')
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                numEquipped = WeaponInstance.objects.filter(ownerChar=equip.ownerChar, status='e',
                                                            referenceWeapon__shield=False).count()
                if numEquipped >= 1:
                    messages.error(request, 'Character already has a non-shield weapons equipped.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    elif equipType == 'armor':
        equip = get_object_or_404(ArmorInstance, pk=pk)
        if status == 'e':
            equippedArmor = ArmorInstance.objects.filter(ownerChar=equip.ownerChar, status='e').first()
            if equippedArmor:
                equippedArmor.status = 'c'
                equippedArmor.save()
    elif equipType == 'misc':
        equip = get_object_or_404(MiscEquipInstance, pk=pk)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    equip.status = status
    equip.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def changePartialArmor(request, pk):
    armor = get_object_or_404(ArmorInstance, pk=pk)
    if armor.partial:
        armor.partial = False
    else:
        armor.partial = True
    armor.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
        form_kwargs={'character': character, 'user': request.user},
        prefix='abi-form',
    )
    vFormset = modelformset_factory(VirtueInstance, form=createCharacter_virtueForm, extra=virtExtra, can_delete=True)
    virtueForm = vFormset(
        None,
        queryset=VirtueInstance.objects.filter(owner=character),
        form_kwargs={'character': character, 'user': request.user},
        prefix='virtue-form',
    )
    fFormset = modelformset_factory(FlawInstance, form=createCharacter_flawForm, extra=flawExtra, can_delete=True)
    flawForm = fFormset(
        None,
        queryset=FlawInstance.objects.filter(owner=character),
        form_kwargs={'character': character, 'user': request.user},
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
            form_kwargs={'character': character, 'user': request.user},
            prefix='abi-form',
        )
        virtueForm = vFormset(
            request.POST,
            queryset=VirtueInstance.objects.filter(owner=character),
            form_kwargs={'character': character, 'user': request.user},
            prefix='virtue-form',
        )
        flawForm = fFormset(
            request.POST,
            queryset=FlawInstance.objects.filter(owner=character),
            form_kwargs={'character': character, 'user': request.user},
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


def delete_sourceset(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    ss.delete()

    return redirect('index')


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
            return redirect('sourceset-virtues', pk=ss.id)

    context = {
        'importForm': importForm,
    }
    return render(request, 'characterSheets/import_virtues.html', context)


def export_virtues(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    output = '{'
    ssVirtues = ss.vf_set.filter(virtueOrFlaw='virtue')
    for virtue in ssVirtues:
        output += '"' + virtue.name + '":{"name":"' + virtue.name + '","description":"' + virtue.description + '","value":"' + virtue.value + '","type":"' + virtue.type + '"},'
    output = output[:-1]
    output += '}'

    context = {
        'ss': ss,
        'output': output
    }

    return render(request, 'characterSheets/export_virtues.html', context)


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
            return redirect('sourceset-virtues', pk=ss.id)

    context = {
        'virtueForm': virtueForm,
        'ss': ss,
    }

    return render(request, 'characterSheets/edit_virtues.html', context)


def import_flaws(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    importForm = importFlawsForm(None)
    if request.method == 'POST':
        importForm = importFlawsForm(request.POST)
        if importForm.is_valid():
            data = importForm.cleaned_data['iData']
            for flaw in data:
                flaw.source = ss
                flaw.save()
            return redirect('sourceset-flaws', pk=ss.id)

    context = {
        'importForm': importForm,
    }
    return render(request, 'characterSheets/import_virtues.html', context)


def export_flaws(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    output = '{'
    ssFlaws = ss.vf_set.filter(virtueOrFlaw='flaw')
    for flaw in ssFlaws:
        output += '"' + flaw.name + '":{"name":"' + flaw.name + '","description":"' + flaw.description + '","value":"' + flaw.value + '","type":"' + flaw.type + '"},'
    output = output[:-1]
    output += '}'

    context = {
        'ss': ss,
        'output': output
    }

    return render(request, 'characterSheets/export_virtues.html', context)


def edit_flaws(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)

    flawExtra = 0
    if len(ss.vf_set.filter(virtueOrFlaw='flaw')) == 0:
        flawExtra = 1

    fFormset = modelformset_factory(VF, form=vfLibForm, extra=flawExtra, can_delete=True)
    flawForm = fFormset(
        None,
        queryset=ss.vf_set.filter(virtueOrFlaw='flaw'),
        form_kwargs={'source': ss, 'vf': 'flaw'},
        prefix='flaw-form',
    )

    if request.method == 'POST':
        flawForm = fFormset(
            request.POST,
            queryset=ss.vf_set.filter(virtueOrFlaw='flaw'),
            form_kwargs={'source': ss, 'vf': 'flaw'},
            prefix='flaw-form',
        )

        if flawForm.is_valid():
            flawForm.save()
            return redirect('sourceset-flaws', pk=ss.id)

    context = {
        'flawForm': flawForm,
        'ss': ss,
    }

    return render(request, 'characterSheets/edit_flaws.html', context)


def import_abilities(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    importForm = importAbilitiesForm(None)
    if request.method == 'POST':
        importForm = importAbilitiesForm(request.POST)
        if importForm.is_valid():
            data = importForm.cleaned_data['iData']
            for pair in data:
                newAbi = pair[0]
                specs = pair[1]
                newAbi.source = ss
                newAbi.save()
                for spec in specs:
                    newSpec = DefaultSpeciality()
                    newSpec.name = spec
                    newSpec.abi = newAbi
                    newSpec.save()
            return redirect('sourceset-abilities', pk=ss.id)

    context = {
        'importForm': importForm,
    }
    return render(request, 'characterSheets/import_virtues.html', context)


def export_abilities(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    output = '{'
    ssAbilities = ss.ability_set.all()
    for abi in ssAbilities:
        output += '"' + abi.name + '":{"name":"' + abi.name + '","description":"' + abi.description + '","needTraining":"' + str(
            abi.needTraining) + '","type":"' + abi.type + '","specialties":['
        for spec in abi.defaultspeciality_set.all():
            output += '"' + spec.name + '",'
        output = output[:-1]
        output += '],'

    output = output[:-1]
    output += '}'

    context = {
        'ss': ss,
        'output': output
    }
    return render(request, 'characterSheets/export_virtues.html', context)


def edit_abilities(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)

    abiExtra = 0
    if len(ss.ability_set.all()) == 0:
        abiExtra = 1

    aFormset = modelformset_factory(Ability, form=abiLibForm, extra=abiExtra, can_delete=True)
    abiForm = aFormset(
        None,
        queryset=ss.ability_set.all(),
        form_kwargs={'source': ss},
        prefix='abi-form',
    )

    if request.method == 'POST':
        abiForm = aFormset(
            request.POST,
            queryset=ss.ability_set.all(),
            form_kwargs={'source': ss},
            prefix='abi-form',
        )

        if abiForm.is_valid():
            abiForm.save()
            for form in abiForm:
                if Ability.objects.filter(pk=form.cleaned_data['specialties'][1].id).exists():
                    for spec in form.cleaned_data['specialties'][1].defaultspeciality_set.all():
                        spec.delete()
                    for spec in form.cleaned_data['specialties'][0]:
                        newSpec = DefaultSpeciality()
                        newSpec.name = spec
                        newSpec.abi = form.cleaned_data['specialties'][1]
                        newSpec.save()

            return redirect('sourceset-abilities', pk=ss.id)

    context = {
        'abilityForm': abiForm,
        'ss': ss,
    }

    return render(request, 'characterSheets/edit_abilities.html', context)


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
    weaponForm = weaponLibForm(request.POST or None, source=ss)
    armorForm = armorLibForm(request.POST or None, source=ss)
    miscEquipForm = miscEquipLibForm(request.POST or None, source=ss)
    if request.method == 'POST':
        form_type = request.POST.get('form-type')
        if form_type == 'weapon' and weaponForm.is_valid():
            weaponForm.save()
            return redirect('sourceset-equipment', pk=pk)
        elif form_type == 'armor' and armorForm.is_valid():
            armorForm.save()
            return redirect('sourceset-equipment', pk=pk)
        elif form_type == 'misc' and miscEquipForm.is_valid():
            miscEquipForm.save()
            return redirect('sourceset-equipment', pk=pk)

    context = {
        'ss': ss,
        'weaponForm': weaponForm,
        'armorForm': armorForm,
        'miscEquipForm': miscEquipForm,
    }

    return render(request, 'characterSheets/sourceset_equipment.html', context)


def delete_weapon(request, pk):
    weapon = get_object_or_404(Weapon, pk=pk)
    source = weapon.source
    weapon.delete()
    return redirect(source.get_equipment_url())


def delete_armor(request, pk):
    armor = get_object_or_404(Armor, pk=pk)
    source = armor.source
    armor.delete()
    return redirect(source.get_equipment_url())


def delete_misc(request, pk):
    misc = get_object_or_404(MiscEquip, pk=pk)
    source = misc.source
    misc.delete()
    return redirect(source.get_equipment_url())


def subscribe_sourceset(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    ss.subscribers.add(request.user)

    return redirect('view-sourceset', pk=ss.id)


def unsubscribe_sourceset(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    ss.subscribers.remove(request.user)

    return redirect('view-sourceset', pk=ss.id)


def sourceset_spells(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    forms = (
        'creo',
        'intellego',
        'muto',
        'perdo',
        'rego'
    )
    techniques = (
        'animal',
        'aquam',
        'auram',
        'corpus',
        'herbam',
        'ignem',
        'imaginem',
        'mentem',
        'terram',
        'vim'
    )

    context = {
        'ss': ss,
        'forms': forms,
        'techniques': techniques
    }

    return render(request, 'characterSheets/sourceset_spells.html', context)


def sourceset_form(request, pk, f):
    ss = get_object_or_404(SourceSet, pk=pk)
    forms = (
        'creo',
        'intellego',
        'muto',
        'perdo',
        'rego'
    )
    techniques = (
        'animal',
        'aquam',
        'auram',
        'corpus',
        'herbam',
        'ignem',
        'imaginem',
        'mentem',
        'terram',
        'vim'
    )

    context = {
        'ss': ss,
        'selectedForm': f,
        'forms': forms,
        'techniques': techniques
    }

    return render(request, 'characterSheets/sourceset_spells_form.html', context)


def sourceset_technique(request, pk, t):
    ss = get_object_or_404(SourceSet, pk=pk)
    forms = (
        'creo',
        'intellego',
        'muto',
        'perdo',
        'rego'
    )
    techniques = (
        'animal',
        'aquam',
        'auram',
        'corpus',
        'herbam',
        'ignem',
        'imaginem',
        'mentem',
        'terram',
        'vim'
    )

    context = {
        'ss': ss,
        'selectedTechnique': t,
        'forms': forms,
        'techniques': techniques
    }

    return render(request, 'characterSheets/sourceset_spells_technique.html', context)


def sourceset_guideline(request, pk, t, f):
    ss = get_object_or_404(SourceSet, pk=pk)
    formsDetailed = {
        'creo': 'cr',
        'intellego': 'in',
        'muto': 'mu',
        'perdo': 'pe',
        'rego': 're',
    }
    techniquesDetailed = {
        'animal': 'an',
        'aquam': 'aq',
        'auram': 'au',
        'corpus': 'co',
        'herbam': 'he',
        'ignem': 'ig',
        'imaginem': 'im',
        'mentem': 'me',
        'terram': 'te',
        'vim': 'vi',
    }
    guideline = SpellGuideline.objects.filter(form=formsDetailed[f], technique=techniquesDetailed[t]).first()
    examples = SpellGuidelineExample.objects.filter(guideline=guideline)

    spells = Spell.objects.filter(form=guideline.form, technique=guideline.technique, source=ss)
    spells = sorted(spells, key=lambda a: a.level())

    if guideline is None:
        form = spellGuidelineForm(request.POST or None, form=formsDetailed[f], technique=techniquesDetailed[t])
    else:
        form = spellGuidelineExampleForm(request.POST or None, guideline=guideline, source=ss)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('sourceset-spells-guideline', pk=pk, f=f, t=t)

    context = {
        'ss': ss,
        'selectedTechnique': t,
        'selectedForm': f,
        'forms': formsDetailed.keys(),
        'techniques': techniquesDetailed.keys(),
        'guideline': guideline,
        'examples': examples,
        'form': form,
        'spells': spells,
    }

    return render(request, 'characterSheets/sourceset_spells_guideline.html', context)


def source_guideline_import_spells(request, pk, guideline):
    ss = get_object_or_404(SourceSet, pk=pk)
    guideline = get_object_or_404(SpellGuideline, pk=guideline)
    forms = []
    for frm in guideline.forms:
        forms.append(frm[1])
    techniques = []
    for technique in guideline.techniques:
        techniques.append(technique[1])

    form = importSpells(request.POST or None, source=ss, form=guideline.form, technique=guideline.technique)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data['iData']
            for spell in data:
                spell.save()

            return redirect('sourceset-spells-guideline', pk=pk, f=guideline.get_form_display(),
                            t=guideline.get_technique_display())

    context = {
        'form': form,
        'ss': ss,
        'selectedTechnique': guideline.get_technique_display(),
        'selectedForm': guideline.get_form_display(),
        'forms': forms,
        'techniques': techniques,
    }

    return render(request, 'characterSheets/sourceset_spells_guideline_import.html', context)


def source_guidelines_import(request, pk, guideline):
    ss = get_object_or_404(SourceSet, pk=pk)
    guideline = get_object_or_404(SpellGuideline, pk=guideline)
    forms = []
    for form in guideline.forms:
        forms.append(form[1])
    techniques = []
    for technique in guideline.techniques:
        techniques.append(technique[1])

    form = importSpellGuidelineExamples(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data['iData']
            for example in data:
                example.source = ss
                example.guideline = guideline
                example.save()

            return redirect('sourceset-spells-guideline', pk=pk, f=guideline.get_form_display(),
                            t=guideline.get_technique_display())

    context = {
        'form': form,
        'ss': ss,
        'selectedTechnique': guideline.get_technique_display(),
        'selectedForm': guideline.get_form_display(),
        'forms': forms,
        'techniques': techniques,
    }

    return render(request, 'characterSheets/sourceset_spells_guideline_import.html', context)


def source_spellCharacteristics(request, pk):
    ss = get_object_or_404(SourceSet, pk=pk)
    ranges = ss.spellcharacteristic_set.filter(type='r')
    durations = ss.spellcharacteristic_set.filter(type='d')
    targets = ss.spellcharacteristic_set.filter(type='t')
    form = addCharacteristic(request.POST or None, source=ss)
    if request.method == 'POST':
        if form.is_valid():
            form.save()

    context = {
        'ss': ss,
        'ranges': ranges,
        'durations': durations,
        'targets': targets,
        'form': form,
    }

    return render(request, 'characterSheets/sourceset_spellCharacteristics.html', context)


def source_guideline_addSpell(request, pk, guideline):
    ss = get_object_or_404(SourceSet, pk=pk)
    guideline = get_object_or_404(SpellGuideline, pk=guideline)
    form = spellLibForm(request.POST or None, source=ss, guideline=guideline)
    if request.method == 'POST':
        if form.is_valid():
            logger.error('form is valid')
            form.save()
            logger.error('form saved')
            return redirect('sourceset-spells-guideline', pk=ss.id, f=guideline.get_form_display(),
                            t=guideline.get_technique_display())
        else:
            logger.error('form not valid')
            logger.error(form.errors)
            logger.error(form.is_bound)

    forms = []
    for x in guideline.forms:
        forms.append(x[1])
    techniques = []
    for technique in guideline.techniques:
        techniques.append(technique[1])

    context = {
        'ss': ss,
        'guideline': guideline,
        'selectedForm': guideline.get_form_display(),
        'selectedTechnique': guideline.get_technique_display(),
        'forms': forms,
        'techniques': techniques,
        'form': form,
    }

    return render(request, 'characterSheets/sourceset_addSpell.html', context)


def delete_spellCharacteristic(request, pk):
    char = get_object_or_404(spellCharacteristic, pk=pk)
    char.delete()

    return redirect('sourceset-char', pk=char.source_id)


def create_spellLanding(request):
    forms = (
        'creo',
        'intellego',
        'muto',
        'perdo',
        'rego'
    )
    techniques = (
        'animal',
        'aquam',
        'auram',
        'corpus',
        'herbam',
        'ignem',
        'imaginem',
        'mentem',
        'terram',
        'vim'
    )

    context = {
        'forms': forms,
        'techniques': techniques,
    }

    return render(request, 'characterSheets/createSpellLanding.html', context)


def create_spell_form(request, f):
    forms = (
        'creo',
        'intellego',
        'muto',
        'perdo',
        'rego'
    )
    techniques = (
        'animal',
        'aquam',
        'auram',
        'corpus',
        'herbam',
        'ignem',
        'imaginem',
        'mentem',
        'terram',
        'vim'
    )

    context = {
        'forms': forms,
        'techniques': techniques,
        'selectedForm': f,
    }

    return render(request, 'characterSheets/createSpellForm.html', context)


def create_spell_technique(request, t):
    forms = (
        'creo',
        'intellego',
        'muto',
        'perdo',
        'rego'
    )
    techniques = (
        'animal',
        'aquam',
        'auram',
        'corpus',
        'herbam',
        'ignem',
        'imaginem',
        'mentem',
        'terram',
        'vim'
    )

    context = {
        'forms': forms,
        'techniques': techniques,
        'selectedTechnique': t,
    }

    return render(request, 'characterSheets/createSpellTechnique.html', context)


def create_spell(request, f, t):
    ss = SourceSet.objects.filter(personal=request.user).first()
    formsDetailed = {
        'creo': 'cr',
        'intellego': 'in',
        'muto': 'mu',
        'perdo': 'pe',
        'rego': 're',
    }
    techniquesDetailed = {
        'animal': 'an',
        'aquam': 'aq',
        'auram': 'au',
        'corpus': 'co',
        'herbam': 'he',
        'ignem': 'ig',
        'imaginem': 'im',
        'mentem': 'me',
        'terram': 'te',
        'vim': 'vi',
    }

    guideline = SpellGuideline.objects.filter(form=formsDetailed[f], technique=techniquesDetailed[t]).first()
    examples = SpellGuidelineExample.objects.filter(guideline=guideline)

    forms = []
    for x in guideline.forms:
        forms.append(x[1])
    techniques = []
    for technique in guideline.techniques:
        techniques.append(technique[1])

    spells = Spell.objects.filter(form=guideline.form, technique=guideline.technique, source__in=request.user.subscribers.all())
    spells = sorted(spells, key=lambda a: a.level())

    form = spellLibForm(request.POST or None, source=ss, guideline=guideline)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # return redirect('create_spell', f=guideline.get_form_display(), t=guideline.get_technique_display())

    context = {
        'forms': forms,
        'techniques': techniques,
        'guideline': guideline,
        'spells': spells,
        'examples': examples,
        'spellForm': form,
    }

    return render(request, 'characterSheets/createSpell.html', context)
