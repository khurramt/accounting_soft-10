#!/usr/bin/env python3
import requests
import json
import unittest
from datetime import datetime, timedelta
import uuid
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the backend URL from frontend/.env
BACKEND_URL = "https://6857cce4-3dd5-4419-a74f-40e213b028bb.preview.emergentagent.com/api"

class QBCloneAdvancedSetupTest(unittest.TestCase):
    """Test suite for QBClone advanced setup wizard API"""
    
    def setUp(self):
        """Set up test data"""
        # Test the root endpoint to ensure API is accessible
        response = requests.get(f"{BACKEND_URL}/")
        self.assertEqual(response.status_code, 200)
        logger.info("API is accessible")
    
    def test_01_comprehensive_company_setup(self):
        """Test the enhanced company creation endpoint with all advanced setup wizard data"""
        logger.info("Testing Comprehensive Company Setup...")
        
        # Create comprehensive company data with all advanced setup wizard fields
        company_data = {
            # Basic company information
            "name": "Comprehensive Test Company LLC",
            "legal_name": "Comprehensive Test Company Legal Name LLC",
            "address": "123 Comprehensive Street",
            "city": "Comprehensive City",
            "state": "CA",
            "zip_code": "12345",
            "country": "United States",
            "phone": "555-123-4567",
            "fax": "555-765-4321",
            "email": "info@comprehensivetestcompany.com",
            "industry": "technology",
            
            # Advanced setup wizard data in settings
            "settings": {
                # Step 1: Business structure and activity information
                "business_structure": "LLC",
                "business_type": "Service",
                "business_subtype": "Technology Consulting",
                "fiscal_year_end": "12-31",
                "tax_id_ein": "12-3456789",
                "state_of_incorporation": "California",
                "date_of_incorporation": "2023-01-01",
                "website": "https://www.comprehensivetestcompany.com",
                "number_of_employees": 15,
                "annual_revenue": 1500000,
                
                # Step 2: Enhanced company details
                "logo_url": "https://www.comprehensivetestcompany.com/logo.png",
                "company_slogan": "Comprehensive Solutions for Complex Problems",
                "business_description": "We provide comprehensive technology consulting services to small and medium businesses.",
                "primary_contact": {
                    "name": "John Comprehensive",
                    "title": "CEO",
                    "email": "john@comprehensivetestcompany.com",
                    "phone": "555-987-6543"
                },
                "social_media": {
                    "linkedin": "https://www.linkedin.com/company/comprehensive-test-company",
                    "twitter": "https://twitter.com/ComprehensiveTC",
                    "facebook": "https://www.facebook.com/ComprehensiveTestCompany"
                },
                
                # Step 3: Business preferences
                "accounting_method": "Accrual",
                "track_inventory": True,
                "inventory_costing_method": "FIFO",
                "track_classes": True,
                "track_locations": True,
                "use_account_numbers": True,
                "has_employees": True,
                "collect_sales_tax": True,
                "multi_currency": True,
                "base_currency": "USD",
                "fiscal_year_start_month": 1,
                "tax_year_same_as_fiscal": True,
                "enable_budgets": True,
                "enable_purchase_orders": True,
                "enable_sales_orders": True,
                "enable_estimates": True,
                "enable_time_tracking": True,
                "enable_projects": True,
                "enable_1099_tracking": True,
                
                # Step 4: Chart of accounts template selection
                "chart_of_accounts_template": "Technology_Consulting",
                "default_accounts": {
                    "accounts_receivable": "1200",
                    "accounts_payable": "2100",
                    "sales_income": "4100",
                    "cost_of_goods_sold": "5000",
                    "inventory_asset": "1300",
                    "undeposited_funds": "1050",
                    "opening_balance_equity": "3000",
                    "retained_earnings": "3900",
                    "sales_tax_payable": "2200",
                    "payroll_liabilities": "2300",
                    "bank_charges": "6100",
                    "rent_expense": "6200",
                    "utilities_expense": "6300",
                    "office_supplies": "6400",
                    "travel_expense": "6500",
                    "meals_entertainment": "6600",
                    "professional_fees": "6700",
                    "advertising_marketing": "6800",
                    "interest_expense": "7100",
                    "depreciation_expense": "7200",
                    "payroll_expense": "7300"
                },
                "account_customizations": [
                    {
                        "name": "Software Subscriptions",
                        "account_type": "Expense",
                        "detail_type": "Office Expenses",
                        "account_number": "6450"
                    },
                    {
                        "name": "Cloud Services",
                        "account_type": "Expense",
                        "detail_type": "Office Expenses",
                        "account_number": "6460"
                    }
                ],
                
                # Step 5: Tax and financial settings
                "tax_form": "1065",
                "tax_agency": "IRS",
                "sales_tax_agency": "California Department of Tax and Fee Administration",
                "sales_tax_rate": 8.25,
                "default_payment_terms": "Net 30",
                "default_markup_percentage": 15,
                "default_discount_terms": {
                    "days": 10,
                    "percentage": 2.0
                },
                "fiscal_year_lock_date": "2023-12-31",
                "tax_lock_date": "2023-12-31",
                "depreciation_method": "Straight Line",
                "default_invoice_due_days": 30,
                "default_bill_due_days": 15,
                "enable_automatic_tax_calculations": True,
                "enable_automatic_payment_reminders": True,
                "reminder_days_before_due": [1, 3, 7],
                "reminder_days_after_due": [1, 7, 14, 30],
                
                # Step 6: User preferences
                "date_format": "MM/DD/YYYY",
                "number_format": "#,###.##",
                "dashboard_layout": "financial_overview",
                "default_view": "accrual",
                "start_page": "dashboard",
                "theme": {
                    "primary_color": "#3B82F6",
                    "secondary_color": "#F3F4F6",
                    "accent_color": "#10B981",
                    "font_family": "Inter"
                },
                "email_notifications": {
                    "invoices_due": True,
                    "bills_due": True,
                    "low_inventory": True,
                    "bank_feeds": True,
                    "system_updates": True
                },
                "report_preferences": {
                    "show_accounts_with_zero_balance": False,
                    "show_cents": True,
                    "negative_numbers_format": "Parentheses",
                    "default_date_range": "This Month",
                    "include_header": True,
                    "include_footer": True
                },
                
                # Step 7: Security settings
                "multi_user": True,
                "audit_trail": True,
                "password_complexity": "high",
                "session_timeout_minutes": 30,
                "two_factor_auth": True,
                "ip_restrictions": {
                    "enabled": False,
                    "allowed_ips": []
                },
                "data_backup": {
                    "frequency": "Daily",
                    "retention_days": 30,
                    "auto_backup_before_updates": True
                },
                "user_roles": {
                    "admin": {
                        "name": "Administrator",
                        "permissions": "full_access"
                    },
                    "accountant": {
                        "name": "Accountant",
                        "permissions": ["view_reports", "create_transactions", "edit_transactions"]
                    },
                    "bookkeeper": {
                        "name": "Bookkeeper",
                        "permissions": ["create_transactions", "edit_transactions"]
                    },
                    "employee": {
                        "name": "Employee",
                        "permissions": ["view_reports", "create_time_entries"]
                    }
                }
            }
        }
        
        # Create company with advanced setup
        response = requests.post(f"{BACKEND_URL}/company", json=company_data)
        self.assertEqual(response.status_code, 200)
        company = response.json()
        logger.info(f"Created company: {company['name']} with ID: {company['id']}")
        
        # Verify all advanced settings were saved
        self.assertEqual(company["name"], company_data["name"])
        self.assertEqual(company["legal_name"], company_data["legal_name"])
        
        # Verify business structure and activity information
        self.assertEqual(company["settings"]["business_structure"], company_data["settings"]["business_structure"])
        self.assertEqual(company["settings"]["business_type"], company_data["settings"]["business_type"])
        self.assertEqual(company["settings"]["tax_id_ein"], company_data["settings"]["tax_id_ein"])
        self.assertEqual(company["settings"]["state_of_incorporation"], company_data["settings"]["state_of_incorporation"])
        
        # Verify enhanced company details
        self.assertEqual(company["settings"]["logo_url"], company_data["settings"]["logo_url"])
        self.assertEqual(company["settings"]["company_slogan"], company_data["settings"]["company_slogan"])
        self.assertEqual(company["settings"]["primary_contact"]["name"], company_data["settings"]["primary_contact"]["name"])
        
        # Verify business preferences
        self.assertEqual(company["settings"]["accounting_method"], company_data["settings"]["accounting_method"])
        self.assertEqual(company["settings"]["track_inventory"], company_data["settings"]["track_inventory"])
        self.assertEqual(company["settings"]["inventory_costing_method"], company_data["settings"]["inventory_costing_method"])
        self.assertEqual(company["settings"]["enable_budgets"], company_data["settings"]["enable_budgets"])
        
        # Verify chart of accounts template
        self.assertEqual(company["settings"]["chart_of_accounts_template"], company_data["settings"]["chart_of_accounts_template"])
        self.assertEqual(company["settings"]["default_accounts"]["accounts_receivable"], 
                         company_data["settings"]["default_accounts"]["accounts_receivable"])
        self.assertEqual(company["settings"]["default_accounts"]["sales_income"], 
                         company_data["settings"]["default_accounts"]["sales_income"])
        
        # Verify account customizations
        self.assertEqual(company["settings"]["account_customizations"][0]["name"], 
                         company_data["settings"]["account_customizations"][0]["name"])
        self.assertEqual(company["settings"]["account_customizations"][1]["account_number"], 
                         company_data["settings"]["account_customizations"][1]["account_number"])
        
        # Verify tax and financial settings
        self.assertEqual(company["settings"]["tax_form"], company_data["settings"]["tax_form"])
        self.assertEqual(company["settings"]["sales_tax_rate"], company_data["settings"]["sales_tax_rate"])
        self.assertEqual(company["settings"]["default_payment_terms"], company_data["settings"]["default_payment_terms"])
        self.assertEqual(company["settings"]["default_discount_terms"]["percentage"], 
                         company_data["settings"]["default_discount_terms"]["percentage"])
        
        # Verify user preferences
        self.assertEqual(company["settings"]["date_format"], company_data["settings"]["date_format"])
        self.assertEqual(company["settings"]["number_format"], company_data["settings"]["number_format"])
        self.assertEqual(company["settings"]["theme"]["primary_color"], company_data["settings"]["theme"]["primary_color"])
        self.assertEqual(company["settings"]["report_preferences"]["negative_numbers_format"], 
                         company_data["settings"]["report_preferences"]["negative_numbers_format"])
        
        # Verify security settings
        self.assertEqual(company["settings"]["multi_user"], company_data["settings"]["multi_user"])
        self.assertEqual(company["settings"]["audit_trail"], company_data["settings"]["audit_trail"])
        self.assertEqual(company["settings"]["password_complexity"], company_data["settings"]["password_complexity"])
        self.assertEqual(company["settings"]["user_roles"]["admin"]["name"], 
                         company_data["settings"]["user_roles"]["admin"]["name"])
        
        logger.info("Comprehensive Company Setup tests passed")
    
    def test_02_data_types_and_optional_fields(self):
        """Test handling of different data types and optional fields"""
        logger.info("Testing Data Types and Optional Fields...")
        
        # Test with minimal required fields
        minimal_company_data = {
            "name": "Minimal Company"
        }
        
        response = requests.post(f"{BACKEND_URL}/company", json=minimal_company_data)
        self.assertEqual(response.status_code, 200)
        minimal_company = response.json()
        logger.info(f"Created minimal company: {minimal_company['name']} with ID: {minimal_company['id']}")
        
        # Verify default values were applied
        self.assertEqual(minimal_company["name"], "Minimal Company")
        self.assertEqual(minimal_company["country"], "United States")
        self.assertEqual(minimal_company["industry"], "general")
        self.assertEqual(minimal_company["settings"], {})
        
        # Test with various data types
        mixed_data_company = {
            "name": "Mixed Data Types Company",
            "settings": {
                "string_value": "test string",
                "integer_value": 42,
                "float_value": 3.14159,
                "boolean_value": True,
                "null_value": None,
                "array_value": [1, 2, 3, 4, 5],
                "object_value": {
                    "nested_key": "nested value",
                    "nested_array": ["a", "b", "c"]
                },
                "date_value": "2023-07-06T12:00:00Z"
            }
        }
        
        response = requests.post(f"{BACKEND_URL}/company", json=mixed_data_company)
        self.assertEqual(response.status_code, 200)
        mixed_company = response.json()
        logger.info(f"Created mixed data types company: {mixed_company['name']} with ID: {mixed_company['id']}")
        
        # Verify all data types were saved correctly
        self.assertEqual(mixed_company["settings"]["string_value"], "test string")
        self.assertEqual(mixed_company["settings"]["integer_value"], 42)
        self.assertEqual(mixed_company["settings"]["float_value"], 3.14159)
        self.assertEqual(mixed_company["settings"]["boolean_value"], True)
        self.assertEqual(mixed_company["settings"]["null_value"], None)
        self.assertEqual(mixed_company["settings"]["array_value"], [1, 2, 3, 4, 5])
        self.assertEqual(mixed_company["settings"]["object_value"]["nested_key"], "nested value")
        self.assertEqual(mixed_company["settings"]["object_value"]["nested_array"], ["a", "b", "c"])
        self.assertEqual(mixed_company["settings"]["date_value"], "2023-07-06T12:00:00Z")
        
        logger.info("Data Types and Optional Fields tests passed")
    
    def test_03_chart_of_accounts_template_selection(self):
        """Test the chart of accounts template selection functionality"""
        logger.info("Testing Chart of Accounts Template Selection...")
        
        # Create company with different chart of accounts templates
        templates = ["General_Business", "Manufacturing", "Professional_Services", "Retail", "Nonprofit"]
        
        for template in templates:
            company_data = {
                "name": f"{template} Template Company",
                "legal_name": f"{template} Template Company LLC",
                "industry": template.lower().replace("_", ""),
                "settings": {
                    "chart_of_accounts_template": template,
                    "accounting_method": "Accrual",
                    "use_account_numbers": True
                }
            }
            
            response = requests.post(f"{BACKEND_URL}/company", json=company_data)
            self.assertEqual(response.status_code, 200)
            company = response.json()
            logger.info(f"Created company with {template} template: {company['name']} with ID: {company['id']}")
            
            # Verify template was saved
            self.assertEqual(company["settings"]["chart_of_accounts_template"], template)
        
        logger.info("Chart of Accounts Template Selection tests passed")

if __name__ == "__main__":
    unittest.main()