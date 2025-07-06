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

class QBCloneAdvancedPaymentTest(unittest.TestCase):
    """Test suite for QBClone advanced payment processing endpoints"""
    
    def setUp(self):
        """Set up test data and clean the database"""
        self.accounts = {}
        self.customers = {}
        self.vendors = {}
        self.transactions = {}
        self.payments = {}
        
        # Test the root endpoint to ensure API is accessible
        response = requests.get(f"{BACKEND_URL}/")
        self.assertEqual(response.status_code, 200)
        logger.info("API is accessible")
        
        # Create necessary accounts
        self.create_accounts()
        
        # Create customers and vendors
        self.create_customers_vendors()
        
        # Create initial transactions (invoices and bills)
        self.create_initial_transactions()
    
    def create_accounts(self):
        """Create necessary accounts for testing"""
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
                "name": "Undeposited Funds",
                "account_type": "Asset",
                "detail_type": "Undeposited Funds",
                "account_number": "1300"
            },
            {
                "name": "Accounts Payable",
                "account_type": "Liability",
                "detail_type": "Accounts Payable",
                "account_number": "2000"
            },
            {
                "name": "Sales Revenue",
                "account_type": "Income",
                "detail_type": "Sales",
                "account_number": "4000"
            },
            {
                "name": "Office Supplies",
                "account_type": "Expense",
                "detail_type": "Office Expenses",
                "account_number": "5000"
            }
        ]
        
        for account in account_data:
            response = requests.post(f"{BACKEND_URL}/accounts", json=account)
            self.assertEqual(response.status_code, 200)
            account_obj = response.json()
            self.accounts[account["name"]] = account_obj
            logger.info(f"Created account: {account['name']} with ID: {account_obj['id']}")
    
    def create_customers_vendors(self):
        """Create test customers and vendors"""
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
    
    def create_initial_transactions(self):
        """Create initial invoices and bills for testing payments"""
        # Create invoices for customers
        invoice_data = [
            {
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
                        "account_id": self.accounts["Sales Revenue"]["id"]
                    }
                ],
                "tax_rate": 8.0,
                "memo": "Invoice for consulting services"
            },
            {
                "transaction_type": "Invoice",
                "customer_id": self.customers["Jane Doe"]["id"],
                "date": datetime.utcnow().isoformat(),
                "due_date": (datetime.utcnow() + timedelta(days=30)).isoformat(),
                "line_items": [
                    {
                        "description": "Product Sale",
                        "quantity": 5,
                        "rate": 200.0,
                        "amount": 1000.0,
                        "account_id": self.accounts["Sales Revenue"]["id"]
                    }
                ],
                "tax_rate": 8.0,
                "memo": "Invoice for product sale"
            }
        ]
        
        for i, invoice in enumerate(invoice_data):
            response = requests.post(f"{BACKEND_URL}/transactions", json=invoice)
            self.assertEqual(response.status_code, 200)
            invoice_obj = response.json()
            self.transactions[f"invoice_{i+1}"] = invoice_obj
            logger.info(f"Created invoice: {invoice_obj['transaction_number']} with ID: {invoice_obj['id']}")
        
        # Create bills for vendors
        bill_data = [
            {
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
                    }
                ],
                "tax_rate": 5.0,
                "memo": "Bill for office supplies"
            },
            {
                "transaction_type": "Bill",
                "vendor_id": self.vendors["Global Services"]["id"],
                "date": datetime.utcnow().isoformat(),
                "due_date": (datetime.utcnow() + timedelta(days=15)).isoformat(),
                "line_items": [
                    {
                        "description": "Consulting Fee",
                        "quantity": 1,
                        "rate": 750.0,
                        "amount": 750.0,
                        "account_id": self.accounts["Office Supplies"]["id"]
                    }
                ],
                "tax_rate": 5.0,
                "memo": "Bill for consulting services"
            }
        ]
        
        for i, bill in enumerate(bill_data):
            response = requests.post(f"{BACKEND_URL}/transactions", json=bill)
            self.assertEqual(response.status_code, 200)
            bill_obj = response.json()
            self.transactions[f"bill_{i+1}"] = bill_obj
            logger.info(f"Created bill: {bill_obj['transaction_number']} with ID: {bill_obj['id']}")
    
    def test_01_open_invoices_endpoint(self):
        """Test the open invoices endpoint"""
        logger.info("Testing Open Invoices Endpoint...")
        
        # Get open invoices for John Smith
        customer_id = self.customers["John Smith"]["id"]
        response = requests.get(f"{BACKEND_URL}/customers/{customer_id}/open-invoices")
        self.assertEqual(response.status_code, 200)
        open_invoices = response.json()
        
        # Verify we have at least one open invoice
        self.assertGreaterEqual(len(open_invoices), 1)
        
        # Verify invoice details
        for invoice in open_invoices:
            self.assertEqual(invoice["customer_id"], customer_id)
            self.assertEqual(invoice["transaction_type"], "Invoice")
            self.assertIn(invoice["status"], ["Open", "Partial"])
            self.assertTrue("balance" in invoice)
            
        logger.info(f"Found {len(open_invoices)} open invoices for customer John Smith")
        
        # Get open invoices for Jane Doe
        customer_id = self.customers["Jane Doe"]["id"]
        response = requests.get(f"{BACKEND_URL}/customers/{customer_id}/open-invoices")
        self.assertEqual(response.status_code, 200)
        open_invoices = response.json()
        
        # Verify we have at least one open invoice
        self.assertGreaterEqual(len(open_invoices), 1)
        
        logger.info(f"Found {len(open_invoices)} open invoices for customer Jane Doe")
        logger.info("Open Invoices Endpoint test passed")
    
    def test_02_open_bills_endpoint(self):
        """Test the open bills endpoint"""
        logger.info("Testing Open Bills Endpoint...")
        
        # Get open bills for Acme Supplies
        vendor_id = self.vendors["Acme Supplies"]["id"]
        response = requests.get(f"{BACKEND_URL}/vendors/{vendor_id}/open-bills")
        self.assertEqual(response.status_code, 200)
        open_bills = response.json()
        
        # Verify we have at least one open bill
        self.assertGreaterEqual(len(open_bills), 1)
        
        # Verify bill details
        for bill in open_bills:
            self.assertEqual(bill["vendor_id"], vendor_id)
            self.assertEqual(bill["transaction_type"], "Bill")
            self.assertIn(bill["status"], ["Open", "Partial"])
            self.assertTrue("balance" in bill)
            
        logger.info(f"Found {len(open_bills)} open bills for vendor Acme Supplies")
        
        # Get open bills for Global Services
        vendor_id = self.vendors["Global Services"]["id"]
        response = requests.get(f"{BACKEND_URL}/vendors/{vendor_id}/open-bills")
        self.assertEqual(response.status_code, 200)
        open_bills = response.json()
        
        # Verify we have at least one open bill
        self.assertGreaterEqual(len(open_bills), 1)
        
        logger.info(f"Found {len(open_bills)} open bills for vendor Global Services")
        logger.info("Open Bills Endpoint test passed")
    
    def test_03_receive_payment(self):
        """Test receiving payment from customer and applying to invoices"""
        logger.info("Testing Receive Payment Endpoint...")
        
        # Get customer's open invoices
        customer_id = self.customers["John Smith"]["id"]
        response = requests.get(f"{BACKEND_URL}/customers/{customer_id}/open-invoices")
        self.assertEqual(response.status_code, 200)
        open_invoices = response.json()
        
        # Verify we have at least one open invoice
        self.assertGreaterEqual(len(open_invoices), 1)
        
        # Get customer's initial balance
        response = requests.get(f"{BACKEND_URL}/customers/{customer_id}")
        self.assertEqual(response.status_code, 200)
        customer_before = response.json()
        initial_balance = customer_before["balance"]
        
        # Get initial AR account balance
        ar_account_id = self.accounts["Accounts Receivable"]["id"]
        response = requests.get(f"{BACKEND_URL}/accounts/{ar_account_id}")
        self.assertEqual(response.status_code, 200)
        ar_account_before = response.json()
        ar_initial_balance = ar_account_before["balance"]
        
        # Get initial Undeposited Funds account balance
        uf_account_id = self.accounts["Undeposited Funds"]["id"]
        response = requests.get(f"{BACKEND_URL}/accounts/{uf_account_id}")
        self.assertEqual(response.status_code, 200)
        uf_account_before = response.json()
        uf_initial_balance = uf_account_before["balance"]
        
        # Create payment data
        invoice_to_pay = open_invoices[0]
        payment_amount = invoice_to_pay["total"]
        
        payment_data = {
            "customer_id": customer_id,
            "payment_amount": payment_amount,
            "payment_method": "Check",
            "payment_date": datetime.utcnow().isoformat(),
            "deposit_to_account_id": uf_account_id,
            "invoice_applications": [
                {
                    "invoice_id": invoice_to_pay["id"],
                    "amount": payment_amount
                }
            ],
            "memo": "Payment for consulting services"
        }
        
        # Submit payment - convert to query parameters
        query_params = {
            "customer_id": payment_data["customer_id"],
            "payment_amount": payment_data["payment_amount"],
            "payment_method": payment_data["payment_method"],
            "payment_date": payment_data["payment_date"],
            "deposit_to_account_id": payment_data["deposit_to_account_id"],
            "memo": payment_data["memo"]
        }
        
        # Add invoice applications as separate parameters
        for i, app in enumerate(payment_data["invoice_applications"]):
            query_params[f"invoice_applications[{i}][invoice_id]"] = app["invoice_id"]
            query_params[f"invoice_applications[{i}][amount]"] = app["amount"]
        
        response = requests.post(f"{BACKEND_URL}/payments/receive", params=query_params)
        self.assertEqual(response.status_code, 200)
        payment_result = response.json()
        
        # Verify payment was successful
        self.assertIn("payment_id", payment_result)
        self.assertEqual(payment_result["message"], "Payment received successfully")
        
        # Store payment ID for later tests
        self.payments["payment_1"] = payment_result["payment_id"]
        
        # Verify invoice status was updated
        response = requests.get(f"{BACKEND_URL}/transactions/{invoice_to_pay['id']}")
        self.assertEqual(response.status_code, 200)
        updated_invoice = response.json()
        
        # Invoice should be marked as Paid
        self.assertEqual(updated_invoice["status"], "Paid")
        
        # Verify customer balance was reduced
        response = requests.get(f"{BACKEND_URL}/customers/{customer_id}")
        self.assertEqual(response.status_code, 200)
        customer_after = response.json()
        
        # Customer balance should be reduced by payment amount
        self.assertAlmostEqual(customer_after["balance"], initial_balance - payment_amount, places=2)
        
        # Verify AR account balance was reduced
        response = requests.get(f"{BACKEND_URL}/accounts/{ar_account_id}")
        self.assertEqual(response.status_code, 200)
        ar_account_after = response.json()
        
        # AR balance should be reduced by payment amount
        self.assertAlmostEqual(ar_account_after["balance"], ar_initial_balance - payment_amount, places=2)
        
        # Verify Undeposited Funds account balance was increased
        response = requests.get(f"{BACKEND_URL}/accounts/{uf_account_id}")
        self.assertEqual(response.status_code, 200)
        uf_account_after = response.json()
        
        # Undeposited Funds balance should be increased by payment amount
        self.assertAlmostEqual(uf_account_after["balance"], uf_initial_balance + payment_amount, places=2)
        
        # Verify journal entries were created
        response = requests.get(f"{BACKEND_URL}/journal-entries")
        self.assertEqual(response.status_code, 200)
        journal_entries = response.json()
        
        # Find entries related to this payment
        payment_entries = [entry for entry in journal_entries if entry.get("transaction_id") == payment_result["payment_id"]]
        
        # Should have at least 2 entries (debit UF, credit AR)
        self.assertGreaterEqual(len(payment_entries), 2)
        
        # Verify proper double-entry bookkeeping
        debit_entries = [entry for entry in payment_entries if entry["debit"] > 0]
        credit_entries = [entry for entry in payment_entries if entry["credit"] > 0]
        
        self.assertGreaterEqual(len(debit_entries), 1)
        self.assertGreaterEqual(len(credit_entries), 1)
        
        total_debits = sum(entry["debit"] for entry in payment_entries)
        total_credits = sum(entry["credit"] for entry in payment_entries)
        
        # Total debits should equal total credits
        self.assertAlmostEqual(total_debits, total_credits, places=2)
        
        logger.info(f"Payment received successfully: ${payment_amount:.2f}")
        logger.info("Receive Payment Endpoint test passed")
    
    def test_04_pay_bills(self):
        """Test paying vendor bills"""
        logger.info("Testing Pay Bills Endpoint...")
        
        # Get vendor's open bills
        vendor_id = self.vendors["Acme Supplies"]["id"]
        response = requests.get(f"{BACKEND_URL}/vendors/{vendor_id}/open-bills")
        self.assertEqual(response.status_code, 200)
        open_bills = response.json()
        
        # Verify we have at least one open bill
        self.assertGreaterEqual(len(open_bills), 1)
        
        # Get vendor's initial balance
        response = requests.get(f"{BACKEND_URL}/vendors/{vendor_id}")
        self.assertEqual(response.status_code, 200)
        vendor_before = response.json()
        initial_balance = vendor_before["balance"]
        
        # Get initial AP account balance
        ap_account_id = self.accounts["Accounts Payable"]["id"]
        response = requests.get(f"{BACKEND_URL}/accounts/{ap_account_id}")
        self.assertEqual(response.status_code, 200)
        ap_account_before = response.json()
        ap_initial_balance = ap_account_before["balance"]
        
        # Get initial Checking account balance
        checking_account_id = self.accounts["Checking Account"]["id"]
        response = requests.get(f"{BACKEND_URL}/accounts/{checking_account_id}")
        self.assertEqual(response.status_code, 200)
        checking_account_before = response.json()
        checking_initial_balance = checking_account_before["balance"]
        
        # Create bill payment data
        bill_to_pay = open_bills[0]
        payment_amount = bill_to_pay["total"]
        
        payment_data = {
            "payment_date": datetime.utcnow().isoformat(),
            "payment_account_id": checking_account_id,
            "payment_method": "Check",
            "bill_payments": [
                {
                    "bill_id": bill_to_pay["id"],
                    "amount": payment_amount
                }
            ],
            "memo": "Payment for office supplies"
        }
        
        # Submit bill payment - convert to query parameters
        query_params = {
            "payment_date": payment_data["payment_date"],
            "payment_account_id": payment_data["payment_account_id"],
            "payment_method": payment_data["payment_method"],
            "memo": payment_data["memo"]
        }
        
        # Add bill payments as separate parameters
        for i, bill_payment in enumerate(payment_data["bill_payments"]):
            query_params[f"bill_payments[{i}][bill_id]"] = bill_payment["bill_id"]
            query_params[f"bill_payments[{i}][amount]"] = bill_payment["amount"]
        
        response = requests.post(f"{BACKEND_URL}/payments/pay-bills", params=query_params)
        self.assertEqual(response.status_code, 200)
        payment_result = response.json()
        
        # Verify payment was successful
        self.assertIn("payment_id", payment_result)
        self.assertEqual(payment_result["message"], "Bills paid successfully")
        
        # Store payment ID for later tests
        self.payments["bill_payment_1"] = payment_result["payment_id"]
        
        # Verify bill status was updated
        response = requests.get(f"{BACKEND_URL}/transactions/{bill_to_pay['id']}")
        self.assertEqual(response.status_code, 200)
        updated_bill = response.json()
        
        # Bill should be marked as Paid
        self.assertEqual(updated_bill["status"], "Paid")
        
        # Verify vendor balance was reduced
        response = requests.get(f"{BACKEND_URL}/vendors/{vendor_id}")
        self.assertEqual(response.status_code, 200)
        vendor_after = response.json()
        
        # Vendor balance should be reduced by payment amount
        self.assertAlmostEqual(vendor_after["balance"], initial_balance - payment_amount, places=2)
        
        # Verify AP account balance was reduced
        response = requests.get(f"{BACKEND_URL}/accounts/{ap_account_id}")
        self.assertEqual(response.status_code, 200)
        ap_account_after = response.json()
        
        # AP balance should be reduced by payment amount
        self.assertAlmostEqual(ap_account_after["balance"], ap_initial_balance - payment_amount, places=2)
        
        # Verify Checking account balance was decreased
        response = requests.get(f"{BACKEND_URL}/accounts/{checking_account_id}")
        self.assertEqual(response.status_code, 200)
        checking_account_after = response.json()
        
        # Checking balance should be decreased by payment amount
        self.assertAlmostEqual(checking_account_after["balance"], checking_initial_balance - payment_amount, places=2)
        
        # Verify journal entries were created
        response = requests.get(f"{BACKEND_URL}/journal-entries")
        self.assertEqual(response.status_code, 200)
        journal_entries = response.json()
        
        # Find entries related to this payment
        payment_entries = [entry for entry in journal_entries if entry.get("transaction_id") == payment_result["payment_id"]]
        
        # Should have at least 2 entries (debit AP, credit Checking)
        self.assertGreaterEqual(len(payment_entries), 2)
        
        # Verify proper double-entry bookkeeping
        debit_entries = [entry for entry in payment_entries if entry["debit"] > 0]
        credit_entries = [entry for entry in payment_entries if entry["credit"] > 0]
        
        self.assertGreaterEqual(len(debit_entries), 1)
        self.assertGreaterEqual(len(credit_entries), 1)
        
        total_debits = sum(entry["debit"] for entry in payment_entries)
        total_credits = sum(entry["credit"] for entry in payment_entries)
        
        # Total debits should equal total credits
        self.assertAlmostEqual(total_debits, total_credits, places=2)
        
        logger.info(f"Bill payment made successfully: ${payment_amount:.2f}")
        logger.info("Pay Bills Endpoint test passed")
    
    def test_05_undeposited_payments(self):
        """Test retrieving undeposited payments"""
        logger.info("Testing Undeposited Payments Endpoint...")
        
        # Get undeposited payments
        response = requests.get(f"{BACKEND_URL}/payments/undeposited")
        self.assertEqual(response.status_code, 200)
        undeposited_payments = response.json()
        
        # We should have at least one undeposited payment from our previous test
        self.assertGreaterEqual(len(undeposited_payments), 1)
        
        # Verify payment details
        for payment in undeposited_payments:
            self.assertEqual(payment["transaction_type"], "Payment")
            self.assertNotEqual(payment["status"], "Deposited")
            
        logger.info(f"Found {len(undeposited_payments)} undeposited payments")
        logger.info("Undeposited Payments Endpoint test passed")
    
    def test_06_make_deposit(self):
        """Test depositing undeposited payments to bank account"""
        logger.info("Testing Make Deposit Endpoint...")
        
        # Get undeposited payments
        response = requests.get(f"{BACKEND_URL}/payments/undeposited")
        self.assertEqual(response.status_code, 200)
        undeposited_payments = response.json()
        
        # We should have at least one undeposited payment from our previous test
        self.assertGreaterEqual(len(undeposited_payments), 1)
        
        # Get initial Undeposited Funds account balance
        uf_account_id = self.accounts["Undeposited Funds"]["id"]
        response = requests.get(f"{BACKEND_URL}/accounts/{uf_account_id}")
        self.assertEqual(response.status_code, 200)
        uf_account_before = response.json()
        uf_initial_balance = uf_account_before["balance"]
        
        # Get initial Checking account balance
        checking_account_id = self.accounts["Checking Account"]["id"]
        response = requests.get(f"{BACKEND_URL}/accounts/{checking_account_id}")
        self.assertEqual(response.status_code, 200)
        checking_account_before = response.json()
        checking_initial_balance = checking_account_before["balance"]
        
        # Create deposit data
        payment_items = []
        total_deposit = 0
        
        for payment in undeposited_payments:
            payment_items.append({
                "payment_id": payment["id"],
                "amount": payment["total"]
            })
            total_deposit += payment["total"]
        
        deposit_data = {
            "deposit_date": datetime.utcnow().isoformat(),
            "deposit_to_account_id": checking_account_id,
            "payment_items": payment_items,
            "memo": "Deposit of customer payments"
        }
        
        # Submit deposit - convert to query parameters
        query_params = {
            "deposit_date": deposit_data["deposit_date"],
            "deposit_to_account_id": deposit_data["deposit_to_account_id"],
            "memo": deposit_data["memo"]
        }
        
        # Add payment items as separate parameters
        for i, item in enumerate(deposit_data["payment_items"]):
            query_params[f"payment_items[{i}][payment_id]"] = item["payment_id"]
            query_params[f"payment_items[{i}][amount]"] = item["amount"]
        
        response = requests.post(f"{BACKEND_URL}/deposits", params=query_params)
        self.assertEqual(response.status_code, 200)
        deposit_result = response.json()
        
        # Verify deposit was successful
        self.assertIn("deposit_id", deposit_result)
        self.assertEqual(deposit_result["message"], "Deposit completed successfully")
        
        # Store deposit ID for later tests
        self.payments["deposit_1"] = deposit_result["deposit_id"]
        
        # Verify payment status was updated
        for payment in undeposited_payments:
            response = requests.get(f"{BACKEND_URL}/transactions/{payment['id']}")
            self.assertEqual(response.status_code, 200)
            updated_payment = response.json()
            
            # Payment should be marked as Deposited
            self.assertEqual(updated_payment["status"], "Deposited")
            
        # Verify Undeposited Funds account balance was decreased
        response = requests.get(f"{BACKEND_URL}/accounts/{uf_account_id}")
        self.assertEqual(response.status_code, 200)
        uf_account_after = response.json()
        
        # Undeposited Funds balance should be decreased by deposit amount
        self.assertAlmostEqual(uf_account_after["balance"], uf_initial_balance - total_deposit, places=2)
        
        # Verify Checking account balance was increased
        response = requests.get(f"{BACKEND_URL}/accounts/{checking_account_id}")
        self.assertEqual(response.status_code, 200)
        checking_account_after = response.json()
        
        # Checking balance should be increased by deposit amount
        self.assertAlmostEqual(checking_account_after["balance"], checking_initial_balance + total_deposit, places=2)
        
        # Verify journal entries were created
        response = requests.get(f"{BACKEND_URL}/journal-entries")
        self.assertEqual(response.status_code, 200)
        journal_entries = response.json()
        
        # Find entries related to this deposit
        deposit_entries = [entry for entry in journal_entries if entry.get("transaction_id") == deposit_result["deposit_id"]]
        
        # Should have at least 2 entries (debit Checking, credit UF)
        self.assertGreaterEqual(len(deposit_entries), 2)
        
        # Verify proper double-entry bookkeeping
        debit_entries = [entry for entry in deposit_entries if entry["debit"] > 0]
        credit_entries = [entry for entry in deposit_entries if entry["credit"] > 0]
        
        self.assertGreaterEqual(len(debit_entries), 1)
        self.assertGreaterEqual(len(credit_entries), 1)
        
        total_debits = sum(entry["debit"] for entry in deposit_entries)
        total_credits = sum(entry["credit"] for entry in deposit_entries)
        
        # Total debits should equal total credits
        self.assertAlmostEqual(total_debits, total_credits, places=2)
        
        logger.info(f"Deposit made successfully: ${total_deposit:.2f}")
        logger.info("Make Deposit Endpoint test passed")
    
    def test_07_journal_entry_endpoint(self):
        """Test creating manual journal entries"""
        logger.info("Testing Journal Entry Endpoint...")
        
        # Create a manual journal entry
        journal_entry = {
            "transaction_id": str(uuid.uuid4()),
            "account_id": self.accounts["Office Supplies"]["id"],
            "debit": 100.0,
            "credit": 0.0,
            "description": "Manual journal entry test",
            "date": datetime.utcnow().isoformat()
        }
        
        # Get initial Office Supplies account balance
        office_account_id = self.accounts["Office Supplies"]["id"]
        response = requests.get(f"{BACKEND_URL}/accounts/{office_account_id}")
        self.assertEqual(response.status_code, 200)
        office_account_before = response.json()
        office_initial_balance = office_account_before["balance"]
        
        # Submit journal entry
        response = requests.post(f"{BACKEND_URL}/journal-entries", json=journal_entry)
        self.assertEqual(response.status_code, 200)
        created_entry = response.json()
        
        # Verify journal entry was created
        self.assertEqual(created_entry["transaction_id"], journal_entry["transaction_id"])
        self.assertEqual(created_entry["account_id"], journal_entry["account_id"])
        self.assertEqual(created_entry["debit"], journal_entry["debit"])
        self.assertEqual(created_entry["credit"], journal_entry["credit"])
        
        # Verify account balance was updated
        response = requests.get(f"{BACKEND_URL}/accounts/{office_account_id}")
        self.assertEqual(response.status_code, 200)
        office_account_after = response.json()
        
        # Office Supplies balance should be increased by debit amount
        self.assertAlmostEqual(office_account_after["balance"], office_initial_balance + journal_entry["debit"], places=2)
        
        logger.info("Journal Entry Endpoint test passed")
    
    def test_08_complete_payment_workflow(self):
        """Test complete payment workflow from invoice to deposit"""
        logger.info("Testing Complete Payment Workflow...")
        
        # 1. Create a new customer invoice
        invoice_data = {
            "transaction_type": "Invoice",
            "customer_id": self.customers["Jane Doe"]["id"],
            "date": datetime.utcnow().isoformat(),
            "due_date": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "line_items": [
                {
                    "description": "Additional Services",
                    "quantity": 5,
                    "rate": 100.0,
                    "amount": 500.0,
                    "account_id": self.accounts["Sales Revenue"]["id"]
                }
            ],
            "tax_rate": 8.0,
            "memo": "Invoice for additional services"
        }
        
        response = requests.post(f"{BACKEND_URL}/transactions", json=invoice_data)
        self.assertEqual(response.status_code, 200)
        invoice = response.json()
        self.transactions["workflow_invoice"] = invoice
        logger.info(f"Created workflow invoice: {invoice['transaction_number']} with ID: {invoice['id']}")
        
        # 2. Receive payment for the invoice
        customer_id = self.customers["Jane Doe"]["id"]
        payment_amount = invoice["total"]
        uf_account_id = self.accounts["Undeposited Funds"]["id"]
        
        # 2. Receive payment for the invoice - convert to query parameters
        query_params = {
            "customer_id": customer_id,
            "payment_amount": payment_amount,
            "payment_method": "Check",
            "payment_date": datetime.utcnow().isoformat(),
            "deposit_to_account_id": uf_account_id,
            "memo": "Payment for additional services"
        }
        
        # Add invoice applications as separate parameters
        query_params["invoice_applications[0][invoice_id]"] = invoice["id"]
        query_params["invoice_applications[0][amount]"] = payment_amount
        
        response = requests.post(f"{BACKEND_URL}/payments/receive", params=query_params)
        self.assertEqual(response.status_code, 200)
        payment_result = response.json()
        self.assertEqual(response.status_code, 200)
        payment_result = response.json()
        self.payments["workflow_payment"] = payment_result["payment_id"]
        logger.info(f"Received workflow payment: {payment_result['payment_id']}")
        
        # 3. Verify invoice is marked as paid
        response = requests.get(f"{BACKEND_URL}/transactions/{invoice['id']}")
        self.assertEqual(response.status_code, 200)
        updated_invoice = response.json()
        self.assertEqual(updated_invoice["status"], "Paid")
        
        # 4. Get undeposited payments
        response = requests.get(f"{BACKEND_URL}/payments/undeposited")
        self.assertEqual(response.status_code, 200)
        undeposited_payments = response.json()
        
        # Find our payment in the undeposited payments
        workflow_payment = None
        for payment in undeposited_payments:
            if payment["id"] == self.payments.get("workflow_payment"):
                workflow_payment = payment
                break
        
        self.assertIsNotNone(workflow_payment)
        
        # 5. Make deposit to checking account - convert to query parameters
        checking_account_id = self.accounts["Checking Account"]["id"]
        
        query_params = {
            "deposit_date": datetime.utcnow().isoformat(),
            "deposit_to_account_id": checking_account_id,
            "memo": "Deposit of workflow payment"
        }
        
        # Add payment items as separate parameters
        query_params["payment_items[0][payment_id]"] = workflow_payment["id"]
        query_params["payment_items[0][amount]"] = workflow_payment["total"]
        
        response = requests.post(f"{BACKEND_URL}/deposits", params=query_params)
        self.assertEqual(response.status_code, 200)
        deposit_result = response.json()
        self.assertEqual(response.status_code, 200)
        deposit_result = response.json()
        self.payments["workflow_deposit"] = deposit_result["deposit_id"]
        logger.info(f"Made workflow deposit: {deposit_result['deposit_id']}")
        
        # 6. Verify payment is marked as deposited
        response = requests.get(f"{BACKEND_URL}/transactions/{workflow_payment['id']}")
        self.assertEqual(response.status_code, 200)
        updated_payment = response.json()
        self.assertEqual(updated_payment["status"], "Deposited")
        
        # 7. Verify journal entries for the entire workflow
        response = requests.get(f"{BACKEND_URL}/journal-entries")
        self.assertEqual(response.status_code, 200)
        journal_entries = response.json()
        
        # Find entries for invoice
        invoice_entries = [entry for entry in journal_entries if entry.get("transaction_id") == invoice["id"]]
        self.assertGreaterEqual(len(invoice_entries), 2)
        
        # Find entries for payment
        payment_entries = [entry for entry in journal_entries if entry.get("transaction_id") == payment_result["payment_id"]]
        self.assertGreaterEqual(len(payment_entries), 2)
        
        # Find entries for deposit
        deposit_entries = [entry for entry in journal_entries if entry.get("transaction_id") == deposit_result["deposit_id"]]
        self.assertGreaterEqual(len(deposit_entries), 2)
        
        logger.info("Complete Payment Workflow test passed")
        logger.info("All advanced payment processing tests completed successfully!")


if __name__ == "__main__":
    unittest.main()