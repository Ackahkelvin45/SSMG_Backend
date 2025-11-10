from rest_framework import viewsets, status, parsers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.db.models import Sum, Avg, Count, Q
from datetime import datetime, timedelta
from decimal import Decimal
from .models import CustomerUser, Service
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ServiceSerializer,
    ServiceCreateSerializer,
    ChangePasswordSerializer,
    CampaignManagerCreateSerializer
)
from helpers.pagination import DefaultPagination
from rest_framework.decorators import action

# Import all campaign models
from campaigns.models import (
    StateOfTheFlockSubmission, SoulWinningSubmission, ServantsArmedTrainedSubmission,
    AntibrutishSubmission, HearingSeeingSubmission, HonourYourProphetSubmission,
    BasontaProliferationSubmission, IntimateCounselingSubmission, TechnologySubmission,
    SheperdingControlSubmission, MultiplicationSubmission, UnderstandingSubmission,
    SheepSeekingSubmission, TestimonySubmission, TelepastoringSubmission,
    GatheringBusSubmission, OrganisedCreativeArtsSubmission, TangerineSubmission,
    SwollenSundaySubmission, SundayManagementSubmission,
    EquipmentSubmission,
)

# Import dashboard serializers
from campaigns.serializers import (
    DashboardSubmissionSerializer,
    DashboardCampaignSerializer
)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return ServiceCreateSerializer
        return ServiceSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomerUser.objects.all().select_related('service').order_by('-created_at')
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser] 

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        if self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # Handles both PUT (full) and PATCH (partial)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid(raise_exception=True):
            service_id = serializer.validated_data.pop('service', None)

            if service_id is not None:
                try:
                    service = Service.objects.get(id=service_id)
                except Service.DoesNotExist:
                    return Response({"message": "Service does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save(service=service)
            else:
                serializer.save()

            return Response(UserSerializer(self.get_object()).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def get_profile(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_service(self, request):
        """Return the authenticated user's service details."""
        service = getattr(request.user, 'service', None)
        if not service:
            return Response({"message": "User has no service assigned"}, status=status.HTTP_404_NOT_FOUND)
        return Response(ServiceSerializer(service).data, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Password changed successfully",
            "password_changed": True
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='create-campaign-manager')
    def create_campaign_manager(self, request):
        """
        Create a campaign manager user and assign campaigns.
        
        Campaign Managers are NOT assigned to a specific service.
        They can fill data for their assigned campaigns across ALL services.
        
        Password is auto-generated (default: "kelvin") - not exposed in the API.
        
        Required fields:
        - first_name, last_name, username, email, phone_number
        - campaign_assignments: list of campaign names (system auto-detects campaign type)
        
        Optional fields:
        - profile_picture
        
        Example request body:
        {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "john@example.com",
            "phone_number": "+1234567890",
            "campaign_assignments": [
                {"campaign_name": "State of the Flock 2025"},
                {"campaign_name": "Soul Winning Initiative"},
                {"campaign_name": "Technology Upgrade"}
            ]
        }
        """
        serializer = CampaignManagerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            CampaignManagerCreateSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Dashboard endpoint that provides different data based on user role.
        
        For Campaign Managers:
        - User details
        - Total assigned campaigns
        - List of assigned campaigns with details
        - Recent submissions (limited to assigned campaigns)
        - Recent campaigns they're assigned to
        
        For other roles (Pastor, Helper, Admin):
        - Standard dashboard (all campaigns and submissions)
        """
        user = request.user
        
        # Check if user is a Campaign Manager
        if user.is_campaign_manager:
            return self._campaign_manager_dashboard(request, user)
        
        # Standard dashboard for other roles
        return self._standard_dashboard(request, user)
    
    def _campaign_manager_dashboard(self, request, user):
        """Dashboard specifically for Campaign Managers"""
        from campaigns.models import CampaignManagerAssignment
        from django.contrib.contenttypes.models import ContentType
        
        # Get all assigned campaigns
        assignments = CampaignManagerAssignment.objects.filter(
            user=user
        ).select_related('content_type')
        
        # Build assigned campaigns data
        assigned_campaigns = []
        assigned_campaign_ids = {}  # Map of content_type_id -> list of campaign IDs
        
        for assignment in assignments:
            campaign = assignment.campaign
            if campaign:
                campaign_type = assignment.content_type.model_class().__name__
                
                # Track for filtering submissions
                ct_id = assignment.content_type.id
                if ct_id not in assigned_campaign_ids:
                    assigned_campaign_ids[ct_id] = []
                assigned_campaign_ids[ct_id].append(assignment.object_id)
                
                assigned_campaigns.append({
                    'id': campaign.id,
                    'name': campaign.name,
                    'description': campaign.description,
                    'campaign_type': campaign_type,
                    'status': campaign.status,
                    'created_at': campaign.created_at,
                    'icon': request.build_absolute_uri(campaign.icon.url) if campaign.icon else None,
                })
        
        # Get submission models mapping
        submission_models = [
            (StateOfTheFlockSubmission, "State of the Flock"),
            (SoulWinningSubmission, "Soul Winning"),
            (ServantsArmedTrainedSubmission, "Servants Armed and Trained"),
            (AntibrutishSubmission, "Antibrutish"),
            (HearingSeeingSubmission, "Hearing and Seeing"),
            (HonourYourProphetSubmission, "Honour Your Prophet"),
            (BasontaProliferationSubmission, "Basonta Proliferation"),
            (IntimateCounselingSubmission, "Intimate Counseling"),
            (TechnologySubmission, "Technology"),
            (SheperdingControlSubmission, "Sheperding Control"),
            (MultiplicationSubmission, "Multiplication"),
            (UnderstandingSubmission, "Understanding"),
            (SheepSeekingSubmission, "Sheep Seeking"),
            (TestimonySubmission, "Testimony"),
            (TelepastoringSubmission, "Telepastoring"),
            (GatheringBusSubmission, "Gathering Bus"),
            (OrganisedCreativeArtsSubmission, "Organised Creative Arts"),
            (TangerineSubmission, "Tangerine"),
            (SwollenSundaySubmission, "Swollen Sunday"),
            (SundayManagementSubmission, "Sunday Management"),
            (EquipmentSubmission, "Equipment"),
        ]
        
        # Get recent submissions (only for assigned campaigns)
        recent_submissions = []
        
        for SubmissionModel, campaign_type_name in submission_models:
            try:
                # Get content type for this submission model
                ct = ContentType.objects.get_for_model(SubmissionModel)
                
                # Check if this content type has any assigned campaigns
                if ct.id in assigned_campaign_ids:
                    # Filter submissions to only assigned campaigns
                    submissions = SubmissionModel.objects.filter(
                        campaign_id__in=assigned_campaign_ids[ct.id],
                        submitted_by=user
                    ).select_related('campaign', 'service').order_by('-created_at')[:10]
                    
                    for sub in submissions:
                        recent_submissions.append({
                            'id': sub.id,
                            'campaign_name': sub.campaign.name,
                            'campaign_type': campaign_type_name,
                            'service_name': sub.service.name if sub.service else 'N/A',
                            'submission_period': sub.submission_period,
                            'created_at': sub.created_at,
                        })
            except Exception:
                continue
        
        # Sort all submissions by created_at and take top 10
        recent_submissions = sorted(
            recent_submissions,
            key=lambda x: x['created_at'],
            reverse=True
        )[:10]
        
        # Return Campaign Manager dashboard data
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role,
                'phone_number': user.phone_number,
                'profile_picture': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
            },
            'total_assigned_campaigns': len(assigned_campaigns),
            'assigned_campaigns': assigned_campaigns,
            'recent_submissions': recent_submissions,
            'recent_campaigns': assigned_campaigns[:5],  # Show 5 most recent
        })
    
    def _standard_dashboard(self, request, user):
        """Standard dashboard for Pastor, Helper, and Admin roles"""
        
        submission_models = [
            (StateOfTheFlockSubmission, "State of the Flock"),
            (SoulWinningSubmission, "Soul Winning"),
            (ServantsArmedTrainedSubmission, "Servants Armed and Trained"),
            (AntibrutishSubmission, "Antibrutish"),
            (HearingSeeingSubmission, "Hearing and Seeing"),
            (HonourYourProphetSubmission, "Honour Your Prophet"),
            (BasontaProliferationSubmission, "Basonta Proliferation"),
            (IntimateCounselingSubmission, "Intimate Counseling"),
            (TechnologySubmission, "Technology"),
            (SheperdingControlSubmission, "Sheperding Control"),
            (MultiplicationSubmission, "Multiplication"),
            (UnderstandingSubmission, "Understanding"),
            (SheepSeekingSubmission, "Sheep Seeking"),
            (TestimonySubmission, "Testimony"),
            (TelepastoringSubmission, "Telepastoring"),
            (GatheringBusSubmission, "Gathering Bus"),
            (OrganisedCreativeArtsSubmission, "Organised Creative Arts"),
            (TangerineSubmission, "Tangerine"),
            (SwollenSundaySubmission, "Swollen Sunday"),
            (SundayManagementSubmission, "Sunday Management"),
            (EquipmentSubmission, "Equipment"),
        ]
        
        # ===== GET RECENT SUBMISSIONS (5 most recent across all types) =====
        all_submissions = []
        campaign_submission_counts = {}  # Track submission counts per campaign
        
        for SubmissionModel, campaign_type_name in submission_models:
            try:
                submissions = SubmissionModel.objects.filter(
                    submitted_by=user
                ).select_related('campaign').order_by('-created_at')[:5]
                
                for sub in submissions:
                    campaign_key = (sub.campaign.id, campaign_type_name)
                    
                    # Count submissions per campaign
                    if campaign_key not in campaign_submission_counts:
                        campaign_submission_counts[campaign_key] = SubmissionModel.objects.filter(
                            submitted_by=user,
                            campaign=sub.campaign
                        ).count()
                    
                    all_submissions.append({
                        'submission': sub,
                        'campaign_type': campaign_type_name,
                        'submission_count': campaign_submission_counts[campaign_key]
                    })
            except Exception:
                # Skip if there's an issue with this model
                continue
        
        # Sort all submissions by created_at (most recent first)
        all_submissions.sort(key=lambda x: x['submission'].created_at, reverse=True)
        
        # Take top 5 across all types, but ensure unique campaigns
        seen_campaigns = set()
        recent_submissions = []
        for sub_data in all_submissions:
            campaign_key = (sub_data['submission'].campaign.id, sub_data['campaign_type'])
            if campaign_key not in seen_campaigns:
                recent_submissions.append(sub_data)
                seen_campaigns.add(campaign_key)
                if len(recent_submissions) >= 5:
                    break
        
        # ===== GET RECENT CAMPAIGNS (5 most recently accessed) =====
        campaign_last_activity = {}
        
        for SubmissionModel, campaign_type_name in submission_models:
            try:
                # Get all user submissions for this type
                submissions = SubmissionModel.objects.filter(
                    submitted_by=user
                ).select_related('campaign').order_by('-created_at')
                
                # Track the most recent submission for each campaign
                for sub in submissions:
                    campaign_key = (sub.campaign.id, campaign_type_name)
                    
                    # Only track if this is the first time we see this campaign
                    if campaign_key not in campaign_last_activity:
                        # Count submissions for this campaign
                        submission_count = SubmissionModel.objects.filter(
                            submitted_by=user,
                            campaign=sub.campaign
                        ).count()
                        
                        campaign_last_activity[campaign_key] = {
                            'campaign': sub.campaign,
                            'campaign_type': campaign_type_name,
                            'last_accessed': sub.created_at,
                            'submission_count': submission_count
                        }
            except Exception:
                continue
        
        # Sort campaigns by last_accessed (most recent first)
        sorted_campaigns = sorted(
            campaign_last_activity.values(),
            key=lambda x: x['last_accessed'],
            reverse=True
        )
        
        # Take top 5
        recent_campaigns = sorted_campaigns[:5]
        
        # ===== CALCULATE STATISTICS =====
        active_campaigns = len(campaign_last_activity)
        
        # Count submissions this month
        current_month = timezone.now().month
        current_year = timezone.now().year
        submissions_this_month = 0
        
        for SubmissionModel, _ in submission_models:
            try:
                count = SubmissionModel.objects.filter(
                    submitted_by=user,
                    created_at__month=current_month,
                    created_at__year=current_year
                ).count()
                submissions_this_month += count
            except Exception:
                continue
        
        # ===== GET SERVICE INFORMATION =====
        service_data = None
        if user.service:
            service_data = {
                'id': user.service.id,
                'name': user.service.name or 'No Service Name',
                'location': user.service.location or 'Location not specified',
                'total_members': user.service.total_members or 0
            }
        
        # ===== SERIALIZE AND RETURN =====
        dashboard_data = {
            'service': service_data,
            'statistics': {
                'active_campaigns': active_campaigns,
                'submissions_this_month': submissions_this_month
            },
            'recent_submissions': DashboardSubmissionSerializer(
                recent_submissions, many=True, context={'request': request}
            ).data,
            'active_campaigns': DashboardCampaignSerializer(
                recent_campaigns, many=True, context={'request': request}
            ).data
        }
        
        return Response(dashboard_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """
        Get comprehensive analytics and growth metrics for the user's church/service.
        
        For Campaign Managers: Shows simplified analytics with only their submissions,
        totals over time, and basic data for assigned campaigns.
        
        For Other Roles: Shows comprehensive analytics.
        
        Query Parameters:
        - period: 'month', 'quarter', 'year', 'all' (default: 'month')
        - start_date: YYYY-MM-DD (optional, for custom range)
        - end_date: YYYY-MM-DD (optional, for custom range)
        """
        user = request.user
        
        # Check if user is a Campaign Manager
        if user.is_campaign_manager:
            return self._campaign_manager_analytics(request, user)
        
        # Standard analytics for other roles
        return self._standard_analytics(request, user)
    
    def _campaign_manager_analytics(self, request, user):
        """Simplified analytics for Campaign Managers - only their submissions"""
        from campaigns.models import CampaignManagerAssignment
        from django.contrib.contenttypes.models import ContentType
        
        # Get assigned campaign IDs
        assignments = CampaignManagerAssignment.objects.filter(user=user).select_related('content_type')
        assigned_campaign_ids = {}  # Map of content_type_id -> list of campaign IDs
        
        for assignment in assignments:
            ct_id = assignment.content_type.id
            if ct_id not in assigned_campaign_ids:
                assigned_campaign_ids[ct_id] = []
            assigned_campaign_ids[ct_id].append(assignment.object_id)
        
        # Determine date range
        period = request.query_params.get('period', 'month').lower()
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        
        now = timezone.now()
        
        if start_date_str and end_date_str:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
            if not start_date or not end_date:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            period_start = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            period_end = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
        elif period == 'week':
            period_start = now - timedelta(days=7)
            period_end = now
        elif period == 'month':
            period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            period_end = now
        elif period == 'quarter':
            quarter = (now.month - 1) // 3
            period_start = now.replace(month=quarter*3+1, day=1, hour=0, minute=0, second=0, microsecond=0)
            period_end = now
        elif period == 'year':
            period_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            period_end = now
        else:  # 'all'
            period_start = None
            period_end = now
        
        # Helper function to filter submissions for assigned campaigns
        def filter_submissions(model, date_field='created_at'):
            from campaigns.views import filter_queryset_for_campaign_manager
            # Get content type for this model
            ct = ContentType.objects.get_for_model(model)
            
            # If this content type has assigned campaigns, filter by them
            if ct.id in assigned_campaign_ids:
                campaign_ids = assigned_campaign_ids[ct.id]
                qs = model.objects.filter(
                    submitted_by=user,
                    campaign_id__in=campaign_ids
                )
            else:
                # No assigned campaigns of this type
                qs = model.objects.none()
            
            # Apply date filtering
            if period_start:
                if date_field == 'created_at':
                    qs = qs.filter(created_at__gte=period_start, created_at__lte=period_end)
                elif date_field == 'submission_period':
                    qs = qs.filter(submission_period__gte=period_start.date(), submission_period__lte=period_end.date())
                elif date_field == 'date':
                    qs = qs.filter(date__gte=period_start.date(), date__lte=period_end.date())
            
            return qs
        
        # Get all submissions for assigned campaigns (all time)
        def get_all_time_submissions(model):
            ct = ContentType.objects.get_for_model(model)
            if ct.id in assigned_campaign_ids:
                campaign_ids = assigned_campaign_ids[ct.id]
                return model.objects.filter(
                    submitted_by=user,
                    campaign_id__in=campaign_ids
                )
            return model.objects.none()
        
        # Submission models mapping
        submission_models = [
            (StateOfTheFlockSubmission, "State of the Flock", 'submission_period'),
            (SoulWinningSubmission, "Soul Winning", 'date'),
            (ServantsArmedTrainedSubmission, "Servants Armed and Trained", 'date'),
            (AntibrutishSubmission, "Antibrutish", 'date'),
            (HearingSeeingSubmission, "Hearing and Seeing", 'date'),
            (HonourYourProphetSubmission, "Honour Your Prophet", 'date'),
            (BasontaProliferationSubmission, "Basonta Proliferation", 'submission_period'),
            (IntimateCounselingSubmission, "Intimate Counseling", 'date'),
            (TechnologySubmission, "Technology", 'date'),
            (SheperdingControlSubmission, "Sheperding Control", 'submission_period'),
            (MultiplicationSubmission, "Multiplication", 'date'),
            (UnderstandingSubmission, "Understanding", 'date'),
            (SheepSeekingSubmission, "Sheep Seeking", 'date'),
            (TestimonySubmission, "Testimony", 'date'),
            (TelepastoringSubmission, "Telepastoring", 'date'),
            (GatheringBusSubmission, "Gathering Bus", 'date'),
            (OrganisedCreativeArtsSubmission, "Organised Creative Arts", 'date'),
            (TangerineSubmission, "Tangerine", 'date'),
            (SwollenSundaySubmission, "Swollen Sunday", 'submission_period'),
            (SundayManagementSubmission, "Sunday Management", 'date'),
            (EquipmentSubmission, "Equipment", 'date'),
        ]
        
        # Calculate totals
        total_submissions_all_time = 0
        total_submissions_this_period = 0
        submissions_by_type = {}
        submissions_over_time = []
        
        for SubmissionModel, campaign_type_name, date_field in submission_models:
            # All time submissions
            all_time_qs = get_all_time_submissions(SubmissionModel)
            all_time_count = all_time_qs.count()
            total_submissions_all_time += all_time_count
            
            # This period submissions
            period_qs = filter_submissions(SubmissionModel, date_field)
            period_count = period_qs.count()
            total_submissions_this_period += period_count
            
            # Store by type
            if all_time_count > 0 or period_count > 0:
                submissions_by_type[campaign_type_name] = {
                    "all_time": all_time_count,
                    "this_period": period_count
                }
            
            # Get submissions over time (last 12 months)
            ct = ContentType.objects.get_for_model(SubmissionModel)
            if ct.id in assigned_campaign_ids:
                campaign_ids = assigned_campaign_ids[ct.id]
                trend_qs = SubmissionModel.objects.filter(
                    submitted_by=user,
                    campaign_id__in=campaign_ids
                ).exclude(**{date_field + '__isnull': True}).order_by('-' + date_field)[:12]
                
                for sub in trend_qs:
                    date_value = getattr(sub, date_field)
                    if date_value:
                        if date_field == 'submission_period':
                            period_key = date_value.strftime("%Y-%m")
                            period_label = date_value.strftime("%b %Y")
                        else:
                            period_key = date_value.strftime("%Y-%m")
                            period_label = date_value.strftime("%b %Y")
                        
                        # Add to submissions_over_time if not already present
                        existing = next((x for x in submissions_over_time if x['period'] == period_key), None)
                        if existing:
                            existing['count'] += 1
                        else:
                            submissions_over_time.append({
                                "period": period_key,
                                "label": period_label,
                                "count": 1
                            })
        
        # Sort submissions over time
        submissions_over_time.sort(key=lambda x: x['period'])
        
        # Get recent submissions (last 10)
        recent_submissions = []
        for SubmissionModel, campaign_type_name, date_field in submission_models:
            ct = ContentType.objects.get_for_model(SubmissionModel)
            if ct.id in assigned_campaign_ids:
                campaign_ids = assigned_campaign_ids[ct.id]
                recent = SubmissionModel.objects.filter(
                    submitted_by=user,
                    campaign_id__in=campaign_ids
                ).select_related('campaign', 'service').order_by('-created_at')[:10]
                
                for sub in recent:
                    recent_submissions.append({
                        "id": sub.id,
                        "campaign_name": sub.campaign.name if sub.campaign else "Unknown",
                        "campaign_type": campaign_type_name,
                        "service_name": sub.service.name if sub.service else "N/A",
                        "submission_period": str(sub.submission_period) if hasattr(sub, 'submission_period') and sub.submission_period else None,
                        "date": str(sub.date) if hasattr(sub, 'date') and sub.date else None,
                        "created_at": sub.created_at.isoformat()
                    })
        
        # Sort by created_at and take top 10
        recent_submissions.sort(key=lambda x: x['created_at'], reverse=True)
        recent_submissions = recent_submissions[:10]
        
        # Basic statistics
        assigned_campaigns_count = len(assigned_campaign_ids)
        total_campaigns_assigned = sum(len(ids) for ids in assigned_campaign_ids.values())
        
        # Build analytics response
        analytics_data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "role": user.role
            },
            "period": {
                "type": period,
                "start": period_start.isoformat() if period_start else None,
                "end": period_end.isoformat()
            },
            "summary": {
                "total_submissions_all_time": total_submissions_all_time,
                "total_submissions_this_period": total_submissions_this_period,
                "assigned_campaigns_count": assigned_campaigns_count,
                "total_campaigns_assigned": total_campaigns_assigned
            },
            "submissions_by_type": submissions_by_type,
            "submissions_over_time": submissions_over_time,
            "recent_submissions": recent_submissions,
            "chart_data": {
                "labels": [item["label"] for item in submissions_over_time],
                "data": [item["count"] for item in submissions_over_time],
                "color": "#2196F3"
            }
        }
        
        return Response(analytics_data, status=status.HTTP_200_OK)
    
    def _standard_analytics(self, request, user):
        """Standard comprehensive analytics for Pastor, Helper, and Admin roles"""
        
        # Determine date range
        period = request.query_params.get('period', 'month').lower()
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        
        now = timezone.now()
        
        if start_date_str and end_date_str:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
            if not start_date or not end_date:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            period_start = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            period_end = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
        elif period == 'week':
            period_start = now - timedelta(days=7)
            period_end = now
        elif period == 'month':
            period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            period_end = now
        elif period == 'quarter':
            quarter = (now.month - 1) // 3
            period_start = now.replace(month=quarter*3+1, day=1, hour=0, minute=0, second=0, microsecond=0)
            period_end = now
        elif period == 'year':
            period_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            period_end = now
        else:  # 'all'
            period_start = None
            period_end = now
        
        # Previous period for comparison
        if period_start:
            period_duration = period_end - period_start
            prev_period_start = period_start - period_duration
            prev_period_end = period_start
        else:
            prev_period_start = None
            prev_period_end = None
        
        def get_queryset(model, date_field='created_at'):
            qs = model.objects.filter(submitted_by=user)
            if period_start:
                if date_field == 'created_at':
                    qs = qs.filter(created_at__gte=period_start, created_at__lte=period_end)
                elif date_field == 'submission_period':
                    qs = qs.filter(submission_period__gte=period_start.date(), submission_period__lte=period_end.date())
                elif date_field == 'date':
                    qs = qs.filter(date__gte=period_start.date(), date__lte=period_end.date())
            return qs
        
        def get_prev_queryset(model, date_field='created_at'):
            qs = model.objects.filter(submitted_by=user)
            if prev_period_start:
                if date_field == 'created_at':
                    qs = qs.filter(created_at__gte=prev_period_start, created_at__lte=prev_period_end)
                elif date_field == 'submission_period':
                    qs = qs.filter(submission_period__gte=prev_period_start.date(), submission_period__lte=prev_period_end.date())
                elif date_field == 'date':
                    qs = qs.filter(date__gte=prev_period_start.date(), date__lte=prev_period_end.date())
            return qs
        
        # ===== MEMBERSHIP ANALYTICS =====
        membership_data = {
            "current": 0,
            "previous": 0,
            "growth": 0,
            "growth_percentage": 0.0,
            "stable": 0,
            "unstable": 0,
            "lost": 0,
            "trend": []
        }
        
        # Get latest membership data
        latest_membership = StateOfTheFlockSubmission.objects.filter(
            submitted_by=user
        ).order_by('-submission_period', '-created_at').first()
        
        if latest_membership:
            membership_data["current"] = latest_membership.total_membership or 0
            membership_data["stable"] = latest_membership.stable or 0
            membership_data["unstable"] = latest_membership.unstable or 0
            membership_data["lost"] = latest_membership.lost or 0
            
            # Get previous period membership
            # Try to find the most recent submission before the latest one
            prev_membership = StateOfTheFlockSubmission.objects.filter(
                submitted_by=user
            ).exclude(submission_period__isnull=True).order_by('-submission_period', '-created_at')
            
            if prev_membership.count() > 1:
                # Get the second most recent (previous) submission
                prev_membership_obj = prev_membership[1]
                membership_data["previous"] = prev_membership_obj.total_membership or 0
                membership_data["growth"] = membership_data["current"] - membership_data["previous"]
                if membership_data["previous"] > 0:
                    membership_data["growth_percentage"] = (membership_data["growth"] / membership_data["previous"]) * 100
            elif prev_period_start:
                # Fallback to period-based comparison if we have a previous period
                prev_membership_obj = StateOfTheFlockSubmission.objects.filter(
                    submitted_by=user,
                    submission_period__lt=period_start.date()
                ).exclude(submission_period__isnull=True).order_by('-submission_period', '-created_at').first()
                
                if prev_membership_obj:
                    membership_data["previous"] = prev_membership_obj.total_membership or 0
                    membership_data["growth"] = membership_data["current"] - membership_data["previous"]
                    if membership_data["previous"] > 0:
                        membership_data["growth_percentage"] = (membership_data["growth"] / membership_data["previous"]) * 100
        
        # Membership trend (last 12 months for better visualization)
        membership_submissions = StateOfTheFlockSubmission.objects.filter(
            submitted_by=user
        ).exclude(submission_period__isnull=True).order_by('-submission_period')[:12]
        
        membership_data["trend"] = [
            {
                "period": sub.submission_period.strftime("%Y-%m") if sub.submission_period else None,
                "label": sub.submission_period.strftime("%b %Y") if sub.submission_period else None,
                "total": sub.total_membership or 0,
                "stable": sub.stable or 0,
                "unstable": sub.unstable or 0,
                "lost": sub.lost or 0
            }
            for sub in membership_submissions
        ]
        membership_data["trend"].reverse()
        
        # Membership line chart data (for multi-series chart)
        membership_data["chart_data"] = {
            "labels": [item["label"] for item in membership_data["trend"]],
            "datasets": [
                {
                    "label": "Total Membership",
                    "data": [item["total"] for item in membership_data["trend"]],
                    "color": "#2196F3"
                },
                {
                    "label": "Stable Members",
                    "data": [item["stable"] for item in membership_data["trend"]],
                    "color": "#4CAF50"
                },
                {
                    "label": "Unstable Members",
                    "data": [item["unstable"] for item in membership_data["trend"]],
                    "color": "#FF9800"
                }
            ]
        }
        
        # ===== SOUL WINNING ANALYTICS =====
        soul_winning_qs = get_queryset(SoulWinningSubmission, 'date')
        soul_winning_prev_qs = get_prev_queryset(SoulWinningSubmission, 'date') if prev_period_start else SoulWinningSubmission.objects.none()
        
        total_souls_all_time = SoulWinningSubmission.objects.filter(
            submitted_by=user
        ).aggregate(total=Sum('no_of_souls_won'))['total'] or 0
        
        souls_this_period = soul_winning_qs.aggregate(
            total=Sum('no_of_souls_won'),
            crusades=Sum('no_of_crusades'),
            outreaches=Sum('no_of_massive_organised_outreaches'),
            dance_outreach=Sum('no_of_dance_outreach'),
            missionaries_sent=Sum('no_of_missionaries_sent')
        )
        
        souls_prev_period = soul_winning_prev_qs.aggregate(
            total=Sum('no_of_souls_won')
        ) if prev_period_start else {'total': 0}
        
        soul_winning_data = {
            "total_all_time": int(total_souls_all_time),
            "this_period": int(souls_this_period['total'] or 0),
            "previous_period": int(souls_prev_period['total'] or 0),
            "crusades": int(souls_this_period['crusades'] or 0),
            "outreaches": int(souls_this_period['outreaches'] or 0),
            "dance_outreach": int(souls_this_period['dance_outreach'] or 0),
            "missionaries_sent": int(souls_this_period['missionaries_sent'] or 0),
            "trend": []
        }
        
        # Soul winning trend (last 12 months)
        soul_trend_qs = SoulWinningSubmission.objects.filter(
            submitted_by=user
        ).exclude(date__isnull=True).order_by('-date')[:12]
        
        soul_winning_data["trend"] = [
            {
                "period": sub.date.strftime("%Y-%m") if sub.date else None,
                "label": sub.date.strftime("%b %Y") if sub.date else None,
                "souls_won": sub.no_of_souls_won or 0,
                "crusades": sub.no_of_crusades or 0,
                "outreaches": sub.no_of_massive_organised_outreaches or 0,
                "dance_outreach": sub.no_of_dance_outreach or 0,
                "missionaries_sent": sub.no_of_missionaries_sent or 0
            }
            for sub in soul_trend_qs
        ]
        soul_winning_data["trend"].reverse()
        
        # Soul winning cumulative trend
        cumulative = 0
        soul_winning_data["cumulative_trend"] = []
        for item in soul_winning_data["trend"]:
            cumulative += item["souls_won"]
            soul_winning_data["cumulative_trend"].append({
                "period": item["period"],
                "label": item["label"],
                "cumulative": cumulative
            })
        
        # Soul winning chart data for stacked bar chart
        soul_winning_data["chart_data"] = {
            "labels": [item["label"] for item in soul_winning_data["trend"]],
            "datasets": [
                {
                    "label": "Souls Won",
                    "data": [item["souls_won"] for item in soul_winning_data["trend"]],
                    "color": "#4CAF50"
                },
                {
                    "label": "Crusades",
                    "data": [item["crusades"] for item in soul_winning_data["trend"]],
                    "color": "#2196F3"
                },
                {
                    "label": "Outreaches",
                    "data": [item["outreaches"] for item in soul_winning_data["trend"]],
                    "color": "#FF9800"
                }
            ],
            "cumulative": {
                "labels": [item["label"] for item in soul_winning_data["cumulative_trend"]],
                "data": [item["cumulative"] for item in soul_winning_data["cumulative_trend"]],
                "color": "#9C27B0"
            }
        }
        
        # ===== LEADERSHIP ANALYTICS =====
        leadership_qs = get_queryset(ServantsArmedTrainedSubmission, 'date')
        leadership_data = {
            "total_leaders": 0,
            "trained_leaders": 0,
            "teaching_sessions": int(leadership_qs.aggregate(total=Sum('no_of_teachings_done_by_pastor'))['total'] or 0),
            "avg_attendance": float(leadership_qs.aggregate(avg=Avg('average_attendance_during_meetings_by_pastor'))['avg'] or 0),
            "hierarchy": {
                "cos": 0,
                "bos": 0,
                "bls": 0,
                "fls": 0,
                "potential_leaders": 0
            },
            "training_metrics": {
                "makarios": int(leadership_qs.aggregate(total=Sum('no_of_leaders_who_have_makarios'))['total'] or 0),
                "dakes_bible": int(leadership_qs.aggregate(total=Sum('no_of_leaders_who_own_dakes_bible'))['total'] or 0),
                "thompson_chain": int(leadership_qs.aggregate(total=Sum('no_of_leaders_who_own_thompson_chain'))['total'] or 0),
                "pose_certified": int(leadership_qs.aggregate(total=Sum('no_of_pose_certified_leaders'))['total'] or 0),
                "iptp_training": int(leadership_qs.aggregate(total=Sum('no_of_leaders_in_iptp_training'))['total'] or 0)
            }
        }
        
        # Get latest sheperding control data for hierarchy
        latest_sheperding = SheperdingControlSubmission.objects.filter(
            submitted_by=user
        ).order_by('-submission_period', '-created_at').first()
        
        if latest_sheperding:
            leadership_data["total_leaders"] = latest_sheperding.current_no_of_leaders or 0
            leadership_data["hierarchy"]["cos"] = latest_sheperding.no_of_cos or 0
            leadership_data["hierarchy"]["bos"] = latest_sheperding.no_of_bos or 0
            leadership_data["hierarchy"]["bls"] = latest_sheperding.no_of_bls or 0
            leadership_data["hierarchy"]["fls"] = latest_sheperding.no_of_fls or 0
            leadership_data["hierarchy"]["potential_leaders"] = latest_sheperding.no_of_potential_leaders or 0
        
        # ===== SMALL GROUP ANALYTICS =====
        small_group_qs = get_queryset(BasontaProliferationSubmission, 'submission_period')
        latest_group = BasontaProliferationSubmission.objects.filter(
            submitted_by=user
        ).order_by('-submission_period', '-created_at').first()
        
        small_group_data = {
            "bacentas": 0,
            "basontas": 0,
            "new_groups": 0,
            "avg_attendance": 0,
            "avg_saturday": 0,
            "avg_sunday": 0,
            "trend": [],
            "chart_data": {}
        }
        
        if latest_group:
            small_group_data["bacentas"] = latest_group.current_number_of_bacentas or 0
            small_group_data["basontas"] = latest_group.no_of_basontas or 0
            small_group_data["new_groups"] = latest_group.no_of_new_bacentas or 0
            small_group_data["avg_attendance"] = latest_group.average_no_of_people_at_bacenta_meeting or 0
            small_group_data["avg_saturday"] = latest_group.avg_no_of_members_saturday_service or 0
            small_group_data["avg_sunday"] = latest_group.avg_no_of_members_sunday_service or 0
        
        # Small group trend (last 12 months)
        group_trend_qs = BasontaProliferationSubmission.objects.filter(
            submitted_by=user
        ).exclude(submission_period__isnull=True).order_by('-submission_period')[:12]
        
        small_group_data["trend"] = [
            {
                "period": sub.submission_period.strftime("%Y-%m") if sub.submission_period else None,
                "label": sub.submission_period.strftime("%b %Y") if sub.submission_period else None,
                "bacentas": sub.current_number_of_bacentas or 0,
                "basontas": sub.no_of_basontas or 0,
                "new_groups": sub.no_of_new_bacentas or 0,
                "avg_attendance": sub.average_no_of_people_at_bacenta_meeting or 0,
                "avg_saturday": sub.avg_no_of_members_saturday_service or 0,
                "avg_sunday": sub.avg_no_of_members_sunday_service or 0
            }
            for sub in group_trend_qs
        ]
        small_group_data["trend"].reverse()
        
        # Small group chart data (dual line chart)
        small_group_data["chart_data"] = {
            "labels": [item["label"] for item in small_group_data["trend"]],
            "datasets": [
                {
                    "label": "Bacentas",
                    "data": [item["bacentas"] for item in small_group_data["trend"]],
                    "color": "#2196F3"
                },
                {
                    "label": "Basontas",
                    "data": [item["basontas"] for item in small_group_data["trend"]],
                    "color": "#4CAF50"
                }
            ]
        }
        
        # ===== ATTENDANCE ANALYTICS =====
        attendance_qs = get_queryset(GatheringBusSubmission, 'date')
        attendance_data = {
            "avg_service": float(attendance_qs.aggregate(avg=Avg('avg_attendance_for_the_service'))['avg'] or 0),
            "avg_saturday": float(attendance_qs.aggregate(avg=Avg('avg_number_of_members_bused'))['avg'] or 0),
            "avg_sunday": 0,
            "avg_bused": float(attendance_qs.aggregate(avg=Avg('avg_number_of_members_bused'))['avg'] or 0),
            "avg_walk_in": float(attendance_qs.aggregate(avg=Avg('avg_number_of_members_who_walk_in'))['avg'] or 0),
            "first_timers": int(attendance_qs.aggregate(total=Sum('avg_number_of_first_timers'))['total'] or 0),
            "trend": [],
            "chart_data": {}
        }
        
        # Get Sunday service from small groups
        if latest_group:
            attendance_data["avg_sunday"] = latest_group.avg_no_of_members_sunday_service or 0
        
        # Swollen Sunday data
        swollen_qs = get_queryset(SwollenSundaySubmission, 'submission_period')
        swollen_data = swollen_qs.aggregate(
            attendance=Sum('attendance_for_swollen_sunday'),
            converts=Sum('no_of_converts_for_swollen_sunday')
        )
        attendance_data["swollen_sunday"] = {
            "attendance": int(swollen_data['attendance'] or 0),
            "converts": int(swollen_data['converts'] or 0)
        }
        
        # Attendance trend (last 12 months)
        attendance_trend_qs = GatheringBusSubmission.objects.filter(
            submitted_by=user
        ).exclude(date__isnull=True).order_by('-date')[:12]
        
        attendance_data["trend"] = [
            {
                "period": sub.date.strftime("%Y-%m") if sub.date else None,
                "label": sub.date.strftime("%b %Y") if sub.date else None,
                "avg_service": sub.avg_attendance_for_the_service or 0,
                "avg_bused": sub.avg_number_of_members_bused or 0,
                "avg_walk_in": sub.avg_number_of_members_who_walk_in or 0,
                "first_timers": sub.avg_number_of_first_timers or 0
            }
            for sub in attendance_trend_qs
        ]
        attendance_data["trend"].reverse()
        
        # Attendance chart data (multi-series line chart)
        attendance_data["chart_data"] = {
            "labels": [item["label"] for item in attendance_data["trend"]],
            "datasets": [
                {
                    "label": "Service Attendance",
                    "data": [item["avg_service"] for item in attendance_data["trend"]],
                    "color": "#2196F3"
                },
                {
                    "label": "Bused Members",
                    "data": [item["avg_bused"] for item in attendance_data["trend"]],
                    "color": "#4CAF50"
                },
                {
                    "label": "Walk-in Members",
                    "data": [item["avg_walk_in"] for item in attendance_data["trend"]],
                    "color": "#FF9800"
                },
                {
                    "label": "First Timers",
                    "data": [item["first_timers"] for item in attendance_data["trend"]],
                    "color": "#9C27B0"
                }
            ]
        }
        
        # Add Sunday service attendance from small groups trend
        if small_group_data["trend"]:
            sunday_attendance = [item["avg_sunday"] for item in small_group_data["trend"]]
            if any(sunday_attendance):
                attendance_data["chart_data"]["datasets"].append({
                    "label": "Sunday Service",
                    "data": sunday_attendance[:len(attendance_data["chart_data"]["labels"])],
                    "color": "#F44336"
                })
        
        # ===== ENGAGEMENT ANALYTICS =====
        engagement_qs = get_queryset(HearingSeeingSubmission, 'date')
        testimony_qs = get_queryset(TestimonySubmission, 'date')
        understanding_qs = get_queryset(UnderstandingSubmission, 'date')
        
        engagement_data = {
            "youtube_subscribers": int(engagement_qs.aggregate(total=Sum('no_of_people_subscribed_bishop_dag_youtube'))['total'] or 0),
            "podcast_subscribers": int(engagement_qs.aggregate(total=Sum('no_of_people_subscribed_es_joys_podcast'))['total'] or 0),
            "messages_listened": int(engagement_qs.aggregate(total=Sum('no_of_messages_listened_to'))['total'] or 0),
            "testimonies_shared": int(testimony_qs.aggregate(total=Sum('number_of_testimonies_shared'))['total'] or 0),
            "lay_school_attendance": float(understanding_qs.aggregate(avg=Avg('average_attendance_at_lay_school_meeting'))['avg'] or 0),
            "lay_school_teachers": int(understanding_qs.aggregate(total=Sum('no_of_lay_school_teachers'))['total'] or 0),
            "trend": [],
            "chart_data": {}
        }
        
        # Engagement trend (last 12 months)
        engagement_trend_qs = HearingSeeingSubmission.objects.filter(
            submitted_by=user
        ).exclude(date__isnull=True).order_by('-date')[:12]
        
        testimony_trend_qs = TestimonySubmission.objects.filter(
            submitted_by=user
        ).exclude(date__isnull=True).order_by('-date')[:12]
        
        understanding_trend_qs = UnderstandingSubmission.objects.filter(
            submitted_by=user
        ).exclude(date__isnull=True).order_by('-date')[:12]
        
        # Group by month for engagement
        engagement_by_month = {}
        for sub in engagement_trend_qs:
            month_key = sub.date.strftime("%Y-%m") if sub.date else None
            if month_key:
                if month_key not in engagement_by_month:
                    engagement_by_month[month_key] = {
                        "period": month_key,
                        "label": sub.date.strftime("%b %Y"),
                        "youtube": 0,
                        "podcast": 0,
                        "messages": 0
                    }
                engagement_by_month[month_key]["youtube"] += sub.no_of_people_subscribed_bishop_dag_youtube or 0
                engagement_by_month[month_key]["podcast"] += sub.no_of_people_subscribed_es_joys_podcast or 0
                engagement_by_month[month_key]["messages"] += sub.no_of_messages_listened_to or 0
        
        testimony_by_month = {}
        for sub in testimony_trend_qs:
            month_key = sub.date.strftime("%Y-%m") if sub.date else None
            if month_key:
                if month_key not in testimony_by_month:
                    testimony_by_month[month_key] = 0
                testimony_by_month[month_key] += sub.number_of_testimonies_shared or 0
        
        # Combine engagement data
        all_months = sorted(set(list(engagement_by_month.keys()) + list(testimony_by_month.keys())))[-12:]
        engagement_data["trend"] = [
            {
                "period": month_key,
                "label": engagement_by_month.get(month_key, {}).get("label", month_key),
                "youtube_subscribers": engagement_by_month.get(month_key, {}).get("youtube", 0),
                "podcast_subscribers": engagement_by_month.get(month_key, {}).get("podcast", 0),
                "messages_listened": engagement_by_month.get(month_key, {}).get("messages", 0),
                "testimonies_shared": testimony_by_month.get(month_key, 0)
            }
            for month_key in all_months
        ]
        engagement_data["trend"].reverse()
        
        # Engagement chart data
        engagement_data["chart_data"] = {
            "labels": [item["label"] for item in engagement_data["trend"]],
            "datasets": [
                {
                    "label": "YouTube Subscribers",
                    "data": [item["youtube_subscribers"] for item in engagement_data["trend"]],
                    "color": "#FF0000"
                },
                {
                    "label": "Podcast Subscribers",
                    "data": [item["podcast_subscribers"] for item in engagement_data["trend"]],
                    "color": "#9C27B0"
                },
                {
                    "label": "Testimonies Shared",
                    "data": [item["testimonies_shared"] for item in engagement_data["trend"]],
                    "color": "#FF9800"
                }
            ]
        }
        
        # ===== MEMBER CARE ANALYTICS =====
        counseling_qs = get_queryset(IntimateCounselingSubmission, 'submission_period')
        telepastoring_qs = get_queryset(TelepastoringSubmission, 'date')
        
        latest_counseling = IntimateCounselingSubmission.objects.filter(
            submitted_by=user
        ).order_by('-submission_period', '-created_at').first()
        
        member_care_data = {
            "members_counseled": int(counseling_qs.aggregate(total=Sum('total_number_of_members_counseled'))['total'] or 0),
            "counseling_coverage": 0.0,
            "calls_made": int(telepastoring_qs.aggregate(total=Sum('total_no_of_calls_made'))['total'] or 0),
            "telepastors": int(telepastoring_qs.aggregate(total=Sum('no_of_telepastors'))['total'] or 0),
            "in_person": int(counseling_qs.aggregate(total=Sum('no_of_members_counseled_in_person'))['total'] or 0),
            "via_calls": int(counseling_qs.aggregate(total=Sum('no_of_members_counseled_via_calls'))['total'] or 0),
            "trend": [],
            "chart_data": {}
        }
        
        if latest_counseling and latest_counseling.total_number_of_members:
            total_members = latest_counseling.total_number_of_members
            if total_members > 0:
                member_care_data["counseling_coverage"] = (member_care_data["members_counseled"] / total_members) * 100
        
        # Member care trend (last 12 months)
        counseling_trend_qs = IntimateCounselingSubmission.objects.filter(
            submitted_by=user
        ).exclude(submission_period__isnull=True).order_by('-submission_period')[:12]
        
        telepastoring_trend_qs = TelepastoringSubmission.objects.filter(
            submitted_by=user
        ).exclude(date__isnull=True).order_by('-date')[:12]
        
        counseling_by_month = {}
        for sub in counseling_trend_qs:
            month_key = sub.submission_period.strftime("%Y-%m") if sub.submission_period else None
            if month_key:
                if month_key not in counseling_by_month:
                    counseling_by_month[month_key] = {
                        "period": month_key,
                        "label": sub.submission_period.strftime("%b %Y"),
                        "counseled": 0,
                        "in_person": 0,
                        "via_calls": 0
                    }
                counseling_by_month[month_key]["counseled"] += sub.total_number_of_members_counseled or 0
                counseling_by_month[month_key]["in_person"] += sub.no_of_members_counseled_in_person or 0
                counseling_by_month[month_key]["via_calls"] += sub.no_of_members_counseled_via_calls or 0
        
        calls_by_month = {}
        for sub in telepastoring_trend_qs:
            month_key = sub.date.strftime("%Y-%m") if sub.date else None
            if month_key:
                if month_key not in calls_by_month:
                    calls_by_month[month_key] = 0
                calls_by_month[month_key] += sub.total_no_of_calls_made or 0
        
        all_care_months = sorted(set(list(counseling_by_month.keys()) + list(calls_by_month.keys())))[-12:]
        member_care_data["trend"] = [
            {
                "period": month_key,
                "label": counseling_by_month.get(month_key, {}).get("label", month_key),
                "members_counseled": counseling_by_month.get(month_key, {}).get("counseled", 0),
                "in_person": counseling_by_month.get(month_key, {}).get("in_person", 0),
                "via_calls": counseling_by_month.get(month_key, {}).get("via_calls", 0),
                "calls_made": calls_by_month.get(month_key, 0)
            }
            for month_key in all_care_months
        ]
        member_care_data["trend"].reverse()
        
        # Member care chart data (stacked bar chart for counseling)
        member_care_data["chart_data"] = {
            "labels": [item["label"] for item in member_care_data["trend"]],
            "datasets": [
                {
                    "label": "Members Counseled",
                    "data": [item["members_counseled"] for item in member_care_data["trend"]],
                    "color": "#2196F3"
                },
                {
                    "label": "In Person",
                    "data": [item["in_person"] for item in member_care_data["trend"]],
                    "color": "#4CAF50"
                },
                {
                    "label": "Via Calls",
                    "data": [item["via_calls"] for item in member_care_data["trend"]],
                    "color": "#FF9800"
                },
                {
                    "label": "Telepastoring Calls",
                    "data": [item["calls_made"] for item in member_care_data["trend"]],
                    "color": "#9C27B0"
                }
            ]
        }
        
        # ===== PRAYER ANALYTICS =====
        prayer_qs = get_queryset(AntibrutishSubmission, 'date')
        prayer_data = {
            "hours_prayed": float(prayer_qs.aggregate(total=Sum('hours_prayed'))['total'] or Decimal('0.0')),
            "participants": int(prayer_qs.aggregate(total=Sum('number_of_people_who_prayed'))['total'] or 0),
            "trend": [],
            "chart_data": {}
        }
        
        # Prayer trend (last 12 months)
        prayer_trend_qs = AntibrutishSubmission.objects.filter(
            submitted_by=user
        ).exclude(date__isnull=True).order_by('-date')[:12]
        
        prayer_by_month = {}
        for sub in prayer_trend_qs:
            month_key = sub.date.strftime("%Y-%m") if sub.date else None
            if month_key:
                if month_key not in prayer_by_month:
                    prayer_by_month[month_key] = {
                        "period": month_key,
                        "label": sub.date.strftime("%b %Y"),
                        "hours": Decimal('0.0'),
                        "participants": 0
                    }
                prayer_by_month[month_key]["hours"] += sub.hours_prayed or Decimal('0.0')
                prayer_by_month[month_key]["participants"] += sub.number_of_people_who_prayed or 0
        
        prayer_data["trend"] = [
            {
                "period": month_key,
                "label": data["label"],
                "hours_prayed": float(data["hours"]),
                "participants": data["participants"]
            }
            for month_key, data in sorted(prayer_by_month.items())[-12:]
        ]
        prayer_data["trend"].reverse()
        
        # Prayer chart data (dual axis chart)
        prayer_data["chart_data"] = {
            "labels": [item["label"] for item in prayer_data["trend"]],
            "datasets": [
                {
                    "label": "Hours Prayed",
                    "data": [item["hours_prayed"] for item in prayer_data["trend"]],
                    "color": "#2196F3",
                    "yAxisID": "y"
                },
                {
                    "label": "Participants",
                    "data": [item["participants"] for item in prayer_data["trend"]],
                    "color": "#4CAF50",
                    "yAxisID": "y1"
                }
            ]
        }
        
        # ===== OUTREACH ANALYTICS (Multiplication & Sheep Seeking) =====
        multiplication_qs = get_queryset(MultiplicationSubmission, 'date')
        sheep_seeking_qs = get_queryset(SheepSeekingSubmission, 'date')
        
        outreach_data = {
            "total_outreaches": int(multiplication_qs.aggregate(total=Sum('no_of_outreaches'))['total'] or 0),
            "members_from_outreaches": int(multiplication_qs.aggregate(total=Sum('no_of_members_who_came_from_outreaches_to_church'))['total'] or 0),
            "total_invites": int(multiplication_qs.aggregate(total=Sum('no_of_invites_done'))['total'] or 0),
            "people_visited": int(sheep_seeking_qs.aggregate(total=Sum('no_of_people_visited'))['total'] or 0),
            "first_time_retained": int(sheep_seeking_qs.aggregate(total=Sum('no_of_first_time_retained'))['total'] or 0),
            "converts_retained": int(sheep_seeking_qs.aggregate(total=Sum('no_of_converts_retained'))['total'] or 0),
            "trend": [],
            "chart_data": {}
        }
        
        # Outreach trend (last 12 months)
        multiplication_trend_qs = MultiplicationSubmission.objects.filter(
            submitted_by=user
        ).exclude(date__isnull=True).order_by('-date')[:12]
        
        sheep_seeking_trend_qs = SheepSeekingSubmission.objects.filter(
            submitted_by=user
        ).exclude(date__isnull=True).order_by('-date')[:12]
        
        outreach_by_month = {}
        for sub in multiplication_trend_qs:
            month_key = sub.date.strftime("%Y-%m") if sub.date else None
            if month_key:
                if month_key not in outreach_by_month:
                    outreach_by_month[month_key] = {
                        "period": month_key,
                        "label": sub.date.strftime("%b %Y"),
                        "outreaches": 0,
                        "members_from_outreaches": 0,
                        "invites": 0
                    }
                outreach_by_month[month_key]["outreaches"] += sub.no_of_outreaches or 0
                outreach_by_month[month_key]["members_from_outreaches"] += sub.no_of_members_who_came_from_outreaches_to_church or 0
                outreach_by_month[month_key]["invites"] += sub.no_of_invites_done or 0
        
        visits_by_month = {}
        for sub in sheep_seeking_trend_qs:
            month_key = sub.date.strftime("%Y-%m") if sub.date else None
            if month_key:
                if month_key not in visits_by_month:
                    visits_by_month[month_key] = {
                        "period": month_key,
                        "label": sub.date.strftime("%b %Y"),
                        "people_visited": 0,
                        "first_time_retained": 0,
                        "converts_retained": 0
                    }
                visits_by_month[month_key]["people_visited"] += sub.no_of_people_visited or 0
                visits_by_month[month_key]["first_time_retained"] += sub.no_of_first_time_retained or 0
                visits_by_month[month_key]["converts_retained"] += sub.no_of_converts_retained or 0
        
        all_outreach_months = sorted(set(list(outreach_by_month.keys()) + list(visits_by_month.keys())))[-12:]
        outreach_data["trend"] = [
            {
                "period": month_key,
                "label": outreach_by_month.get(month_key, visits_by_month.get(month_key, {})).get("label", month_key),
                "outreaches": outreach_by_month.get(month_key, {}).get("outreaches", 0),
                "members_from_outreaches": outreach_by_month.get(month_key, {}).get("members_from_outreaches", 0),
                "invites": outreach_by_month.get(month_key, {}).get("invites", 0),
                "people_visited": visits_by_month.get(month_key, {}).get("people_visited", 0),
                "first_time_retained": visits_by_month.get(month_key, {}).get("first_time_retained", 0),
                "converts_retained": visits_by_month.get(month_key, {}).get("converts_retained", 0)
            }
            for month_key in all_outreach_months
        ]
        outreach_data["trend"].reverse()
        
        # Outreach chart data (funnel-style stacked chart)
        outreach_data["chart_data"] = {
            "labels": [item["label"] for item in outreach_data["trend"]],
            "datasets": [
                {
                    "label": "Outreaches",
                    "data": [item["outreaches"] for item in outreach_data["trend"]],
                    "color": "#2196F3"
                },
                {
                    "label": "People Visited",
                    "data": [item["people_visited"] for item in outreach_data["trend"]],
                    "color": "#4CAF50"
                },
                {
                    "label": "Members from Outreaches",
                    "data": [item["members_from_outreaches"] for item in outreach_data["trend"]],
                    "color": "#FF9800"
                },
                {
                    "label": "First Time Retained",
                    "data": [item["first_time_retained"] for item in outreach_data["trend"]],
                    "color": "#9C27B0"
                },
                {
                    "label": "Converts Retained",
                    "data": [item["converts_retained"] for item in outreach_data["trend"]],
                    "color": "#F44336"
                }
            ]
        }
        
        # ===== BUILD RESPONSE =====
        analytics_data = {
            "period": {
                "type": period,
                "start": period_start.isoformat() if period_start else None,
                "end": period_end.isoformat() if period_end else None
            },
            "membership": membership_data,
            "soul_winning": soul_winning_data,
            "leadership": leadership_data,
            "small_groups": small_group_data,
            "attendance": attendance_data,
            "engagement": engagement_data,
            "member_care": member_care_data,
            "prayer": prayer_data,
            "outreach": outreach_data
        }
        
        return Response(analytics_data, status=status.HTTP_200_OK)

