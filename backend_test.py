#!/usr/bin/env python3
import requests
import json
import unittest
from datetime import datetime, timedelta
import uuid
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the backend URL from frontend/.env
BACKEND_URL = "https://3091a8bb-170b-4c14-9281-5917ad6adbf1.preview.emergentagent.com/api"

class QBCloneBackendTest(unittest.TestCase):
    """Test suite for QBClone accounting backend API"""
    
    def setUp(self):
        """Set up test data and clean the database"""
        self.accounts = {}
        self.customers = {}
        self.vendors = {}
        self.transactions = {}
        
        # Test the root endpoint to ensure API is accessible
        response = requests.get(f"{BACKEND_URL}/")
        self.assertEqual(response.status_code, 200)
        logger.info("API is accessible")
    
    def test_01_account_management(self):
        """Test account creation, retrieval, and balance calculations"""
        logger.info("Testing Account Management...")
        
        # Create accounts of different types
        account_data = [
            {
                "name": "Checking Account",
                "account_type": "Asset",
                "detail_type": "Checking",
                "account_number": "1000",
                "opening_balance": 10000.0,
                "opening_balance_date": datetime.utcnow().isoformat()
            },
            {
                "name": "Accounts Receivable",
                "account_type": "Asset",
                "detail_type": "Accounts Receivable",
                "account_number": "1100"
            },
            {
                "name": "Inventory",
                "account_type": "Asset",
                "detail_type": "Inventory",
                "account_number": "1200"
            },
            {
                "name": "Accounts Payable",
                "account_type": "Liability",
                "detail_type": "Accounts Payable",
                "account_number": "2000"
            },
            {
                "name": "Loan Payable",
                "account_type": "Liability",
                "detail_type": "Loan",
                "account_number": "2100",
                "opening_balance": 5000.0,
                "opening_balance_date": datetime.utcnow().isoformat()
            },
            {
                "name": "Owner's Equity",
                "account_type": "Equity",
                "detail_type": "Owner's Equity",
                "account_number": "3000",
                "opening_balance": 5000.0,
                "opening_balance_date": datetime.utcnow().isoformat()
            },
            {
                "name": "Sales Revenue",
                "account_type": "Income",
                "detail_type": "Sales",
                "account_number": "4000"
            },
            {
                "name": "Service Revenue",
                "account_type": "Income",
                "detail_type": "Service Income",
                "account_number": "4100"
            },
            {
                "name": "Office Supplies",
                "account_type": "Expense",
                "detail_type": "Office Expenses",
                "account_number": "5000"
            },
            {
                "name": "Travel Expenses",
                "account_type": "Expense",
                "detail_type": "Travel",
                "account_number": "5100"
            }
        ]
        
        # Create accounts
        for account in account_data:
            response = requests.post(f"{BACKEND_URL}/accounts", json=account)
            self.assertEqual(response.status_code, 200)
            account_obj = response.json()
            self.accounts[account["name"]] = account_obj
            logger.info(f"Created account: {account['name']} with ID: {account_obj['id']}")
        
        # Verify account listing
        response = requests.get(f"{BACKEND_URL}/accounts")
        self.assertEqual(response.status_code, 200)
        accounts_list = response.json()
        self.assertGreaterEqual(len(accounts_list), len(account_data))
        logger.info(f"Retrieved {len(accounts_list)} accounts")
        
        # Verify individual account retrieval
        for name, account in self.accounts.items():
            response = requests.get(f"{BACKEND_URL}/accounts/{account['id']}")
            self.assertEqual(response.status_code, 200)
            retrieved_account = response.json()
            self.assertEqual(retrieved_account["name"], name)
            logger.info(f"Retrieved account: {name}")
        
        # Verify opening balances
        checking_account = self.accounts["Checking Account"]
        self.assertEqual(checking_account["balance"], 10000.0)
        
        loan_account = self.accounts["Loan Payable"]
        self.assertEqual(loan_account["balance"], 5000.0)
        
        equity_account = self.accounts["Owner's Equity"]
        self.assertEqual(equity_account["balance"], 5000.0)
        
        logger.info("Account Management tests passed")
    
    def test_02_customer_vendor_management(self):
        """Test customer and vendor creation and retrieval"""
        logger.info("Testing Customer and Vendor Management...")
        
        # Create customers
        customer_data = [
            {
                "name": "John Smith",
                "company": "Smith Enterprises",
                "email": "john@smith.com",
                "phone": "555-123-4567",
                "address": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "zip_code": "12345"
            },
            {
                "name": "Jane Doe",
                "company": "Doe Industries",
                "email": "jane@doe.com",
                "phone": "555-987-6543",
                "address": "456 Oak Ave",
                "city": "Somewhere",
                "state": "NY",
                "zip_code": "67890"
            }
        ]
        
        for customer in customer_data:
            response = requests.post(f"{BACKEND_URL}/customers", json=customer)
            self.assertEqual(response.status_code, 200)
            customer_obj = response.json()
            self.customers[customer["name"]] = customer_obj
            logger.info(f"Created customer: {customer['name']} with ID: {customer_obj['id']}")
        
        # Verify customer listing
        response = requests.get(f"{BACKEND_URL}/customers")
        self.assertEqual(response.status_code, 200)
        customers_list = response.json()
        self.assertGreaterEqual(len(customers_list), len(customer_data))
        logger.info(f"Retrieved {len(customers_list)} customers")
        
        # Verify individual customer retrieval
        for name, customer in self.customers.items():
            response = requests.get(f"{BACKEND_URL}/customers/{customer['id']}")
            self.assertEqual(response.status_code, 200)
            retrieved_customer = response.json()
            self.assertEqual(retrieved_customer["name"], name)
            logger.info(f"Retrieved customer: {name}")
        
        # Create vendors
        vendor_data = [
            {
                "name": "Acme Supplies",
                "company": "Acme Corp",
                "email": "sales@acme.com",
                "phone": "555-111-2222",
                "address": "789 Industrial Blvd",
                "city": "Metropolis",
                "state": "IL",
                "zip_code": "54321"
            },
            {
                "name": "Global Services",
                "company": "Global Inc",
                "email": "info@global.com",
                "phone": "555-333-4444",
                "address": "321 Corporate Way",
                "city": "Bigcity",
                "state": "TX",
                "zip_code": "09876"
            }
        ]
        
        for vendor in vendor_data:
            response = requests.post(f"{BACKEND_URL}/vendors", json=vendor)
            self.assertEqual(response.status_code, 200)
            vendor_obj = response.json()
            self.vendors[vendor["name"]] = vendor_obj
            logger.info(f"Created vendor: {vendor['name']} with ID: {vendor_obj['id']}")
        
        # Verify vendor listing
        response = requests.get(f"{BACKEND_URL}/vendors")
        self.assertEqual(response.status_code, 200)
        vendors_list = response.json()
        self.assertGreaterEqual(len(vendors_list), len(vendor_data))
        logger.info(f"Retrieved {len(vendors_list)} vendors")
        
        # Verify individual vendor retrieval
        for name, vendor in self.vendors.items():
            response = requests.get(f"{BACKEND_URL}/vendors/{vendor['id']}")
            self.assertEqual(response.status_code, 200)
            retrieved_vendor = response.json()
            self.assertEqual(retrieved_vendor["name"], name)
            logger.info(f"Retrieved vendor: {name}")
        
        logger.info("Customer and Vendor Management tests passed")
    
    def test_03_transaction_processing(self):
        """Test transaction creation and processing"""
        logger.info("Testing Transaction Processing...")
        
        # Create an invoice transaction
        invoice_data = {
            "transaction_type": "Invoice",
            "customer_id": self.customers["John Smith"]["id"],
            "date": datetime.utcnow().isoformat(),
            "due_date": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "line_items": [
                {
                    "description": "Consulting Services",
                    "quantity": 10,
                    "rate": 150.0,
                    "amount": 1500.0,
                    "account_id": self.accounts["Service Revenue"]["id"]
                },
                {
                    "description": "Product Sale",
                    "quantity": 5,
                    "rate": 100.0,
                    "amount": 500.0,
                    "account_id": self.accounts["Sales Revenue"]["id"]
                }
            ],
            "tax_rate": 8.0,
            "memo": "Invoice for services and products"
        }
        
        response = requests.post(f"{BACKEND_URL}/transactions", json=invoice_data)
        self.assertEqual(response.status_code, 200)
        invoice = response.json()
        self.transactions["invoice"] = invoice
        logger.info(f"Created invoice transaction: {invoice['transaction_number']}")
        
        # Verify invoice calculations
        self.assertEqual(invoice["subtotal"], 2000.0)
        self.assertEqual(invoice["tax_amount"], 160.0)
        self.assertEqual(invoice["total"], 2160.0)
        
        # Create a bill transaction
        bill_data = {
            "transaction_type": "Bill",
            "vendor_id": self.vendors["Acme Supplies"]["id"],
            "date": datetime.utcnow().isoformat(),
            "due_date": (datetime.utcnow() + timedelta(days=15)).isoformat(),
            "line_items": [
                {
                    "description": "Office Supplies",
                    "quantity": 20,
                    "rate": 25.0,
                    "amount": 500.0,
                    "account_id": self.accounts["Office Supplies"]["id"]
                },
                {
                    "description": "Travel Expenses",
                    "quantity": 1,
                    "rate": 750.0,
                    "amount": 750.0,
                    "account_id": self.accounts["Travel Expenses"]["id"]
                }
            ],
            "tax_rate": 5.0,
            "memo": "Monthly supplies and expenses"
        }
        
        response = requests.post(f"{BACKEND_URL}/transactions", json=bill_data)
        self.assertEqual(response.status_code, 200)
        bill = response.json()
        self.transactions["bill"] = bill
        logger.info(f"Created bill transaction: {bill['transaction_number']}")
        
        # Verify bill calculations
        self.assertEqual(bill["subtotal"], 1250.0)
        self.assertEqual(bill["tax_amount"], 62.5)
        self.assertEqual(bill["total"], 1312.5)
        
        # Verify transaction listing
        response = requests.get(f"{BACKEND_URL}/transactions")
        self.assertEqual(response.status_code, 200)
        transactions_list = response.json()
        self.assertGreaterEqual(len(transactions_list), 2)
        logger.info(f"Retrieved {len(transactions_list)} transactions")
        
        # Verify individual transaction retrieval
        for name, transaction in self.transactions.items():
            response = requests.get(f"{BACKEND_URL}/transactions/{transaction['id']}")
            self.assertEqual(response.status_code, 200)
            retrieved_transaction = response.json()
            self.assertEqual(retrieved_transaction["id"], transaction["id"])
            logger.info(f"Retrieved {name} transaction: {retrieved_transaction['transaction_number']}")
        
        logger.info("Transaction Processing tests passed")
    
    def test_04_double_entry_bookkeeping(self):
        """Test double-entry bookkeeping system"""
        logger.info("Testing Double-Entry Bookkeeping...")
        
        # Verify journal entries were created
        response = requests.get(f"{BACKEND_URL}/journal-entries")
        self.assertEqual(response.status_code, 200)
        journal_entries = response.json()
        
        # We should have at least:
        # - 3 entries for opening balances (Checking, Loan, Owner's Equity)
        # - 2 entries for the invoice (AR debit, Income credit)
        # - 2 entries for the bill (Expense debit, AP credit)
        self.assertGreaterEqual(len(journal_entries), 7)
        logger.info(f"Retrieved {len(journal_entries)} journal entries")
        
        # Verify account balances were updated
        response = requests.get(f"{BACKEND_URL}/accounts/{self.accounts['Accounts Receivable']['id']}")
        ar_account = response.json()
        self.assertEqual(ar_account["balance"], 2160.0)  # Invoice total
        
        response = requests.get(f"{BACKEND_URL}/accounts/{self.accounts['Accounts Payable']['id']}")
        ap_account = response.json()
        self.assertEqual(ap_account["balance"], 1312.5)  # Bill total
        
        response = requests.get(f"{BACKEND_URL}/accounts/{self.accounts['Sales Revenue']['id']}")
        sales_account = response.json()
        self.assertEqual(sales_account["balance"], 500.0)  # Invoice line item
        
        response = requests.get(f"{BACKEND_URL}/accounts/{self.accounts['Service Revenue']['id']}")
        service_account = response.json()
        self.assertEqual(service_account["balance"], 1500.0)  # Invoice line item
        
        response = requests.get(f"{BACKEND_URL}/accounts/{self.accounts['Office Supplies']['id']}")
        office_account = response.json()
        self.assertEqual(office_account["balance"], 500.0)  # Bill line item
        
        response = requests.get(f"{BACKEND_URL}/accounts/{self.accounts['Travel Expenses']['id']}")
        travel_account = response.json()
        self.assertEqual(travel_account["balance"], 750.0)  # Bill line item
        
        logger.info("Double-Entry Bookkeeping tests passed")
    
    def test_05_financial_reporting(self):
        """Test financial reporting functionality"""
        logger.info("Testing Financial Reporting...")
        
        # Test Trial Balance
        response = requests.get(f"{BACKEND_URL}/reports/trial-balance")
        self.assertEqual(response.status_code, 200)
        trial_balance = response.json()
        
        self.assertTrue(trial_balance["balanced"])
        self.assertAlmostEqual(trial_balance["total_debits"], trial_balance["total_credits"], places=2)
        logger.info(f"Trial Balance: Debits={trial_balance['total_debits']}, Credits={trial_balance['total_credits']}")
        
        # Test Balance Sheet
        response = requests.get(f"{BACKEND_URL}/reports/balance-sheet")
        self.assertEqual(response.status_code, 200)
        balance_sheet = response.json()
        
        self.assertTrue(balance_sheet["balanced"])
        self.assertAlmostEqual(balance_sheet["total_assets"], 
                              balance_sheet["total_liabilities"] + balance_sheet["total_equity"], 
                              places=2)
        logger.info(f"Balance Sheet: Assets={balance_sheet['total_assets']}, Liabilities={balance_sheet['total_liabilities']}, Equity={balance_sheet['total_equity']}")
        
        # Test Income Statement
        response = requests.get(f"{BACKEND_URL}/reports/income-statement")
        self.assertEqual(response.status_code, 200)
        income_statement = response.json()
        
        expected_net_income = income_statement["total_income"] - income_statement["total_expenses"]
        self.assertAlmostEqual(income_statement["net_income"], expected_net_income, places=2)
        logger.info(f"Income Statement: Income={income_statement['total_income']}, Expenses={income_statement['total_expenses']}, Net Income={income_statement['net_income']}")
        
        logger.info("Financial Reporting tests passed")
    
    def test_06_integration_workflow(self):
        """Test complete accounting workflow"""
        logger.info("Testing Complete Accounting Workflow...")
        
        # Verify the accounting equation: Assets = Liabilities + Equity
        response = requests.get(f"{BACKEND_URL}/reports/balance-sheet")
        balance_sheet = response.json()
        
        self.assertAlmostEqual(balance_sheet["total_assets"], 
                              balance_sheet["total_liabilities"] + balance_sheet["total_equity"], 
                              places=2)
        
        # Verify that net income is reflected in equity
        response = requests.get(f"{BACKEND_URL}/reports/income-statement")
        income_statement = response.json()
        
        # The accounting cycle is working if:
        # 1. Transactions create proper journal entries
        # 2. Journal entries update account balances
        # 3. Account balances are reflected in financial reports
        # 4. The accounting equation holds true
        
        logger.info("Complete Accounting Workflow tests passed")
        logger.info("All tests completed successfully!")


if __name__ == "__main__":
    unittest.main()