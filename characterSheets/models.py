import sys
from itertools import chain

from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User


class SourceSet(models.Model):
    name = models.CharField(max_length=200, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscribers')
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view-sourceset', args=[self.id])

    def get_equipment_url(self):
        return reverse('sourceset-equipment', args=[self.id])

    class Meta:
        permissions = {
            ('source_can_edit', 'Can Edit'),
            ('source_owner', 'Owner'),
            ('source_can_view', 'Can View'),
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


class House(models.Model):
    """Model representing a hermetic house"""

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    domusMagna = models.CharField(max_length=200)
    primus = models.CharField(max_length=200)


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

    def encumbrance(self):
        """returns the character's encumbrance"""
        burden = 0
        for wep in self.weaponinstance_set.all():
            if wep.referenceWeapon.load and wep.status != 's':
                burden += wep.referenceWeapon.load
        for armor in self.armorinstance_set.all():
            if armor.referenceArmor.load and armor.status != 's':
                if armor.partial:
                    burden += armor.referenceArmor.partialLoad
                else:
                    burden += armor.referenceArmor.load
        for misc in self.miscequipinstance_set.all():
            if misc.referenceEquip.load and misc.status != 's':
                burden += misc.referenceEquip.load

        if self.str > 0:
            burden -= self.str
            if burden < 0:
                burden = 0

        return burden

    def equippedWeapons(self):
        """returns the character's equipped weapons"""
        weap = WeaponInstance.objects.filter(ownerChar=self, status='e', referenceWeapon__shield=False).first()
        shield = WeaponInstance.objects.filter(ownerChar=self, status='e', referenceWeapon__shield=True).first()
        if shield is not None:
            output = {
                'weapon': weap,
                'load': weap.referenceWeapon.load + shield.referenceWeapon.load,
                'shield': shield,
                'init': self.qik + weap.referenceWeapon.init - self.encumbrance(),
                'attack': self.dex + weap.get_ability_score() + weap.referenceWeapon.atk,
                'defence': self.qik + shield.get_ability_score() + weap.referenceWeapon.dfn + shield.referenceWeapon.dfn,
                'rangedDefence': self.qik + shield.get_ability_score() + shield.referenceWeapon.dfn,
                'damage': self.str + weap.referenceWeapon.dam,
            }
        else:
            output = {
                'weapon': weap,
                'load': weap.referenceWeapon.load,
                'init': self.qik + weap.referenceWeapon.init - self.encumbrance(),
                'attack': self.dex + weap.get_ability_score() + weap.referenceWeapon.atk,
                'defence': self.qik + weap.get_ability_score() + weap.referenceWeapon.dfn,
                'rangedDefence': self.qik + weap.get_ability_score(),
                'damage': self.str + weap.referenceWeapon.dam,
            }
        return output

    def equippedArmor(self):
        """returns the character's equipped armor"""
        return ArmorInstance.objects.filter(ownerChar=self, status='e').first()

    def soak(self):
        """returns the character's soak value"""
        armor = self.equippedArmor()
        if armor is not None:
            if armor.partial:
                return self.sta + armor.referenceArmor.partialProt
            else:
                return self.sta + armor.referenceArmor.prot
        else:
            return self.sta

    # Magic related stats

    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, blank=True)
    sigil = models.CharField('Wizard\'s Sigil', max_length=500, null=True, blank=True)
    parens = models.CharField(max_length=500, null=True, blank=True)
    covApprentice = models.CharField('Covenant of Apprenticeship', max_length=200, null=True, blank=True)


class Art(models.Model):
    """model representing a character's art"""
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    names = (
        ('cr', 'creo'),
        ('in', 'intellego'),
        ('mu', 'muto'),
        ('pe', 'perdo'),
        ('re', 'rego'),
        ('an', 'animal'),
        ('aq', 'aquam'),
        ('au', 'auram'),
        ('co', 'corpus'),
        ('he', 'herbam'),
        ('ig', 'ignem'),
        ('im', 'imaginem'),
        ('me', 'mentem'),
        ('te', 'terram'),
        ('vi', 'vim')
    )

    name = models.CharField(choices=names, max_length=2)
    score = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)

    class Meta:
        unique_together = ['name','character']

    def technique(self):
        """Returns true if the art is a technique, and false if it's a form"""
        techs = ('cr', 'in', 'mu', 'pe', 're')
        if self.name in techs:
            return True
        else:
            return False

    def __str__(self):
        return self.character.name + ' ' + self.get_name_display()


class spellCharacteristic(models.Model):
    """model representing a spell characteristic"""
    source = models.ForeignKey(SourceSet, on_delete=models.CASCADE)

    types = (
        ('r', 'range'),
        ('d', 'duration'),
        ('t', 'target'),
    )
    type = models.CharField(choices=types, max_length=1)

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Spell(models.Model):
    """model representing a spell lib entry"""
    source = models.ForeignKey(SourceSet, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=2000)
    forms = (
        ('cr', 'creo'),
        ('in', 'intellego'),
        ('mu', 'muto'),
        ('pe', 'perdo'),
        ('re', 'rego'),
    )
    form = models.CharField(choices=forms, max_length=2)
    techniques = (
        ('an', 'animal'),
        ('aq', 'aquam'),
        ('au', 'auram'),
        ('co', 'corpus'),
        ('he', 'herbam'),
        ('ig', 'ignem'),
        ('im', 'imaginem'),
        ('me', 'mentem'),
        ('te', 'terram'),
        ('vi', 'vim'),
    )
    technique = models.CharField(choices=techniques, max_length=2)
    spellRange = models.ForeignKey(spellCharacteristic, limit_choices_to={'type': 'r'}, on_delete=models.CASCADE,
                                   related_name='range')
    spellDuration = models.ForeignKey(spellCharacteristic, limit_choices_to={'type': 'd'}, on_delete=models.CASCADE,
                                      related_name='duration')
    spellTarget = models.ForeignKey(spellCharacteristic, limit_choices_to={'type': 't'}, on_delete=models.CASCADE,
                                    related_name='target')
    base = models.IntegerField(default=0)
    other = models.IntegerField(null=True, blank=True)
    ritual = models.BooleanField(default=False)

    def level(self):
        """Returns the spell level"""
        if self.other:
            if self.base + self.other + self.spellRange.level + self.spellDuration.level + self.spellTarget.level > 5:
                if self.base >= 5:
                    return self.base + (
                                self.spellRange.level + self.spellDuration.level + self.spellTarget.level + self.other) * 5
                else:
                    return (self.spellRange.level + self.spellDuration.level + self.spellTarget.level + self.other - (5 - self.base)) * 5 + 5
            else:
                return self.base + self.other + self.spellRange.level + self.spellDuration.level + self.spellTarget.level

        else:
            if self.base + self.spellRange.level + self.spellDuration.level + self.spellTarget.level > 5:
                if self.base >= 5:
                    return self.base + (
                            self.spellRange.level + self.spellDuration.level + self.spellTarget.level) * 5
                else:
                    return (self.spellRange.level + self.spellDuration.level + self.spellTarget.level - (5 - self.base)) * 5 + 5
            else:
                return self.base + self.spellRange.level + self.spellDuration.level + self.spellTarget.level

    def levelReason(self):
        """Returns a breakdown on the spell level calculation"""
        output = 'base: ' + str(self.base) + ' R: ' + self.spellRange.name + "(" + str(self.spellRange.level) + ")" \
                 + ' D: ' + self.spellDuration.name + "(" + str(self.spellDuration.level) + ")" \
                 + ' T: ' + self.spellTarget.name + "(" + str(self.spellTarget.level) + ")"
        if self.other:
            output += ' other: ' + str(self.other)
        return output

    def __str__(self):
        return self.name


class SpellInstance(models.Model):
    """model representing an instance of a spell"""
    referenceSpell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)
    mastery = models.IntegerField(default=0)
    notes = models.CharField(max_length=1000, null=True, blank=True)


class SpellGuideline(models.Model):
    """model representing a spell guideline"""
    description = models.CharField(max_length=10000, null=True, blank=True)
    forms = (
        ('cr', 'creo'),
        ('in', 'intellego'),
        ('mu', 'muto'),
        ('pe', 'perdo'),
        ('re', 'rego'),
    )
    form = models.CharField(choices=forms, max_length=2)
    techniques = (
        ('an', 'animal'),
        ('aq', 'aquam'),
        ('au', 'auram'),
        ('co', 'corpus'),
        ('he', 'herbam'),
        ('ig', 'ignem'),
        ('im', 'imaginem'),
        ('me', 'mentem'),
        ('te', 'terram'),
        ('vi', 'vim'),
    )
    technique = models.CharField(choices=techniques, max_length=2)
    general = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.get_form_display().capitalize() + ' ' + self.get_technique_display().capitalize() + ' Guidelines'

    class Meta:
        unique_together = ('form', 'technique')


class SpellGuidelineExample(models.Model):
    """model representing examples of a spell guideline"""
    source = models.ForeignKey(SourceSet, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    description = models.CharField(max_length=500)
    guideline = models.ForeignKey(SpellGuideline, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Covenant(models.Model):
    """model representing a covenant"""
    name = models.CharField(max_length=200)


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


class Weapon(models.Model):
    """Model representing weapon equipment"""

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=10000, null=True, blank=True)
    source = models.ForeignKey(SourceSet, on_delete=models.CASCADE)
    costTypes = (
        ('n', 'n/a'),
        ('i', 'inexpensive'),
        ('s', 'standard'),
        ('e', 'expensive'),
    )
    cost = models.CharField(choices=costTypes, default='n', null=True, blank=True, max_length=1)
    load = models.IntegerField(default=0, null=True, blank=True)

    ability = models.ForeignKey(Ability, on_delete=models.CASCADE, null=True, blank=True)
    init = models.IntegerField('Initiative', default=0)
    atk = models.IntegerField('Attack', default=0)
    dfn = models.IntegerField('Defence', default=0)
    dam = models.IntegerField('Damage', default=0)
    strength = models.IntegerField(null=True, blank=True)
    range = models.IntegerField(null=True, blank=True)
    shield = models.BooleanField(default=False)
    twoHanded = models.BooleanField('Two-handed', default=False)
    freeHand = models.BooleanField('Can hold other objects in same hand', default=False)

    def __str__(self):
        return self.name

    def get_delete_url(self):
        return reverse('delete-weapon', args=[self.id])


class WeaponInstance(models.Model):
    """Model representing a specific weapon"""

    referenceWeapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    ownerChar = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True)
    ownerCovenant = models.ForeignKey(Covenant, on_delete=models.SET_NULL, null=True, blank=True)
    statusChoices = (
        ('e', 'equipped'),
        ('c', 'carried'),
        ('s', 'stored'),
    )
    status = models.CharField(choices=statusChoices, max_length=1, default='c')
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.referenceWeapon.name

    def get_ability_score(self):
        if self.ownerChar:
            try:
                return AbilityInstance.objects.filter(owner=self.ownerChar,
                                                      referenceAbility=self.referenceWeapon.ability).first().score
            except AttributeError:
                return 0
        else:
            return 0

    def get_ability(self):
        return self.referenceWeapon.ability.name


class Armor(models.Model):
    """Model representing armor equipment"""

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=10000, null=True, blank=True)
    source = models.ForeignKey(SourceSet, on_delete=models.CASCADE)
    costTypes = (
        ('n', 'n/a'),
        ('i', 'inexpensive'),
        ('s', 'standard'),
        ('e', 'expensive'),
    )
    cost = models.CharField(choices=costTypes, default='n', null=True, blank=True, max_length=1)
    load = models.IntegerField(default=0, null=True, blank=True)

    prot = models.IntegerField('Protection', null=True, blank=True)
    partialProt = models.IntegerField('Partial Protection', null=True, blank=True)
    partialLoad = models.IntegerField('Partial Load', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_delete_url(self):
        return reverse('delete-armor', args=[self.id])


class ArmorInstance(models.Model):
    """Model representing a specific set of armor"""

    referenceArmor = models.ForeignKey(Armor, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    ownerChar = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True)
    ownerCovenant = models.ForeignKey(Covenant, on_delete=models.SET_NULL, null=True, blank=True)
    statusChoices = (
        ('e', 'equipped'),
        ('c', 'carried'),
        ('s', 'stored'),
    )
    status = models.CharField(choices=statusChoices, max_length=1, default='c')
    description = models.CharField(max_length=200, null=True, blank=True)
    partial = models.BooleanField(default=False)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.referenceArmor.name


class MiscEquip(models.Model):
    """Model representing equipment that doesn't fit into other types"""

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=10000, null=True, blank=True)
    source = models.ForeignKey(SourceSet, on_delete=models.CASCADE)
    costTypes = (
        ('n', 'n/a'),
        ('i', 'inexpensive'),
        ('s', 'standard'),
        ('e', 'expensive'),
    )
    cost = models.CharField(choices=costTypes, default='n', null=True, blank=True, max_length=1)
    load = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_delete_url(self):
        return reverse('delete-misc', args=[self.id])


class MiscEquipInstance(models.Model):
    """Model representing instance of misc equip"""

    referenceEquip = models.ForeignKey(MiscEquip, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    ownerChar = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True)
    ownerCovenant = models.ForeignKey(Covenant, on_delete=models.SET_NULL, null=True, blank=True)
    statusChoices = (
        ('e', 'equipped'),
        ('c', 'carried'),
        ('s', 'stored'),
    )
    status = models.CharField(choices=statusChoices, max_length=1, default='c')
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.referenceEquip.name
