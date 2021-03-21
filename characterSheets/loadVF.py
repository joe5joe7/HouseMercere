import os, django

import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'houseMercere.settings')
django.setup()

from characterSheets import models

def loadVF():
    with open('virtueLib','r') as file:
        data = json.load(file)

    for virt in list(data.keys()):

        newVirtue = models.VF()
        newVirtue.name = data[virt]['name']
        newVirtue.description = data[virt]['description']
        newVirtue.value = data[virt]['value'].lower()
        typeChoices = {
            'General': 'general',
            'Hermetic': 'hermetic',
            'Supernatural': 'supernatural',
            'Social Status': 'socialStatus',
            'Special': 'special',
            'Personality':'personality',
            'Story':'story',
        }
        newVirtue.type = typeChoices[data[virt]['type']]
        newVirtue.virtueOrFlaw = 'virtue'
        print(newVirtue)
        newVirtue.save()

    with open('flawLib','r') as file:
        data = json.load(file)

    for virt in list(data.keys()):

        newVirtue = models.VF()
        newVirtue.name = data[virt]['name']
        newVirtue.description = data[virt]['description']
        newVirtue.value = data[virt]['value'].lower()
        typeChoices = {
            'General': 'general',
            'Hermetic': 'hermetic',
            'Supernatural': 'supernatural',
            'Social Status': 'socialStatus',
            'Special': 'special',
            'Personality':'personality',
            'Story':'story',
        }
        newVirtue.type = typeChoices[data[virt]['type']]
        newVirtue.virtueOrFlaw = 'flaw'
        print(newVirtue)
        newVirtue.save()

    with open('abilityLib','r') as file:
        data = json.load(file)

    for abi in list(data.keys()):

        newAbi = models.Ability()
        newAbi.name = data[abi]['name']
        newAbi.description = data[abi]['description']
        newAbi.needTraining = data[abi]['needTraining']
        typeChoices = {
            '(General)': 'general',
            '(Academic)': 'academic',
            '(Arcane)': 'arcane',
            '(Martial)': 'martial',
            '(Supernatural)': 'supernatural',

        }
        newAbi.type=typeChoices[data[abi]['type']]
        newAbi.save()

        for x in data[abi]['specialties']:
            newSpec = models.Speciality()
            newSpec.name = x
            newSpec.abi = newAbi
            newSpec.save()


loadVF()
