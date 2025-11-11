from rest_framework import viewsets, permissions, status, parsers, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.db.models import Q
from django.utils.dateparse import parse_date

from helpers.pagination import DefaultPagination
from .models import (
    StateOfTheFlockCampaign, StateOfTheFlockSubmission,
    SoulWinningCampaign, SoulWinningSubmission,
    ServantsArmedTrainedCampaign, ServantsArmedTrainedSubmission,
    AntibrutishCampaign, AntibrutishSubmission,
    HearingSeeingCampaign, HearingSeeingSubmission,
    HonourYourProphetCampaign, HonourYourProphetSubmission,
    BasontaProliferationCampaign, BasontaProliferationSubmission,
    IntimateCounselingCampaign, IntimateCounselingSubmission,
    TechnologyCampaign, TechnologySubmission,
    SheperdingControlCampaign, SheperdingControlSubmission,
    MultiplicationCampaign, MultiplicationSubmission,
    UnderstandingCampaign, UnderstandingSubmission,
    SheepSeekingCampaign, SheepSeekingSubmission,
    TestimonyCampaign, TestimonySubmission,
    TelepastoringCampaign, TelepastoringSubmission,
    GatheringBusCampaign, GatheringBusSubmission,
    OrganisedCreativeArtsCampaign, OrganisedCreativeArtsSubmission,
    TangerineCampaign, TangerineSubmission,
    SwollenSundayCampaign, SwollenSundaySubmission,
    SundayManagementCampaign, SundayManagementSubmission,
    EquipmentCampaign, EquipmentSubmission,
)
from .serializers import (
    StateOfTheFlockCampaignSerializer, StateOfTheFlockSubmissionSerializer,
    SoulWinningCampaignSerializer, SoulWinningSubmissionSerializer,
    ServantsArmedTrainedCampaignSerializer, ServantsArmedTrainedSubmissionSerializer,
    AntibrutishCampaignSerializer, AntibrutishSubmissionSerializer,
    HearingSeeingCampaignSerializer, HearingSeeingSubmissionSerializer,
    HonourYourProphetCampaignSerializer, HonourYourProphetSubmissionSerializer,
    BasontaProliferationCampaignSerializer, BasontaProliferationSubmissionSerializer,
    IntimateCounselingCampaignSerializer, IntimateCounselingSubmissionSerializer,
    TechnologyCampaignSerializer, TechnologySubmissionSerializer,
    SheperdingControlCampaignSerializer, SheperdingControlSubmissionSerializer,
    MultiplicationCampaignSerializer, MultiplicationSubmissionSerializer,
    UnderstandingCampaignSerializer, UnderstandingSubmissionSerializer,
    SheepSeekingCampaignSerializer, SheepSeekingSubmissionSerializer,
    TestimonyCampaignSerializer, TestimonySubmissionSerializer,
    TelepastoringCampaignSerializer, TelepastoringSubmissionSerializer,
    GatheringBusCampaignSerializer, GatheringBusSubmissionSerializer,
    OrganisedCreativeArtsCampaignSerializer, OrganisedCreativeArtsSubmissionSerializer,
    TangerineCampaignSerializer, TangerineSubmissionSerializer,
    SwollenSundayCampaignSerializer, SwollenSundaySubmissionSerializer,
    SundayManagementCampaignSerializer, SundayManagementSubmissionSerializer,
    EquipmentCampaignSerializer, EquipmentSubmissionSerializer,
)


class AllCampaignsListView(APIView):
    """
    View to retrieve all campaigns across all campaign types.
    
    For Campaign Managers: Only returns campaigns assigned to them.
    For other roles: Returns all campaigns.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        List campaigns based on user role:
        - Campaign Managers: Only assigned campaigns
        - Other roles: All campaigns
        """
        user = request.user
        campaigns = []
        
        # Define all campaign models and their serializers
        campaign_types = [
            (StateOfTheFlockCampaign, StateOfTheFlockCampaignSerializer),
            (SoulWinningCampaign, SoulWinningCampaignSerializer),
            (ServantsArmedTrainedCampaign, ServantsArmedTrainedCampaignSerializer),
            (AntibrutishCampaign, AntibrutishCampaignSerializer),
            (HearingSeeingCampaign, HearingSeeingCampaignSerializer),
            (HonourYourProphetCampaign, HonourYourProphetCampaignSerializer),
            (BasontaProliferationCampaign, BasontaProliferationCampaignSerializer),
            (IntimateCounselingCampaign, IntimateCounselingCampaignSerializer),
            (TechnologyCampaign, TechnologyCampaignSerializer),
            (SheperdingControlCampaign, SheperdingControlCampaignSerializer),
            (MultiplicationCampaign, MultiplicationCampaignSerializer),
            (UnderstandingCampaign, UnderstandingCampaignSerializer),
            (SheepSeekingCampaign, SheepSeekingCampaignSerializer),
            (TestimonyCampaign, TestimonyCampaignSerializer),
            (TelepastoringCampaign, TelepastoringCampaignSerializer),
            (GatheringBusCampaign, GatheringBusCampaignSerializer),
            (OrganisedCreativeArtsCampaign, OrganisedCreativeArtsCampaignSerializer),
            (TangerineCampaign, TangerineCampaignSerializer),
            (SwollenSundayCampaign, SwollenSundayCampaignSerializer),
            (SundayManagementCampaign, SundayManagementCampaignSerializer),
            (EquipmentCampaign, EquipmentCampaignSerializer),
        ]
        
        # Get active campaigns filter from query params
        status_filter = request.query_params.get('status', None)
        
        # If user is a Campaign Manager, get their assigned campaigns
        assigned_campaign_ids = {}
        if user.is_campaign_manager:
            from campaigns.models import CampaignManagerAssignment
            from django.contrib.contenttypes.models import ContentType
            
            assignments = CampaignManagerAssignment.objects.filter(
                user=user
            ).select_related('content_type')
            
            # Build a map of content_type_id -> list of campaign IDs
            for assignment in assignments:
                ct_id = assignment.content_type.id
                if ct_id not in assigned_campaign_ids:
                    assigned_campaign_ids[ct_id] = []
                assigned_campaign_ids[ct_id].append(assignment.object_id)
        
        for model, serializer_class in campaign_types:
            # Get content type for this campaign model
            from django.contrib.contenttypes.models import ContentType
            ct = ContentType.objects.get_for_model(model)
            
            # If Campaign Manager, filter to only assigned campaigns
            if user.is_campaign_manager:
                if ct.id in assigned_campaign_ids:
                    # Only get campaigns that are assigned to this manager
                    campaign_ids = assigned_campaign_ids[ct.id]
                    queryset = model.objects.filter(id__in=campaign_ids)
                else:
                    # This campaign type has no assignments, skip it
                    continue
            else:
                # For other roles, get all campaigns
                queryset = model.objects.all()
            
            # Apply status filter if provided
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            serializer = serializer_class(queryset, many=True, context={'request': request})
            campaigns.extend(serializer.data)
        
        # Sort by created_at descending
        campaigns.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return Response({
            'count': len(campaigns),
            'results': campaigns
        }, status=status.HTTP_200_OK)


# ============= Submission ViewSets =============

def filter_queryset_for_campaign_manager(queryset, user, campaign_model):
    """
    Helper function to filter queryset for Campaign Managers.
    Only returns submissions for campaigns assigned to the manager.
    """
    if user.is_campaign_manager:
        from campaigns.models import CampaignManagerAssignment
        from django.contrib.contenttypes.models import ContentType
        
        # Get content type for this campaign model
        ct = ContentType.objects.get_for_model(campaign_model)
        
        # Get assigned campaign IDs for this content type
        assignments = CampaignManagerAssignment.objects.filter(
            user=user,
            content_type=ct
        )
        
        assigned_campaign_ids = [assignment.object_id for assignment in assignments]
        
        # Filter to only assigned campaigns
        if assigned_campaign_ids:
            queryset = queryset.filter(campaign_id__in=assigned_campaign_ids)
        else:
            # No assigned campaigns of this type, return empty queryset
            queryset = queryset.none()
    
    return queryset


def validate_campaign_manager_assignment(user, campaign_model, campaign_id):
    """
    Helper function to validate that a Campaign Manager is assigned to a campaign.
    Raises ValidationError if not assigned.
    """
    print("\n" + "="*80)
    print("🔍 DEBUG: validate_campaign_manager_assignment")
    print("="*80)
    print(f"User ID: {user.id}")
    print(f"User Name: {user.full_name}")
    print(f"User Email: {user.email}")
    print(f"User Role: {user.role}")
    print(f"Is Campaign Manager: {user.is_campaign_manager}")
    print(f"Campaign Model: {campaign_model}")
    print(f"Campaign Model Name: {campaign_model.__name__}")
    print(f"Campaign ID (raw): {repr(campaign_id)}")
    print(f"Campaign ID Type: {type(campaign_id).__name__}")
    
    if user.is_campaign_manager:
        from campaigns.models import CampaignManagerAssignment
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(campaign_model)
        
        print(f"Content Type: {ct}")
        print(f"Content Type ID: {ct.id}")
        print(f"Content Type Model: {ct.model}")
        print(f"Content Type App Label: {ct.app_label}")
        
        # Convert campaign_id to integer (it comes as string from request)
        try:
            campaign_id_int = int(campaign_id)
            print(f"Campaign ID (converted to int): {campaign_id_int}")
        except (ValueError, TypeError) as e:
            print(f"❌ ERROR converting campaign_id: {e}")
            raise serializers.ValidationError({"campaign": "Invalid campaign id format."})
        
        # Check all assignments for this user
        all_assignments = CampaignManagerAssignment.objects.filter(user=user)
        print(f"\n📋 All assignments for user {user.id}:")
        for assignment in all_assignments:
            print(f"  - Content Type: {assignment.content_type.model} (ID: {assignment.content_type.id})")
            print(f"    Object ID: {assignment.object_id} (type: {type(assignment.object_id).__name__})")
            print(f"    Campaign: {assignment.campaign}")
        
        # Check the specific query
        query_result = CampaignManagerAssignment.objects.filter(
            user=user,
            content_type=ct,
            object_id=campaign_id_int
        )
        print(f"\n🔎 Query Details:")
        print(f"  - Filter: user={user.id}, content_type={ct.id}, object_id={campaign_id_int}")
        print(f"  - Query exists(): {query_result.exists()}")
        print(f"  - Query count(): {query_result.count()}")
        
        if query_result.exists():
            print(f"  ✅ ASSIGNMENT FOUND!")
            for assignment in query_result:
                print(f"     Assignment ID: {assignment.id}")
                print(f"     Created: {assignment.created_at}")
        else:
            print(f"  ❌ NO ASSIGNMENT FOUND!")
            print(f"\n🔍 Checking if it's a type mismatch...")
            # Try with string
            query_str = CampaignManagerAssignment.objects.filter(
                user=user,
                content_type=ct,
                object_id=str(campaign_id_int)
            )
            print(f"  - Query with STRING object_id: {query_str.exists()}")
            # Try with original value
            query_orig = CampaignManagerAssignment.objects.filter(
                user=user,
                content_type=ct,
                object_id=campaign_id
            )
            print(f"  - Query with ORIGINAL campaign_id: {query_orig.exists()}")
        
        print("="*80 + "\n")
        
        if not query_result.exists():
            raise serializers.ValidationError({"campaign": "You are not assigned to this campaign."})


def get_service_for_submission(user, request_data):
    """
    Helper function to determine which service to use for a submission.
    Campaign Managers must provide a service ID in request data.
    Other users use their assigned service.
    """
    if user.is_campaign_manager:
        service_id = request_data.get('service')
        if not service_id:
            raise serializers.ValidationError({"service": "Campaign Managers must specify a service."})
        try:
            from authentication.models import Service
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            raise serializers.ValidationError({"service": "Invalid service id."})
        return service
    else:
        return getattr(user, 'service', None)


class StateOfTheFlockSubmissionViewSet(viewsets.ModelViewSet):
    queryset = StateOfTheFlockSubmission.objects.all()
    serializer_class = StateOfTheFlockSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, StateOfTheFlockCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = StateOfTheFlockCampaign.objects.get(id=campaign_id)
        except StateOfTheFlockCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, StateOfTheFlockCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class SoulWinningSubmissionViewSet(viewsets.ModelViewSet):
    queryset = SoulWinningSubmission.objects.all()
    serializer_class = SoulWinningSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, SoulWinningCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = SoulWinningCampaign.objects.get(id=campaign_id)
        except SoulWinningCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, SoulWinningCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class ServantsArmedTrainedSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ServantsArmedTrainedSubmission.objects.all()
    serializer_class = ServantsArmedTrainedSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, ServantsArmedTrainedCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = ServantsArmedTrainedCampaign.objects.get(id=campaign_id)
        except ServantsArmedTrainedCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, ServantsArmedTrainedCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class AntibrutishSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AntibrutishSubmission.objects.all()
    serializer_class = AntibrutishSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, AntibrutishCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = AntibrutishCampaign.objects.get(id=campaign_id)
        except AntibrutishCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, AntibrutishCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class HearingSeeingSubmissionViewSet(viewsets.ModelViewSet):
    queryset = HearingSeeingSubmission.objects.all()
    serializer_class = HearingSeeingSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, HearingSeeingCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = HearingSeeingCampaign.objects.get(id=campaign_id)
        except HearingSeeingCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, HearingSeeingCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class HonourYourProphetSubmissionViewSet(viewsets.ModelViewSet):
    queryset = HonourYourProphetSubmission.objects.all()
    serializer_class = HonourYourProphetSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, HonourYourProphetCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = HonourYourProphetCampaign.objects.get(id=campaign_id)
        except HonourYourProphetCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, HonourYourProphetCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class BasontaProliferationSubmissionViewSet(viewsets.ModelViewSet):
    queryset = BasontaProliferationSubmission.objects.all()
    serializer_class = BasontaProliferationSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, BasontaProliferationCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = BasontaProliferationCampaign.objects.get(id=campaign_id)
        except BasontaProliferationCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, BasontaProliferationCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class IntimateCounselingSubmissionViewSet(viewsets.ModelViewSet):
    queryset = IntimateCounselingSubmission.objects.all()
    serializer_class = IntimateCounselingSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, IntimateCounselingCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = IntimateCounselingCampaign.objects.get(id=campaign_id)
        except IntimateCounselingCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, IntimateCounselingCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class TechnologySubmissionViewSet(viewsets.ModelViewSet):
    queryset = TechnologySubmission.objects.all()
    serializer_class = TechnologySubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, TechnologyCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = TechnologyCampaign.objects.get(id=campaign_id)
        except TechnologyCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, TechnologyCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class SheperdingControlSubmissionViewSet(viewsets.ModelViewSet):
    queryset = SheperdingControlSubmission.objects.all()
    serializer_class = SheperdingControlSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, SheperdingControlCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = SheperdingControlCampaign.objects.get(id=campaign_id)
        except SheperdingControlCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, SheperdingControlCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class MultiplicationSubmissionViewSet(viewsets.ModelViewSet):
    queryset = MultiplicationSubmission.objects.all()
    serializer_class = MultiplicationSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, MultiplicationCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = MultiplicationCampaign.objects.get(id=campaign_id)
        except MultiplicationCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, MultiplicationCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class UnderstandingSubmissionViewSet(viewsets.ModelViewSet):
    queryset = UnderstandingSubmission.objects.all()
    serializer_class = UnderstandingSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, UnderstandingCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = UnderstandingCampaign.objects.get(id=campaign_id)
        except UnderstandingCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, UnderstandingCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class SheepSeekingSubmissionViewSet(viewsets.ModelViewSet):
    queryset = SheepSeekingSubmission.objects.all()
    serializer_class = SheepSeekingSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, SheepSeekingCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = SheepSeekingCampaign.objects.get(id=campaign_id)
        except SheepSeekingCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, SheepSeekingCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class TestimonySubmissionViewSet(viewsets.ModelViewSet):
    queryset = TestimonySubmission.objects.all()
    serializer_class = TestimonySubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, TestimonyCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        print("\n" + "="*80)
        print("🔍 DEBUG: TestimonySubmissionViewSet.perform_create")
        print("="*80)
        print(f"Request Method: {self.request.method}")
        print(f"Request Content-Type: {self.request.content_type}")
        print(f"Request Data (raw): {self.request.data}")
        print(f"Request Query Params: {self.request.query_params}")
        
        user = self.request.user
        print(f"\n👤 User from request:")
        print(f"  - ID: {user.id}")
        print(f"  - Name: {user.full_name}")
        print(f"  - Email: {user.email}")
        print(f"  - Role: {user.role}")
        
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        print(f"\n📦 Campaign ID extraction:")
        print(f"  - From request.data.get('campaign'): {repr(self.request.data.get('campaign'))}")
        print(f"  - From query_params.get('campaign'): {repr(self.request.query_params.get('campaign'))}")
        print(f"  - Final campaign_id: {repr(campaign_id)}")
        print(f"  - campaign_id type: {type(campaign_id).__name__ if campaign_id else 'None'}")
        
        if not campaign_id:
            print("  ❌ ERROR: campaign_id is None or empty!")
            raise serializers.ValidationError({"campaign": "This field is required."})
        
        try:
            campaign = TestimonyCampaign.objects.get(id=campaign_id)
            print(f"  ✅ Campaign found: {campaign.name} (ID: {campaign.id})")
        except TestimonyCampaign.DoesNotExist:
            print(f"  ❌ ERROR: TestimonyCampaign with id={campaign_id} does not exist!")
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        except ValueError as e:
            print(f"  ❌ ERROR: Invalid campaign_id format: {e}")
            raise serializers.ValidationError({"campaign": "Invalid campaign id format."})
        
        # Check if Campaign Manager is assigned to this campaign
        print(f"\n🔐 Calling validate_campaign_manager_assignment...")
        validate_campaign_manager_assignment(user, TestimonyCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        print(f"\n✅ Validation passed! Saving submission...")
        print(f"  - Service: {service.name if service else 'None'} (ID: {service.id if service else 'None'})")
        print("="*80 + "\n")
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class TelepastoringSubmissionViewSet(viewsets.ModelViewSet):
    queryset = TelepastoringSubmission.objects.all()
    serializer_class = TelepastoringSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, TelepastoringCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = TelepastoringCampaign.objects.get(id=campaign_id)
        except TelepastoringCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, TelepastoringCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class GatheringBusSubmissionViewSet(viewsets.ModelViewSet):
    queryset = GatheringBusSubmission.objects.all()
    serializer_class = GatheringBusSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, GatheringBusCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = GatheringBusCampaign.objects.get(id=campaign_id)
        except GatheringBusCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, GatheringBusCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class OrganisedCreativeArtsSubmissionViewSet(viewsets.ModelViewSet):
    queryset = OrganisedCreativeArtsSubmission.objects.all()
    serializer_class = OrganisedCreativeArtsSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, OrganisedCreativeArtsCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = OrganisedCreativeArtsCampaign.objects.get(id=campaign_id)
        except OrganisedCreativeArtsCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, OrganisedCreativeArtsCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class TangerineSubmissionViewSet(viewsets.ModelViewSet):
    queryset = TangerineSubmission.objects.all()
    serializer_class = TangerineSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, TangerineCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = TangerineCampaign.objects.get(id=campaign_id)
        except TangerineCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, TangerineCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class SwollenSundaySubmissionViewSet(viewsets.ModelViewSet):
    queryset = SwollenSundaySubmission.objects.all()
    serializer_class = SwollenSundaySubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, SwollenSundayCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = SwollenSundayCampaign.objects.get(id=campaign_id)
        except SwollenSundayCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, SwollenSundayCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class SundayManagementSubmissionViewSet(viewsets.ModelViewSet):
    queryset = SundayManagementSubmission.objects.all()
    serializer_class = SundayManagementSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, SundayManagementCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = SundayManagementCampaign.objects.get(id=campaign_id)
        except SundayManagementCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, SundayManagementCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)


class EquipmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = EquipmentSubmission.objects.all()
    serializer_class = EquipmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter for Campaign Managers - only show assigned campaigns
        queryset = filter_queryset_for_campaign_manager(queryset, user, EquipmentCampaign)
        
        campaign_id = self.request.query_params.get('campaign', None)
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date_parsed = parse_date(start_date)
            if start_date_parsed:
                queryset = queryset.filter(submission_period__gte=start_date_parsed)
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            if end_date_parsed:
                queryset = queryset.filter(submission_period__lte=end_date_parsed)
        
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        campaign_id = self.request.data.get('campaign') or self.request.query_params.get('campaign')
        if not campaign_id:
            raise serializers.ValidationError({"campaign": "This field is required."})
        try:
            campaign = EquipmentCampaign.objects.get(id=campaign_id)
        except EquipmentCampaign.DoesNotExist:
            raise serializers.ValidationError({"campaign": "Invalid campaign id."})
        
        # Check if Campaign Manager is assigned to this campaign
        validate_campaign_manager_assignment(user, EquipmentCampaign, campaign_id)
        
        # Get service (Campaign Managers select, others use assigned)
        service = get_service_for_submission(user, self.request.data)
        serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)
