from django import forms

# class editCharacter(forms.Form):
#     name = forms.CharField(help_text="Enter the character's name")
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelformset_factory, BaseModelFormSet
from django.forms import formset_factory
from guardian.shortcuts import assign_perm

from characterSheets.models import Character, Saga, AbilityInstance, VirtueInstance, FlawInstance, Personality, \
    Reputation, SourceSet, VF, Ability, Armor, Weapon, MiscEquip


class changeSaga(ModelForm):
    class Meta:
        model = Saga
        fields = '__all__'

    members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)
    storyGuide = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)


class changeCharacter(ModelForm):
    class Meta:
        model = Character
        fields = '__all__'


class createCharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'type', 'age', 'size', 'confidence', 'decrepitude', 'effectsAging',
                  'warping', 'effectsWarping', 'birthName', 'yearBorn', 'gender', 'nationality',
                  'origin', 'religion', 'title', 'height', 'weight', 'hair', 'eyes', 'handedness',
                  'int', 'per', 'str', 'sta', 'pre', 'com', 'dex', 'qik')

        scores = (
            (-3, -3),
            (-2, -2),
            (-1, -1),
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'size': forms.NumberInput(attrs={'class': 'form-control'}),
            'confidence': forms.NumberInput(attrs={'class': 'form-control'}),
            'decrepitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'warping': forms.NumberInput(attrs={'class': 'form-control'}),
            'birthName': forms.TextInput(attrs={'class': 'form-control'}),
            'yearBorn': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'origin': forms.TextInput(attrs={'class': 'form-control'}),
            'religion': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'height': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
            'hair': forms.TextInput(attrs={'class': 'form-control'}),
            'eyes': forms.TextInput(attrs={'class': 'form-control'}),
            'handedness': forms.Select(attrs={'class': 'form-control'}),
            'int': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'per': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'str': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'sta': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'pre': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'com': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'dex': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'qik': forms.Select(choices=scores, attrs={'class': 'form-control'}),
        }


class characterBasicForm(ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'type', 'age', 'int', 'per', 'str', 'sta', 'pre', 'com', 'dex', 'qik')

        scores = (
            (-3, -3),
            (-2, -2),
            (-1, -1),
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'int': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'per': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'str': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'sta': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'pre': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'com': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'dex': forms.Select(choices=scores, attrs={'class': 'form-control'}),
            'qik': forms.Select(choices=scores, attrs={'class': 'form-control'}),
        }


class characterDetailForm(ModelForm):
    class Meta:
        model = Character

        fields = ('size', 'confidence', 'decrepitude', 'effectsAging',
                  'warping', 'effectsWarping', 'birthName', 'yearBorn', 'gender', 'nationality',
                  'origin', 'religion', 'title', 'height', 'weight', 'hair', 'eyes', 'handedness',)

        widgets = {
            'size': forms.NumberInput(attrs={'class': 'form-control'}),
            'confidence': forms.NumberInput(attrs={'class': 'form-control'}),
            'decrepitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'warping': forms.NumberInput(attrs={'class': 'form-control'}),
            'birthName': forms.TextInput(attrs={'class': 'form-control'}),
            'yearBorn': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'origin': forms.TextInput(attrs={'class': 'form-control'}),
            'religion': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'height': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
            'hair': forms.TextInput(attrs={'class': 'form-control'}),
            'eyes': forms.TextInput(attrs={'class': 'form-control'}),
            'handedness': forms.Select(attrs={'class': 'form-control'}),
        }


class createCharacter_detailsForm(ModelForm):
    class Meta:
        model = Character
        fields = ('effectsAging', 'effectsWarping')
        widgets = {
            'effectsAging': forms.Textarea(attrs={'class': 'form-control'}),
            'effectsWarping': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(createCharacter_detailsForm, self).__init__(*args, **kwargs)

        if self.instance.warping < 1:
            self.fields.pop('effectsWarping')

        if self.instance.decrepitude < 1:
            self.fields.pop('effectsAging')


class abilitiesForm(ModelForm):
    class Meta:
        model = AbilityInstance
        fields = ('referenceAbility', 'specialty', 'xp', 'score')

        widgets = {
            'referenceAbility': forms.Select(attrs={'class': 'form-control'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control'}),
            'xp': forms.NumberInput(attrs={'class': 'form-control save'}),
            'score': forms.NumberInput(attrs={'class': 'form-control save'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.character = kwargs.pop('character', None)
        super(abilitiesForm, self).__init__(*args, **kwargs)
        self.instance.owner = self.character
        self.fields['referenceAbility'].queryset = Ability.objects.filter(source__in=self.user.subscribers.all())


AbilityFormset = formset_factory(abilitiesForm, extra=1, can_delete=True)


class personalityForm(ModelForm):
    class Meta:
        model = Personality
        fields = ('name', 'score')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop('character', None)
        super(personalityForm, self).__init__(*args, **kwargs)
        self.instance.owner = self.character


class reputationForm(ModelForm):
    class Meta:
        model = Reputation
        fields = ('content', 'score', 'type')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.character = kwargs.pop('character', None)
        super(reputationForm, self).__init__(*args, **kwargs)
        self.instance.owner = self.character


class addCharacterToSaga(ModelForm):
    class Meta:
        model = Character
        fields = ('saga',)

        widgets = {
            'saga': forms.Select(attrs={'class': 'form-control'}),
        }


class removeCharacterSaga(ModelForm):
    confirm = forms.BooleanField()

    class Meta:
        model = Character
        fields = ('saga', 'confirm')

        widgets = {
            'saga': forms.HiddenInput(attrs={'class': 'form-control'}),
            'confirm': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }

    def clean_saga(self):
        data = None
        return data


class confirmationForm(forms.Form):
    confirm = forms.BooleanField()


class createCharacter_virtueForm(ModelForm):
    class Meta:
        model = VirtueInstance
        fields = ('referenceVirtue', 'specificationDetails')

        widgets = {
            'referenceVirtue': forms.Select(attrs={'class': 'form-control'}),
            'specificationDetails': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.character = kwargs.pop('character', None)
        super(createCharacter_virtueForm, self).__init__(*args, **kwargs)
        self.instance.owner = self.character
        self.fields['referenceVirtue'].queryset = VF.objects.filter(source__in=self.user.subscribers.all(),
                                                                    virtueOrFlaw='virtue')


VirtueFormset = formset_factory(createCharacter_virtueForm, extra=1, can_delete=True)


class createCharacter_flawForm(ModelForm):
    class Meta:
        model = FlawInstance
        fields = ('referenceFlaw', 'specificationDetails')

        widgets = {
            'referenceFlaw': forms.Select(attrs={'class': 'form-control'}),
            'specificationDetails': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.character = kwargs.pop('character', None)
        super(createCharacter_flawForm, self).__init__(*args, **kwargs)
        self.instance.owner = self.character
        self.fields['referenceFlaw'].queryset = VF.objects.filter(source__in=self.user.subscribers.all(),
                                                                  virtueOrFlaw='flaw')


FlawFormset = formset_factory(createCharacter_flawForm, extra=1, can_delete=True)


class addSourceSet(ModelForm):
    class Meta:
        model = SourceSet
        fields = ('name',)


class vfLibForm(ModelForm):
    class Meta:
        model = VF
        fields = ('name', 'description', 'value', 'type')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'value': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.VorF = kwargs.pop('vf', None)
        self.source = kwargs.pop('source', None)
        super(vfLibForm, self).__init__(*args, **kwargs)
        self.instance.virtueOrFlaw = self.VorF
        self.instance.source = self.source


class abiLibForm(ModelForm):
    class Meta:
        model = Ability
        fields = ('name', 'description', 'type', 'needTraining')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'needTraining': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

    specialties = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.source = kwargs.pop('source', None)
        super(abiLibForm, self).__init__(*args, **kwargs)
        self.instance.source = self.source
        initSpecs = ''
        for spec in self.instance.defaultspeciality_set.all():
            initSpecs += spec.name + ','
        initSpecs = initSpecs[:-1]
        self.fields['specialties'].initial = initSpecs

    def clean_specialties(self):
        specs = self.cleaned_data['specialties']
        data = specs.split(',')
        abi = self.instance
        return data, abi


class weaponLibForm(ModelForm):
    class Meta:
        model = Weapon
        fields = ('name', 'description', 'ability', 'init', 'atk', 'dfn', 'dam', 'strength', 'range', 'cost', 'load')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'ability': forms.Select(attrs={'class': 'form-control'}),
            'init': forms.NumberInput(attrs={'class': 'form-control'}),
            'atk': forms.NumberInput(attrs={'class': 'form-control'}),
            'dfn': forms.NumberInput(attrs={'class': 'form-control'}),
            'dam': forms.NumberInput(attrs={'class': 'form-control'}),
            'strength': forms.NumberInput(attrs={'class': 'form-control'}),
            'range': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost': forms.Select(attrs={'class': 'form-control'}),
            'load': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.source = kwargs.pop('source', None)
        super(weaponLibForm, self).__init__(*args, **kwargs)
        self.instance.source = self.source


class armorLibForm(ModelForm):
    class Meta:
        model = Armor
        fields = ('name', 'description', 'cost', 'load', 'prot', 'partialProt', 'partialLoad')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'cost': forms.Select(attrs={'class': 'form-control'}),
            'load': forms.NumberInput(attrs={'class': 'form-control'}),
            'prot': forms.NumberInput(attrs={'class': 'form-control'}),
            'partialProt': forms.NumberInput(attrs={'class': 'form-control'}),
            'partialLoad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.source = kwargs.pop('source', None)
        super(armorLibForm, self).__init__(*args, **kwargs)
        self.instance.source = self.source


class miscEquipLibForm(ModelForm):
    class Meta:
        model = MiscEquip
        fields = ('name', 'description', 'cost', 'load')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'cost': forms.Select(attrs={'class': 'form-control'}),
            'load': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.source = kwargs.pop('source', None)
        super(miscEquipLibForm, self).__init__(*args, **kwargs)
        self.instance.source = self.source


class importVirtuesForm(forms.Form):
    iData = forms.JSONField(label='Import Data', max_length=100000)

    def clean_iData(self):
        data = self.cleaned_data['iData']
        output = []
        try:
            for key in data.keys():
                newVirtue = VF()
                newVirtue.name = data[key]['name']
                newVirtue.description = data[key]['description']
                newVirtue.value = data[key]['value'].lower()
                newVirtue.type = data[key]['type'].lower()
                if data[key]['type'].lower() == 'social status':
                    newVirtue.type = 'socialStatus'
                newVirtue.virtueOrFlaw = 'virtue'
                output.append(newVirtue)
            return output
        except:
            raise ValidationError('JSON data is improperly formatted.')


class importFlawsForm(forms.Form):
    iData = forms.JSONField(label='Import Data', max_length=100000)

    def clean_iData(self):
        data = self.cleaned_data['iData']
        output = []
        try:
            for key in data.keys():
                newFlaw = VF()
                newFlaw.name = data[key]['name']
                newFlaw.description = data[key]['description']
                newFlaw.value = data[key]['value'].lower()
                newFlaw.type = data[key]['type'].lower()
                if data[key]['type'].lower() == 'social status':
                    newFlaw.type = 'socialStatus'
                newFlaw.virtueOrFlaw = 'flaw'
                output.append(newFlaw)
            return output
        except:
            raise ValidationError('JSON data is improperly formatted.')


class importAbilitiesForm(forms.Form):
    iData = forms.JSONField(label='Import Data', max_length=100000)

    def clean_iData(self):
        data = self.cleaned_data['iData']
        output = []
        try:
            for key in data.keys():
                newAbility = Ability()
                newAbility.name = data[key]['name']
                newAbility.description = data[key]['description']
                if data[key]['type'][0] == '(':
                    newAbility.type = data[key]['type'][1:-1].lower()
                else:
                    newAbility.type = data[key]['type'].lower()
                newAbility.needTraining = data[key]['needTraining']
                specialties = data[key]['specialties']
                output.append([newAbility, specialties])

            return output
        except:
            raise ValidationError('JSON data is improperly formatted.')
