from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AllCampaignsListView,
    StateOfTheFlockSubmissionViewSet,
    SoulWinningSubmissionViewSet,
    ServantsArmedTrainedSubmissionViewSet,
    AntibrutishSubmissionViewSet,
    HearingSeeingSubmissionViewSet,
    HonourYourProphetSubmissionViewSet,
    BasontaProliferationSubmissionViewSet,
    IntimateCounselingSubmissionViewSet,
    TechnologySubmissionViewSet,
    SheperdingControlSubmissionViewSet,
    MultiplicationSubmissionViewSet,
    UnderstandingSubmissionViewSet,
    SheepSeekingSubmissionViewSet,
    TestimonySubmissionViewSet,
    TelepastoringSubmissionViewSet,
    GatheringBusSubmissionViewSet,
    OrganisedCreativeArtsSubmissionViewSet,
    TangerineSubmissionViewSet,
    SwollenSundaySubmissionViewSet,
    SundayManagementSubmissionViewSet,
)

router = DefaultRouter()

# Register all submission viewsets
router.register(r'state-of-flock/submissions', StateOfTheFlockSubmissionViewSet, basename='state-of-flock-submission')
router.register(r'soul-winning/submissions', SoulWinningSubmissionViewSet, basename='soul-winning-submission')
router.register(r'servants-armed-trained/submissions', ServantsArmedTrainedSubmissionViewSet, basename='servants-armed-trained-submission')
router.register(r'antibrutish/submissions', AntibrutishSubmissionViewSet, basename='antibrutish-submission')
router.register(r'hearing-seeing/submissions', HearingSeeingSubmissionViewSet, basename='hearing-seeing-submission')
router.register(r'honour-your-prophet/submissions', HonourYourProphetSubmissionViewSet, basename='honour-your-prophet-submission')
router.register(r'basonta-proliferation/submissions', BasontaProliferationSubmissionViewSet, basename='basonta-proliferation-submission')
router.register(r'intimate-counseling/submissions', IntimateCounselingSubmissionViewSet, basename='intimate-counseling-submission')
router.register(r'technology/submissions', TechnologySubmissionViewSet, basename='technology-submission')
router.register(r'sheperding-control/submissions', SheperdingControlSubmissionViewSet, basename='sheperding-control-submission')
router.register(r'multiplication/submissions', MultiplicationSubmissionViewSet, basename='multiplication-submission')
router.register(r'understanding/submissions', UnderstandingSubmissionViewSet, basename='understanding-submission')
router.register(r'sheep-seeking/submissions', SheepSeekingSubmissionViewSet, basename='sheep-seeking-submission')
router.register(r'testimony/submissions', TestimonySubmissionViewSet, basename='testimony-submission')
router.register(r'telepastoring/submissions', TelepastoringSubmissionViewSet, basename='telepastoring-submission')
router.register(r'gathering-bus/submissions', GatheringBusSubmissionViewSet, basename='gathering-bus-submission')
router.register(r'organised-creative-arts/submissions', OrganisedCreativeArtsSubmissionViewSet, basename='organised-creative-arts-submission')
router.register(r'tangerine/submissions', TangerineSubmissionViewSet, basename='tangerine-submission')
router.register(r'swollen-sunday/submissions', SwollenSundaySubmissionViewSet, basename='swollen-sunday-submission')
router.register(r'sunday-management/submissions', SundayManagementSubmissionViewSet, basename='sunday-management-submission')

urlpatterns = [
    path('all/', AllCampaignsListView.as_view(), name='all-campaigns-list'),
    path('', include(router.urls)),
]
