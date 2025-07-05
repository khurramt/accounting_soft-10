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
BACKEND_URL = "https://fdd67b0e-2cf0-4493-90a2-a31cadc00fd0.preview.emergentagent.com/api"

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
        
    def test_07_company_management(self):
        """Test company management endpoints"""
        logger.info("Testing Company Management...")
        
        # Test company creation
        company_data = {
            "name": "Test Company LLC",
            "legal_name": "Test Company Legal Name LLC",
            "address": "123 Test Street",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345",
            "country": "United States",
            "phone": "555-123-4567",
            "email": "info@testcompany.com",
            "industry": "technology"
        }
        
        response = requests.post(f"{BACKEND_URL}/company", json=company_data)
        self.assertEqual(response.status_code, 200)
        company = response.json()
        logger.info(f"Created company: {company['name']} with ID: {company['id']}")
        
        # Test company retrieval
        response = requests.get(f"{BACKEND_URL}/company")
        self.assertEqual(response.status_code, 200)
        retrieved_company = response.json()
        self.assertEqual(retrieved_company["name"], company_data["name"])
        logger.info(f"Retrieved company: {retrieved_company['name']}")
        
        # Test company update
        update_data = company_data.copy()
        update_data["name"] = "Updated Test Company LLC"
        
        response = requests.put(f"{BACKEND_URL}/company/{company['id']}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_company = response.json()
        self.assertEqual(updated_company["name"], update_data["name"])
        logger.info(f"Updated company to: {updated_company['name']}")
        
        logger.info("Company Management tests passed")
    
    def test_08_employee_management(self):
        """Test employee management endpoints"""
        logger.info("Testing Employee Management...")
        
        # Create employees
        employee_data = [
            {
                "name": "Alice Johnson",
                "status": "Active",
                "title": "Software Developer",
                "ssn": "123-45-6789",
                "employee_id": "EMP001",
                "email": "alice@example.com",
                "phone": "555-111-2222",
                "address": "123 Tech Lane",
                "city": "Techville",
                "state": "CA",
                "zip_code": "90210",
                "hire_date": datetime.utcnow().isoformat(),
                "pay_type": "Salary",
                "pay_rate": 85000.0,
                "pay_schedule": "Bi-weekly",
                "vacation_balance": 80.0,
                "sick_balance": 40.0
            },
            {
                "name": "Bob Smith",
                "status": "Active",
                "title": "Sales Manager",
                "employee_id": "EMP002",
                "email": "bob@example.com",
                "phone": "555-333-4444",
                "hire_date": datetime.utcnow().isoformat(),
                "pay_type": "Commission",
                "pay_rate": 50000.0
            }
        ]
        
        employees = {}
        for employee in employee_data:
            response = requests.post(f"{BACKEND_URL}/employees", json=employee)
            self.assertEqual(response.status_code, 200)
            employee_obj = response.json()
            employees[employee["name"]] = employee_obj
            logger.info(f"Created employee: {employee['name']} with ID: {employee_obj['id']}")
        
        # Verify employee listing
        response = requests.get(f"{BACKEND_URL}/employees")
        self.assertEqual(response.status_code, 200)
        employees_list = response.json()
        self.assertGreaterEqual(len(employees_list), len(employee_data))
        logger.info(f"Retrieved {len(employees_list)} employees")
        
        # Verify individual employee retrieval
        for name, employee in employees.items():
            response = requests.get(f"{BACKEND_URL}/employees/{employee['id']}")
            self.assertEqual(response.status_code, 200)
            retrieved_employee = response.json()
            self.assertEqual(retrieved_employee["name"], name)
            logger.info(f"Retrieved employee: {name}")
        
        # Test employee update
        update_data = {
            "name": "Alice Johnson-Updated",
            "title": "Senior Software Developer",
            "pay_rate": 95000.0,
            "status": "Active"
        }
        
        response = requests.put(f"{BACKEND_URL}/employees/{employees['Alice Johnson']['id']}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_employee = response.json()
        self.assertEqual(updated_employee["name"], update_data["name"])
        self.assertEqual(updated_employee["title"], update_data["title"])
        self.assertEqual(updated_employee["pay_rate"], update_data["pay_rate"])
        logger.info(f"Updated employee: {updated_employee['name']}")
        
        logger.info("Employee Management tests passed")
    
    def test_09_item_management(self):
        """Test item management endpoints"""
        logger.info("Testing Item Management...")
        
        # Create items
        item_data = [
            {
                "name": "Laptop Computer",
                "item_number": "IT001",
                "item_type": "Inventory",
                "description": "High-performance laptop",
                "sales_price": 1299.99,
                "cost": 899.99,
                "income_account_id": self.accounts["Sales Revenue"]["id"],
                "expense_account_id": self.accounts["Office Supplies"]["id"],
                "inventory_account_id": self.accounts["Inventory"]["id"],
                "qty_on_hand": 25.0,
                "reorder_point": 5.0
            },
            {
                "name": "Consulting Services",
                "item_number": "SVC001",
                "item_type": "Service",
                "description": "Professional consulting services",
                "sales_price": 150.0,
                "income_account_id": self.accounts["Service Revenue"]["id"]
            }
        ]
        
        items = {}
        for item in item_data:
            response = requests.post(f"{BACKEND_URL}/items", json=item)
            self.assertEqual(response.status_code, 200)
            item_obj = response.json()
            items[item["name"]] = item_obj
            logger.info(f"Created item: {item['name']} with ID: {item_obj['id']}")
        
        # Verify item listing
        response = requests.get(f"{BACKEND_URL}/items")
        self.assertEqual(response.status_code, 200)
        items_list = response.json()
        self.assertGreaterEqual(len(items_list), len(item_data))
        logger.info(f"Retrieved {len(items_list)} items")
        
        # Verify individual item retrieval
        for name, item in items.items():
            response = requests.get(f"{BACKEND_URL}/items/{item['id']}")
            self.assertEqual(response.status_code, 200)
            retrieved_item = response.json()
            self.assertEqual(retrieved_item["name"], name)
            logger.info(f"Retrieved item: {name}")
        
        # Test item update
        update_data = {
            "name": "Laptop Computer Pro",
            "description": "High-performance professional laptop",
            "sales_price": 1499.99,
            "cost": 999.99,
            "qty_on_hand": 30.0,
            "item_type": "Inventory"
        }
        
        response = requests.put(f"{BACKEND_URL}/items/{items['Laptop Computer']['id']}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_item = response.json()
        self.assertEqual(updated_item["name"], update_data["name"])
        self.assertEqual(updated_item["sales_price"], update_data["sales_price"])
        logger.info(f"Updated item: {updated_item['name']}")
        
        logger.info("Item Management tests passed")
    
    def test_10_advanced_transaction_types(self):
        """Test advanced transaction types"""
        logger.info("Testing Advanced Transaction Types...")
        
        # Create a sales receipt transaction
        sales_receipt_data = {
            "transaction_type": "Sales Receipt",
            "customer_id": self.customers["Jane Doe"]["id"],
            "date": datetime.utcnow().isoformat(),
            "line_items": [
                {
                    "description": "Laptop Sale",
                    "quantity": 1,
                    "rate": 1499.99,
                    "amount": 1499.99,
                    "account_id": self.accounts["Sales Revenue"]["id"]
                }
            ],
            "tax_rate": 8.0,
            "payment_method": "Credit Card",
            "deposit_to_account_id": self.accounts["Checking Account"]["id"],
            "memo": "Walk-in sale"
        }
        
        response = requests.post(f"{BACKEND_URL}/transactions", json=sales_receipt_data)
        self.assertEqual(response.status_code, 200)
        sales_receipt = response.json()
        self.transactions["sales_receipt"] = sales_receipt
        logger.info(f"Created sales receipt transaction: {sales_receipt['transaction_number']}")
        
        # Create a check transaction
        check_data = {
            "transaction_type": "Check",
            "vendor_id": self.vendors["Global Services"]["id"],
            "date": datetime.utcnow().isoformat(),
            "line_items": [
                {
                    "description": "Consulting Fee",
                    "quantity": 1,
                    "rate": 2500.0,
                    "amount": 2500.0,
                    "account_id": self.accounts["Office Supplies"]["id"]
                }
            ],
            "payment_method": "Check",
            "deposit_to_account_id": self.accounts["Checking Account"]["id"],
            "memo": "Monthly consulting fee"
        }
        
        response = requests.post(f"{BACKEND_URL}/transactions", json=check_data)
        self.assertEqual(response.status_code, 200)
        check = response.json()
        self.transactions["check"] = check
        logger.info(f"Created check transaction: {check['transaction_number']}")
        
        # Test fund transfer
        transfer_data = {
            "from_account_id": self.accounts["Checking Account"]["id"],
            "to_account_id": self.accounts["Undeposited Funds"]["id"] if "Undeposited Funds" in self.accounts else self.accounts["Checking Account"]["id"],
            "amount": 1000.0,
            "date": datetime.utcnow().isoformat(),
            "memo": "Test fund transfer"
        }
        
        response = requests.post(f"{BACKEND_URL}/transfers", params=transfer_data)
        self.assertEqual(response.status_code, 200)
        transfer = response.json()
        logger.info(f"Created fund transfer: {transfer['transfer_id']}")
        
        # Verify journal entries for these transactions
        response = requests.get(f"{BACKEND_URL}/journal-entries")
        self.assertEqual(response.status_code, 200)
        journal_entries = response.json()
        
        # Find entries related to our new transactions
        sales_receipt_entries = [entry for entry in journal_entries if entry.get("transaction_id") == sales_receipt["id"]]
        check_entries = [entry for entry in journal_entries if entry.get("transaction_id") == check["id"]]
        transfer_entries = [entry for entry in journal_entries if entry.get("transaction_id") == transfer["transfer_id"]]
        
        # Verify proper double-entry bookkeeping
        self.assertGreaterEqual(len(sales_receipt_entries), 2)  # At least 2 entries for sales receipt
        self.assertGreaterEqual(len(check_entries), 2)  # At least 2 entries for check
        self.assertEqual(len(transfer_entries), 2)  # Exactly 2 entries for transfer
        
        logger.info("Advanced Transaction Types tests passed")
    
    def test_11_enhanced_reporting(self):
        """Test enhanced reporting functionality"""
        logger.info("Testing Enhanced Reporting...")
        
        # Test A/R Aging Report
        response = requests.get(f"{BACKEND_URL}/reports/ar-aging")
        self.assertEqual(response.status_code, 200)
        ar_aging = response.json()
        
        self.assertIn("ar_aging", ar_aging)
        logger.info(f"A/R Aging Report retrieved with {len(ar_aging['ar_aging'])} customers")
        
        # Test A/P Aging Report
        response = requests.get(f"{BACKEND_URL}/reports/ap-aging")
        self.assertEqual(response.status_code, 200)
        ap_aging = response.json()
        
        self.assertIn("ap_aging", ap_aging)
        logger.info(f"A/P Aging Report retrieved with {len(ap_aging['ap_aging'])} vendors")
        
        logger.info("Enhanced Reporting tests passed")
    
    def test_12_additional_entities(self):
        """Test additional entity endpoints"""
        logger.info("Testing Additional Entities...")
        
        # Test Class creation and retrieval
        class_data = {"name": "Marketing Department"}
        response = requests.post(f"{BACKEND_URL}/classes", json=class_data)
        self.assertEqual(response.status_code, 200)
        class_obj = response.json()
        logger.info(f"Created class: {class_obj['name']} with ID: {class_obj['id']}")
        
        response = requests.get(f"{BACKEND_URL}/classes")
        self.assertEqual(response.status_code, 200)
        classes = response.json()
        self.assertGreaterEqual(len(classes), 1)
        logger.info(f"Retrieved {len(classes)} classes")
        
        # Test Location creation and retrieval
        location_data = {"name": "Main Office"}
        response = requests.post(f"{BACKEND_URL}/locations", json=location_data)
        self.assertEqual(response.status_code, 200)
        location_obj = response.json()
        logger.info(f"Created location: {location_obj['name']} with ID: {location_obj['id']}")
        
        response = requests.get(f"{BACKEND_URL}/locations")
        self.assertEqual(response.status_code, 200)
        locations = response.json()
        self.assertGreaterEqual(len(locations), 1)
        logger.info(f"Retrieved {len(locations)} locations")
        
        # Test Terms creation and retrieval
        terms_data = {
            "name": "Net 30",
            "days_due": 30,
            "discount_days": 10,
            "discount_percent": 2.0
        }
        response = requests.post(f"{BACKEND_URL}/terms", json=terms_data)
        self.assertEqual(response.status_code, 200)
        terms_obj = response.json()
        logger.info(f"Created terms: {terms_obj['name']} with ID: {terms_obj['id']}")
        
        response = requests.get(f"{BACKEND_URL}/terms")
        self.assertEqual(response.status_code, 200)
        terms_list = response.json()
        self.assertGreaterEqual(len(terms_list), 1)
        logger.info(f"Retrieved {len(terms_list)} terms")
        
        # Test Price Level creation and retrieval
        price_level_data = {
            "name": "Wholesale",
            "adjustment_type": "Percentage",
            "adjustment_value": -15.0
        }
        response = requests.post(f"{BACKEND_URL}/price-levels", json=price_level_data)
        self.assertEqual(response.status_code, 200)
        price_level_obj = response.json()
        logger.info(f"Created price level: {price_level_obj['name']} with ID: {price_level_obj['id']}")
        
        response = requests.get(f"{BACKEND_URL}/price-levels")
        self.assertEqual(response.status_code, 200)
        price_levels = response.json()
        self.assertGreaterEqual(len(price_levels), 1)
        logger.info(f"Retrieved {len(price_levels)} price levels")
        
        # Test ToDo creation and retrieval
        todo_data = {
            "title": "Complete quarterly tax filing",
            "description": "Prepare and submit Q2 tax documents",
            "due_date": (datetime.utcnow() + timedelta(days=15)).isoformat(),
            "priority": "High"
        }
        response = requests.post(f"{BACKEND_URL}/todos", json=todo_data)
        self.assertEqual(response.status_code, 200)
        todo_obj = response.json()
        logger.info(f"Created todo: {todo_obj['title']} with ID: {todo_obj['id']}")
        
        response = requests.get(f"{BACKEND_URL}/todos")
        self.assertEqual(response.status_code, 200)
        todos = response.json()
        self.assertGreaterEqual(len(todos), 1)
        logger.info(f"Retrieved {len(todos)} todos")
        
        # Test Memorized Transaction creation and retrieval
        memorized_transaction_data = {
            "name": "Monthly Rent",
            "transaction_template": {
                "transaction_type": "Check",
                "vendor_id": self.vendors["Acme Supplies"]["id"],
                "line_items": [
                    {
                        "description": "Office Rent",
                        "amount": 2000.0,
                        "account_id": self.accounts["Office Supplies"]["id"]
                    }
                ]
            },
            "frequency": "Monthly",
            "next_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
        }
        response = requests.post(f"{BACKEND_URL}/memorized-transactions", json=memorized_transaction_data)
        self.assertEqual(response.status_code, 200)
        memorized_transaction_obj = response.json()
        logger.info(f"Created memorized transaction: {memorized_transaction_obj['name']} with ID: {memorized_transaction_obj['id']}")
        
        response = requests.get(f"{BACKEND_URL}/memorized-transactions")
        self.assertEqual(response.status_code, 200)
        memorized_transactions = response.json()
        self.assertGreaterEqual(len(memorized_transactions), 1)
        logger.info(f"Retrieved {len(memorized_transactions)} memorized transactions")
        
        logger.info("Additional Entities tests passed")
    
    def test_13_manual_journal_entry(self):
        """Test manual journal entry functionality"""
        logger.info("Testing Manual Journal Entry...")
        
        # Test with balanced entries (debits = credits)
        balanced_entry = {
            "date": datetime.utcnow().isoformat(),
            "reference": "JE-TEST-001",
            "memo": "Test balanced journal entry",
            "entries": [
                {
                    "account_id": self.accounts["Office Supplies"]["id"],
                    "debit": 500.0,
                    "credit": 0.0,
                    "description": "Office supplies purchase"
                },
                {
                    "account_id": self.accounts["Checking Account"]["id"],
                    "debit": 0.0,
                    "credit": 500.0,
                    "description": "Payment for office supplies"
                }
            ]
        }
        
        response = requests.post(f"{BACKEND_URL}/manual-journal-entry", json=balanced_entry)
        self.assertEqual(response.status_code, 200)
        journal_result = response.json()
        self.assertEqual(journal_result["entries_created"], 2)
        self.assertEqual(journal_result["total_debits"], 500.0)
        self.assertEqual(journal_result["total_credits"], 500.0)
        logger.info(f"Created balanced manual journal entry: {journal_result['transaction_number']}")
        
        # Test with unbalanced entries (should return 400 error)
        unbalanced_entry = {
            "date": datetime.utcnow().isoformat(),
            "reference": "JE-TEST-002",
            "memo": "Test unbalanced journal entry",
            "entries": [
                {
                    "account_id": self.accounts["Office Supplies"]["id"],
                    "debit": 750.0,
                    "credit": 0.0,
                    "description": "Office supplies purchase"
                },
                {
                    "account_id": self.accounts["Checking Account"]["id"],
                    "debit": 0.0,
                    "credit": 500.0,
                    "description": "Payment for office supplies"
                }
            ]
        }
        
        response = requests.post(f"{BACKEND_URL}/manual-journal-entry", json=unbalanced_entry)
        self.assertEqual(response.status_code, 400)
        error_result = response.json()
        self.assertIn("Journal entry must be balanced", error_result["detail"])
        logger.info("Correctly rejected unbalanced journal entry")
        
        # Test with single entry (should return 400 error)
        single_entry = {
            "date": datetime.utcnow().isoformat(),
            "reference": "JE-TEST-003",
            "memo": "Test single entry journal",
            "entries": [
                {
                    "account_id": self.accounts["Office Supplies"]["id"],
                    "debit": 500.0,
                    "credit": 0.0,
                    "description": "Office supplies purchase"
                }
            ]
        }
        
        response = requests.post(f"{BACKEND_URL}/manual-journal-entry", json=single_entry)
        self.assertEqual(response.status_code, 400)
        error_result = response.json()
        self.assertIn("Journal entry must have at least 2 entries", error_result["detail"])
        logger.info("Correctly rejected journal entry with only one entry")
        
        # Verify journal entries were created and account balances updated
        response = requests.get(f"{BACKEND_URL}/journal-entries")
        self.assertEqual(response.status_code, 200)
        journal_entries = response.json()
        
        # Find entries related to our manual journal entry
        manual_entries = [entry for entry in journal_entries if entry.get("transaction_id") == journal_result["transaction_id"]]
        self.assertEqual(len(manual_entries), 2)
        
        # Verify account balances were updated
        response = requests.get(f"{BACKEND_URL}/accounts/{self.accounts['Office Supplies']['id']}")
        office_account = response.json()
        self.assertGreaterEqual(office_account["balance"], 500.0)  # Should include our manual entry
        
        logger.info("Manual Journal Entry tests passed")
    
    def test_14_enhanced_transfer_functionality(self):
        """Test enhanced transfer functionality"""
        logger.info("Testing Enhanced Transfer Functionality...")
        
        # Test valid transfer
        valid_transfer = {
            "from_account_id": self.accounts["Checking Account"]["id"],
            "to_account_id": self.accounts["Undeposited Funds"]["id"],
            "amount": 2500.0,
            "transfer_date": datetime.utcnow().isoformat(),
            "reference_number": "TRF-TEST-001",
            "memo": "Test valid transfer"
        }
        
        response = requests.post(f"{BACKEND_URL}/transfers", json=valid_transfer)
        self.assertEqual(response.status_code, 200)
        transfer_result = response.json()
        self.assertIn("transfer_id", transfer_result)
        self.assertIn("transaction_number", transfer_result)
        logger.info(f"Created valid transfer: {transfer_result['transaction_number']}")
        
        # Test transfer to same account (should return 400 error)
        same_account_transfer = {
            "from_account_id": self.accounts["Checking Account"]["id"],
            "to_account_id": self.accounts["Checking Account"]["id"],
            "amount": 1000.0,
            "transfer_date": datetime.utcnow().isoformat(),
            "memo": "Test same account transfer"
        }
        
        response = requests.post(f"{BACKEND_URL}/transfers", json=same_account_transfer)
        self.assertEqual(response.status_code, 400)
        error_result = response.json()
        self.assertIn("Cannot transfer to the same account", error_result["detail"])
        logger.info("Correctly rejected transfer to same account")
        
        # Test transfer with non-existent account (should return 404 error)
        invalid_account_transfer = {
            "from_account_id": self.accounts["Checking Account"]["id"],
            "to_account_id": str(uuid.uuid4()),  # Random non-existent ID
            "amount": 1000.0,
            "transfer_date": datetime.utcnow().isoformat(),
            "memo": "Test invalid account transfer"
        }
        
        response = requests.post(f"{BACKEND_URL}/transfers", json=invalid_account_transfer)
        self.assertEqual(response.status_code, 404)
        error_result = response.json()
        self.assertIn("Destination account not found", error_result["detail"])
        logger.info("Correctly rejected transfer with non-existent account")
        
        # Test transfer with negative amount (should return 400 error)
        negative_amount_transfer = {
            "from_account_id": self.accounts["Checking Account"]["id"],
            "to_account_id": self.accounts["Undeposited Funds"]["id"],
            "amount": -500.0,
            "transfer_date": datetime.utcnow().isoformat(),
            "memo": "Test negative amount transfer"
        }
        
        response = requests.post(f"{BACKEND_URL}/transfers", json=negative_amount_transfer)
        self.assertEqual(response.status_code, 400)
        error_result = response.json()
        self.assertIn("Transfer amount must be positive", error_result["detail"])
        logger.info("Correctly rejected transfer with negative amount")
        
        # Verify journal entries were created and account balances updated
        response = requests.get(f"{BACKEND_URL}/journal-entries")
        self.assertEqual(response.status_code, 200)
        journal_entries = response.json()
        
        # Find entries related to our transfer
        transfer_entries = [entry for entry in journal_entries if entry.get("transaction_id") == transfer_result["transfer_id"]]
        self.assertEqual(len(transfer_entries), 2)
        
        # Verify account balances were updated
        response = requests.get(f"{BACKEND_URL}/accounts/{self.accounts['Checking Account']['id']}")
        checking_account = response.json()
        
        response = requests.get(f"{BACKEND_URL}/accounts/{self.accounts['Undeposited Funds']['id']}")
        undeposited_funds_account = response.json()
        
        logger.info("Enhanced Transfer Functionality tests passed")
    
    def test_15_payment_processing(self):
        """Test payment processing endpoints"""
        logger.info("Testing Payment Processing...")
        
        # Test receive payment
        payment_data = {
            "customer_id": self.customers["John Smith"]["id"],
            "payment_amount": 1000.0,
            "payment_method": "Check",
            "payment_date": datetime.utcnow().isoformat(),
            "deposit_to_account_id": self.accounts["Undeposited Funds"]["id"],
            "invoice_applications": [
                {
                    "invoice_id": self.transactions["invoice"]["id"],
                    "amount": 1000.0
                }
            ],
            "memo": "Payment for invoice"
        }
        
        response = requests.post(f"{BACKEND_URL}/payments/receive", params=payment_data)
        self.assertEqual(response.status_code, 200)
        payment_result = response.json()
        self.assertIn("payment_id", payment_result)
        logger.info(f"Created payment receipt: {payment_result['payment_id']}")
        
        # Test pay bills
        bill_payment_data = {
            "payment_date": datetime.utcnow().isoformat(),
            "payment_account_id": self.accounts["Checking Account"]["id"],
            "payment_method": "Check",
            "bill_payments": [
                {
                    "bill_id": self.transactions["bill"]["id"],
                    "amount": 500.0
                }
            ],
            "memo": "Payment for bill"
        }
        
        response = requests.post(f"{BACKEND_URL}/payments/pay-bills", params=bill_payment_data)
        self.assertEqual(response.status_code, 200)
        bill_payment_result = response.json()
        self.assertIn("payment_id", bill_payment_result)
        logger.info(f"Created bill payment: {bill_payment_result['payment_id']}")
        
        # Test make deposit
        deposit_data = {
            "deposit_date": datetime.utcnow().isoformat(),
            "deposit_to_account_id": self.accounts["Checking Account"]["id"],
            "payment_items": [
                {
                    "payment_id": payment_result["payment_id"],
                    "amount": 1000.0
                }
            ],
            "memo": "Deposit customer payment"
        }
        
        response = requests.post(f"{BACKEND_URL}/deposits", params=deposit_data)
        self.assertEqual(response.status_code, 200)
        deposit_result = response.json()
        self.assertIn("deposit_id", deposit_result)
        logger.info(f"Created deposit: {deposit_result['deposit_id']}")
        
        # Test get open invoices
        response = requests.get(f"{BACKEND_URL}/customers/{self.customers['John Smith']['id']}/open-invoices")
        self.assertEqual(response.status_code, 200)
        open_invoices = response.json()
        logger.info(f"Retrieved {len(open_invoices)} open invoices for customer")
        
        # Test get open bills
        response = requests.get(f"{BACKEND_URL}/vendors/{self.vendors['Acme Supplies']['id']}/open-bills")
        self.assertEqual(response.status_code, 200)
        open_bills = response.json()
        logger.info(f"Retrieved {len(open_bills)} open bills for vendor")
        
        # Test get undeposited payments
        response = requests.get(f"{BACKEND_URL}/payments/undeposited")
        self.assertEqual(response.status_code, 200)
        undeposited_payments = response.json()
        logger.info(f"Retrieved {len(undeposited_payments)} undeposited payments")
        
        logger.info("Payment Processing tests passed")
    
    def test_16_data_integrity(self):
        """Test data integrity and serialization"""
        logger.info("Testing Data Integrity and Serialization...")
        
        # Test GET /api/journal-entries
        response = requests.get(f"{BACKEND_URL}/journal-entries")
        self.assertEqual(response.status_code, 200)
        journal_entries = response.json()
        
        # Verify no MongoDB ObjectId issues
        for entry in journal_entries:
            self.assertNotIn("_id", entry)
            self.assertTrue(isinstance(entry["id"], str))
            self.assertTrue(isinstance(entry["transaction_id"], str))
            self.assertTrue(isinstance(entry["account_id"], str))
        
        logger.info(f"Journal entries serialization verified for {len(journal_entries)} entries")
        
        # Test GET /api/transactions
        response = requests.get(f"{BACKEND_URL}/transactions")
        self.assertEqual(response.status_code, 200)
        transactions = response.json()
        
        # Verify no MongoDB ObjectId issues
        for transaction in transactions:
            self.assertNotIn("_id", transaction)
            self.assertTrue(isinstance(transaction["id"], str))
            if transaction.get("customer_id"):
                self.assertTrue(isinstance(transaction["customer_id"], str))
            if transaction.get("vendor_id"):
                self.assertTrue(isinstance(transaction["vendor_id"], str))
        
        logger.info(f"Transactions serialization verified for {len(transactions)} transactions")
        
        # Test GET /api/accounts
        response = requests.get(f"{BACKEND_URL}/accounts")
        self.assertEqual(response.status_code, 200)
        accounts = response.json()
        
        # Verify no MongoDB ObjectId issues
        for account in accounts:
            self.assertNotIn("_id", account)
            self.assertTrue(isinstance(account["id"], str))
            if account.get("parent_id"):
                self.assertTrue(isinstance(account["parent_id"], str))
        
        logger.info(f"Accounts serialization verified for {len(accounts)} accounts")
        
        logger.info("Data Integrity and Serialization tests passed")
        logger.info("All tests completed successfully!")


    def test_17_banking_and_reconciliation(self):
        """Test banking and reconciliation functionality"""
        logger.info("Testing Banking and Reconciliation...")
        
        # Create a checking account for testing if not already created
        if "Checking Account" not in self.accounts:
            checking_account_data = {
                "name": "Checking Account",
                "account_type": "Asset",
                "detail_type": "Checking",
                "account_number": "1000",
                "opening_balance": 10000.0,
                "opening_balance_date": datetime.utcnow().isoformat()
            }
            response = requests.post(f"{BACKEND_URL}/accounts", json=checking_account_data)
            self.assertEqual(response.status_code, 200)
            self.accounts["Checking Account"] = response.json()
            logger.info(f"Created checking account with ID: {self.accounts['Checking Account']['id']}")
        
        # 1. Test Bank Transactions
        logger.info("Testing Bank Transactions...")
        
        # Create bank transactions
        bank_transaction_data = [
            {
                "account_id": self.accounts["Checking Account"]["id"],
                "date": datetime.utcnow().isoformat(),
                "description": "Deposit from Customer",
                "amount": 1500.0,
                "transaction_type": "Credit",
                "reference_number": "DEP12345"
            },
            {
                "account_id": self.accounts["Checking Account"]["id"],
                "date": datetime.utcnow().isoformat(),
                "description": "Payment to Vendor",
                "amount": -750.0,
                "transaction_type": "Debit",
                "reference_number": "CHK67890",
                "check_number": "1001"
            },
            {
                "account_id": self.accounts["Checking Account"]["id"],
                "date": datetime.utcnow().isoformat(),
                "description": "Monthly Service Fee",
                "amount": -25.0,
                "transaction_type": "Debit"
            }
        ]
        
        bank_transactions = []
        for transaction in bank_transaction_data:
            response = requests.post(f"{BACKEND_URL}/bank-transactions", json=transaction)
            self.assertEqual(response.status_code, 200)
            bank_transaction = response.json()
            bank_transactions.append(bank_transaction)
            logger.info(f"Created bank transaction: {bank_transaction['description']} with ID: {bank_transaction['id']}")
        
        # Get all bank transactions
        response = requests.get(f"{BACKEND_URL}/bank-transactions")
        self.assertEqual(response.status_code, 200)
        all_transactions = response.json()
        self.assertGreaterEqual(len(all_transactions), len(bank_transaction_data))
        logger.info(f"Retrieved {len(all_transactions)} bank transactions")
        
        # Get bank transactions for specific account
        response = requests.get(f"{BACKEND_URL}/bank-transactions?account_id={self.accounts['Checking Account']['id']}")
        self.assertEqual(response.status_code, 200)
        account_transactions = response.json()
        self.assertGreaterEqual(len(account_transactions), len(bank_transaction_data))
        logger.info(f"Retrieved {len(account_transactions)} bank transactions for checking account")
        
        # 2. Test Reconciliation
        logger.info("Testing Reconciliation...")
        
        # Create a reconciliation
        reconciliation_data = {
            "account_id": self.accounts["Checking Account"]["id"],
            "statement_date": datetime.utcnow().isoformat(),
            "statement_ending_balance": 10725.0,  # Opening balance + transactions
            "notes": "Monthly bank statement reconciliation"
        }
        
        response = requests.post(f"{BACKEND_URL}/reconciliations", json=reconciliation_data)
        self.assertEqual(response.status_code, 200)
        reconciliation = response.json()
        logger.info(f"Created reconciliation with ID: {reconciliation['id']}")
        
        # Get all reconciliations
        response = requests.get(f"{BACKEND_URL}/reconciliations")
        self.assertEqual(response.status_code, 200)
        all_reconciliations = response.json()
        self.assertGreaterEqual(len(all_reconciliations), 1)
        logger.info(f"Retrieved {len(all_reconciliations)} reconciliations")
        
        # Get reconciliations for specific account
        response = requests.get(f"{BACKEND_URL}/reconciliations?account_id={self.accounts['Checking Account']['id']}")
        self.assertEqual(response.status_code, 200)
        account_reconciliations = response.json()
        self.assertGreaterEqual(len(account_reconciliations), 1)
        logger.info(f"Retrieved {len(account_reconciliations)} reconciliations for checking account")
        
        # Get specific reconciliation
        response = requests.get(f"{BACKEND_URL}/reconciliations/{reconciliation['id']}")
        self.assertEqual(response.status_code, 200)
        retrieved_reconciliation = response.json()
        self.assertEqual(retrieved_reconciliation["id"], reconciliation["id"])
        logger.info(f"Retrieved reconciliation: {retrieved_reconciliation['id']}")
        
        # Update reconciliation
        update_data = {
            "notes": "Updated reconciliation notes"
        }
        response = requests.put(f"{BACKEND_URL}/reconciliations/{reconciliation['id']}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_reconciliation = response.json()
        self.assertEqual(updated_reconciliation["notes"], update_data["notes"])
        logger.info(f"Updated reconciliation: {updated_reconciliation['id']}")
        
        # Mark transactions as reconciled
        for transaction in bank_transactions:
            response = requests.put(
                f"{BACKEND_URL}/bank-transactions/{transaction['id']}/reconcile",
                params={"reconciliation_id": reconciliation["id"]}
            )
            self.assertEqual(response.status_code, 200)
            logger.info(f"Marked transaction {transaction['id']} as reconciled")
        
        # Complete reconciliation
        response = requests.post(f"{BACKEND_URL}/reconciliations/{reconciliation['id']}/complete")
        self.assertEqual(response.status_code, 200)
        completion_result = response.json()
        self.assertIn("message", completion_result)
        self.assertIn("status", completion_result)
        logger.info(f"Completed reconciliation with status: {completion_result['status']}")
        
        # 3. Test Bank Import
        logger.info("Testing Bank Import...")
        
        # Create sample CSV content
        csv_content = """Date,Description,Amount,Reference,Check Number
2023-05-01,Deposit from Client,1250.00,DEP123,
2023-05-02,Office Supplies,-89.99,POS456,
2023-05-03,Client Payment,750.50,DEP789,
2023-05-04,Utility Bill,-125.75,ACH012,
2023-05-05,Check Payment,-500.00,CHK345,1002
"""
        
        # Create a temporary CSV file
        with open("/tmp/bank_statement.csv", "w") as f:
            f.write(csv_content)
        
        # Test CSV import
        with open("/tmp/bank_statement.csv", "rb") as f:
            files = {"file": ("bank_statement.csv", f, "text/csv")}
            response = requests.post(
                f"{BACKEND_URL}/bank-import/csv/{self.accounts['Checking Account']['id']}",
                files=files
            )
            self.assertEqual(response.status_code, 200)
            csv_import_result = response.json()
            self.assertEqual(csv_import_result["total_transactions"], 5)
            logger.info(f"CSV import preview: {csv_import_result['total_transactions']} transactions")
        
        # Create sample QFX content (simplified)
        qfx_content = """OFXHEADER:100
DATA:OFXSGML
<OFX>
<BANKMSGSRSV1>
<STMTTRNRS>
<STMTRS>
<BANKTRANLIST>
<STMTTRN>
<TRNTYPE>CREDIT
<DTPOSTED>20230601
<TRNAMT>1500.00
<FITID>123456
<NAME>Deposit
<MEMO>Client Deposit
</STMTTRN>
<STMTTRN>
<TRNTYPE>DEBIT
<DTPOSTED>20230602
<TRNAMT>-250.00
<FITID>789012
<NAME>Withdrawal
<MEMO>ATM Withdrawal
</STMTTRN>
<STMTTRN>
<TRNTYPE>DEBIT
<DTPOSTED>20230603
<TRNAMT>-75.50
<CHECKNUM>1003
<FITID>345678
<NAME>Check Payment
<MEMO>Office Supplies
</STMTTRN>
</BANKTRANLIST>
</STMTRS>
</STMTTRNRS>
</BANKMSGSRSV1>
</OFX>"""
        
        # Create a temporary QFX file
        with open("/tmp/bank_statement.qfx", "w") as f:
            f.write(qfx_content)
        
        # Test QFX import
        with open("/tmp/bank_statement.qfx", "rb") as f:
            files = {"file": ("bank_statement.qfx", f, "application/x-ofx")}
            response = requests.post(
                f"{BACKEND_URL}/bank-import/qfx/{self.accounts['Checking Account']['id']}",
                files=files
            )
            self.assertEqual(response.status_code, 200)
            qfx_import_result = response.json()
            self.assertEqual(qfx_import_result["total_transactions"], 3)
            logger.info(f"QFX import preview: {qfx_import_result['total_transactions']} transactions")
        
        # Test import confirmation
        # Use the transactions from the CSV import preview
        if csv_import_result["preview_transactions"]:
            response = requests.post(
                f"{BACKEND_URL}/bank-import/confirm/{self.accounts['Checking Account']['id']}",
                json=csv_import_result["preview_transactions"]
            )
            self.assertEqual(response.status_code, 200)
            confirm_result = response.json()
            self.assertIn("imported_transactions", confirm_result)
            logger.info(f"Confirmed import of {confirm_result['imported_transactions']} transactions")
        
        # 4. Test Reconciliation Reports
        logger.info("Testing Reconciliation Reports...")
        
        response = requests.get(f"{BACKEND_URL}/reports/reconciliation/{self.accounts['Checking Account']['id']}")
        self.assertEqual(response.status_code, 200)
        report = response.json()
        self.assertIn("account", report)
        self.assertIn("reconciliations", report)
        self.assertIn("summary", report)
        logger.info(f"Retrieved reconciliation report with {len(report['reconciliations'])} reconciliations")
        
        logger.info("Banking and Reconciliation tests passed")

    def test_18_enhanced_reports(self):
        """Test enhanced reporting endpoints for Phase 3"""
        logger.info("Testing Enhanced Reports...")
        
        # 1. Test Customer Aging Details
        if "John Smith" in self.customers:
            customer_id = self.customers["John Smith"]["id"]
            response = requests.get(f"{BACKEND_URL}/reports/customer-aging-details/{customer_id}")
            self.assertEqual(response.status_code, 200)
            customer_aging = response.json()
            
            self.assertIn("customer", customer_aging)
            self.assertIn("aging_buckets", customer_aging)
            self.assertIn("summary", customer_aging)
            
            # Verify structure
            self.assertEqual(customer_aging["customer"]["name"], "John Smith")
            self.assertIn("current", customer_aging["aging_buckets"])
            self.assertIn("days_31_60", customer_aging["aging_buckets"])
            self.assertIn("days_61_90", customer_aging["aging_buckets"])
            self.assertIn("over_90", customer_aging["aging_buckets"])
            
            # Verify summary calculations
            self.assertEqual(
                customer_aging["summary"]["total_outstanding"],
                customer_aging["summary"]["current_total"] +
                customer_aging["summary"]["days_31_60_total"] +
                customer_aging["summary"]["days_61_90_total"] +
                customer_aging["summary"]["over_90_total"]
            )
            
            logger.info(f"Customer aging details retrieved with total outstanding: ${customer_aging['summary']['total_outstanding']:.2f}")
        
        # 2. Test Vendor Aging Details
        if "Acme Supplies" in self.vendors:
            vendor_id = self.vendors["Acme Supplies"]["id"]
            response = requests.get(f"{BACKEND_URL}/reports/vendor-aging-details/{vendor_id}")
            self.assertEqual(response.status_code, 200)
            vendor_aging = response.json()
            
            self.assertIn("vendor", vendor_aging)
            self.assertIn("aging_buckets", vendor_aging)
            self.assertIn("summary", vendor_aging)
            
            # Verify structure
            self.assertEqual(vendor_aging["vendor"]["name"], "Acme Supplies")
            self.assertIn("current", vendor_aging["aging_buckets"])
            self.assertIn("days_31_60", vendor_aging["aging_buckets"])
            self.assertIn("days_61_90", vendor_aging["aging_buckets"])
            self.assertIn("over_90", vendor_aging["aging_buckets"])
            
            # Verify summary calculations
            self.assertEqual(
                vendor_aging["summary"]["total_outstanding"],
                vendor_aging["summary"]["current_total"] +
                vendor_aging["summary"]["days_31_60_total"] +
                vendor_aging["summary"]["days_61_90_total"] +
                vendor_aging["summary"]["over_90_total"]
            )
            
            logger.info(f"Vendor aging details retrieved with total outstanding: ${vendor_aging['summary']['total_outstanding']:.2f}")
        
        # 3. Test Cash Flow Projections
        response = requests.get(f"{BACKEND_URL}/reports/cash-flow-projections?months=12")
        self.assertEqual(response.status_code, 200)
        cash_flow = response.json()
        
        self.assertIn("current_cash_position", cash_flow)
        self.assertIn("total_receivables", cash_flow)
        self.assertIn("total_payables", cash_flow)
        self.assertIn("projections", cash_flow)
        
        # Verify projections structure
        self.assertEqual(len(cash_flow["projections"]), 12)  # 12 months
        for projection in cash_flow["projections"]:
            self.assertIn("month", projection)
            self.assertIn("month_name", projection)
            self.assertIn("opening_balance", projection)
            self.assertIn("expected_inflows", projection)
            self.assertIn("projected_inflows", projection)
            self.assertIn("expected_outflows", projection)
            self.assertIn("projected_outflows", projection)
            self.assertIn("net_cash_flow", projection)
            self.assertIn("closing_balance", projection)
        
        logger.info(f"Cash flow projections retrieved for 12 months with current cash position: ${cash_flow['current_cash_position']:.2f}")
        
        # 4. Test Profit & Loss by Class
        # First, ensure we have at least one class
        if not hasattr(self, 'class_id'):
            class_data = {"name": "Test Class"}
            response = requests.post(f"{BACKEND_URL}/classes", json=class_data)
            self.assertEqual(response.status_code, 200)
            self.class_id = response.json()["id"]
        
        response = requests.get(f"{BACKEND_URL}/reports/profit-loss-by-class?start_date=2023-01-01&end_date=2023-12-31")
        self.assertEqual(response.status_code, 200)
        pl_by_class = response.json()
        
        self.assertIn("report_period", pl_by_class)
        self.assertIn("classes", pl_by_class)
        self.assertIn("totals", pl_by_class)
        
        # Verify structure
        self.assertIn("start_date", pl_by_class["report_period"])
        self.assertIn("end_date", pl_by_class["report_period"])
        self.assertIn("total_income", pl_by_class["totals"])
        self.assertIn("total_expenses", pl_by_class["totals"])
        self.assertIn("net_income", pl_by_class["totals"])
        
        # Verify calculations
        self.assertEqual(
            pl_by_class["totals"]["net_income"],
            pl_by_class["totals"]["total_income"] - pl_by_class["totals"]["total_expenses"]
        )
        
        logger.info(f"Profit & Loss by Class report retrieved with net income: ${pl_by_class['totals']['net_income']:.2f}")
        
        # 5. Test Profit & Loss by Location
        # First, ensure we have at least one location
        if not hasattr(self, 'location_id'):
            location_data = {"name": "Test Location"}
            response = requests.post(f"{BACKEND_URL}/locations", json=location_data)
            self.assertEqual(response.status_code, 200)
            self.location_id = response.json()["id"]
        
        response = requests.get(f"{BACKEND_URL}/reports/profit-loss-by-location?start_date=2023-01-01&end_date=2023-12-31")
        self.assertEqual(response.status_code, 200)
        pl_by_location = response.json()
        
        self.assertIn("report_period", pl_by_location)
        self.assertIn("locations", pl_by_location)
        self.assertIn("totals", pl_by_location)
        
        # Verify structure
        self.assertIn("start_date", pl_by_location["report_period"])
        self.assertIn("end_date", pl_by_location["report_period"])
        self.assertIn("total_income", pl_by_location["totals"])
        self.assertIn("total_expenses", pl_by_location["totals"])
        self.assertIn("net_income", pl_by_location["totals"])
        
        # Verify calculations
        self.assertEqual(
            pl_by_location["totals"]["net_income"],
            pl_by_location["totals"]["total_income"] - pl_by_location["totals"]["total_expenses"]
        )
        
        logger.info(f"Profit & Loss by Location report retrieved with net income: ${pl_by_location['totals']['net_income']:.2f}")
        
        logger.info("Enhanced Reports tests passed")
    
    def test_19_dashboard_analytics(self):
        """Test dashboard analytics endpoints for Phase 3"""
        logger.info("Testing Dashboard Analytics...")
        
        # 1. Test Dashboard Metrics
        response = requests.get(f"{BACKEND_URL}/analytics/dashboard-metrics")
        self.assertEqual(response.status_code, 200)
        dashboard = response.json()
        
        self.assertIn("financial_metrics", dashboard)
        self.assertIn("alerts", dashboard)
        self.assertIn("recent_activity", dashboard)
        
        # Verify financial metrics structure
        metrics = dashboard["financial_metrics"]
        self.assertIn("total_cash", metrics)
        self.assertIn("total_ar", metrics)
        self.assertIn("total_ap", metrics)
        self.assertIn("working_capital", metrics)
        self.assertIn("current_month_income", metrics)
        self.assertIn("current_month_expenses", metrics)
        self.assertIn("current_month_profit", metrics)
        
        # Verify calculations
        self.assertEqual(metrics["working_capital"], metrics["total_ar"] - metrics["total_ap"])
        self.assertEqual(metrics["current_month_profit"], metrics["current_month_income"] - metrics["current_month_expenses"])
        
        # Verify alerts structure
        alerts = dashboard["alerts"]
        self.assertIn("overdue_invoices_count", alerts)
        self.assertIn("overdue_amount", alerts)
        self.assertIn("cash_flow_status", alerts)
        
        logger.info(f"Dashboard metrics retrieved with working capital: ${metrics['working_capital']:.2f}")
        
        # 2. Test KPI Trends
        response = requests.get(f"{BACKEND_URL}/analytics/kpi-trends?period=12months")
        self.assertEqual(response.status_code, 200)
        trends = response.json()
        
        self.assertIn("trends", trends)
        self.assertIsInstance(trends["trends"], list)
        
        if trends["trends"]:
            trend = trends["trends"][0]
            self.assertIn("period", trend)
            self.assertIn("income", trend)
            self.assertIn("expenses", trend)
            self.assertIn("profit", trend)
            self.assertIn("transaction_count", trend)
            
            # Verify calculations
            self.assertEqual(trend["profit"], trend["income"] - trend["expenses"])
        
        logger.info(f"KPI trends retrieved with {len(trends['trends'])} periods")
        
        # 3. Test Drill-Down: Income
        response = requests.get(f"{BACKEND_URL}/analytics/drill-down/income?period=current_month")
        self.assertEqual(response.status_code, 200)
        income_drill = response.json()
        
        self.assertIn("metric", income_drill)
        self.assertIn("period", income_drill)
        self.assertIn("total", income_drill)
        self.assertIn("transactions", income_drill)
        
        self.assertEqual(income_drill["metric"], "income")
        
        logger.info(f"Income drill-down retrieved with total: ${income_drill['total']:.2f}")
        
        # 4. Test Drill-Down: Expenses
        response = requests.get(f"{BACKEND_URL}/analytics/drill-down/expenses?period=current_month")
        self.assertEqual(response.status_code, 200)
        expenses_drill = response.json()
        
        self.assertIn("metric", expenses_drill)
        self.assertIn("period", expenses_drill)
        self.assertIn("total", expenses_drill)
        self.assertIn("transactions", expenses_drill)
        
        self.assertEqual(expenses_drill["metric"], "expenses")
        
        logger.info(f"Expenses drill-down retrieved with total: ${expenses_drill['total']:.2f}")
        
        # 5. Test Drill-Down: Overdue Invoices
        response = requests.get(f"{BACKEND_URL}/analytics/drill-down/overdue_invoices")
        self.assertEqual(response.status_code, 200)
        overdue_drill = response.json()
        
        self.assertIn("metric", overdue_drill)
        self.assertIn("period", overdue_drill)
        self.assertIn("total", overdue_drill)
        self.assertIn("count", overdue_drill)
        self.assertIn("invoices", overdue_drill)
        
        self.assertEqual(overdue_drill["metric"], "overdue_invoices")
        
        logger.info(f"Overdue invoices drill-down retrieved with count: {overdue_drill['count']}")
        
        # 6. Test Invalid Metric
        response = requests.get(f"{BACKEND_URL}/analytics/drill-down/invalid_metric")
        self.assertEqual(response.status_code, 400)
        error = response.json()
        self.assertIn("detail", error)
        
        logger.info("Dashboard Analytics tests passed")

if __name__ == "__main__":
    unittest.main()