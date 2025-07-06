#!/usr/bin/env python3
import requests
import json
import unittest
from datetime import datetime, timedelta
import uuid
import logging
import os
import base64
from io import BytesIO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the backend URL from frontend/.env
BACKEND_URL = "https://6857cce4-3dd5-4419-a74f-40e213b028bb.preview.emergentagent.com/api"

class QBClonePhase4EndpointsTest(unittest.TestCase):
    """Test suite for QBClone Phase 4 Professional Features Endpoints"""
    
    def setUp(self):
        """Set up test data and clean the database"""
        self.company_id = None
        self.form_templates = {}
        self.custom_fields = {}
        self.permissions = {}
        self.user_roles = {}
        
        # Test the root endpoint to ensure API is accessible
        response = requests.get(f"{BACKEND_URL}/")
        self.assertEqual(response.status_code, 200)
        logger.info("API is accessible")
        
        # Create a test company if needed
        self.create_test_company()
    
    def create_test_company(self):
        """Create a test company for branding tests"""
        company_data = {
            "name": "Phase 4 Endpoints Test Company",
            "legal_name": "Phase 4 Endpoints Test Company LLC",
            "address": "789 Test Boulevard",
            "city": "Testville",
            "state": "TX",
            "zip_code": "54321",
            "country": "United States",
            "phone": "555-123-4567",
            "email": "info@phase4endpoints.com",
            "industry": "technology"
        }
        
        response = requests.post(f"{BACKEND_URL}/company", json=company_data)
        self.assertEqual(response.status_code, 200)
        company = response.json()
        self.company_id = company["id"]
        logger.info(f"Created test company with ID: {self.company_id}")
    
    def test_01_form_templates_endpoints(self):
        """Test form templates endpoints"""
        logger.info("Testing Form Templates Endpoints...")
        
        # 1. POST /api/form-templates - Create form templates
        template_data = {
            "name": "Standard Invoice Template",
            "template_type": "invoice",
            "is_default": True,
            "header_layout": {"title": "INVOICE", "subtitle": ""},
            "show_logo": True,
            "logo_position": "left",
            "show_company_info": True,
            "company_info_position": "top-right",
            "show_customer_info": True,
            "customer_info_position": "top-left",
            "line_items_columns": ["item", "description", "quantity", "rate", "amount"],
            "show_line_item_numbers": True,
            "show_subtotal": True,
            "show_tax": True,
            "show_total": True,
            "totals_position": "bottom-right",
            "footer_text": "Thank you for your business!",
            "show_terms": True,
            "show_memo": True,
            "primary_color": "#3B82F6",
            "secondary_color": "#F3F4F6",
            "font_family": "Arial",
            "font_size": "12px"
        }
        
        response = requests.post(f"{BACKEND_URL}/form-templates", json=template_data)
        self.assertEqual(response.status_code, 200)
        template = response.json()
        template_id = template["id"]
        self.form_templates["invoice"] = template
        logger.info(f"POST /api/form-templates - Created form template: {template['name']} with ID: {template_id}")
        
        # 2. GET /api/form-templates - List form templates
        response = requests.get(f"{BACKEND_URL}/form-templates")
        self.assertEqual(response.status_code, 200)
        templates = response.json()
        self.assertGreaterEqual(len(templates), 1)
        logger.info(f"GET /api/form-templates - Retrieved {len(templates)} form templates")
        
        # 3. GET /api/form-templates/{id} - Retrieve specific template
        response = requests.get(f"{BACKEND_URL}/form-templates/{template_id}")
        self.assertEqual(response.status_code, 200)
        retrieved_template = response.json()
        self.assertEqual(retrieved_template["id"], template_id)
        self.assertEqual(retrieved_template["name"], template_data["name"])
        logger.info(f"GET /api/form-templates/{template_id} - Retrieved form template: {retrieved_template['name']}")
        
        # 4. PUT /api/form-templates/{id} - Update template
        update_data = {
            "name": "Updated Invoice Template",
            "template_type": "invoice",
            "is_default": True,
            "header_layout": {"title": "INVOICE", "subtitle": "Updated Template"},
            "primary_color": "#4F46E5",
            "secondary_color": "#E0E7FF",
            "font_family": "Helvetica",
            "font_size": "11px"
        }
        
        response = requests.put(f"{BACKEND_URL}/form-templates/{template_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_template = response.json()
        self.assertEqual(updated_template["name"], update_data["name"])
        self.assertEqual(updated_template["primary_color"], update_data["primary_color"])
        logger.info(f"PUT /api/form-templates/{template_id} - Updated form template: {updated_template['name']}")
        
        # 5. POST /api/form-templates/{id}/set-default - Set default template
        # Create another template first
        template_data2 = {
            "name": "Secondary Invoice Template",
            "template_type": "invoice",
            "is_default": False,
            "primary_color": "#10B981",
            "secondary_color": "#ECFDF5"
        }
        
        response = requests.post(f"{BACKEND_URL}/form-templates", json=template_data2)
        self.assertEqual(response.status_code, 200)
        template2 = response.json()
        template2_id = template2["id"]
        self.form_templates["invoice2"] = template2
        
        response = requests.post(f"{BACKEND_URL}/form-templates/{template2_id}/set-default")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        logger.info(f"POST /api/form-templates/{template2_id}/set-default - {result['message']}")
        
        # Verify the template is now default
        response = requests.get(f"{BACKEND_URL}/form-templates/{template2_id}")
        self.assertEqual(response.status_code, 200)
        default_template = response.json()
        self.assertTrue(default_template["is_default"])
        
        # 6. DELETE /api/form-templates/{id} - Delete template
        response = requests.delete(f"{BACKEND_URL}/form-templates/{template_id}")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        logger.info(f"DELETE /api/form-templates/{template_id} - {result['message']}")
        
        # Verify template was deleted
        response = requests.get(f"{BACKEND_URL}/form-templates/{template_id}")
        self.assertEqual(response.status_code, 404)
        
        logger.info("Form Templates Endpoints tests passed")
    
    def test_02_custom_fields_endpoints(self):
        """Test custom fields endpoints"""
        logger.info("Testing Custom Fields Endpoints...")
        
        # 1. POST /api/custom-fields - Create custom field
        field_data = {
            "name": "customer_type",
            "label": "Customer Type",
            "field_type": "dropdown",
            "required": True,
            "options": ["Individual", "Business", "Government", "Non-profit"],
            "default_value": "Business"
        }
        
        response = requests.post(f"{BACKEND_URL}/custom-fields", json=field_data)
        self.assertEqual(response.status_code, 200)
        field = response.json()
        field_id = field["id"]
        self.custom_fields["dropdown"] = field
        logger.info(f"POST /api/custom-fields - Created custom field: {field['name']} with ID: {field_id}")
        
        # 2. GET /api/custom-fields - List custom fields
        response = requests.get(f"{BACKEND_URL}/custom-fields")
        self.assertEqual(response.status_code, 200)
        fields = response.json()
        self.assertGreaterEqual(len(fields), 1)
        logger.info(f"GET /api/custom-fields - Retrieved {len(fields)} custom fields")
        
        # 3. GET /api/custom-fields/{id} - Retrieve specific custom field
        response = requests.get(f"{BACKEND_URL}/custom-fields/{field_id}")
        self.assertEqual(response.status_code, 200)
        retrieved_field = response.json()
        self.assertEqual(retrieved_field["id"], field_id)
        self.assertEqual(retrieved_field["name"], field_data["name"])
        logger.info(f"GET /api/custom-fields/{field_id} - Retrieved custom field: {retrieved_field['name']}")
        
        # 4. PUT /api/custom-fields/{id} - Update custom field
        update_data = {
            "name": "customer_type",
            "label": "Client Category",
            "field_type": "dropdown",
            "required": True,
            "options": ["Individual", "Small Business", "Enterprise", "Government", "Non-profit"],
            "default_value": "Small Business"
        }
        
        response = requests.put(f"{BACKEND_URL}/custom-fields/{field_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_field = response.json()
        self.assertEqual(updated_field["label"], update_data["label"])
        self.assertEqual(len(updated_field["options"]), 5)
        self.assertEqual(updated_field["default_value"], update_data["default_value"])
        logger.info(f"PUT /api/custom-fields/{field_id} - Updated custom field: {updated_field['name']}")
        
        # 5. DELETE /api/custom-fields/{id} - Delete custom field
        # Create another field to delete
        field_data2 = {
            "name": "project_code",
            "label": "Project Code",
            "field_type": "text",
            "required": False
        }
        
        response = requests.post(f"{BACKEND_URL}/custom-fields", json=field_data2)
        self.assertEqual(response.status_code, 200)
        field2 = response.json()
        field2_id = field2["id"]
        
        response = requests.delete(f"{BACKEND_URL}/custom-fields/{field2_id}")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        logger.info(f"DELETE /api/custom-fields/{field2_id} - {result['message']}")
        
        # Verify field was deleted
        response = requests.get(f"{BACKEND_URL}/custom-fields/{field2_id}")
        self.assertEqual(response.status_code, 404)
        
        logger.info("Custom Fields Endpoints tests passed")
    
    def test_03_company_branding_endpoints(self):
        """Test company branding endpoints"""
        logger.info("Testing Company Branding Endpoints...")
        
        # 1. POST /api/company-branding - Create/update branding
        branding_data = {
            "company_id": self.company_id,
            "company_name": "Phase 4 Endpoints Test Company",
            "tagline": "Professional Testing Solutions",
            "primary_color": "#3B82F6",
            "secondary_color": "#F3F4F6",
            "font_family": "Arial"
        }
        
        response = requests.post(f"{BACKEND_URL}/company-branding", json=branding_data)
        self.assertEqual(response.status_code, 200)
        branding = response.json()
        logger.info(f"POST /api/company-branding - Created company branding for company ID: {branding['company_id']}")
        
        # 2. GET /api/company-branding/{company_id} - Retrieve branding
        response = requests.get(f"{BACKEND_URL}/company-branding/{self.company_id}")
        self.assertEqual(response.status_code, 200)
        retrieved_branding = response.json()
        self.assertEqual(retrieved_branding["company_id"], self.company_id)
        self.assertEqual(retrieved_branding["company_name"], branding_data["company_name"])
        self.assertEqual(retrieved_branding["tagline"], branding_data["tagline"])
        logger.info(f"GET /api/company-branding/{self.company_id} - Retrieved company branding for: {retrieved_branding['company_name']}")
        
        # 3. POST /api/company-branding - Update existing branding
        update_data = {
            "company_id": self.company_id,
            "company_name": "Phase 4 Endpoints Test Company",
            "tagline": "Excellence in Professional Testing",
            "primary_color": "#4F46E5",
            "secondary_color": "#E0E7FF",
            "font_family": "Helvetica"
        }
        
        response = requests.post(f"{BACKEND_URL}/company-branding", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_branding = response.json()
        self.assertEqual(updated_branding["tagline"], update_data["tagline"])
        self.assertEqual(updated_branding["primary_color"], update_data["primary_color"])
        self.assertEqual(updated_branding["font_family"], update_data["font_family"])
        logger.info(f"POST /api/company-branding - Updated company branding for: {updated_branding['company_name']}")
        
        # 4. POST /api/company-branding/{company_id}/upload-logo - Upload logo
        # Create a simple test image
        image_data = BytesIO()
        image_data.write(b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
        image_data.seek(0)
        
        files = {'file': ('company_logo.gif', image_data, 'image/gif')}
        response = requests.post(f"{BACKEND_URL}/company-branding/{self.company_id}/upload-logo", files=files)
        self.assertEqual(response.status_code, 200)
        logo_result = response.json()
        self.assertIn("message", logo_result)
        self.assertEqual(logo_result["filename"], "company_logo.gif")
        logger.info(f"POST /api/company-branding/{self.company_id}/upload-logo - {logo_result['message']}")
        
        # Verify logo was uploaded
        response = requests.get(f"{BACKEND_URL}/company-branding/{self.company_id}")
        self.assertEqual(response.status_code, 200)
        branding_with_logo = response.json()
        self.assertIsNotNone(branding_with_logo["logo_base64"])
        self.assertEqual(branding_with_logo["logo_filename"], "company_logo.gif")
        self.assertEqual(branding_with_logo["logo_mime_type"], "image/gif")
        
        logger.info("Company Branding Endpoints tests passed")
    
    def test_04_permissions_endpoints(self):
        """Test permissions endpoints"""
        logger.info("Testing Permissions Endpoints...")
        
        # 1. POST /api/permissions - Create permission
        permission_data = {
            "name": "reports_export",
            "description": "Export reports to various formats",
            "module": "reports",
            "actions": ["export_pdf", "export_csv", "export_excel"]
        }
        
        response = requests.post(f"{BACKEND_URL}/permissions", json=permission_data)
        self.assertEqual(response.status_code, 200)
        permission = response.json()
        permission_id = permission["id"]
        self.permissions["export"] = permission
        logger.info(f"POST /api/permissions - Created permission: {permission['name']} with ID: {permission_id}")
        
        # 2. GET /api/permissions - List permissions
        response = requests.get(f"{BACKEND_URL}/permissions")
        self.assertEqual(response.status_code, 200)
        permissions = response.json()
        self.assertGreaterEqual(len(permissions), 1)
        logger.info(f"GET /api/permissions - Retrieved {len(permissions)} permissions")
        
        # Verify our permission is in the list
        found = False
        for p in permissions:
            if p["id"] == permission_id:
                found = True
                self.assertEqual(p["name"], permission_data["name"])
                self.assertEqual(p["module"], permission_data["module"])
                break
        self.assertTrue(found, "Created permission not found in permissions list")
        
        logger.info("Permissions Endpoints tests passed")
    
    def test_05_user_roles_endpoints(self):
        """Test user roles endpoints"""
        logger.info("Testing User Roles Endpoints...")
        
        # First create some permissions to use in roles
        permission_data = [
            {
                "name": "dashboard_view",
                "description": "View dashboard",
                "module": "dashboard",
                "actions": ["read"]
            },
            {
                "name": "reports_view",
                "description": "View reports",
                "module": "reports",
                "actions": ["read"]
            },
            {
                "name": "settings_manage",
                "description": "Manage settings",
                "module": "settings",
                "actions": ["read", "update"]
            }
        ]
        
        permission_ids = []
        for data in permission_data:
            response = requests.post(f"{BACKEND_URL}/permissions", json=data)
            self.assertEqual(response.status_code, 200)
            permission = response.json()
            permission_ids.append(permission["id"])
            self.permissions[data["name"]] = permission
            logger.info(f"Created permission: {permission['name']} with ID: {permission['id']}")
        
        # 1. POST /api/user-roles - Create user role
        role_data = {
            "name": "Report Viewer",
            "description": "Can view dashboards and reports",
            "permissions": [permission_ids[0], permission_ids[1]],
            "is_admin": False
        }
        
        response = requests.post(f"{BACKEND_URL}/user-roles", json=role_data)
        self.assertEqual(response.status_code, 200)
        role = response.json()
        role_id = role["id"]
        self.user_roles["viewer"] = role
        logger.info(f"POST /api/user-roles - Created user role: {role['name']} with ID: {role_id}")
        
        # 2. GET /api/user-roles - List user roles
        response = requests.get(f"{BACKEND_URL}/user-roles")
        self.assertEqual(response.status_code, 200)
        roles = response.json()
        self.assertGreaterEqual(len(roles), 1)
        logger.info(f"GET /api/user-roles - Retrieved {len(roles)} user roles")
        
        # 3. GET /api/user-roles/{id} - Retrieve specific role
        response = requests.get(f"{BACKEND_URL}/user-roles/{role_id}")
        self.assertEqual(response.status_code, 200)
        retrieved_role = response.json()
        self.assertEqual(retrieved_role["id"], role_id)
        self.assertEqual(retrieved_role["name"], role_data["name"])
        self.assertEqual(len(retrieved_role["permissions"]), 2)
        logger.info(f"GET /api/user-roles/{role_id} - Retrieved user role: {retrieved_role['name']}")
        
        # 4. PUT /api/user-roles/{id} - Update user role
        update_data = {
            "name": "Report Viewer Plus",
            "description": "Can view dashboards, reports, and manage settings",
            "permissions": permission_ids,
            "is_admin": False
        }
        
        response = requests.put(f"{BACKEND_URL}/user-roles/{role_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_role = response.json()
        self.assertEqual(updated_role["name"], update_data["name"])
        self.assertEqual(updated_role["description"], update_data["description"])
        self.assertEqual(len(updated_role["permissions"]), 3)
        logger.info(f"PUT /api/user-roles/{role_id} - Updated user role: {updated_role['name']}")
        
        logger.info("User Roles Endpoints tests passed")
    
    def test_06_audit_log_endpoints(self):
        """Test audit log endpoints"""
        logger.info("Testing Audit Log Endpoints...")
        
        # Create a test user ID
        user_id = str(uuid.uuid4())
        
        # 1. POST /api/audit-log - Create audit log entry
        audit_data = {
            "user_id": user_id,
            "action": "create",
            "resource_type": "invoice",
            "resource_id": str(uuid.uuid4()),
            "new_values": {"number": "INV-001", "amount": 1000.00},
            "ip_address": "192.168.1.100",
            "user_agent": "Mozilla/5.0 (Test Browser)"
        }
        
        response = requests.post(f"{BACKEND_URL}/audit-log", json=audit_data)
        self.assertEqual(response.status_code, 200)
        audit_entry = response.json()
        audit_id = audit_entry["id"]
        logger.info(f"POST /api/audit-log - Created audit log entry with ID: {audit_id}")
        
        # Create a few more audit entries for the same resource
        for action in ["update", "view", "print"]:
            data = audit_data.copy()
            data["action"] = action
            if action == "update":
                data["old_values"] = {"amount": 1000.00}
                data["new_values"] = {"amount": 1200.00}
            
            response = requests.post(f"{BACKEND_URL}/audit-log", json=data)
            self.assertEqual(response.status_code, 200)
            logger.info(f"Created additional audit log entry for action: {action}")
        
        # 2. GET /api/audit-log - List audit logs
        response = requests.get(f"{BACKEND_URL}/audit-log")
        self.assertEqual(response.status_code, 200)
        logs = response.json()
        self.assertGreaterEqual(len(logs), 4)  # At least our 4 entries
        logger.info(f"GET /api/audit-log - Retrieved {len(logs)} audit logs")
        
        # 3. GET /api/audit-log with filtering
        response = requests.get(f"{BACKEND_URL}/audit-log?user_id={user_id}")
        self.assertEqual(response.status_code, 200)
        user_logs = response.json()
        self.assertGreaterEqual(len(user_logs), 4)
        for log in user_logs:
            self.assertEqual(log["user_id"], user_id)
        logger.info(f"GET /api/audit-log?user_id={user_id} - Retrieved {len(user_logs)} logs for user")
        
        # 4. GET /api/audit-log/{resource_type}/{resource_id} - Get resource-specific logs
        resource_type = audit_data["resource_type"]
        resource_id = audit_data["resource_id"]
        response = requests.get(f"{BACKEND_URL}/audit-log/{resource_type}/{resource_id}")
        self.assertEqual(response.status_code, 200)
        resource_logs = response.json()
        self.assertGreaterEqual(len(resource_logs), 4)
        for log in resource_logs:
            self.assertEqual(log["resource_type"], resource_type)
            self.assertEqual(log["resource_id"], resource_id)
        logger.info(f"GET /api/audit-log/{resource_type}/{resource_id} - Retrieved {len(resource_logs)} logs for resource")
        
        logger.info("Audit Log Endpoints tests passed")
    
    def test_07_setup_endpoints(self):
        """Test setup endpoints"""
        logger.info("Testing Setup Endpoints...")
        
        # 1. POST /api/setup/default-permissions - Setup default permissions
        response = requests.post(f"{BACKEND_URL}/setup/default-permissions")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        logger.info(f"POST /api/setup/default-permissions - {result['message']}")
        
        # Verify permissions and roles were created
        response = requests.get(f"{BACKEND_URL}/permissions")
        self.assertEqual(response.status_code, 200)
        permissions = response.json()
        self.assertGreaterEqual(len(permissions), 6)  # At least 6 default permissions
        
        response = requests.get(f"{BACKEND_URL}/user-roles")
        self.assertEqual(response.status_code, 200)
        roles = response.json()
        self.assertGreaterEqual(len(roles), 3)  # At least 3 default roles
        
        # Check for specific default roles
        role_names = [role["name"] for role in roles]
        admin_role_exists = "Administrator" in role_names
        accountant_role_exists = "Accountant" in role_names
        user_role_exists = "User" in role_names
        
        if admin_role_exists and accountant_role_exists and user_role_exists:
            logger.info("Default roles were created successfully")
        
        logger.info("Setup Endpoints tests passed")

if __name__ == "__main__":
    unittest.main()