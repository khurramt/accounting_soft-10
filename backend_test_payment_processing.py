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

class QBClonePaymentProcessingTest(unittest.TestCase):
    """Test suite for QBClone advanced payment processing endpoints"""
    
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
        
        # Create test accounts
        self.create_test_accounts()
        
        # Create test customers and vendors
        self.create_test_customers_vendors()
        
        # Create test invoices and bills
        self.create_test_invoices_bills()
    
    def create_test_accounts(self):
        """Create test accounts needed for payment processing"""
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
    
    def create_test_customers_vendors(self):
        """Create test customers and vendors"""
        # Create customers
        customer_data = [
            {
                "name": "Test Customer 1",
                "company": "Test Company 1",
                "email": "customer1@test.com",
                "phone": "555-123-4567"
            },
            {
                "name": "Test Customer 2",
                "company": "Test Company 2",
                "email": "customer2@test.com",
                "phone": "555-987-6543"
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
                "name": "Test Vendor 1",
                "company": "Vendor Company 1",
                "email": "vendor1@test.com",
                "phone": "555-111-2222"
            },
            {
                "name": "Test Vendor 2",
                "company": "Vendor Company 2",
                "email": "vendor2@test.com",
                "phone": "555-333-4444"
            }
        ]
        
        for vendor in vendor_data:
            response = requests.post(f"{BACKEND_URL}/vendors", json=vendor)
            self.assertEqual(response.status_code, 200)
            vendor_obj = response.json()
            self.vendors[vendor["name"]] = vendor_obj
            logger.info(f"Created vendor: {vendor['name']} with ID: {vendor_obj['id']}")
    
    def create_test_invoices_bills(self):
        """Create test invoices and bills for payment processing tests"""
        # Create invoices for customers
        for customer_name, customer in self.customers.items():
            invoice_data = {
                "transaction_type": "Invoice",
                "customer_id": customer["id"],
                "date": datetime.utcnow().isoformat(),
                "due_date": (datetime.utcnow() + timedelta(days=30)).isoformat(),
                "line_items": [
                    {
                        "description": f"Test Service for {customer_name}",
                        "quantity": 1,
                        "rate": 1000.0,
                        "amount": 1000.0,
                        "account_id": self.accounts["Sales Revenue"]["id"]
                    }
                ],
                "tax_rate": 5.0,
                "memo": f"Test invoice for {customer_name}"
            }
            
            response = requests.post(f"{BACKEND_URL}/transactions", json=invoice_data)
            self.assertEqual(response.status_code, 200)
            invoice = response.json()
            self.transactions[f"invoice_{customer_name}"] = invoice
            logger.info(f"Created invoice for {customer_name}: {invoice['transaction_number']}")
        
        # Create bills for vendors
        for vendor_name, vendor in self.vendors.items():
            bill_data = {
                "transaction_type": "Bill",
                "vendor_id": vendor["id"],
                "date": datetime.utcnow().isoformat(),
                "due_date": (datetime.utcnow() + timedelta(days=15)).isoformat(),
                "line_items": [
                    {
                        "description": f"Test Expense from {vendor_name}",
                        "quantity": 1,
                        "rate": 500.0,
                        "amount": 500.0,
                        "account_id": self.accounts["Office Supplies"]["id"]
                    }
                ],
                "tax_rate": 5.0,
                "memo": f"Test bill from {vendor_name}"
            }
            
            response = requests.post(f"{BACKEND_URL}/transactions", json=bill_data)
            self.assertEqual(response.status_code, 200)
            bill = response.json()
            self.transactions[f"bill_{vendor_name}"] = bill
            logger.info(f"Created bill from {vendor_name}: {bill['transaction_number']}")
    
    def test_01_get_open_invoices(self):
        """Test GET /api/customers/{customer_id}/open-invoices endpoint"""
        logger.info("Testing GET open invoices endpoint...")
        
        for customer_name, customer in self.customers.items():
            response = requests.get(f"{BACKEND_URL}/customers/{customer['id']}/open-invoices")
            self.assertEqual(response.status_code, 200, f"Failed to get open invoices for {customer_name}")
            
            open_invoices = response.json()
            self.assertIsInstance(open_invoices, list)
            self.assertGreaterEqual(len(open_invoices), 1)
            
            # Verify invoice data
            for invoice in open_invoices:
                self.assertEqual(invoice["customer_id"], customer["id"])
                self.assertEqual(invoice["transaction_type"], "Invoice")
                self.assertIn("balance", invoice)
                self.assertIn("total", invoice)
                
            logger.info(f"Successfully retrieved {len(open_invoices)} open invoices for {customer_name}")
    
    def test_02_get_open_bills(self):
        """Test GET /api/vendors/{vendor_id}/open-bills endpoint"""
        logger.info("Testing GET open bills endpoint...")
        
        for vendor_name, vendor in self.vendors.items():
            response = requests.get(f"{BACKEND_URL}/vendors/{vendor['id']}/open-bills")
            self.assertEqual(response.status_code, 200, f"Failed to get open bills for {vendor_name}")
            
            open_bills = response.json()
            self.assertIsInstance(open_bills, list)
            self.assertGreaterEqual(len(open_bills), 1)
            
            # Verify bill data
            for bill in open_bills:
                self.assertEqual(bill["vendor_id"], vendor["id"])
                self.assertEqual(bill["transaction_type"], "Bill")
                self.assertIn("balance", bill)
                self.assertIn("total", bill)
                
            logger.info(f"Successfully retrieved {len(open_bills)} open bills for {vendor_name}")
    
    def test_03_receive_payment(self):
        """Test POST /api/payments/receive endpoint"""
        logger.info("Testing receive payment endpoint...")
        
        # Get customer and invoice
        customer_name = "Test Customer 1"
        customer = self.customers[customer_name]
        invoice = self.transactions[f"invoice_{customer_name}"]
        
        # Create payment data
        payment_data = {
            "customer_id": customer["id"],
            "payment_amount": invoice["total"],
            "payment_method": "Check",
            "payment_date": datetime.utcnow().isoformat(),
            "deposit_to_account_id": self.accounts["Undeposited Funds"]["id"],
            "memo": f"Payment from {customer_name}"
        }
        
        # Add invoice application as a separate parameter
        invoice_application = {
            "invoice_id": invoice["id"],
            "amount": invoice["total"]
        }
        
        # Send payment request
        response = requests.post(
            f"{BACKEND_URL}/payments/receive", 
            params=payment_data,
            json=[invoice_application]
        )
        self.assertEqual(response.status_code, 200, "Failed to receive payment")
        
        payment_result = response.json()
        self.assertIn("payment_id", payment_result)
        self.assertIn("message", payment_result)
        
        logger.info(f"Successfully received payment: {payment_result['payment_id']}")
        
        # Verify invoice status was updated
        response = requests.get(f"{BACKEND_URL}/customers/{customer['id']}/open-invoices")
        self.assertEqual(response.status_code, 200)
        open_invoices = response.json()
        
        # The invoice should no longer be in open invoices or have a reduced balance
        invoice_still_open = False
        for open_invoice in open_invoices:
            if open_invoice["id"] == invoice["id"]:
                invoice_still_open = True
                self.assertLess(open_invoice["balance"], invoice["total"])
        
        if not invoice_still_open:
            logger.info("Invoice was properly marked as paid")
    
    def test_04_pay_bills(self):
        """Test POST /api/payments/pay-bills endpoint"""
        logger.info("Testing pay bills endpoint...")
        
        # Get vendor and bill
        vendor_name = "Test Vendor 1"
        vendor = self.vendors[vendor_name]
        bill = self.transactions[f"bill_{vendor_name}"]
        
        # Create bill payment data
        bill_payment_data = {
            "payment_date": datetime.utcnow().isoformat(),
            "payment_account_id": self.accounts["Checking Account"]["id"],
            "payment_method": "Check",
            "memo": f"Payment to {vendor_name}"
        }
        
        # Add bill payment as a separate parameter
        bill_payment = {
            "bill_id": bill["id"],
            "amount": bill["total"]
        }
        
        # Send bill payment request
        response = requests.post(
            f"{BACKEND_URL}/payments/pay-bills", 
            params=bill_payment_data,
            json=[bill_payment]
        )
        self.assertEqual(response.status_code, 200, "Failed to pay bills")
        
        payment_result = response.json()
        self.assertIn("payment_id", payment_result)
        self.assertIn("message", payment_result)
        
        logger.info(f"Successfully paid bills: {payment_result['payment_id']}")
        
        # Verify bill status was updated
        response = requests.get(f"{BACKEND_URL}/vendors/{vendor['id']}/open-bills")
        self.assertEqual(response.status_code, 200)
        open_bills = response.json()
        
        # The bill should no longer be in open bills or have a reduced balance
        bill_still_open = False
        for open_bill in open_bills:
            if open_bill["id"] == bill["id"]:
                bill_still_open = True
                self.assertLess(open_bill["balance"], bill["total"])
        
        if not bill_still_open:
            logger.info("Bill was properly marked as paid")
    
    def test_05_get_undeposited_payments(self):
        """Test GET /api/payments/undeposited endpoint"""
        logger.info("Testing get undeposited payments endpoint...")
        
        response = requests.get(f"{BACKEND_URL}/payments/undeposited")
        self.assertEqual(response.status_code, 200, "Failed to get undeposited payments")
        
        undeposited_payments = response.json()
        self.assertIsInstance(undeposited_payments, list)
        
        # We should have at least one undeposited payment from our previous test
        self.assertGreaterEqual(len(undeposited_payments), 1)
        
        for payment in undeposited_payments:
            self.assertEqual(payment["transaction_type"], "Payment")
            self.assertNotEqual(payment["status"], "Deposited")
        
        logger.info(f"Successfully retrieved {len(undeposited_payments)} undeposited payments")
    
    def test_06_make_deposit(self):
        """Test POST /api/deposits endpoint"""
        logger.info("Testing make deposit endpoint...")
        
        # Get undeposited payments
        response = requests.get(f"{BACKEND_URL}/payments/undeposited")
        self.assertEqual(response.status_code, 200)
        undeposited_payments = response.json()
        
        if len(undeposited_payments) > 0:
            # Create deposit data
            deposit_data = {
                "deposit_date": datetime.utcnow().isoformat(),
                "deposit_to_account_id": self.accounts["Checking Account"]["id"],
                "memo": "Test deposit"
            }
            
            # Add payment items as a separate parameter
            payment_items = [
                {
                    "payment_id": payment["id"],
                    "amount": payment["total"]
                } for payment in undeposited_payments
            ]
            
            # Send deposit request
            response = requests.post(
                f"{BACKEND_URL}/deposits", 
                params=deposit_data,
                json=payment_items
            )
            self.assertEqual(response.status_code, 200, "Failed to make deposit")
            
            deposit_result = response.json()
            self.assertIn("deposit_id", deposit_result)
            self.assertIn("message", deposit_result)
            
            logger.info(f"Successfully made deposit: {deposit_result['deposit_id']}")
            
            # Verify payments were marked as deposited
            response = requests.get(f"{BACKEND_URL}/payments/undeposited")
            self.assertEqual(response.status_code, 200)
            remaining_undeposited = response.json()
            
            # There should be fewer undeposited payments now
            self.assertLess(len(remaining_undeposited), len(undeposited_payments))
            logger.info(f"Undeposited payments reduced from {len(undeposited_payments)} to {len(remaining_undeposited)}")
        else:
            logger.warning("No undeposited payments found to test deposit functionality")
    
    def test_07_core_transaction_endpoints(self):
        """Test core transaction endpoints to ensure they still work"""
        logger.info("Testing core transaction endpoints...")
        
        # Test GET /api/transactions
        response = requests.get(f"{BACKEND_URL}/transactions")
        self.assertEqual(response.status_code, 200, "Failed to get transactions")
        
        transactions = response.json()
        self.assertIsInstance(transactions, list)
        self.assertGreaterEqual(len(transactions), 4)  # We created at least 4 transactions
        
        logger.info(f"Successfully retrieved {len(transactions)} transactions")
        
        # Test POST /api/transactions with a new transaction
        new_transaction_data = {
            "transaction_type": "Journal",
            "date": datetime.utcnow().isoformat(),
            "line_items": [
                {
                    "description": "Test Journal Entry",
                    "quantity": 1,
                    "rate": 100.0,
                    "amount": 100.0,
                    "account_id": self.accounts["Office Supplies"]["id"]
                }
            ],
            "memo": "Test journal entry"
        }
        
        response = requests.post(f"{BACKEND_URL}/transactions", json=new_transaction_data)
        self.assertEqual(response.status_code, 200, "Failed to create new transaction")
        
        new_transaction = response.json()
        self.assertEqual(new_transaction["transaction_type"], "Journal")
        
        logger.info(f"Successfully created new transaction: {new_transaction['transaction_number']}")
    
    def test_08_account_entity_endpoints(self):
        """Test account and entity endpoints to ensure they still work"""
        logger.info("Testing account and entity endpoints...")
        
        # Test GET /api/accounts
        response = requests.get(f"{BACKEND_URL}/accounts")
        self.assertEqual(response.status_code, 200, "Failed to get accounts")
        
        accounts = response.json()
        self.assertIsInstance(accounts, list)
        self.assertGreaterEqual(len(accounts), 6)  # We created at least 6 accounts
        
        logger.info(f"Successfully retrieved {len(accounts)} accounts")
        
        # Test GET /api/customers
        response = requests.get(f"{BACKEND_URL}/customers")
        self.assertEqual(response.status_code, 200, "Failed to get customers")
        
        customers = response.json()
        self.assertIsInstance(customers, list)
        self.assertGreaterEqual(len(customers), 2)  # We created at least 2 customers
        
        logger.info(f"Successfully retrieved {len(customers)} customers")
        
        # Test GET /api/vendors
        response = requests.get(f"{BACKEND_URL}/vendors")
        self.assertEqual(response.status_code, 200, "Failed to get vendors")
        
        vendors = response.json()
        self.assertIsInstance(vendors, list)
        self.assertGreaterEqual(len(vendors), 2)  # We created at least 2 vendors
        
        logger.info(f"Successfully retrieved {len(vendors)} vendors")

if __name__ == "__main__":
    unittest.main()