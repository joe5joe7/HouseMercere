from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from characterSheets.models import Saga, Character
from main.forms import NewUserForm


def index(request):
    """View function for home page"""

    sagaList = Saga.objects.all()
    context = {
        'sagas': sagaList,
    }
    return render(request, 'index.html', context=context)

# @login_required
# def profile(request):
#     sagaMemberList = Saga.objects.filter(members=request.user)
#     sagaStoryGuideList = Saga.objects.filter(storyGuide=request.user)
#     sgCharacterBySaga = []
#     mSagaCharacterList={}
#     for mSaga in sagaMemberList:
#         mSagaCharacterList[mSaga] = Character.objects.filter(saga=mSaga,player=request.user)
#     sSagaCharacterList = {}
#     for sSaga in sagaStoryGuideList:
#         sSagaCharacterList[sSaga] = Character.objects.filter(saga=sSaga , player=request.user)
#
#     context = {
#         'sagaMemberList': sagaMemberList,
#         'sagaStoryGuideList': sagaStoryGuideList,
#         'mSagaCharacterList': mSagaCharacterList,
#         'sSagaCharacterList': sSagaCharacterList,
#     }
#     return render(request, 'profile.html', context=context)

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('index')
        messages.error(request, "Unsuccessful registration, please correct errors.")
    form = NewUserForm
    return render(request, 'register.html', context={'form':form})
