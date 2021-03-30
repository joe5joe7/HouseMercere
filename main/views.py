from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from guardian.shortcuts import get_objects_for_user

from characterSheets.models import Saga, Character, SourceSet
from main.forms import NewUserForm


def index(request):
    """View function for home page"""

    sagaList = Saga.objects.all()
    context = {
        'sagas': sagaList,
    }
    return render(request, 'index.html', context=context)


@login_required
def profile(request):
    ownedSets = get_objects_for_user(request.user,'characterSheets.source_can_edit')
    # for x in SourceSet.objects.all():
    #     if request.user.has_perm('can_edit',x):
    #         ownedSets.append(x)


    context = {
        'ownedSets': ownedSets,
    }

    return render(request, 'profile.html', context)


def register(request):
    form = NewUserForm(None)
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Registration successful.")
            return redirect('index')
        else:
            messages.error(request, "Unsuccessful registration, please correct errors.")

    return render(request, 'register.html', context={'form': form})
