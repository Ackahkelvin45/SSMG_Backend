from django.contrib import admin
from .models import (
    StateOfTheFlockCampaign, StateOfTheFlockSubmission,
    SoulWinningCampaign, SoulWinningSubmission, SoulWinningSubmissionFile,
    ServantsArmedTrainedCampaign, ServantsArmedTrainedSubmission, ServantsArmedTrainedSubmissionFile,
    AntibrutishCampaign, AntibrutishSubmission, AntibrutishSubmissionFile,
    HearingSeeingCampaign, HearingSeeingSubmission,
    HonourYourProphetCampaign, HonourYourProphetSubmission, HonourYourProphetSubmissionFile,
    BasontaProliferationCampaign, BasontaProliferationSubmission, BasontaProliferationSubmissionFile,
    IntimateCounselingCampaign, IntimateCounselingSubmission,
    TechnologyCampaign, TechnologySubmission, TechnologySubmissionFile,
    SheperdingControlCampaign, SheperdingControlSubmission,
    MultiplicationCampaign, MultiplicationSubmission, MultiplicationSubmissionFile,
    UnderstandingCampaign, UnderstandingSubmission, UnderstandingSubmissionFile,
    SheepSeekingCampaign, SheepSeekingSubmission, SheepSeekingSubmissionFile,
    TestimonyCampaign, TestimonySubmission,
    TelepastoringCampaign, TelepastoringSubmission, TelepastoringSubmissionFile,
    GatheringBusCampaign, GatheringBusSubmission, GatheringBusSubmissionFile,
    OrganisedCreativeArtsCampaign, OrganisedCreativeArtsSubmission,
    TangerineCampaign, TangerineSubmission,
    SwollenSundayCampaign, SwollenSundaySubmission, SwollenSundaySubmissionFile,
    SundayManagementCampaign, SundayManagementSubmission, SundayManagementSubmissionFile,
)


class SoulWinningSubmissionFileInline(admin.TabularInline):
    model = SoulWinningSubmissionFile
    extra = 0


class ServantsArmedTrainedSubmissionFileInline(admin.TabularInline):
    model = ServantsArmedTrainedSubmissionFile
    extra = 0


class AntibrutishSubmissionFileInline(admin.TabularInline):
    model = AntibrutishSubmissionFile
    extra = 0


class HonourYourProphetSubmissionFileInline(admin.TabularInline):
    model = HonourYourProphetSubmissionFile
    extra = 0


class BasontaProliferationSubmissionFileInline(admin.TabularInline):
    model = BasontaProliferationSubmissionFile
    extra = 0


class TechnologySubmissionFileInline(admin.TabularInline):
    model = TechnologySubmissionFile
    extra = 0


class MultiplicationSubmissionFileInline(admin.TabularInline):
    model = MultiplicationSubmissionFile
    extra = 0


class UnderstandingSubmissionFileInline(admin.TabularInline):
    model = UnderstandingSubmissionFile
    extra = 0


class SheepSeekingSubmissionFileInline(admin.TabularInline):
    model = SheepSeekingSubmissionFile
    extra = 0


class TelepastoringSubmissionFileInline(admin.TabularInline):
    model = TelepastoringSubmissionFile
    extra = 0


class GatheringBusSubmissionFileInline(admin.TabularInline):
    model = GatheringBusSubmissionFile
    extra = 0


class SwollenSundaySubmissionFileInline(admin.TabularInline):
    model = SwollenSundaySubmissionFile
    extra = 0


class SundayManagementSubmissionFileInline(admin.TabularInline):
    model = SundayManagementSubmissionFile
    extra = 0


@admin.register(StateOfTheFlockSubmission)
class StateOfTheFlockSubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(SoulWinningSubmission)
class SoulWinningSubmissionAdmin(admin.ModelAdmin):
    inlines = [SoulWinningSubmissionFileInline]


@admin.register(ServantsArmedTrainedSubmission)
class ServantsArmedTrainedSubmissionAdmin(admin.ModelAdmin):
    inlines = [ServantsArmedTrainedSubmissionFileInline]


@admin.register(AntibrutishSubmission)
class AntibrutishSubmissionAdmin(admin.ModelAdmin):
    inlines = [AntibrutishSubmissionFileInline]


@admin.register(HearingSeeingSubmission)
class HearingSeeingSubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(HonourYourProphetSubmission)
class HonourYourProphetSubmissionAdmin(admin.ModelAdmin):
    inlines = [HonourYourProphetSubmissionFileInline]


@admin.register(BasontaProliferationSubmission)
class BasontaProliferationSubmissionAdmin(admin.ModelAdmin):
    inlines = [BasontaProliferationSubmissionFileInline]


@admin.register(IntimateCounselingSubmission)
class IntimateCounselingSubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(TechnologySubmission)
class TechnologySubmissionAdmin(admin.ModelAdmin):
    inlines = [TechnologySubmissionFileInline]


@admin.register(SheperdingControlSubmission)
class SheperdingControlSubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(MultiplicationSubmission)
class MultiplicationSubmissionAdmin(admin.ModelAdmin):
    inlines = [MultiplicationSubmissionFileInline]


@admin.register(UnderstandingSubmission)
class UnderstandingSubmissionAdmin(admin.ModelAdmin):
    inlines = [UnderstandingSubmissionFileInline]


@admin.register(SheepSeekingSubmission)
class SheepSeekingSubmissionAdmin(admin.ModelAdmin):
    inlines = [SheepSeekingSubmissionFileInline]


@admin.register(TestimonySubmission)
class TestimonySubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(TelepastoringSubmission)
class TelepastoringSubmissionAdmin(admin.ModelAdmin):
    inlines = [TelepastoringSubmissionFileInline]


@admin.register(GatheringBusSubmission)
class GatheringBusSubmissionAdmin(admin.ModelAdmin):
    inlines = [GatheringBusSubmissionFileInline]


@admin.register(OrganisedCreativeArtsSubmission)
class OrganisedCreativeArtsSubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(TangerineSubmission)
class TangerineSubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(SwollenSundaySubmission)
class SwollenSundaySubmissionAdmin(admin.ModelAdmin):
    inlines = [SwollenSundaySubmissionFileInline]


@admin.register(SundayManagementSubmission)
class SundayManagementSubmissionAdmin(admin.ModelAdmin):
    inlines = [SundayManagementSubmissionFileInline]


# Campaign models
admin.site.register(StateOfTheFlockCampaign)
admin.site.register(SoulWinningCampaign)
admin.site.register(ServantsArmedTrainedCampaign)
admin.site.register(AntibrutishCampaign)
admin.site.register(HearingSeeingCampaign)
admin.site.register(HonourYourProphetCampaign)
admin.site.register(BasontaProliferationCampaign)
admin.site.register(IntimateCounselingCampaign)
admin.site.register(TechnologyCampaign)
admin.site.register(SheperdingControlCampaign)
admin.site.register(MultiplicationCampaign)
admin.site.register(UnderstandingCampaign)
admin.site.register(SheepSeekingCampaign)
admin.site.register(TestimonyCampaign)
admin.site.register(TelepastoringCampaign)
admin.site.register(GatheringBusCampaign)
admin.site.register(OrganisedCreativeArtsCampaign)
admin.site.register(TangerineCampaign)
admin.site.register(SwollenSundayCampaign)
admin.site.register(SundayManagementCampaign)
