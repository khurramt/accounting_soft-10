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

class QBCloneCompanySetupTest(unittest.TestCase):
    """Test suite for QBClone advanced company setup API"""
    
    def setUp(self):
        """Set up test data"""
        # Test the root endpoint to ensure API is accessible
        response = requests.get(f"{BACKEND_URL}/")
        self.assertEqual(response.status_code, 200)
        logger.info("API is accessible")
    
    def test_01_advanced_company_setup(self):
        """Test the enhanced company creation endpoint with advanced setup wizard data"""
        logger.info("Testing Advanced Company Setup...")
        
        # Create comprehensive company data with all advanced setup wizard fields
        company_data = {
            "name": "Advanced Test Company LLC",
            "legal_name": "Advanced Test Company Legal Name LLC",
            "address": "123 Advanced Street",
            "city": "Advanced City",
            "state": "CA",
            "zip_code": "12345",
            "country": "United States",
            "phone": "555-123-4567",
            "email": "info@advancedtestcompany.com",
            "industry": "technology",
            "settings": {
                # Business structure and activity information
                "business_structure": "LLC",
                "business_type": "Service",
                "business_subtype": "Technology Consulting",
                "fiscal_year_end": "12-31",
                "tax_id_ein": "12-3456789",
                "state_of_incorporation": "California",
                "date_of_incorporation": "2023-01-01",
                "website": "https://www.advancedtestcompany.com",
                
                # Business preferences
                "accounting_method": "Accrual",
                "track_inventory": True,
                "track_classes": True,
                "track_locations": True,
                "use_account_numbers": True,
                "has_employees": True,
                "collect_sales_tax": True,
                "multi_currency": False,
                
                # Chart of accounts template
                "chart_of_accounts_template": "Technology_Consulting",
                "default_accounts": {
                    "accounts_receivable": "1200",
                    "accounts_payable": "2100",
                    "sales_income": "4100",
                    "cost_of_goods_sold": "5000",
                    "inventory_asset": "1300",
                    "undeposited_funds": "1050"
                },
                
                # Tax and financial settings
                "tax_form": "1065",
                "tax_agency": "IRS",
                "sales_tax_agency": "California Department of Tax and Fee Administration",
                "sales_tax_rate": 8.25,
                "default_payment_terms": "Net 30",
                "default_markup_percentage": 15,
                
                # User preferences
                "date_format": "MM/DD/YYYY",
                "number_format": "#,###.##",
                "dashboard_layout": "financial_overview",
                "default_view": "accrual",
                "start_page": "dashboard",
                
                # Security settings
                "multi_user": True,
                "audit_trail": True,
                "password_complexity": "high",
                "session_timeout_minutes": 30,
                "two_factor_auth": False
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
        self.assertEqual(company["settings"]["business_structure"], company_data["settings"]["business_structure"])
        self.assertEqual(company["settings"]["accounting_method"], company_data["settings"]["accounting_method"])
        self.assertEqual(company["settings"]["chart_of_accounts_template"], company_data["settings"]["chart_of_accounts_template"])
        self.assertEqual(company["settings"]["tax_form"], company_data["settings"]["tax_form"])
        self.assertEqual(company["settings"]["date_format"], company_data["settings"]["date_format"])
        self.assertEqual(company["settings"]["multi_user"], company_data["settings"]["multi_user"])
        
        # Retrieve the company to verify persistence
        response = requests.get(f"{BACKEND_URL}/company")
        self.assertEqual(response.status_code, 200)
        retrieved_company = response.json()
        
        # Verify all advanced settings were retrieved correctly
        self.assertEqual(retrieved_company["name"], company_data["name"])
        self.assertEqual(retrieved_company["settings"]["business_structure"], company_data["settings"]["business_structure"])
        self.assertEqual(retrieved_company["settings"]["accounting_method"], company_data["settings"]["accounting_method"])
        self.assertEqual(retrieved_company["settings"]["chart_of_accounts_template"], company_data["settings"]["chart_of_accounts_template"])
        self.assertEqual(retrieved_company["settings"]["default_accounts"]["accounts_receivable"], 
                         company_data["settings"]["default_accounts"]["accounts_receivable"])
        self.assertEqual(retrieved_company["settings"]["tax_form"], company_data["settings"]["tax_form"])
        self.assertEqual(retrieved_company["settings"]["date_format"], company_data["settings"]["date_format"])
        self.assertEqual(retrieved_company["settings"]["multi_user"], company_data["settings"]["multi_user"])
        
        logger.info("Advanced Company Setup tests passed")

if __name__ == "__main__":
    unittest.main()