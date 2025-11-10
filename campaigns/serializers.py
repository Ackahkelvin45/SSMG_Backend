from rest_framework import serializers
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
    EquipmentCampaign, EquipmentSubmission, EquipmentSubmissionFile,
)


# ============= Base Campaign Serializers =============

class BaseCampaignSerializer(serializers.ModelSerializer):
    """Base serializer for all campaign types"""
    class Meta:
        fields = ['id', 'name', 'description', 'icon', 'campaign_id', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'name', 'description', 'icon', 'campaign_id', 'status', 'created_at', 'updated_at']


# ============= Individual Campaign Serializers =============

class StateOfTheFlockCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = StateOfTheFlockCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "State of the Flock"


class SoulWinningCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = SoulWinningCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Soul Winning"


class ServantsArmedTrainedCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = ServantsArmedTrainedCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Servants Armed and Trained"


class AntibrutishCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = AntibrutishCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Antibrutish"


class HearingSeeingCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = HearingSeeingCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Hearing and Seeing"


class HonourYourProphetCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = HonourYourProphetCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Honour Your Prophet"


class BasontaProliferationCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = BasontaProliferationCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Basonta Proliferation"


class IntimateCounselingCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = IntimateCounselingCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Intimate Counseling"


class TechnologyCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = TechnologyCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Technology"


class SheperdingControlCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = SheperdingControlCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Sheperding Control"


class MultiplicationCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = MultiplicationCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Multiplication"


class UnderstandingCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = UnderstandingCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Understanding"


class SheepSeekingCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = SheepSeekingCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Sheep Seeking"


class TestimonyCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = TestimonyCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Testimony"


class TelepastoringCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = TelepastoringCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Telepastoring"


class GatheringBusCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = GatheringBusCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Gathering Bus"


class OrganisedCreativeArtsCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = OrganisedCreativeArtsCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Organised Creative Arts"


class TangerineCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = TangerineCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Tangerine"


class SwollenSundayCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = SwollenSundayCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Swollen Sunday"


class SundayManagementCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = SundayManagementCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Sunday Management"


class EquipmentCampaignSerializer(BaseCampaignSerializer):
    campaign_type = serializers.SerializerMethodField()
    
    class Meta(BaseCampaignSerializer.Meta):
        model = EquipmentCampaign
        fields = BaseCampaignSerializer.Meta.fields + ['campaign_type']
    
    def get_campaign_type(self, obj):
        return "Equipment"


# ============= Submission File Serializers =============

class SubmissionFileSerializer(serializers.ModelSerializer):
    """Base serializer for submission files"""
    class Meta:
        fields = ['id', 'file', 'uploaded_at']
        read_only_fields = ['id', 'file', 'uploaded_at']


class SoulWinningSubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = SoulWinningSubmissionFile


class ServantsArmedTrainedSubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = ServantsArmedTrainedSubmissionFile


class AntibrutishSubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = AntibrutishSubmissionFile


class HonourYourProphetSubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = HonourYourProphetSubmissionFile


class BasontaProliferationSubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = BasontaProliferationSubmissionFile


class TechnologySubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = TechnologySubmissionFile


class MultiplicationSubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = MultiplicationSubmissionFile


class UnderstandingSubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = UnderstandingSubmissionFile


class SheepSeekingSubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = SheepSeekingSubmissionFile


class TelepastoringSubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = TelepastoringSubmissionFile


class GatheringBusSubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = GatheringBusSubmissionFile


class SwollenSundaySubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = SwollenSundaySubmissionFile


class SundayManagementSubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = SundayManagementSubmissionFile


class EquipmentSubmissionFileSerializer(SubmissionFileSerializer):
    class Meta(SubmissionFileSerializer.Meta):
        model = EquipmentSubmissionFile


# ============= Submission Serializers =============

class StateOfTheFlockSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = StateOfTheFlockSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'total_membership', 'lost', 'stable', 'unstable',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'created_at', 'updated_at'
        ]


class SoulWinningSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = SoulWinningSubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = SoulWinningSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'no_of_crusades', 'no_of_massive_organised_outreaches',
            'no_of_dance_outreach', 'no_of_souls_won', 'no_of_missionaries_in_training',
            'no_of_missionaries_sent', 'pictures', 'picture_files', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = SoulWinningSubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            SoulWinningSubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


class ServantsArmedTrainedSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = ServantsArmedTrainedSubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = ServantsArmedTrainedSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'no_of_teachings_done_by_pastor',
            'average_attendance_during_meetings_by_pastor', 'no_of_leaders_who_have_makarios',
            'no_of_leaders_who_own_dakes_bible', 'no_of_leaders_who_own_thompson_chain',
            'no_of_pose_certified_leaders', 'no_of_leaders_in_iptp_training',
            'pictures', 'picture_files', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = ServantsArmedTrainedSubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            ServantsArmedTrainedSubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


class AntibrutishSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = AntibrutishSubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = AntibrutishSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'type_of_prayer', 'hours_prayed',
            'number_of_people_who_prayed', 'pictures', 'picture_files',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = AntibrutishSubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            AntibrutishSubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


class HearingSeeingSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = HearingSeeingSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'avg_number_of_leaders_that_join_flow',
            'no_of_people_subscribed_bishop_dag_youtube', 'no_of_people_subscribed_es_joys_podcast',
            'no_of_messages_listened_to', 'titles_of_messages_listened_to',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'created_at', 'updated_at'
        ]


class HonourYourProphetSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = HonourYourProphetSubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = HonourYourProphetSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'no_of_people_who_honoured_with_offering',
            'activities_done_to_honour_prophet', 'pictures', 'picture_files',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = HonourYourProphetSubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            HonourYourProphetSubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


class BasontaProliferationSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = BasontaProliferationSubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = BasontaProliferationSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'no_of_bacentas_at_beginning_of_month', 'current_number_of_bacentas',
            'no_of_new_bacentas', 'no_of_leaders_who_are_leavers',
            'no_of_replacements_new_leaders_available', 'average_no_of_people_at_bacenta_meeting',
            'no_of_basontas', 'average_number_of_people_at_basonta_meetings',
            'avg_no_of_members_saturday_service', 'avg_no_of_members_sunday_service',
            'pictures', 'picture_files', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = BasontaProliferationSubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            BasontaProliferationSubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


class IntimateCounselingSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = IntimateCounselingSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'total_number_of_members', 'total_number_of_members_counseled',
            'no_of_members_counseled_via_calls', 'no_of_members_counseled_in_person',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'created_at', 'updated_at'
        ]


class TechnologySubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = TechnologySubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = TechnologySubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'list_of_equipments_in_church', 'pictures', 'picture_files',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = TechnologySubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            TechnologySubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


class SheperdingControlSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = SheperdingControlSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'current_no_of_leaders', 'no_of_cos', 'no_of_bos',
            'no_of_bls', 'no_of_fls', 'no_of_potential_leaders', 'no_of_leaders_who_have_been_sacked',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'created_at', 'updated_at'
        ]


class MultiplicationSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = MultiplicationSubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = MultiplicationSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'no_of_outreaches', 'type_of_outreaches',
            'no_of_members_who_came_from_outreaches_to_church', 'no_of_invites_done',
            'avg_number_of_people_invited_per_week', 'pictures', 'picture_files',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = MultiplicationSubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            MultiplicationSubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


class UnderstandingSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = UnderstandingSubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = UnderstandingSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'lay_school_material_being_taught',
            'no_of_lay_school_teachers', 'average_attendance_at_lay_school_meeting',
            'pictures', 'picture_files', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = UnderstandingSubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            UnderstandingSubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


class SheepSeekingSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = SheepSeekingSubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = SheepSeekingSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'no_of_people_visited', 'types_of_visits_done',
            'no_of_idl_visits_done', 'no_of_first_time_retained', 'no_of_convert_visits_done',
            'no_of_converts_retained', 'pictures', 'picture_files', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = SheepSeekingSubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            SheepSeekingSubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


class TestimonySubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = TestimonySubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'number_of_testimonies_shared', 'type_of_testimony_shared',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'created_at', 'updated_at'
        ]


class TelepastoringSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = TelepastoringSubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = TelepastoringSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'no_of_telepastors', 'total_no_of_calls_made',
            'categories_of_people_called', 'pictures', 'picture_files',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = TelepastoringSubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            TelepastoringSubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


class GatheringBusSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = GatheringBusSubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = GatheringBusSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'avg_number_of_members_bused',
            'avg_number_of_members_who_walk_in', 'avg_number_of_buses_for_service',
            'avg_attendance_for_the_service', 'avg_number_of_first_timers',
            'pictures', 'picture_files', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = GatheringBusSubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            GatheringBusSubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


class OrganisedCreativeArtsSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = OrganisedCreativeArtsSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'was_there_any_organisation_of_creative_arts',
            'which_basonta_was_responsible', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'created_at', 'updated_at'
        ]


class TangerineSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = TangerineSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'no_of_tangerines', 'types_of_tangerines',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'created_at', 'updated_at'
        ]


class SwollenSundaySubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = SwollenSundaySubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = SwollenSundaySubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'attendance_for_swollen_sunday', 'no_of_converts_for_swollen_sunday',
            'pictures', 'picture_files', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = SwollenSundaySubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            SwollenSundaySubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


class SundayManagementSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = SundayManagementSubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = SundayManagementSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'month', 'no_of_meetings_per_month',
            'pictures', 'picture_files', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = SundayManagementSubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            SundayManagementSubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


class EquipmentSubmissionSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pictures = EquipmentSubmissionFileSerializer(many=True, read_only=True)
    picture_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = EquipmentSubmission
        fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'submission_period', 'date', 'equipment_name', 'equipment_type', 'quantity',
            'condition', 'location', 'purchase_date', 'purchase_cost', 'current_value',
            'supplier_name', 'warranty_expiry_date', 'maintenance_notes', 'is_functional',
            'pictures', 'picture_files', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'campaign', 'submitted_by', 'submitted_by_name', 'service', 'service_name',
            'pictures', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        picture_files = validated_data.pop('picture_files', [])
        submission = EquipmentSubmission.objects.create(**validated_data)
        
        for picture in picture_files:
            EquipmentSubmissionFile.objects.create(submission=submission, file=picture)
        
        return submission


# ============= Dashboard Serializers =============

class DashboardSubmissionSerializer(serializers.Serializer):
    """Lightweight serializer for recent submissions in dashboard"""
    id = serializers.IntegerField()
    campaign_id = serializers.IntegerField(source='campaign.id')
    campaign_name = serializers.CharField(source='campaign.name')
    campaign_type = serializers.CharField()
    submission_period = serializers.DateField(allow_null=True)
    created_at = serializers.DateTimeField()
    submission_count = serializers.IntegerField()
    preview_data = serializers.SerializerMethodField()
    
    def get_preview_data(self, obj):
        """Get a preview of key submission data based on type"""
        submission = obj.get('submission')
        campaign_type = obj.get('campaign_type')
        
        # Return relevant preview fields based on campaign type
        preview = {}
        
        if campaign_type == "Soul Winning":
            preview['no_of_souls_won'] = getattr(submission, 'no_of_souls_won', None)
            preview['no_of_crusades'] = getattr(submission, 'no_of_crusades', None)
        elif campaign_type == "State of the Flock":
            preview['total_membership'] = getattr(submission, 'total_membership', None)
            preview['stable'] = getattr(submission, 'stable', None)
        elif campaign_type == "Antibrutish":
            preview['type_of_prayer'] = getattr(submission, 'type_of_prayer', None)
            preview['hours_prayed'] = str(getattr(submission, 'hours_prayed', None))
        elif campaign_type == "Multiplication":
            preview['no_of_outreaches'] = getattr(submission, 'no_of_outreaches', None)
        elif campaign_type == "Testimony":
            preview['number_of_testimonies_shared'] = getattr(submission, 'number_of_testimonies_shared', None)
        
        return preview
    
    def to_representation(self, instance):
        """Custom representation to flatten the submission object"""
        submission = instance.get('submission')
        campaign_type = instance.get('campaign_type')
        submission_count = instance.get('submission_count', 0)
        
        return {
            'id': submission.id,
            'campaign_id': submission.campaign.id,
            'campaign_name': submission.campaign.name,
            'campaign_type': campaign_type,
            'submission_period': submission.submission_period,
            'created_at': submission.created_at,
            'submission_count': submission_count,
            'preview_data': self.get_preview_data(instance)
        }


class DashboardCampaignSerializer(serializers.Serializer):
    """Lightweight serializer for recent campaigns in dashboard"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    campaign_type = serializers.CharField()
    status = serializers.CharField()
    icon = serializers.ImageField(allow_null=True)
    last_accessed = serializers.DateTimeField()
    submission_count = serializers.IntegerField()
    
    def to_representation(self, instance):
        """Custom representation to handle campaign object"""
        campaign = instance.get('campaign')
        submission_count = instance.get('submission_count', 0)
        
        return {
            'id': campaign.id,
            'name': campaign.name,
            'campaign_type': instance.get('campaign_type'),
            'status': campaign.status,
            'icon': campaign.icon.url if campaign.icon else None,
            'last_accessed': instance.get('last_accessed'),
            'submission_count': submission_count
        }

