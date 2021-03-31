import sys

from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User


class SourceSet(models.Model):
    name = models.CharField(max_length=200)
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscribers')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view-sourceset', args=[self.id])

    class Meta:
        permissions = {
            ('source_can_edit', 'Can Edit'),
        }



class Saga(models.Model):
    """Model representing a saga"""

    name = models.CharField(max_length=200, help_text='The name of the saga', primary_key=True)
    storyGuide = models.ManyToManyField(User, related_name='Storyguide')
    members = models.ManyToManyField(User, related_name='Member')
    sourceSets = models.ManyToManyField(SourceSet, blank=True)

    def __str__(self):
        """String representing the saga"""
        return self.name

    def get_absolute_url(self):
        """Returns a url to access a detailed record of this saga"""
        return reverse('saga-detail', args=[self.name])

    def name_id(self):
        """Returns the name with spaces replaced by _ for templates"""
        return self.name.replace(' ', '_')


class VF(models.Model):
    """Model representing a virtue or flaw"""
    name = models.CharField(max_length=200, help_text='Virtue or flaw name')
    description = models.TextField(max_length=10000, help_text='Virtue or flaw Description')
    source = models.ForeignKey(SourceSet, on_delete=models.CASCADE)

    vfChoices = (
        ('virtue', 'virtue'),
        ('flaw', 'flaw')
    )
    virtueOrFlaw = models.CharField(choices=vfChoices, max_length=6, help_text='Enter either virtue of flaw')

    valueChoices = (
        ('minor', 'minor'),
        ('major', 'major'),
        ('free', 'free'),
        ('special', 'special'),
    )
    value = models.CharField(choices=valueChoices, max_length=11)

    typeChoices = (
        ('general', 'general'),
        ('hermetic', 'hermetic'),
        ('supernatural', 'supernatural'),
        ('socialStatus', 'social status'),
        ('personality', 'personality'),
        ('story', 'story'),
        ('special', 'special'),
    )
    type = models.CharField(choices=typeChoices, max_length=13)

    class Meta:
        unique_together = (('name', 'source'),)

    def __str__(self):
        """String representing the vf"""
        return self.name

    def playersCharacter(self, player, request):
        """returns a list of characters owned by a player"""
        return Character.objects.filter(player=request.user)


class Ability(models.Model):
    """model represents an ability"""

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=10000)
    source = models.ForeignKey(SourceSet, on_delete=models.CASCADE)

    typeChoices = (
        ('general', 'general'),
        ('academic', 'academic'),
        ('arcane', 'arcane'),
        ('martial', 'martial'),
        ('supernatural', 'supernatural'),
    )
    type = models.CharField(choices=typeChoices, max_length=13)
    needTraining = models.BooleanField(default=False)

    class Meta:
        unique_together = (('name', 'source'),)

    def __str__(self):
        """String representing the ability"""
        return self.name


class DefaultSpeciality(models.Model):
    """Model representing a speciality"""

    name = models.CharField(max_length=200)
    abi = models.ForeignKey(Ability, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        """String representing default speciality"""
        return self.name


class Character(models.Model):
    """model represents a specific character"""

    name = models.CharField(max_length=200, help_text='Enter the name of the character')
    player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    typeChoices = (
        ('g', 'grog'),
        ('c', 'companion'),
        ('m', 'magus'),
        ('n', 'npc'),
    )
    type = models.CharField('Character Type:', choices=typeChoices, max_length=1, default='n')
    saga = models.ForeignKey(Saga, null=True, on_delete=models.SET_NULL, blank=True)
    age = models.IntegerField(help_text='Enter the character\'s age', null=True, blank=True, default=25)
    size = models.IntegerField(help_text='Character size, most humans are size 0', default=0)
    confidence = models.IntegerField(help_text='Character\'s confidence', default=0)
    decrepitude = models.IntegerField(default=0, help_text='Character\'s decrepitude score')
    effectsAging = models.TextField('Effects of Aging', max_length=1000, null=True, blank=True,
                                    help_text='Effects of a character\'s aging')
    warping = models.IntegerField(default=0, help_text='Character\'s warping score')
    effectsWarping = models.TextField('Effects of Warping', max_length=1000, null=True, blank=True,
                                      help_text='Effects of a character\'s warping')
    birthName = models.CharField('Birth Name', max_length=200, help_text='Enter the character\'s birth name', null=True,
                                 blank=True, default='same')
    yearBorn = models.IntegerField('Year Born', help_text='Enter the year the character was born', null=True,
                                   blank=True, default=1195)
    genderChoices = (
        ('m', 'male'),
        ('f', 'female'),
        ('nb', 'non-binary'),
        ('o', 'other'),
    )
    gender = models.CharField(max_length=2, choices=genderChoices, help_text='Character\'s gender', null=True,
                              blank=True)
    nationality = models.CharField(max_length=200, help_text='Character\'s nationality', null=True, blank=True)
    origin = models.CharField('Place of Origin', max_length=200, help_text='Character\'s place of origin', null=True,
                              blank=True)
    religion = models.CharField(max_length=200, help_text='Character\'s religion', null=True, blank=True)
    title = models.CharField(max_length=200, help_text='Character\'s title', null=True, blank=True)
    height = models.CharField(max_length=10, help_text='Character\'s height', null=True, blank=True)
    weight = models.CharField(max_length=10, help_text='Character\'s weight', null=True, blank=True)
    hair = models.CharField('Hair Color', max_length=200, help_text='Character\'s hair color', null=True, blank=True)
    eyes = models.CharField('Eye Color', max_length=200, help_text='Character\'s eye color', null=True, blank=True)
    handChoices = (
        ('l', 'left handed'),
        ('r', 'right handed'),
        ('a', 'ambidextrous'),
    )
    handedness = models.CharField(max_length=1, choices=handChoices, help_text='Character\'s dominant hand',
                                  null=True, blank=True, default='r')

    # characteristics

    int = models.IntegerField('intelligence', default=0)
    per = models.IntegerField('perception', default=0)
    str = models.IntegerField('strength', default=0)
    sta = models.IntegerField('stamina', default=0)
    pre = models.IntegerField('presence', default=0)
    com = models.IntegerField('communication', default=0)
    dex = models.IntegerField('dexterity', default=0)
    qik = models.IntegerField('quickness', default=0)

    fatigueScore = models.IntegerField('Fatigue Level', default=0)

    lightWounds = models.IntegerField('Light Wounds', default=0)
    mediumWounds = models.IntegerField('Medium Wounds', default=0)
    heavyWounds = models.IntegerField('Heavy Wounds', default=0)
    incapacitated = models.BooleanField(default=False)
    dead = models.BooleanField(default=False)

    # virtues = models.ManyToManyField(
    #     VF,
    #     limit_choices_to={'virtueOrFlaw': 'virtue'},
    #     related_name='virtues',
    #     blank=True,
    # )
    # flaws = models.ManyToManyField(
    #     VF,
    #     limit_choices_to={'virtueOrFlaw': 'flaw'},
    #     related_name='flaws',
    #     blank = True,
    # )

    def __str__(self):
        """String representing the character"""
        return self.name

    def get_absolute_url(self):
        """Returns a url to access a detailed record of this saga"""
        return reverse('character-detail', args=[self.id])

    def woundsRange(self):
        if self.size < -4:
            size = -4
        else:
            size = self.size

        woundRange = {
            'light': (1, 5 + size),
            'medium': (6 + size, 10 + size * 2),
            'heavy': (11 + size * 2, 15 + size * 3),
            'incapacitated': (16 + size * 3, 20 + size * 4),
            'dead': (21 * size * 4, 100000)
        }

        return woundRange

    def wounds(self):
        data = {
            'light': (self.lightWounds / 5) * 100,
            'medium': (self.mediumWounds / 5) * 100,
            'heavy': (self.heavyWounds / 5) * 100,
            'incapacitated': int(self.incapacitated) * 100,
            'dead': int(self.dead) * 100,
        }

        return data

    def fatigueStr(self):
        """String representation of current fatigue score"""
        if self.fatigueScore > 5:
            self.fatigueScore = 5

        fatigueDict = {
            0: 'Fresh',
            1: 'Winded',
            2: 'Weary(-1)',
            3: 'Tired (-3)',
            4: 'Dazed (-5)',
            5: 'Unconscious'
        }

        return fatigueDict[self.fatigueScore]

    def fatigueScorePercentage(self):
        """returns fatigue as a number between 0 and 100 representing how fatigued the character is"""
        return int((self.fatigueScore / 5) * 100) if self.fatigueScore else 0

    # def removeSaga(self, request):
    #     """Removes character form current saga"""
    #     self.saga = None
    #     return self.get_absolute_url()


class Personality(models.Model):
    """model representing a specific characters personality trait"""
    name = models.CharField(max_length=200)
    score = models.IntegerField(default=0)
    owner = models.ForeignKey(Character, on_delete=models.CASCADE)


class Reputation(models.Model):
    """model representing a specific characters reputation"""
    content = models.CharField(max_length=200)
    score = models.IntegerField(default=0)
    repTypes = (
        ('l', 'Local'),
        ('e', 'ecclesiastical'),
        ('h', 'hermetic'),
    )
    type = models.CharField(choices=repTypes, default='l', max_length=1)
    owner = models.ForeignKey(Character, on_delete=models.CASCADE)


class AbilityInstance(models.Model):
    """model representing a specific instance of an ability"""

    referenceAbility = models.ForeignKey(Ability, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=200, null=True, blank=True)
    xp = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    owner = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        """returns the name of the reference ability"""
        return self.referenceAbility.name


class VirtueInstance(models.Model):
    """Model representing a specific virtue"""
    referenceVirtue = models.ForeignKey(VF, on_delete=models.CASCADE, limit_choices_to={'virtueOrFlaw': 'virtue'})
    specificationDetails = models.CharField(max_length=1000, null=True, blank=True)
    owner = models.ForeignKey(Character, on_delete=models.CASCADE)


class FlawInstance(models.Model):
    """Model representing a specific virtue"""
    referenceFlaw = models.ForeignKey(VF, on_delete=models.CASCADE, limit_choices_to={'virtueOrFlaw': 'flaw'})
    specificationDetails = models.CharField(max_length=1000, null=True, blank=True)
    owner = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        return self.referenceFlaw.name


class Equipment(models.Model):
    """Model representing a piece of equipment"""
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=10000, null=True, blank=True)
    source = models.ForeignKey(SourceSet, on_delete=models.CASCADE)
    types = (
        ('w', 'weapon'),
        ('a', 'armor'),
        ('s', 'summa'),
        ('t', 'tractus'),
        ('o', 'other'),
    )
    type = models.CharField(choices=types, max_length=1)

    # Weapon stats
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE, null=True, blank=True)
    init = models.IntegerField('Initiative', null=True, blank=True)
    atk = models.IntegerField('Attack', null=True, blank=True)
    dfn = models.IntegerField('Defence', null=True, blank=True)
    dam = models.IntegerField('Damage', null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    range = models.IntegerField(null=True, blank=True)

    # Armor stats
    prot = models.IntegerField('Protection', null=True, blank=True)
    partialProt = models.IntegerField('Partial Protection', null=True, blank=True)
    partialLoad = models.IntegerField('Partial Load', null=True, blank=True)

    costTypes = (
        ('n', 'n/a'),
        ('i', 'inexpensive'),
        ('s', 'standard'),
        ('e', 'expensive'),
    )

    cost = models.CharField(choices=costTypes, default='n', null=True, blank=True, max_length=1)
    # Move worn to equip instance
    # worn = models.BooleanField(default=False)
    load = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name
