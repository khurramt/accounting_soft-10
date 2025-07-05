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
BACKEND_URL = "https://3358b22c-e36b-4508-a104-1bb982922bba.preview.emergentagent.com/api"

class QBClonePhase4FeaturesTest(unittest.TestCase):
    """Test suite for QBClone Phase 4 Professional Features"""
    
    def setUp(self):
        """Set up test data and clean the database"""
        self.company_id = None
        self.form_templates = {}
        self.custom_fields = {}
        self.permissions = {}
        self.user_roles = {}
        self.audit_logs = {}
        
        # Test the root endpoint to ensure API is accessible
        response = requests.get(f"{BACKEND_URL}/")
        self.assertEqual(response.status_code, 200)
        logger.info("API is accessible")
        
        # Create a test company if needed
        self.create_test_company()
    
    def create_test_company(self):
        """Create a test company for branding tests"""
        company_data = {
            "name": "Phase 4 Test Company",
            "legal_name": "Phase 4 Test Company LLC",
            "address": "456 Professional Ave",
            "city": "Enterprise",
            "state": "CA",
            "zip_code": "90210",
            "country": "United States",
            "phone": "555-987-6543",
            "email": "info@phase4test.com",
            "industry": "professional_services"
        }
        
        response = requests.post(f"{BACKEND_URL}/company", json=company_data)
        self.assertEqual(response.status_code, 200)
        company = response.json()
        self.company_id = company["id"]
        logger.info(f"Created test company with ID: {self.company_id}")
    
    def test_01_form_templates_api(self):
        """Test form templates API endpoints"""
        logger.info("Testing Form Templates API...")
        
        # 1. Create form templates (POST /api/form-templates)
        template_data = [
            {
                "name": "Professional Invoice",
                "template_type": "invoice",
                "is_default": True,
                "header_layout": {"title": "INVOICE", "subtitle": "Professional Services"},
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
                "primary_color": "#4F46E5",
                "secondary_color": "#E0E7FF",
                "font_family": "Montserrat",
                "font_size": "12px"
            },
            {
                "name": "Modern Estimate",
                "template_type": "estimate",
                "is_default": True,
                "header_layout": {"title": "ESTIMATE", "subtitle": ""},
                "show_logo": True,
                "logo_position": "center",
                "primary_color": "#10B981",
                "secondary_color": "#ECFDF5",
                "font_family": "Poppins",
                "font_size": "11px"
            },
            {
                "name": "Compact Receipt",
                "template_type": "receipt",
                "is_default": True,
                "header_layout": {"title": "RECEIPT", "subtitle": ""},
                "show_logo": True,
                "logo_position": "right",
                "primary_color": "#3B82F6",
                "secondary_color": "#DBEAFE",
                "font_family": "Inter",
                "font_size": "10px"
            }
        ]
        
        for template in template_data:
            response = requests.post(f"{BACKEND_URL}/form-templates", json=template)
            self.assertEqual(response.status_code, 200)
            template_obj = response.json()
            self.form_templates[template["name"]] = template_obj
            logger.info(f"Created form template: {template['name']} with ID: {template_obj['id']}")
        
        # 2. List form templates (GET /api/form-templates)
        response = requests.get(f"{BACKEND_URL}/form-templates")
        self.assertEqual(response.status_code, 200)
        templates = response.json()
        self.assertGreaterEqual(len(templates), len(template_data))
        logger.info(f"Retrieved {len(templates)} form templates")
        
        # Filter templates by type
        response = requests.get(f"{BACKEND_URL}/form-templates?template_type=invoice")
        self.assertEqual(response.status_code, 200)
        invoice_templates = response.json()
        self.assertGreaterEqual(len(invoice_templates), 1)
        logger.info(f"Retrieved {len(invoice_templates)} invoice templates")
        
        # 3. Get specific form template (GET /api/form-templates/{id})
        template_id = self.form_templates["Professional Invoice"]["id"]
        response = requests.get(f"{BACKEND_URL}/form-templates/{template_id}")
        self.assertEqual(response.status_code, 200)
        template = response.json()
        self.assertEqual(template["name"], "Professional Invoice")
        self.assertEqual(template["template_type"], "invoice")
        logger.info(f"Retrieved form template: {template['name']}")
        
        # 4. Update form template (PUT /api/form-templates/{id})
        update_data = {
            "name": "Professional Invoice 2.0",
            "template_type": "invoice",
            "is_default": True,
            "header_layout": {"title": "INVOICE", "subtitle": "Premium Services"},
            "show_logo": True,
            "logo_position": "left",
            "primary_color": "#2563EB",
            "secondary_color": "#BFDBFE",
            "font_family": "Roboto",
            "font_size": "12px"
        }
        
        response = requests.put(f"{BACKEND_URL}/form-templates/{template_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_template = response.json()
        self.assertEqual(updated_template["name"], update_data["name"])
        self.assertEqual(updated_template["primary_color"], update_data["primary_color"])
        logger.info(f"Updated form template: {updated_template['name']}")
        
        # 5. Set default template (POST /api/form-templates/{id}/set-default)
        non_default_template_id = self.form_templates["Modern Estimate"]["id"]
        response = requests.post(f"{BACKEND_URL}/form-templates/{non_default_template_id}/set-default")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        logger.info(f"Set template as default: {result['message']}")
        
        # Verify the template is now default
        response = requests.get(f"{BACKEND_URL}/form-templates/{non_default_template_id}")
        self.assertEqual(response.status_code, 200)
        template = response.json()
        self.assertTrue(template["is_default"])
        
        # 6. Delete form template (DELETE /api/form-templates/{id})
        template_to_delete_id = self.form_templates["Compact Receipt"]["id"]
        response = requests.delete(f"{BACKEND_URL}/form-templates/{template_to_delete_id}")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        logger.info(f"Deleted form template: {result['message']}")
        
        # Verify template was deleted
        response = requests.get(f"{BACKEND_URL}/form-templates/{template_to_delete_id}")
        self.assertEqual(response.status_code, 404)
        
        logger.info("Form Templates API tests passed")
    
    def test_02_custom_fields_api(self):
        """Test custom fields API endpoints"""
        logger.info("Testing Custom Fields API...")
        
        # 1. Create custom fields (POST /api/custom-fields)
        field_data = [
            {
                "name": "customer_industry",
                "label": "Industry",
                "field_type": "dropdown",
                "required": False,
                "options": ["Technology", "Healthcare", "Finance", "Education", "Manufacturing", "Retail", "Other"],
                "default_value": "Technology"
            },
            {
                "name": "project_reference",
                "label": "Project Reference",
                "field_type": "text",
                "required": True
            },
            {
                "name": "contract_date",
                "label": "Contract Date",
                "field_type": "date",
                "required": False
            },
            {
                "name": "special_instructions",
                "label": "Special Instructions",
                "field_type": "textarea",
                "required": False
            }
        ]
        
        for field in field_data:
            response = requests.post(f"{BACKEND_URL}/custom-fields", json=field)
            self.assertEqual(response.status_code, 200)
            field_obj = response.json()
            self.custom_fields[field["name"]] = field_obj
            logger.info(f"Created custom field: {field['name']} with ID: {field_obj['id']}")
        
        # 2. List custom fields (GET /api/custom-fields)
        response = requests.get(f"{BACKEND_URL}/custom-fields")
        self.assertEqual(response.status_code, 200)
        fields = response.json()
        self.assertGreaterEqual(len(fields), len(field_data))
        logger.info(f"Retrieved {len(fields)} custom fields")
        
        # 3. Get specific custom field
        field_id = self.custom_fields["customer_industry"]["id"]
        response = requests.get(f"{BACKEND_URL}/custom-fields/{field_id}")
        self.assertEqual(response.status_code, 200)
        field = response.json()
        self.assertEqual(field["name"], "customer_industry")
        self.assertEqual(field["field_type"], "dropdown")
        logger.info(f"Retrieved custom field: {field['name']}")
        
        # 4. Update custom field (PUT /api/custom-fields/{id})
        update_data = {
            "name": "customer_industry",
            "label": "Business Sector",
            "field_type": "dropdown",
            "required": True,
            "options": ["Technology", "Healthcare", "Finance", "Education", "Manufacturing", "Retail", "Hospitality", "Other"],
            "default_value": "Technology"
        }
        
        response = requests.put(f"{BACKEND_URL}/custom-fields/{field_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_field = response.json()
        self.assertEqual(updated_field["label"], update_data["label"])
        self.assertEqual(updated_field["required"], update_data["required"])
        self.assertEqual(len(updated_field["options"]), 8)
        logger.info(f"Updated custom field: {updated_field['name']}")
        
        # 5. Delete custom field (DELETE /api/custom-fields/{id})
        field_to_delete_id = self.custom_fields["special_instructions"]["id"]
        response = requests.delete(f"{BACKEND_URL}/custom-fields/{field_to_delete_id}")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        logger.info(f"Deleted custom field: {result['message']}")
        
        # Verify field was deleted
        response = requests.get(f"{BACKEND_URL}/custom-fields/{field_to_delete_id}")
        self.assertEqual(response.status_code, 404)
        
        logger.info("Custom Fields API tests passed")
    
    def test_03_company_branding_api(self):
        """Test company branding API endpoints"""
        logger.info("Testing Company Branding API...")
        
        # 1. Create company branding (POST /api/company-branding)
        branding_data = {
            "company_id": self.company_id,
            "company_name": "Phase 4 Test Company",
            "tagline": "Professional Accounting Solutions",
            "primary_color": "#4F46E5",
            "secondary_color": "#E0E7FF",
            "font_family": "Montserrat"
        }
        
        response = requests.post(f"{BACKEND_URL}/company-branding", json=branding_data)
        self.assertEqual(response.status_code, 200)
        branding = response.json()
        logger.info(f"Created company branding for company ID: {branding['company_id']}")
        
        # 2. Get company branding (GET /api/company-branding/{company_id})
        response = requests.get(f"{BACKEND_URL}/company-branding/{self.company_id}")
        self.assertEqual(response.status_code, 200)
        retrieved_branding = response.json()
        self.assertEqual(retrieved_branding["company_name"], branding_data["company_name"])
        self.assertEqual(retrieved_branding["tagline"], branding_data["tagline"])
        logger.info(f"Retrieved company branding for: {retrieved_branding['company_name']}")
        
        # 3. Update company branding (POST /api/company-branding)
        update_data = {
            "company_id": self.company_id,
            "company_name": "Phase 4 Test Company",
            "tagline": "Excellence in Financial Solutions",
            "primary_color": "#2563EB",
            "secondary_color": "#BFDBFE",
            "font_family": "Roboto"
        }
        
        response = requests.post(f"{BACKEND_URL}/company-branding", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_branding = response.json()
        self.assertEqual(updated_branding["tagline"], update_data["tagline"])
        self.assertEqual(updated_branding["primary_color"], update_data["primary_color"])
        logger.info(f"Updated company branding for: {updated_branding['company_name']}")
        
        # 4. Upload company logo (POST /api/company-branding/{company_id}/upload-logo)
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
        logger.info(f"Uploaded company logo: {logo_result['message']}")
        
        # Verify logo was uploaded
        response = requests.get(f"{BACKEND_URL}/company-branding/{self.company_id}")
        self.assertEqual(response.status_code, 200)
        branding_with_logo = response.json()
        self.assertIsNotNone(branding_with_logo["logo_base64"])
        self.assertEqual(branding_with_logo["logo_filename"], "company_logo.gif")
        self.assertEqual(branding_with_logo["logo_mime_type"], "image/gif")
        logger.info("Verified logo was uploaded successfully")
        
        logger.info("Company Branding API tests passed")
    
    def test_04_role_permissions_api(self):
        """Test role and permissions API endpoints"""
        logger.info("Testing Role & Permissions API...")
        
        # 1. Create permissions (POST /api/permissions)
        permission_data = [
            {
                "name": "form_templates_read",
                "description": "Read form templates",
                "module": "forms",
                "actions": ["read"]
            },
            {
                "name": "form_templates_write",
                "description": "Create, update, and delete form templates",
                "module": "forms",
                "actions": ["create", "update", "delete"]
            },
            {
                "name": "custom_fields_read",
                "description": "Read custom fields",
                "module": "forms",
                "actions": ["read"]
            },
            {
                "name": "custom_fields_write",
                "description": "Create, update, and delete custom fields",
                "module": "forms",
                "actions": ["create", "update", "delete"]
            },
            {
                "name": "company_branding_read",
                "description": "Read company branding",
                "module": "company",
                "actions": ["read"]
            },
            {
                "name": "company_branding_write",
                "description": "Update company branding",
                "module": "company",
                "actions": ["create", "update"]
            }
        ]
        
        for permission in permission_data:
            response = requests.post(f"{BACKEND_URL}/permissions", json=permission)
            self.assertEqual(response.status_code, 200)
            permission_obj = response.json()
            self.permissions[permission["name"]] = permission_obj
            logger.info(f"Created permission: {permission['name']} with ID: {permission_obj['id']}")
        
        # 2. Get all permissions (GET /api/permissions)
        response = requests.get(f"{BACKEND_URL}/permissions")
        self.assertEqual(response.status_code, 200)
        permissions = response.json()
        self.assertGreaterEqual(len(permissions), len(permission_data))
        logger.info(f"Retrieved {len(permissions)} permissions")
        
        # 3. Create user roles (POST /api/user-roles)
        role_data = [
            {
                "name": "Form Designer",
                "description": "Can design and manage form templates",
                "permissions": [
                    self.permissions["form_templates_read"]["id"],
                    self.permissions["form_templates_write"]["id"],
                    self.permissions["custom_fields_read"]["id"],
                    self.permissions["custom_fields_write"]["id"]
                ],
                "is_admin": False
            },
            {
                "name": "Branding Manager",
                "description": "Can manage company branding",
                "permissions": [
                    self.permissions["company_branding_read"]["id"],
                    self.permissions["company_branding_write"]["id"]
                ],
                "is_admin": False
            },
            {
                "name": "Design Administrator",
                "description": "Has all design and branding permissions",
                "permissions": [p["id"] for p in self.permissions.values()],
                "is_admin": True
            }
        ]
        
        for role in role_data:
            response = requests.post(f"{BACKEND_URL}/user-roles", json=role)
            self.assertEqual(response.status_code, 200)
            role_obj = response.json()
            self.user_roles[role["name"]] = role_obj
            logger.info(f"Created user role: {role['name']} with ID: {role_obj['id']}")
        
        # 4. Get all user roles (GET /api/user-roles)
        response = requests.get(f"{BACKEND_URL}/user-roles")
        self.assertEqual(response.status_code, 200)
        roles = response.json()
        self.assertGreaterEqual(len(roles), len(role_data))
        logger.info(f"Retrieved {len(roles)} user roles")
        
        # 5. Get specific user role (GET /api/user-roles/{id})
        role_id = self.user_roles["Form Designer"]["id"]
        response = requests.get(f"{BACKEND_URL}/user-roles/{role_id}")
        self.assertEqual(response.status_code, 200)
        role = response.json()
        self.assertEqual(role["name"], "Form Designer")
        self.assertEqual(len(role["permissions"]), 4)
        logger.info(f"Retrieved user role: {role['name']}")
        
        # 6. Update user role (PUT /api/user-roles/{id})
        update_data = {
            "name": "Form Designer Plus",
            "description": "Can design and manage form templates with additional permissions",
            "permissions": [
                self.permissions["form_templates_read"]["id"],
                self.permissions["form_templates_write"]["id"],
                self.permissions["custom_fields_read"]["id"],
                self.permissions["custom_fields_write"]["id"],
                self.permissions["company_branding_read"]["id"]
            ],
            "is_admin": False
        }
        
        response = requests.put(f"{BACKEND_URL}/user-roles/{role_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_role = response.json()
        self.assertEqual(updated_role["name"], update_data["name"])
        self.assertEqual(len(updated_role["permissions"]), 5)
        logger.info(f"Updated user role: {updated_role['name']}")
        
        logger.info("Role & Permissions API tests passed")
    
    def test_05_audit_log_api(self):
        """Test audit log API endpoints"""
        logger.info("Testing Audit Log API...")
        
        # Create a test form template for audit logging
        template_data = {
            "name": "Audit Test Template",
            "template_type": "invoice",
            "is_default": False,
            "header_layout": {"title": "INVOICE", "subtitle": "Audit Test"},
            "show_logo": True,
            "logo_position": "left",
            "primary_color": "#3B82F6",
            "secondary_color": "#F3F4F6"
        }
        
        response = requests.post(f"{BACKEND_URL}/form-templates", json=template_data)
        self.assertEqual(response.status_code, 200)
        template = response.json()
        template_id = template["id"]
        logger.info(f"Created test form template for audit logging: {template['name']} with ID: {template_id}")
        
        # Create a test custom field for audit logging
        field_data = {
            "name": "audit_test_field",
            "label": "Audit Test Field",
            "field_type": "text",
            "required": False
        }
        
        response = requests.post(f"{BACKEND_URL}/custom-fields", json=field_data)
        self.assertEqual(response.status_code, 200)
        field = response.json()
        field_id = field["id"]
        logger.info(f"Created test custom field for audit logging: {field['name']} with ID: {field_id}")
        
        # 1. Create audit log entries (POST /api/audit-log)
        audit_log_data = [
            {
                "user_id": str(uuid.uuid4()),
                "action": "create",
                "resource_type": "form_template",
                "resource_id": template_id,
                "new_values": {"name": "Audit Test Template", "template_type": "invoice"},
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0 (Test Browser)"
            },
            {
                "user_id": str(uuid.uuid4()),
                "action": "update",
                "resource_type": "custom_field",
                "resource_id": self.custom_fields["customer_industry"]["id"],
                "old_values": {"label": "Industry"},
                "new_values": {"label": "Business Sector"},
                "ip_address": "192.168.1.101",
                "user_agent": "Chrome/91.0"
            },
            {
                "user_id": str(uuid.uuid4()),
                "action": "create",
                "resource_type": "company_branding",
                "resource_id": self.company_id,
                "new_values": {"company_name": "Phase 4 Test Company", "tagline": "Professional Accounting Solutions"},
                "ip_address": "192.168.1.102",
                "user_agent": "Firefox/89.0"
            }
        ]
        
        for log in audit_log_data:
            response = requests.post(f"{BACKEND_URL}/audit-log", json=log)
            self.assertEqual(response.status_code, 200)
            log_obj = response.json()
            self.audit_logs[f"{log['action']}_{log['resource_type']}"] = log_obj
            logger.info(f"Created audit log entry: {log_obj['id']} for {log['action']} {log['resource_type']}")
        
        # 2. Get all audit logs (GET /api/audit-log)
        response = requests.get(f"{BACKEND_URL}/audit-log")
        self.assertEqual(response.status_code, 200)
        logs = response.json()
        self.assertGreaterEqual(len(logs), len(audit_log_data))
        logger.info(f"Retrieved {len(logs)} audit logs")
        
        # 3. Get audit logs with filtering
        user_id = audit_log_data[0]["user_id"]
        response = requests.get(f"{BACKEND_URL}/audit-log?user_id={user_id}")
        self.assertEqual(response.status_code, 200)
        user_logs = response.json()
        for log in user_logs:
            if log["user_id"] == user_id:
                logger.info(f"Successfully filtered audit logs by user_id: {user_id}")
                break
        
        # 4. Get audit logs for specific resource (GET /api/audit-log/{resource_type}/{resource_id})
        resource_type = audit_log_data[1]["resource_type"]
        resource_id = audit_log_data[1]["resource_id"]
        response = requests.get(f"{BACKEND_URL}/audit-log/{resource_type}/{resource_id}")
        self.assertEqual(response.status_code, 200)
        resource_logs = response.json()
        for log in resource_logs:
            if log["resource_id"] == resource_id and log["resource_type"] == resource_type:
                logger.info(f"Successfully retrieved audit logs for {resource_type} {resource_id}")
                break
        
        logger.info("Audit Log API tests passed")
    
    def test_06_setup_api(self):
        """Test setup API endpoints"""
        logger.info("Testing Setup API...")
        
        # Setup default permissions (POST /api/setup/default-permissions)
        response = requests.post(f"{BACKEND_URL}/setup/default-permissions")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        logger.info(f"Setup default permissions: {result['message']}")
        
        # Verify permissions were created
        response = requests.get(f"{BACKEND_URL}/permissions")
        self.assertEqual(response.status_code, 200)
        permissions = response.json()
        self.assertGreaterEqual(len(permissions), 12)  # At least 12 default permissions
        
        # Verify roles were created
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
        
        logger.info("Setup API tests passed")
    
    def test_07_integration(self):
        """Test integration between different Phase 4 features"""
        logger.info("Testing Phase 4 Feature Integration...")
        
        # 1. Create a custom field for form templates
        custom_field_data = {
            "name": "payment_terms",
            "label": "Payment Terms",
            "field_type": "dropdown",
            "required": True,
            "options": ["Net 15", "Net 30", "Net 45", "Net 60", "Due on Receipt"],
            "default_value": "Net 30"
        }
        
        response = requests.post(f"{BACKEND_URL}/custom-fields", json=custom_field_data)
        self.assertEqual(response.status_code, 200)
        custom_field = response.json()
        logger.info(f"Created custom field for integration test: {custom_field['name']}")
        
        # 2. Create a form template that uses the custom field
        template_data = {
            "name": "Integration Invoice Template",
            "template_type": "invoice",
            "is_default": False,
            "header_layout": {"title": "INVOICE", "subtitle": "Integration Test"},
            "show_logo": True,
            "logo_position": "left",
            "primary_color": "#3B82F6",
            "secondary_color": "#F3F4F6",
            "custom_fields": [custom_field]
        }
        
        response = requests.post(f"{BACKEND_URL}/form-templates", json=template_data)
        self.assertEqual(response.status_code, 200)
        template = response.json()
        logger.info(f"Created form template with custom field: {template['name']}")
        
        # 3. Create a user role with permissions to manage form templates
        # First, get the permissions
        response = requests.get(f"{BACKEND_URL}/permissions")
        self.assertEqual(response.status_code, 200)
        permissions = response.json()
        
        # Find relevant permissions
        form_permissions = []
        for permission in permissions:
            if permission["module"] in ["admin", "forms", "templates"]:
                form_permissions.append(permission["id"])
        
        # Create the role
        role_data = {
            "name": "Form Template Manager",
            "description": "Can manage form templates",
            "permissions": form_permissions,
            "is_admin": False
        }
        
        response = requests.post(f"{BACKEND_URL}/user-roles", json=role_data)
        self.assertEqual(response.status_code, 200)
        role = response.json()
        logger.info(f"Created user role for form template management: {role['name']}")
        
        # 4. Create an audit log entry for the template creation
        audit_data = {
            "user_id": str(uuid.uuid4()),
            "action": "create",
            "resource_type": "form_template",
            "resource_id": template["id"],
            "new_values": template,
            "ip_address": "192.168.1.100",
            "user_agent": "Integration Test"
        }
        
        response = requests.post(f"{BACKEND_URL}/audit-log", json=audit_data)
        self.assertEqual(response.status_code, 200)
        audit_log = response.json()
        logger.info(f"Created audit log entry for template creation: {audit_log['id']}")
        
        # 5. Verify the audit log entry
        response = requests.get(f"{BACKEND_URL}/audit-log/form_template/{template['id']}")
        self.assertEqual(response.status_code, 200)
        logs = response.json()
        self.assertGreaterEqual(len(logs), 1)
        logger.info(f"Retrieved audit logs for the template: {len(logs)} entries")
        
        logger.info("Phase 4 Feature Integration tests passed")

if __name__ == "__main__":
    unittest.main()