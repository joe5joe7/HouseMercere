from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Saga(models.Model):
    """Model representing a saga"""

    name = models.CharField(max_length=200, help_text='The name of the saga', primary_key=True)
    storyGuide = models.ManyToManyField(User, related_name='Storyguide')
    members = models.ManyToManyField(User, related_name='Member')

    def __str__(self):
        """String representing the saga"""
        return self.name

    def get_absolute_url(self):
        """Returns a url to access a detailed record of this saga"""
        return reverse('saga-detail', args=[self.name])

    def name_id(self):
        """Returns the name with spaces replaced by _ for templates"""
        return self.name.replace(' ','_')



class VF(models.Model):
    """Model representing a virtue"""
    name = models.CharField(max_length=200, help_text='Virtue or flaw name')
    description = models.TextField(max_length=2000, help_text='Virtue or flaw Description')
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

    def __str__(self):
        """String representing the vf"""
        return self.name

    def playersCharacter(self,player,request):
        """returns a list of characters owned by a player"""
        return Character.objects.filter(player=request.user)


class Ability(models.Model):
    """model represents an ability"""

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)

    typeChoices = (
        ('general', 'general'),
        ('academic', 'academic'),
        ('arcane', 'arcane'),
        ('martial', 'martial'),
        ('supernatural', 'supernatural'),
    )
    type = models.CharField(choices=typeChoices, max_length=13)
    needTraining = models.BooleanField(default=False)

    def __str__(self):
        """String representing the ability"""
        return self.name


class Speciality(models.Model):
    """Model representing a speciality"""

    name = models.CharField(max_length=200)
    abi = models.ForeignKey(Ability, null=True, blank=True, on_delete=models.SET_NULL)


class Character(models.Model):
    """model represents a specific character"""

    name = models.CharField(max_length=200, help_text='Enter the name of the character')
    player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    typeChoices = (
        ('g','grog'),
        ('c','companion'),
        ('m','magus'),
        ('n','npc'),
    )
    type = models.CharField('Character Type:',choices=typeChoices,max_length=1,default='n')
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
    birthName = models.CharField('Birth Name', max_length=200, help_text='Enter the character\'s birth name', null=True, blank=True)
    yearBorn = models.IntegerField('Year Born', help_text='Enter the year the character was born', null=True, blank=True)
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
                                  null=True, blank=True)

    # characteristics
    scores = (
        (-3, -3),
        (-2, -2),
        (-1, -1),
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
    )

    int = models.IntegerField('intelligence', choices=scores, default=0)
    per = models.IntegerField('perception', choices=scores, default=0)
    str = models.IntegerField('strength', choices=scores, default=0)
    sta = models.IntegerField('stamina', choices=scores, default=0)
    pre = models.IntegerField('presence', choices=scores, default=0)
    com = models.IntegerField('communication', choices=scores, default=0)
    dex = models.IntegerField('dexterity', choices=scores, default=0)
    qik = models.IntegerField('quickness', choices=scores, default=0)

    virtues = models.ManyToManyField(
        VF,
        limit_choices_to={'virtueOrFlaw': 'virtue'},
        related_name='virtues',
        blank=True,
    )
    flaws = models.ManyToManyField(
        VF,
        limit_choices_to={'virtueOrFlaw': 'flaw'},
        related_name='flaws',
        blank = True,
    )

    def __str__(self):
        """String representing the character"""
        return self.name

    def get_absolute_url(self):
        """Returns a url to access a detailed record of this saga"""
        return reverse('character-detail', args=[self.id])
