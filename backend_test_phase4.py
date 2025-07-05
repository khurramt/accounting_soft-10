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
from PIL import Image
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the backend URL from frontend/.env
BACKEND_URL = "https://ecc4dc05-109d-4342-9bbf-50fb5400ea9e.preview.emergentagent.com/api"

class QBClonePhase4BackendTest(unittest.TestCase):
    """Test suite for QBClone Phase 4 backend API features"""
    
    def setUp(self):
        """Set up test data and clean the database"""
        self.form_templates = {}
        self.custom_fields = {}
        self.company_branding = {}
        self.users = {}
        self.permissions = {}
        self.user_roles = {}
        self.auth_tokens = {}
        self.audit_logs = {}
        
        # Test the root endpoint to ensure API is accessible
        response = requests.get(f"{BACKEND_URL}/")
        self.assertEqual(response.status_code, 200)
        logger.info("API is accessible")
    
    def test_01_form_customization_api(self):
        """Test form customization API endpoints"""
        logger.info("Testing Form Customization API...")
        
        # 1. Create form template
        template_data = {
            "name": "Custom Invoice Template",
            "template_type": "invoice",
            "is_default": False,
            "header_layout": {"title": "INVOICE", "subtitle": "Thank you for your business"},
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
            "primary_color": "#336699",
            "secondary_color": "#F5F5F5",
            "font_family": "Arial",
            "font_size": "12px"
        }
        
        response = requests.post(f"{BACKEND_URL}/form-templates", json=template_data)
        self.assertEqual(response.status_code, 200)
        template = response.json()
        self.form_templates["invoice"] = template
        logger.info(f"Created form template: {template['name']} with ID: {template['id']}")
        
        # Create another template for testing
        template_data2 = {
            "name": "Custom Estimate Template",
            "template_type": "estimate",
            "is_default": False,
            "primary_color": "#663399",
            "secondary_color": "#F0F0F0",
            "font_family": "Helvetica",
            "font_size": "11px"
        }
        
        response = requests.post(f"{BACKEND_URL}/form-templates", json=template_data2)
        self.assertEqual(response.status_code, 200)
        template2 = response.json()
        self.form_templates["estimate"] = template2
        logger.info(f"Created form template: {template2['name']} with ID: {template2['id']}")
        
        # 2. List form templates
        response = requests.get(f"{BACKEND_URL}/form-templates")
        self.assertEqual(response.status_code, 200)
        templates = response.json()
        self.assertGreaterEqual(len(templates), 2)
        logger.info(f"Retrieved {len(templates)} form templates")
        
        # 3. Get specific template
        response = requests.get(f"{BACKEND_URL}/form-templates/{template['id']}")
        self.assertEqual(response.status_code, 200)
        retrieved_template = response.json()
        self.assertEqual(retrieved_template["id"], template["id"])
        self.assertEqual(retrieved_template["name"], template["name"])
        logger.info(f"Retrieved form template: {retrieved_template['name']}")
        
        # 4. Update template
        # Get the current template first
        response = requests.get(f"{BACKEND_URL}/form-templates/{template['id']}")
        current_template = response.json()
        
        # Update only specific fields
        update_data = current_template.copy()
        update_data["name"] = "Updated Invoice Template"
        update_data["primary_color"] = "#3366CC"
        update_data["footer_text"] = "Updated footer text"
        
        response = requests.put(f"{BACKEND_URL}/form-templates/{template['id']}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_template = response.json()
        self.assertEqual(updated_template["name"], update_data["name"])
        self.assertEqual(updated_template["primary_color"], update_data["primary_color"])
        self.assertEqual(updated_template["footer_text"], update_data["footer_text"])
        logger.info(f"Updated form template: {updated_template['name']}")
        
        # 5. Set template as default
        response = requests.post(f"{BACKEND_URL}/form-templates/{template['id']}/set-default")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        logger.info(f"Set template as default: {result['message']}")
        
        # Verify template is now default
        response = requests.get(f"{BACKEND_URL}/form-templates/{template['id']}")
        self.assertEqual(response.status_code, 200)
        default_template = response.json()
        self.assertTrue(default_template["is_default"])
        
        # 6. Delete template
        response = requests.delete(f"{BACKEND_URL}/form-templates/{template2['id']}")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        logger.info(f"Deleted form template: {result['message']}")
        
        # Verify template was deleted
        response = requests.get(f"{BACKEND_URL}/form-templates/{template2['id']}")
        self.assertEqual(response.status_code, 404)
        
        logger.info("Form Customization API tests passed")
    
    def test_02_custom_fields_api(self):
        """Test custom fields API endpoints"""
        logger.info("Testing Custom Fields API...")
        
        # 1. Create custom field
        field_data = {
            "name": "customer_industry",
            "label": "Industry",
            "field_type": "dropdown",
            "required": False,
            "options": ["Technology", "Healthcare", "Finance", "Education", "Other"],
            "default_value": "Other"
        }
        
        response = requests.post(f"{BACKEND_URL}/custom-fields", json=field_data)
        self.assertEqual(response.status_code, 200)
        field = response.json()
        self.custom_fields["dropdown"] = field
        logger.info(f"Created custom field: {field['label']} with ID: {field['id']}")
        
        # Create another custom field
        field_data2 = {
            "name": "project_code",
            "label": "Project Code",
            "field_type": "text",
            "required": True
        }
        
        response = requests.post(f"{BACKEND_URL}/custom-fields", json=field_data2)
        self.assertEqual(response.status_code, 200)
        field2 = response.json()
        self.custom_fields["text"] = field2
        logger.info(f"Created custom field: {field2['label']} with ID: {field2['id']}")
        
        # 2. List custom fields
        response = requests.get(f"{BACKEND_URL}/custom-fields")
        self.assertEqual(response.status_code, 200)
        fields = response.json()
        self.assertGreaterEqual(len(fields), 2)
        logger.info(f"Retrieved {len(fields)} custom fields")
        
        # 3. Get specific custom field
        response = requests.get(f"{BACKEND_URL}/custom-fields/{field['id']}")
        self.assertEqual(response.status_code, 200)
        retrieved_field = response.json()
        self.assertEqual(retrieved_field["id"], field["id"])
        self.assertEqual(retrieved_field["name"], field["name"])
        logger.info(f"Retrieved custom field: {retrieved_field['label']}")
        
        # 4. Update custom field
        # Get the current field first
        response = requests.get(f"{BACKEND_URL}/custom-fields/{field['id']}")
        current_field = response.json()
        
        # Update only specific fields
        update_data = current_field.copy()
        update_data["label"] = "Business Industry"
        update_data["options"] = ["Technology", "Healthcare", "Finance", "Education", "Retail", "Other"]
        update_data["default_value"] = "Technology"
        
        response = requests.put(f"{BACKEND_URL}/custom-fields/{field['id']}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_field = response.json()
        self.assertEqual(updated_field["label"], update_data["label"])
        self.assertEqual(updated_field["options"], update_data["options"])
        self.assertEqual(updated_field["default_value"], update_data["default_value"])
        logger.info(f"Updated custom field: {updated_field['label']}")
        
        # 5. Delete custom field
        response = requests.delete(f"{BACKEND_URL}/custom-fields/{field2['id']}")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        logger.info(f"Deleted custom field: {result['message']}")
        
        # Verify field was deleted
        response = requests.get(f"{BACKEND_URL}/custom-fields/{field2['id']}")
        self.assertEqual(response.status_code, 404)
        
        logger.info("Custom Fields API tests passed")
    
    def test_03_company_branding_api(self):
        """Test company branding API endpoints"""
        logger.info("Testing Company Branding API...")
        
        # Create a company first if needed
        company_data = {
            "name": "Test Branding Company",
            "legal_name": "Test Branding Company LLC",
            "email": "info@testbranding.com"
        }
        
        response = requests.post(f"{BACKEND_URL}/company", json=company_data)
        self.assertEqual(response.status_code, 200)
        company = response.json()
        company_id = company["id"]
        logger.info(f"Created company with ID: {company_id}")
        
        # 1. Create/update company branding
        branding_data = {
            "company_id": company_id,
            "company_name": "Test Branding Company",
            "tagline": "Quality Accounting Solutions",
            "primary_color": "#336699",
            "secondary_color": "#F5F5F5",
            "font_family": "Arial"
        }
        
        response = requests.post(f"{BACKEND_URL}/company-branding", json=branding_data)
        self.assertEqual(response.status_code, 200)
        branding = response.json()
        self.company_branding["default"] = branding
        logger.info(f"Created company branding with ID: {branding['id']}")
        
        # 2. Get company branding
        response = requests.get(f"{BACKEND_URL}/company-branding/{company_id}")
        self.assertEqual(response.status_code, 200)
        retrieved_branding = response.json()
        self.assertEqual(retrieved_branding["id"], branding["id"])
        self.assertEqual(retrieved_branding["company_name"], branding_data["company_name"])
        logger.info(f"Retrieved company branding for: {retrieved_branding['company_name']}")
        
        # 3. Upload logo
        # Create a simple test image
        img = np.zeros((100, 300, 3), dtype=np.uint8)
        img[:,:,0] = 255  # Red
        img[:50,:,1] = 255  # Yellow top half
        
        # Convert to PIL Image and save to a file
        pil_img = Image.fromarray(img.astype('uint8'))
        pil_img.save("/tmp/test_logo.png")
        
        # Upload the file
        with open("/tmp/test_logo.png", "rb") as f:
            files = {"file": ("test_logo.png", f, "image/png")}
            response = requests.post(f"{BACKEND_URL}/company-branding/{company_id}/upload-logo", files=files)
        self.assertEqual(response.status_code, 200)
        logo_result = response.json()
        self.assertIn("message", logo_result)
        logger.info(f"Uploaded logo: {logo_result['message']}")
        
        # Verify logo was uploaded
        response = requests.get(f"{BACKEND_URL}/company-branding/{company_id}")
        self.assertEqual(response.status_code, 200)
        updated_branding = response.json()
        self.assertIsNotNone(updated_branding["logo_base64"])
        self.assertEqual(updated_branding["logo_filename"], "test_logo.png")
        logger.info("Logo upload verified")
        
        logger.info("Company Branding API tests passed")
    
    def test_04_user_management_api(self):
        """Test user management API endpoints"""
        logger.info("Testing User Management API...")
        
        # 1. Create user
        user_data = {
            "username": "testuser1",
            "full_name": "Test User One",
            "email": "testuser1@example.com",
            "password": "SecurePassword123!",
            "role": "User"
        }
        
        response = requests.post(f"{BACKEND_URL}/users", json=user_data)
        self.assertEqual(response.status_code, 200)
        user = response.json()
        self.users["user1"] = user
        logger.info(f"Created user: {user['username']} with ID: {user['id']}")
        
        # Create admin user
        admin_data = {
            "username": "adminuser",
            "full_name": "Admin User",
            "email": "admin@example.com",
            "password": "AdminPassword123!",
            "role": "Admin"
        }
        
        response = requests.post(f"{BACKEND_URL}/users", json=admin_data)
        self.assertEqual(response.status_code, 200)
        admin = response.json()
        self.users["admin"] = admin
        logger.info(f"Created admin user: {admin['username']} with ID: {admin['id']}")
        
        # 2. List users
        response = requests.get(f"{BACKEND_URL}/users")
        self.assertEqual(response.status_code, 200)
        users = response.json()
        self.assertGreaterEqual(len(users), 2)
        logger.info(f"Retrieved {len(users)} users")
        
        # 3. Get specific user
        response = requests.get(f"{BACKEND_URL}/users/{user['id']}")
        self.assertEqual(response.status_code, 200)
        retrieved_user = response.json()
        self.assertEqual(retrieved_user["id"], user["id"])
        self.assertEqual(retrieved_user["username"], user["username"])
        logger.info(f"Retrieved user: {retrieved_user['username']}")
        
        # 4. Update user
        # Get the current user first
        response = requests.get(f"{BACKEND_URL}/users/{user['id']}")
        current_user = response.json()
        
        # Update only specific fields
        update_data = current_user.copy()
        update_data["full_name"] = "Updated Test User"
        update_data["email"] = "updated.testuser@example.com"
        update_data["role"] = "Manager"
        # Add password field which is required for update
        update_data["password"] = "SecurePassword123!"
        
        response = requests.put(f"{BACKEND_URL}/users/{user['id']}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_user = response.json()
        self.assertEqual(updated_user["full_name"], update_data["full_name"])
        self.assertEqual(updated_user["email"], update_data["email"])
        self.assertEqual(updated_user["role"], update_data["role"])
        logger.info(f"Updated user: {updated_user['username']}")
        
        # 5. Delete user
        response = requests.delete(f"{BACKEND_URL}/users/{user['id']}")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        logger.info(f"Deleted user: {result['message']}")
        
        # Verify user was deactivated (not actually deleted)
        response = requests.get(f"{BACKEND_URL}/users/{user['id']}")
        self.assertEqual(response.status_code, 200)
        deactivated_user = response.json()
        self.assertFalse(deactivated_user["active"])
        
        logger.info("User Management API tests passed")
    
    def test_05_role_permissions_api(self):
        """Test role and permissions API endpoints"""
        logger.info("Testing Role & Permissions API...")
        
        # 1. Create permissions
        permission_data = [
            {
                "name": "accounts_view",
                "description": "View accounts",
                "module": "accounts",
                "actions": ["read"]
            },
            {
                "name": "accounts_edit",
                "description": "Edit accounts",
                "module": "accounts",
                "actions": ["create", "update"]
            },
            {
                "name": "transactions_view",
                "description": "View transactions",
                "module": "transactions",
                "actions": ["read"]
            },
            {
                "name": "transactions_edit",
                "description": "Edit transactions",
                "module": "transactions",
                "actions": ["create", "update", "delete"]
            }
        ]
        
        for perm in permission_data:
            response = requests.post(f"{BACKEND_URL}/permissions", json=perm)
            self.assertEqual(response.status_code, 200)
            permission = response.json()
            self.permissions[perm["name"]] = permission
            logger.info(f"Created permission: {permission['name']} with ID: {permission['id']}")
        
        # 2. List permissions
        response = requests.get(f"{BACKEND_URL}/permissions")
        self.assertEqual(response.status_code, 200)
        permissions = response.json()
        self.assertGreaterEqual(len(permissions), len(permission_data))
        logger.info(f"Retrieved {len(permissions)} permissions")
        
        # 3. Create user role
        role_data = {
            "name": "Accountant",
            "description": "Accounting staff with limited permissions",
            "permissions": [
                self.permissions["accounts_view"]["id"],
                self.permissions["accounts_edit"]["id"],
                self.permissions["transactions_view"]["id"]
            ],
            "is_admin": False
        }
        
        response = requests.post(f"{BACKEND_URL}/user-roles", json=role_data)
        self.assertEqual(response.status_code, 200)
        role = response.json()
        self.user_roles["accountant"] = role
        logger.info(f"Created user role: {role['name']} with ID: {role['id']}")
        
        # Create another role
        admin_role_data = {
            "name": "Administrator",
            "description": "Full system access",
            "permissions": [
                self.permissions["accounts_view"]["id"],
                self.permissions["accounts_edit"]["id"],
                self.permissions["transactions_view"]["id"],
                self.permissions["transactions_edit"]["id"]
            ],
            "is_admin": True
        }
        
        response = requests.post(f"{BACKEND_URL}/user-roles", json=admin_role_data)
        self.assertEqual(response.status_code, 200)
        admin_role = response.json()
        self.user_roles["admin"] = admin_role
        logger.info(f"Created admin role: {admin_role['name']} with ID: {admin_role['id']}")
        
        # 4. List user roles
        response = requests.get(f"{BACKEND_URL}/user-roles")
        self.assertEqual(response.status_code, 200)
        roles = response.json()
        self.assertGreaterEqual(len(roles), 2)
        logger.info(f"Retrieved {len(roles)} user roles")
        
        # 5. Get specific role
        response = requests.get(f"{BACKEND_URL}/user-roles/{role['id']}")
        self.assertEqual(response.status_code, 200)
        retrieved_role = response.json()
        self.assertEqual(retrieved_role["id"], role["id"])
        self.assertEqual(retrieved_role["name"], role["name"])
        logger.info(f"Retrieved user role: {retrieved_role['name']}")
        
        # 6. Update role
        # Get the current role first
        response = requests.get(f"{BACKEND_URL}/user-roles/{role['id']}")
        current_role = response.json()
        
        # Update only specific fields
        update_data = current_role.copy()
        update_data["name"] = "Senior Accountant"
        update_data["description"] = "Senior accounting staff with additional permissions"
        update_data["permissions"] = [
            self.permissions["accounts_view"]["id"],
            self.permissions["accounts_edit"]["id"],
            self.permissions["transactions_view"]["id"],
            self.permissions["transactions_edit"]["id"]
        ]
        
        response = requests.put(f"{BACKEND_URL}/user-roles/{role['id']}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_role = response.json()
        self.assertEqual(updated_role["name"], update_data["name"])
        self.assertEqual(updated_role["description"], update_data["description"])
        self.assertEqual(len(updated_role["permissions"]), len(update_data["permissions"]))
        logger.info(f"Updated user role: {updated_role['name']}")
        
        logger.info("Role & Permissions API tests passed")
    
    def test_06_authentication_api(self):
        """Test authentication API endpoints"""
        logger.info("Testing Authentication API...")
        
        # Create a test user if needed
        user_data = {
            "username": "authuser",
            "full_name": "Authentication Test User",
            "email": "authuser@example.com",
            "password": "AuthPassword123!",
            "role": "User"
        }
        
        response = requests.post(f"{BACKEND_URL}/users", json=user_data)
        self.assertEqual(response.status_code, 200)
        auth_user = response.json()
        logger.info(f"Created auth test user: {auth_user['username']} with ID: {auth_user['id']}")
        
        # 1. Login
        login_data = {
            "username": "authuser",
            "password": "AuthPassword123!"
        }
        
        response = requests.post(f"{BACKEND_URL}/auth/login", params=login_data)
        self.assertEqual(response.status_code, 200)
        login_result = response.json()
        self.assertIn("token", login_result)
        self.assertIn("user", login_result)
        token = login_result["token"]
        self.auth_tokens["authuser"] = token
        logger.info(f"User login successful, token received")
        
        # 2. Verify session
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BACKEND_URL}/auth/verify", headers=headers)
        self.assertEqual(response.status_code, 200)
        verify_result = response.json()
        self.assertIn("valid", verify_result)
        self.assertTrue(verify_result["valid"])
        self.assertEqual(verify_result["user"]["username"], "authuser")
        logger.info("Session verification successful")
        
        # Test invalid token
        headers = {"Authorization": "Bearer invalid_token"}
        response = requests.get(f"{BACKEND_URL}/auth/verify", headers=headers)
        self.assertEqual(response.status_code, 401)
        
        # 3. Logout
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BACKEND_URL}/auth/logout", headers=headers)
        self.assertEqual(response.status_code, 200)
        logout_result = response.json()
        self.assertIn("message", logout_result)
        logger.info(f"User logout successful: {logout_result['message']}")
        
        # Verify token is invalidated
        response = requests.get(f"{BACKEND_URL}/auth/verify", headers=headers)
        self.assertEqual(response.status_code, 401)
        
        logger.info("Authentication API tests passed")
    
    def test_07_audit_log_api(self):
        """Test audit log API endpoints"""
        logger.info("Testing Audit Log API...")
        
        # Create a test user for audit logs
        user_data = {
            "username": "audituser",
            "full_name": "Audit Test User",
            "email": "audituser@example.com",
            "password": "AuditPassword123!",
            "role": "User"
        }
        
        response = requests.post(f"{BACKEND_URL}/users", json=user_data)
        self.assertEqual(response.status_code, 200)
        audit_user = response.json()
        logger.info(f"Created audit test user: {audit_user['username']} with ID: {audit_user['id']}")
        
        # 1. Create audit log entry
        audit_data = {
            "user_id": audit_user["id"],
            "action": "create",
            "resource_type": "account",
            "resource_id": str(uuid.uuid4()),
            "old_values": None,
            "new_values": {"name": "Test Account", "account_type": "Asset"},
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0 (Test Browser)"
        }
        
        response = requests.post(f"{BACKEND_URL}/audit-log", json=audit_data)
        self.assertEqual(response.status_code, 200)
        audit_entry = response.json()
        self.audit_logs["create"] = audit_entry
        logger.info(f"Created audit log entry with ID: {audit_entry['id']}")
        
        # Create another audit log entry
        audit_data2 = {
            "user_id": audit_user["id"],
            "action": "update",
            "resource_type": "account",
            "resource_id": audit_data["resource_id"],
            "old_values": {"name": "Test Account"},
            "new_values": {"name": "Updated Test Account"},
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0 (Test Browser)"
        }
        
        response = requests.post(f"{BACKEND_URL}/audit-log", json=audit_data2)
        self.assertEqual(response.status_code, 200)
        audit_entry2 = response.json()
        self.audit_logs["update"] = audit_entry2
        logger.info(f"Created audit log entry with ID: {audit_entry2['id']}")
        
        # 2. List all audit logs
        response = requests.get(f"{BACKEND_URL}/audit-log")
        self.assertEqual(response.status_code, 200)
        audit_logs = response.json()
        self.assertGreaterEqual(len(audit_logs), 2)
        logger.info(f"Retrieved {len(audit_logs)} audit log entries")
        
        # 3. Get resource-specific audit logs
        response = requests.get(f"{BACKEND_URL}/audit-log/account/{audit_data['resource_id']}")
        self.assertEqual(response.status_code, 200)
        resource_logs = response.json()
        self.assertGreaterEqual(len(resource_logs), 2)
        logger.info(f"Retrieved {len(resource_logs)} audit log entries for specific resource")
        
        logger.info("Audit Log API tests passed")
    
    def test_08_setup_api(self):
        """Test setup API endpoints"""
        logger.info("Testing Setup API...")
        
        # 1. Setup default permissions
        response = requests.post(f"{BACKEND_URL}/setup/default-permissions")
        self.assertEqual(response.status_code, 200)
        setup_result = response.json()
        self.assertIn("message", setup_result)
        # The message could be either about creating permissions or that they already exist
        logger.info(f"Setup default permissions: {setup_result['message']}")
        
        # Verify permissions were created
        response = requests.get(f"{BACKEND_URL}/permissions")
        self.assertEqual(response.status_code, 200)
        permissions = response.json()
        self.assertGreaterEqual(len(permissions), 1)  # At least some permissions should exist
        
        logger.info("Setup API tests passed")
    
    def test_09_error_handling(self):
        """Test error handling for API endpoints"""
        logger.info("Testing Error Handling...")
        
        # 1. Test missing resource
        response = requests.get(f"{BACKEND_URL}/form-templates/{str(uuid.uuid4())}")
        self.assertEqual(response.status_code, 404)
        error = response.json()
        self.assertIn("detail", error)
        logger.info("404 error handling works correctly")
        
        # 2. Test invalid data
        invalid_template = {
            "name": "Invalid Template",
            "template_type": "invalid_type",
            "is_default": "not_a_boolean"  # Should be boolean
        }
        
        response = requests.post(f"{BACKEND_URL}/form-templates", json=invalid_template)
        self.assertIn(response.status_code, [400, 422])  # Either is acceptable
        logger.info("Invalid data error handling works correctly")
        
        # 3. Test authentication errors
        headers = {"Authorization": "Bearer invalid_token"}
        response = requests.get(f"{BACKEND_URL}/auth/verify", headers=headers)
        self.assertIn(response.status_code, [401, 422])  # Either is acceptable
        logger.info("Authentication error handling works correctly")
        
        logger.info("Error Handling tests passed")
    
    def test_10_integration_tests(self):
        """Test integration between different API endpoints"""
        logger.info("Testing API Integration...")
        
        # 1. Create user with role and verify permissions
        # First create a role with specific permissions
        permission_data = {
            "name": "reports_view",
            "description": "View reports",
            "module": "reports",
            "actions": ["read"]
        }
        
        response = requests.post(f"{BACKEND_URL}/permissions", json=permission_data)
        self.assertEqual(response.status_code, 200)
        permission = response.json()
        
        role_data = {
            "name": "Report Viewer",
            "description": "User who can only view reports",
            "permissions": [permission["id"]],
            "is_admin": False
        }
        
        response = requests.post(f"{BACKEND_URL}/user-roles", json=role_data)
        self.assertEqual(response.status_code, 200)
        role = response.json()
        
        # Create user with this role
        user_data = {
            "username": "reportuser",
            "full_name": "Report Viewer User",
            "email": "reports@example.com",
            "password": "ReportPassword123!",
            "role": role["name"]
        }
        
        response = requests.post(f"{BACKEND_URL}/users", json=user_data)
        self.assertEqual(response.status_code, 200)
        user = response.json()
        
        # Login as this user
        login_data = {
            "username": "reportuser",
            "password": "ReportPassword123!"
        }
        
        response = requests.post(f"{BACKEND_URL}/auth/login", params=login_data)
        self.assertEqual(response.status_code, 200)
        login_result = response.json()
        token = login_result["token"]
        
        # Create audit log for this user's login
        audit_data = {
            "user_id": user["id"],
            "action": "login",
            "resource_type": "auth",
            "resource_id": user["id"],
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0 (Test Browser)"
        }
        
        response = requests.post(f"{BACKEND_URL}/audit-log", json=audit_data)
        self.assertEqual(response.status_code, 200)
        
        # Verify audit log contains this entry
        response = requests.get(f"{BACKEND_URL}/audit-log/auth/{user['id']}")
        self.assertEqual(response.status_code, 200)
        audit_logs = response.json()
        self.assertGreaterEqual(len(audit_logs), 1)
        
        # Logout
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BACKEND_URL}/auth/logout", headers=headers)
        self.assertEqual(response.status_code, 200)
        
        logger.info("API Integration tests passed")
        
        logger.info("All Phase 4 backend tests completed successfully!")


if __name__ == "__main__":
    unittest.main()