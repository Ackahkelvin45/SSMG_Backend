#!/usr/bin/env python
"""
Test script to verify Campaign Manager submission fix.
This script helps test that Campaign Managers can now submit to their assigned campaigns.

Usage:
    python test_campaign_manager_submission.py
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SSMGBackend.settings')
django.setup()

from authentication.models import CustomerUser
from campaigns.models import (
    CampaignManagerAssignment,
    SoulWinningCampaign,
    StateOfTheFlockCampaign
)
from django.contrib.contenttypes.models import ContentType


def test_campaign_manager_assignments():
    """Test that Campaign Manager assignments are working correctly"""
    
    print("=" * 80)
    print("CAMPAIGN MANAGER SUBMISSION FIX - TEST SCRIPT")
    print("=" * 80)
    print()
    
    # Find all Campaign Managers
    campaign_managers = CustomerUser.objects.filter(role='CAMPAIGN_MANAGER')
    
    if not campaign_managers.exists():
        print("❌ No Campaign Managers found in the database!")
        print("   Create a Campaign Manager first using:")
        print("   POST /api/auth/users/create-campaign-manager/")
        return
    
    print(f"✅ Found {campaign_managers.count()} Campaign Manager(s)\n")
    
    for cm in campaign_managers:
        print("-" * 80)
        print(f"Campaign Manager: {cm.full_name} (@{cm.username})")
        print(f"Email: {cm.email}")
        print(f"ID: {cm.id}")
        print()
        
        # Get assignments
        assignments = CampaignManagerAssignment.objects.filter(user=cm).select_related('content_type')
        
        if not assignments.exists():
            print("  ⚠️  No campaigns assigned to this Campaign Manager!")
            print("     Assign campaigns using:")
            print(f"     PATCH /api/auth/users/{cm.id}/update-campaign-manager/")
            print()
            continue
        
        print(f"  📋 Assigned Campaigns: {assignments.count()}")
        print()
        
        for i, assignment in enumerate(assignments, 1):
            campaign = assignment.campaign
            content_type = assignment.content_type
            
            print(f"  {i}. Campaign: {campaign}")
            print(f"     Type: {content_type.model}")
            print(f"     Campaign ID: {assignment.object_id}")
            print(f"     Content Type ID: {content_type.id}")
            
            # Test the validation logic
            campaign_id_str = str(assignment.object_id)  # As it comes from request
            campaign_id_int = int(campaign_id_str)  # After conversion
            
            # Test with string (OLD WAY - would fail)
            test_with_string = CampaignManagerAssignment.objects.filter(
                user=cm,
                content_type=content_type,
                object_id=campaign_id_str  # String
            ).exists()
            
            # Test with int (NEW WAY - works correctly)
            test_with_int = CampaignManagerAssignment.objects.filter(
                user=cm,
                content_type=content_type,
                object_id=campaign_id_int  # Integer
            ).exists()
            
            print(f"     Lookup with string '{campaign_id_str}': {'✅ Found' if test_with_string else '❌ Not Found'}")
            print(f"     Lookup with int {campaign_id_int}: {'✅ Found' if test_with_int else '❌ Not Found'}")
            
            if test_with_int and not test_with_string:
                print(f"     ✅ FIX WORKING: Int conversion solves the issue!")
            elif test_with_string and test_with_int:
                print(f"     ℹ️  Both work (database may auto-convert)")
            elif not test_with_int:
                print(f"     ❌ ERROR: Assignment not found even with int!")
            
            print()
        
        # Test example submission validation
        if assignments.exists():
            first_assignment = assignments.first()
            campaign_model = first_assignment.content_type.model_class()
            campaign_id = first_assignment.object_id
            
            print(f"  🧪 Test Validation:")
            print(f"     Campaign Model: {campaign_model.__name__}")
            print(f"     Campaign ID: {campaign_id}")
            
            # Simulate the validation function
            ct = ContentType.objects.get_for_model(campaign_model)
            
            # Test with string (OLD - would fail)
            validation_str = CampaignManagerAssignment.objects.filter(
                user=cm,
                content_type=ct,
                object_id=str(campaign_id)
            ).exists()
            
            # Test with int (NEW - works)
            validation_int = CampaignManagerAssignment.objects.filter(
                user=cm,
                content_type=ct,
                object_id=int(campaign_id)
            ).exists()
            
            print(f"     Validation with string: {'✅ PASS' if validation_str else '❌ FAIL'}")
            print(f"     Validation with int: {'✅ PASS' if validation_int else '❌ FAIL'}")
            
            if validation_int:
                print(f"     ✅ This Campaign Manager CAN submit to this campaign!")
            else:
                print(f"     ❌ This Campaign Manager CANNOT submit (assignment missing)")
        
        print()
    
    print("=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    print()
    print("📝 SUMMARY:")
    print("   - Campaign Managers should be able to submit to assigned campaigns")
    print("   - The fix converts campaign_id from string to int before validation")
    print("   - All validations with int should show ✅ PASS")
    print()
    print("📌 NEXT STEPS:")
    print("   1. Test via API: POST /api/campaigns/{type}/submissions/")
    print("   2. Include 'campaign' and 'service' fields in the request")
    print("   3. Use an assigned campaign ID")
    print()


def show_campaign_info():
    """Show available campaigns for testing"""
    print("\n" + "=" * 80)
    print("AVAILABLE CAMPAIGNS FOR TESTING")
    print("=" * 80)
    print()
    
    # Show some campaigns
    campaigns = [
        ("Soul Winning", SoulWinningCampaign),
        ("State of the Flock", StateOfTheFlockCampaign),
    ]
    
    for name, model in campaigns:
        campaign_list = model.objects.all()[:5]
        if campaign_list.exists():
            print(f"📌 {name} Campaigns:")
            for c in campaign_list:
                print(f"   ID: {c.id}, Name: {c.name}")
            print()


if __name__ == '__main__':
    try:
        test_campaign_manager_assignments()
        show_campaign_info()
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()


