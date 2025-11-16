from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from authentication.models import Service
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Base abstract model for common campaign fields
class BaseCampaign(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        Active = 'ACTIVE','Active'
        Inactive = 'INACTIVE', 'Inactive'
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    icon = models.ImageField(upload_to="icons", null=True, blank=True)
    campaign_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES.choices, default='Active')

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class BaseSubmission(models.Model):
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        
    )
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    submission_period = models.DateField(help_text="The first day of the month this submission is for.", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-submission_period', '-created_at']

    def __str__(self):
        if self.submission_period:
            return f"{self.submitted_by.username} ({self.submission_period.strftime('%B %Y')})"
        return f"{self.submitted_by.username}"


class SubmissionFile(models.Model):
   

    file = models.ImageField(upload_to='campaign_submissions/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.file.name}"

# Campaign 1: State of the Flock Campaign
class StateOfTheFlockCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_sof'

class StateOfTheFlockSubmission(BaseSubmission):
    campaign = models.ForeignKey(StateOfTheFlockCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    total_membership = models.IntegerField(null=True, blank=True)
    lost = models.IntegerField(null=True, blank=True)
    stable = models.IntegerField(null=True, blank=True)
    unstable = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'submission_sof'


def _recalculate_service_total_membership(service: Service):
    """
    Helper to recalculate and update Service.total_members based on
    the latest StateOfTheFlockSubmission for that service.
    """
    if not service:
        return

    latest_submission = (
        StateOfTheFlockSubmission.objects
        .filter(service=service)
        .order_by('-submission_period', '-created_at')
        .first()
    )

    if latest_submission and latest_submission.total_membership is not None:
        service.total_members = latest_submission.total_membership
    else:
        # If there is no submission or total_membership is null, clear the value
        service.total_members = None

    service.save(update_fields=['total_members'])


@receiver(post_save, sender=StateOfTheFlockSubmission)
def update_service_total_membership_on_save(sender, instance, **kwargs):
    """
    When a StateOfTheFlockSubmission is created or updated, update the
    related Service.total_members.

    Works for all roles (Pastors, Helpers, Campaign Managers), since the
    submission already has the correct service set.
    """
    if instance.service_id:
        _recalculate_service_total_membership(instance.service)


@receiver(post_delete, sender=StateOfTheFlockSubmission)
def update_service_total_membership_on_delete(sender, instance, **kwargs):
    """
    When a StateOfTheFlockSubmission is deleted, recalculate the
    Service.total_members based on remaining submissions.
    """
    if instance.service_id:
        _recalculate_service_total_membership(instance.service)


class SoulWinningCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_swc'

class SoulWinningSubmission(BaseSubmission):
    campaign = models.ForeignKey(SoulWinningCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    no_of_crusades = models.IntegerField(null=True, blank=True)
    no_of_massive_organised_outreaches = models.IntegerField(null=True, blank=True)
    no_of_dance_outreach = models.IntegerField(null=True, blank=True)
    no_of_souls_won = models.IntegerField(null=True, blank=True)
    no_of_missionaries_in_training = models.IntegerField(null=True, blank=True)
    no_of_missionaries_sent = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'submission_swc'
       

class SoulWinningSubmissionFile(SubmissionFile):
    submission = models.ForeignKey(SoulWinningSubmission, on_delete=models.CASCADE, related_name='pictures')

# Campaign 3: Servants Armed and Trained
class ServantsArmedTrainedCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_sat'

class ServantsArmedTrainedSubmission(BaseSubmission):
    campaign = models.ForeignKey(ServantsArmedTrainedCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    no_of_teachings_done_by_pastor = models.IntegerField(null=True, blank=True)
    average_attendance_during_meetings_by_pastor = models.IntegerField(null=True, blank=True)
    no_of_leaders_who_have_makarios = models.IntegerField(null=True, blank=True)
    no_of_leaders_who_own_dakes_bible = models.IntegerField(null=True, blank=True)
    no_of_leaders_who_own_thompson_chain = models.IntegerField(null=True, blank=True)
    no_of_pose_certified_leaders = models.IntegerField(null=True, blank=True)
    no_of_leaders_in_iptp_training = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'submission_sat'
      

class ServantsArmedTrainedSubmissionFile(SubmissionFile):
    submission = models.ForeignKey(ServantsArmedTrainedSubmission, on_delete=models.CASCADE, related_name='pictures')

# Campaign 4: Antibrutish Campaign
class AntibrutishCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_ant'

class AntibrutishSubmission(BaseSubmission):
    campaign = models.ForeignKey(AntibrutishCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    type_of_prayer = models.CharField(max_length=500)
    hours_prayed = models.DecimalField(max_digits=5, decimal_places=2)
    number_of_people_who_prayed = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'submission_ant'

class AntibrutishSubmissionFile(SubmissionFile):
    submission = models.ForeignKey(AntibrutishSubmission, on_delete=models.CASCADE, related_name='pictures')

# Campaign 5: Hearing and Seeing Campaign
class HearingSeeingCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_hs'

class HearingSeeingSubmission(BaseSubmission):
    campaign = models.ForeignKey(HearingSeeingCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    avg_number_of_leaders_that_join_flow = models.IntegerField(null=True, blank=True)
    no_of_people_subscribed_bishop_dag_youtube = models.IntegerField(null=True, blank=True)
    no_of_people_subscribed_es_joys_podcast = models.IntegerField(null=True, blank=True)
    no_of_messages_listened_to = models.IntegerField(null=True, blank=True)
    titles_of_messages_listened_to = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'submission_hs'

# Campaign 6: Honour Your Prophet Campaign
class HonourYourProphetCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_hyp'

class HonourYourProphetSubmission(BaseSubmission):
    campaign = models.ForeignKey(HonourYourProphetCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    no_of_people_who_honoured_with_offering = models.IntegerField(null=True, blank=True)
    activities_done_to_honour_prophet = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'submission_hyp'

class HonourYourProphetSubmissionFile(SubmissionFile):
    submission = models.ForeignKey(HonourYourProphetSubmission, on_delete=models.CASCADE, related_name='pictures')

# Campaign 7: Basonta Proliferation Campaign
class BasontaProliferationCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_bsp'

class BasontaProliferationSubmission(BaseSubmission):
    campaign = models.ForeignKey(BasontaProliferationCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    no_of_bacentas_at_beginning_of_month = models.IntegerField(null=True, blank=True)
    current_number_of_bacentas = models.IntegerField(null=True, blank=True)
    no_of_new_bacentas = models.IntegerField(null=True, blank=True)
    no_of_leaders_who_are_leavers = models.IntegerField(null=True, blank=True)
    no_of_replacements_new_leaders_available = models.IntegerField(null=True, blank=True)
    average_no_of_people_at_bacenta_meeting = models.IntegerField(null=True, blank=True)
    no_of_basontas = models.IntegerField(null=True, blank=True)
    average_number_of_people_at_basonta_meetings = models.IntegerField(null=True, blank=True)
    avg_no_of_members_saturday_service = models.IntegerField(null=True, blank=True)
    avg_no_of_members_sunday_service = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'submission_bsp'

class BasontaProliferationSubmissionFile(SubmissionFile):
    submission = models.ForeignKey(BasontaProliferationSubmission, on_delete=models.CASCADE, related_name='pictures')

# Campaign 8: Intimate Counseling Campaign
class IntimateCounselingCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_inc'

class IntimateCounselingSubmission(BaseSubmission):
    campaign = models.ForeignKey(IntimateCounselingCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    total_number_of_members = models.IntegerField(null=True, blank=True)
    total_number_of_members_counseled = models.IntegerField(null=True, blank=True)
    no_of_members_counseled_via_calls = models.IntegerField(null=True, blank=True)
    no_of_members_counseled_in_person = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'submission_inc'

# Campaign 9: Technology Campaign
class TechnologyCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_tech'

class TechnologySubmission(BaseSubmission):
    campaign = models.ForeignKey(TechnologyCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    list_of_equipments_in_church = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'submission_tech'

class TechnologySubmissionFile(SubmissionFile):
    submission = models.ForeignKey(TechnologySubmission, on_delete=models.CASCADE, related_name='pictures')

# Campaign 10: Sheperding Control Campaign
class SheperdingControlCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_shc'

class SheperdingControlSubmission(BaseSubmission):
    campaign = models.ForeignKey(SheperdingControlCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    current_no_of_leaders = models.IntegerField(null=True, blank=True)
    no_of_cos = models.IntegerField(null=True, blank=True)
    no_of_bos = models.IntegerField(null=True, blank=True)
    no_of_bls = models.IntegerField(null=True, blank=True)
    no_of_fls = models.IntegerField(null=True, blank=True)
    no_of_potential_leaders = models.IntegerField()
    no_of_leaders_who_have_been_sacked = models.IntegerField()

    class Meta:
        db_table = 'submission_shc'


# Campaign 11: Multiplication Campaign
class MultiplicationCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_mult'

class MultiplicationSubmission(BaseSubmission):
    campaign = models.ForeignKey(MultiplicationCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    no_of_outreaches = models.IntegerField(null=True, blank=True)
    type_of_outreaches = models.TextField(null=True, blank=True)
    no_of_members_who_came_from_outreaches_to_church = models.IntegerField(null=True, blank=True)
    no_of_invites_done = models.IntegerField(null=True, blank=True)
    avg_number_of_people_invited_per_week = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'submission_mult'

class MultiplicationSubmissionFile(SubmissionFile):
    submission = models.ForeignKey(MultiplicationSubmission, on_delete=models.CASCADE, related_name='pictures')

# Campaign 12: Understanding Campaign
class UnderstandingCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_uc'

class UnderstandingSubmission(BaseSubmission):
    campaign = models.ForeignKey(UnderstandingCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    lay_school_material_being_taught = models.CharField(max_length=200)
    no_of_lay_school_teachers = models.IntegerField(null=True, blank=True)
    average_attendance_at_lay_school_meeting = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'submission_uc'


class UnderstandingSubmissionFile(SubmissionFile):
    submission = models.ForeignKey(UnderstandingSubmission, on_delete=models.CASCADE, related_name='pictures')

# Campaign 13: Sheep Seeking Campaign
class SheepSeekingCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_shs'

class SheepSeekingSubmission(BaseSubmission):
    campaign = models.ForeignKey(SheepSeekingCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    no_of_people_visited = models.IntegerField(null=True, blank=True)
    types_of_visits_done = models.TextField(null=True, blank=True)
    no_of_idl_visits_done = models.IntegerField(null=True, blank=True)
    no_of_first_time_retained = models.IntegerField(null=True, blank=True)
    no_of_convert_visits_done = models.IntegerField(null=True, blank=True)
    no_of_converts_retained = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'submission_shs'

class SheepSeekingSubmissionFile(SubmissionFile):
    submission = models.ForeignKey(SheepSeekingSubmission, on_delete=models.CASCADE, related_name='pictures')

# Campaign 14: Testimony Campaign
class TestimonyCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_tes'

class TestimonySubmission(BaseSubmission):
    campaign = models.ForeignKey(TestimonyCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    number_of_testimonies_shared = models.IntegerField(null=True, blank=True)
    type_of_testimony_shared = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'submission_tes'

# Campaign 15: Telepastoring Campaign
class TelepastoringCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_tel'

class TelepastoringSubmission(BaseSubmission):
    campaign = models.ForeignKey(TelepastoringCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    no_of_telepastors = models.IntegerField(null=True, blank=True)
    total_no_of_calls_made = models.IntegerField(null=True, blank=True)
    categories_of_people_called = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'submission_tel'

class TelepastoringSubmissionFile(SubmissionFile):
    submission = models.ForeignKey(TelepastoringSubmission, on_delete=models.CASCADE, related_name='pictures')

# Campaign 16: Gathering Bus Campaign
class GatheringBusCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_gbc'

class GatheringBusSubmission(BaseSubmission):
    campaign = models.ForeignKey(GatheringBusCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    avg_number_of_members_bused = models.IntegerField(null=True, blank=True)
    avg_number_of_members_who_walk_in = models.IntegerField(null=True, blank=True)
    avg_number_of_buses_for_service = models.IntegerField(null=True, blank=True)
    avg_attendance_for_the_service = models.IntegerField(null=True, blank=True)
    avg_number_of_first_timers = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'submission_gbc'

class GatheringBusSubmissionFile(SubmissionFile):
    submission = models.ForeignKey(GatheringBusSubmission, on_delete=models.CASCADE, related_name='pictures')

# Campaign 17: Organised Creative Arts Campaign
class OrganisedCreativeArtsCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_oca'

class OrganisedCreativeArtsSubmission(BaseSubmission):
    campaign = models.ForeignKey(OrganisedCreativeArtsCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    was_there_any_organisation_of_creative_arts = models.BooleanField(null=True, blank=True)
    which_basonta_was_responsible = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'submission_oca'

# Campaign 18: Tangerine Campaign
class TangerineCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_tan'

class TangerineSubmission(BaseSubmission):
    campaign = models.ForeignKey(TangerineCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    no_of_tangerines = models.IntegerField(null=True, blank=True)
    types_of_tangerines = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'submission_tan'

# Campaign 19: Swollen Sunday Campaign
class SwollenSundayCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_ss'

class SwollenSundaySubmission(BaseSubmission):
    campaign = models.ForeignKey(SwollenSundayCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    attendance_for_swollen_sunday = models.IntegerField(null=True, blank=True)
    no_of_converts_for_swollen_sunday = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'submission_ss'

class SwollenSundaySubmissionFile(SubmissionFile):
    submission = models.ForeignKey(SwollenSundaySubmission, on_delete=models.CASCADE, related_name='pictures')

# Campaign 20: Sunday Management Campaign
class SundayManagementCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_sm'

class SundayManagementSubmission(BaseSubmission):
    campaign = models.ForeignKey(SundayManagementCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    month = models.DateField(help_text="Month this submission is for")
    no_of_meetings_per_month = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'submission_sm'
        

class SundayManagementSubmissionFile(SubmissionFile):
    submission = models.ForeignKey(SundayManagementSubmission, on_delete=models.CASCADE, related_name='pictures')


# Campaign 21: Equipment Campaign
class EquipmentCampaign(BaseCampaign):
    class Meta:
        db_table = 'campaign_equip'

class EquipmentSubmission(BaseSubmission):
    campaign = models.ForeignKey(EquipmentCampaign, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateField(null=True, blank=True)
    equipment_name = models.CharField(max_length=200, null=True, blank=True)
    equipment_type = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    condition = models.CharField(max_length=100, null=True, blank=True, help_text="e.g., New, Good, Fair, Poor")
    location = models.CharField(max_length=200, null=True, blank=True, help_text="Where the equipment is located")
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    supplier_name = models.CharField(max_length=200, null=True, blank=True)
    warranty_expiry_date = models.DateField(null=True, blank=True)
    maintenance_notes = models.TextField(null=True, blank=True)
    is_functional = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        db_table = 'submission_equip'

class EquipmentSubmissionFile(SubmissionFile):
    submission = models.ForeignKey(EquipmentSubmission, on_delete=models.CASCADE, related_name='pictures')


# Campaign Manager Assignment Model
class CampaignManagerAssignment(models.Model):
    """
    Links a Campaign Manager user to one or more campaigns.
    Campaign Managers can be assigned to multiple campaigns and can fill data for those campaigns across ALL services.
    Campaign Managers are NOT tied to a specific service.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='campaign_assignments',
        limit_choices_to={'role': 'CAMPAIGN_MANAGER'}
    )
    
    # Generic foreign key to link to any campaign type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    campaign = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'campaign_manager_assignments'
        unique_together = ['user', 'content_type', 'object_id']
        verbose_name = 'Campaign Manager Assignment'
        verbose_name_plural = 'Campaign Manager Assignments'
    
    def __str__(self):
        campaign_name = str(self.campaign) if self.campaign else 'Unknown Campaign'
        return f"{self.user.full_name} -> {campaign_name}"