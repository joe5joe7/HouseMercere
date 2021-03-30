from .models import Saga, Character

def profile_data(request):
    """Context processor for profile data, should be adde to every view call"""
    if request.user.is_authenticated:
        sagaMemberList = Saga.objects.filter(members=request.user)
        sagaStoryGuideList = Saga.objects.filter(storyGuide=request.user)
        sagaMemberList = list(set(sagaMemberList)-set(sagaStoryGuideList))
        mSagaCharacterList = {}
        for mSaga in sagaMemberList:
            mSagaCharacterList[mSaga] = Character.objects.filter(saga=mSaga, player=request.user)
        sSagaCharacterList = {}
        for sSaga in sagaStoryGuideList:
            sSagaCharacterList[sSaga] = Character.objects.filter(saga=sSaga, player=request.user)
        sagalessCharacterList= Character.objects.filter(saga=None, player=request.user)


        data = {
            'sagaMemberList': sagaMemberList,
            'sagaStoryGuideList': sagaStoryGuideList,
            'mSagaCharacterList': mSagaCharacterList,
            'sSagaCharacterList': sSagaCharacterList,
            'sagalessCharacterList': sagalessCharacterList
        }

    else:
        data = {
            'sagaMemberList': None,
            'sagaStoryGuideList': None,
            'mSagaCharacterList': None,
            'sSagaCharacterList': None,
            'sagalessCharacterList': None,
        }

    return data
