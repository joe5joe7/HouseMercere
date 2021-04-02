# Generated by Django 3.1.7 on 2021-03-27 05:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=2000)),
                ('type', models.CharField(choices=[('general', 'general'), ('academic', 'academic'), ('arcane', 'arcane'), ('martial', 'martial'), ('supernatural', 'supernatural')], max_length=13)),
                ('needTraining', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name of the character', max_length=200)),
                ('type', models.CharField(choices=[('g', 'grog'), ('c', 'companion'), ('m', 'magus'), ('n', 'npc')], default='n', max_length=1, verbose_name='Character Type:')),
                ('age', models.IntegerField(blank=True, default=25, help_text="Enter the character's age", null=True)),
                ('size', models.IntegerField(default=0, help_text='Character size, most humans are size 0')),
                ('confidence', models.IntegerField(default=0, help_text="Character's confidence")),
                ('decrepitude', models.IntegerField(default=0, help_text="Character's decrepitude score")),
                ('effectsAging', models.TextField(blank=True, help_text="Effects of a character's aging", max_length=1000, null=True, verbose_name='Effects of Aging')),
                ('warping', models.IntegerField(default=0, help_text="Character's warping score")),
                ('effectsWarping', models.TextField(blank=True, help_text="Effects of a character's warping", max_length=1000, null=True, verbose_name='Effects of Warping')),
                ('birthName', models.CharField(blank=True, default='same', help_text="Enter the character's birth name", max_length=200, null=True, verbose_name='Birth Name')),
                ('yearBorn', models.IntegerField(blank=True, default=1195, help_text='Enter the year the character was born', null=True, verbose_name='Year Born')),
                ('gender', models.CharField(blank=True, choices=[('m', 'male'), ('f', 'female'), ('nb', 'non-binary'), ('o', 'other')], help_text="Character's gender", max_length=2, null=True)),
                ('nationality', models.CharField(blank=True, help_text="Character's nationality", max_length=200, null=True)),
                ('origin', models.CharField(blank=True, help_text="Character's place of origin", max_length=200, null=True, verbose_name='Place of Origin')),
                ('religion', models.CharField(blank=True, help_text="Character's religion", max_length=200, null=True)),
                ('title', models.CharField(blank=True, help_text="Character's title", max_length=200, null=True)),
                ('height', models.CharField(blank=True, help_text="Character's height", max_length=10, null=True)),
                ('weight', models.CharField(blank=True, help_text="Character's weight", max_length=10, null=True)),
                ('hair', models.CharField(blank=True, help_text="Character's hair color", max_length=200, null=True, verbose_name='Hair Color')),
                ('eyes', models.CharField(blank=True, help_text="Character's eye color", max_length=200, null=True, verbose_name='Eye Color')),
                ('handedness', models.CharField(blank=True, choices=[('l', 'left handed'), ('r', 'right handed'), ('a', 'ambidextrous')], default='r', help_text="Character's dominant hand", max_length=1, null=True)),
                ('int', models.IntegerField(default=0, verbose_name='intelligence')),
                ('per', models.IntegerField(default=0, verbose_name='perception')),
                ('str', models.IntegerField(default=0, verbose_name='strength')),
                ('sta', models.IntegerField(default=0, verbose_name='stamina')),
                ('pre', models.IntegerField(default=0, verbose_name='presence')),
                ('com', models.IntegerField(default=0, verbose_name='communication')),
                ('dex', models.IntegerField(default=0, verbose_name='dexterity')),
                ('qik', models.IntegerField(default=0, verbose_name='quickness')),
                ('fatigueScore', models.IntegerField(default=0, verbose_name='Fatigue Level')),
                ('lightWounds', models.IntegerField(default=0, verbose_name='Light Wounds')),
                ('mediumWounds', models.IntegerField(default=0, verbose_name='Medium Wounds')),
                ('heavyWounds', models.IntegerField(default=0, verbose_name='Heavy Wounds')),
                ('incapacitated', models.BooleanField(default=False)),
                ('dead', models.BooleanField(default=False)),
                ('player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Saga',
            fields=[
                ('name', models.CharField(help_text='The name of the saga', max_length=200, primary_key=True, serialize=False)),
                ('members', models.ManyToManyField(related_name='Member', to=settings.AUTH_USER_MODEL)),
                ('storyGuide', models.ManyToManyField(related_name='Storyguide', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SourceSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('sagas', models.ManyToManyField(blank=True, to='characterSheets.Saga')),
                ('subscribers', models.ManyToManyField(blank=True, related_name='subscribers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': {('can_edit', 'Can Edit')},
            },
        ),
        migrations.CreateModel(
            name='VF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Virtue or flaw name', max_length=200)),
                ('description', models.TextField(help_text='Virtue or flaw Description', max_length=2000)),
                ('virtueOrFlaw', models.CharField(choices=[('virtue', 'virtue'), ('flaw', 'flaw')], help_text='Enter either virtue of flaw', max_length=6)),
                ('value', models.CharField(choices=[('minor', 'minor'), ('major', 'major'), ('free', 'free'), ('special', 'special')], max_length=11)),
                ('type', models.CharField(choices=[('general', 'general'), ('hermetic', 'hermetic'), ('supernatural', 'supernatural'), ('socialStatus', 'social status'), ('personality', 'personality'), ('story', 'story'), ('special', 'special')], max_length=13)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characterSheets.sourceset')),
            ],
            options={
                'unique_together': {('name', 'source')},
            },
        ),
        migrations.CreateModel(
            name='VirtueInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specificationDetails', models.CharField(blank=True, max_length=1000, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characterSheets.character')),
                ('referenceVirtue', models.ForeignKey(limit_choices_to={'virtueOrFlaw': 'virtue'}, on_delete=django.db.models.deletion.CASCADE, to='characterSheets.vf')),
            ],
        ),
        migrations.CreateModel(
            name='Reputation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('score', models.IntegerField(default=0)),
                ('type', models.CharField(choices=[('l', 'Local'), ('e', 'ecclesiastical'), ('h', 'hermetic')], default='l', max_length=1)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characterSheets.character')),
            ],
        ),
        migrations.CreateModel(
            name='Personality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('score', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characterSheets.character')),
            ],
        ),
        migrations.CreateModel(
            name='FlawInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specificationDetails', models.CharField(blank=True, max_length=1000, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characterSheets.character')),
                ('referenceFlaw', models.ForeignKey(limit_choices_to={'virtueOrFlaw': 'flaw'}, on_delete=django.db.models.deletion.CASCADE, to='characterSheets.vf')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentLib',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('type', models.CharField(choices=[('w', 'weapon'), ('a', 'armor'), ('s', 'summa'), ('t', 'tractus'), ('o', 'other')], max_length=1)),
                ('init', models.IntegerField(blank=True, null=True, verbose_name='Initiative')),
                ('atk', models.IntegerField(blank=True, null=True, verbose_name='Attack')),
                ('dfn', models.IntegerField(blank=True, null=True, verbose_name='Defence')),
                ('dam', models.IntegerField(blank=True, null=True, verbose_name='Damage')),
                ('strength', models.IntegerField(blank=True, null=True)),
                ('range', models.IntegerField(blank=True, null=True)),
                ('prot', models.IntegerField(blank=True, null=True, verbose_name='Protection')),
                ('partialProt', models.IntegerField(blank=True, null=True, verbose_name='Partial Protection')),
                ('partialLoad', models.IntegerField(blank=True, null=True, verbose_name='Partial Load')),
                ('cost', models.CharField(blank=True, choices=[('n', 'n/a'), ('i', 'inexpensive'), ('s', 'standard'), ('e', 'expensive')], default='n', max_length=1, null=True)),
                ('worn', models.BooleanField(default=False)),
                ('load', models.IntegerField(blank=True, default=0, null=True)),
                ('ability', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='characterSheets.ability')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characterSheets.sourceset')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultSpeciality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('abi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='characterSheets.ability')),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='saga',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='characterSheets.saga'),
        ),
        migrations.CreateModel(
            name='AbilityInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialty', models.CharField(blank=True, max_length=200, null=True)),
                ('xp', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characterSheets.character')),
                ('referenceAbility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characterSheets.ability')),
            ],
        ),
        migrations.AddField(
            model_name='ability',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characterSheets.sourceset'),
        ),
        migrations.AlterUniqueTogether(
            name='ability',
            unique_together={('name', 'source')},
        ),
    ]
