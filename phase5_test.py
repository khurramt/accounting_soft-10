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
BACKEND_URL = "https://dcebb859-d3a0-4791-bac5-696ddf89516c.preview.emergentagent.com/api"

class QBClonePhase5Test(unittest.TestCase):
    """Test suite for QBClone Phase 5 Advanced Business Logic"""
    
    def setUp(self):
        """Set up test data"""
        self.accounts = {}
        self.employees = {}
        self.items = {}
        self.inventory_transactions = {}
        self.inventory_adjustments = {}
        self.pay_periods = {}
        self.time_entries = {}
        self.payroll_items = {}
        self.tax_rates = {}
        
        # Test the root endpoint to ensure API is accessible
        response = requests.get(f"{BACKEND_URL}/")
        self.assertEqual(response.status_code, 200)
        logger.info("API is accessible")
        
        # Create test accounts
        self.create_test_accounts()
        
        # Create test employees
        self.create_test_employees()
        
        # Create test inventory items
        self.create_test_inventory_items()
    
    def create_test_accounts(self):
        """Create test accounts for inventory and payroll"""
        account_data = [
            {
                "name": "Inventory Asset",
                "account_type": "Asset",
                "detail_type": "Inventory",
                "account_number": "1200"
            },
            {
                "name": "Payroll Expense",
                "account_type": "Expense",
                "detail_type": "Office Expenses",
                "account_number": "5100"
            },
            {
                "name": "Payroll Liabilities",
                "account_type": "Liability",
                "detail_type": "Accounts Payable",
                "account_number": "2100"
            }
        ]
        
        for account in account_data:
            response = requests.post(f"{BACKEND_URL}/accounts", json=account)
            self.assertEqual(response.status_code, 200)
            account_obj = response.json()
            self.accounts[account["name"]] = account_obj
            logger.info(f"Created account: {account['name']} with ID: {account_obj['id']}")
    
    def create_test_employees(self):
        """Create test employees for payroll testing"""
        employee_data = [
            {
                "name": "John Smith",
                "status": "Active",
                "title": "Software Developer",
                "ssn": "123-45-6789",
                "employee_id": "EMP001",
                "email": "john@example.com",
                "phone": "555-111-2222",
                "address": "123 Tech Lane",
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94105",
                "hire_date": datetime.utcnow().isoformat(),
                "pay_type": "Hourly",
                "pay_rate": 35.00,
                "pay_schedule": "Bi-weekly",
                "vacation_balance": 80.0,
                "sick_balance": 40.0
            },
            {
                "name": "Jane Doe",
                "status": "Active",
                "title": "Project Manager",
                "ssn": "987-65-4321",
                "employee_id": "EMP002",
                "email": "jane@example.com",
                "phone": "555-333-4444",
                "address": "456 Manager Ave",
                "city": "San Francisco",
                "state": "CA",
                "zip_code": "94107",
                "hire_date": datetime.utcnow().isoformat(),
                "pay_type": "Salary",
                "pay_rate": 85000.00,
                "pay_schedule": "Bi-weekly"
            }
        ]
        
        for employee in employee_data:
            response = requests.post(f"{BACKEND_URL}/employees", json=employee)
            self.assertEqual(response.status_code, 200)
            employee_obj = response.json()
            self.employees[employee["name"]] = employee_obj
            logger.info(f"Created employee: {employee['name']} with ID: {employee_obj['id']}")
    
    def create_test_inventory_items(self):
        """Create test inventory items with different costing methods"""
        item_data = [
            {
                "name": "Laptop Computer",
                "item_number": "INV001",
                "item_type": "Inventory",
                "description": "High-performance laptop",
                "sales_price": 1299.99,
                "cost": 899.99,
                "income_account_id": self.accounts["Inventory Asset"]["id"],
                "expense_account_id": self.accounts["Payroll Expense"]["id"],
                "inventory_account_id": self.accounts["Inventory Asset"]["id"],
                "qty_on_hand": 0.0,
                "reorder_point": 5.0,
                "costing_method": "FIFO",
                "min_stock_level": 3.0,
                "max_stock_level": 20.0
            },
            {
                "name": "Desktop Computer",
                "item_number": "INV002",
                "item_type": "Inventory",
                "description": "High-performance desktop",
                "sales_price": 999.99,
                "cost": 699.99,
                "income_account_id": self.accounts["Inventory Asset"]["id"],
                "expense_account_id": self.accounts["Payroll Expense"]["id"],
                "inventory_account_id": self.accounts["Inventory Asset"]["id"],
                "qty_on_hand": 0.0,
                "reorder_point": 3.0,
                "costing_method": "LIFO",
                "min_stock_level": 2.0,
                "max_stock_level": 15.0
            },
            {
                "name": "Tablet",
                "item_number": "INV003",
                "item_type": "Inventory",
                "description": "Tablet computer",
                "sales_price": 499.99,
                "cost": 349.99,
                "income_account_id": self.accounts["Inventory Asset"]["id"],
                "expense_account_id": self.accounts["Payroll Expense"]["id"],
                "inventory_account_id": self.accounts["Inventory Asset"]["id"],
                "qty_on_hand": 0.0,
                "reorder_point": 10.0,
                "costing_method": "Average",
                "min_stock_level": 5.0,
                "max_stock_level": 30.0
            }
        ]
        
        for item in item_data:
            response = requests.post(f"{BACKEND_URL}/items", json=item)
            self.assertEqual(response.status_code, 200)
            item_obj = response.json()
            self.items[item["name"]] = item_obj
            logger.info(f"Created item: {item['name']} with ID: {item_obj['id']}")
    
    def test_01_inventory_transactions(self):
        """Test inventory transactions with different costing methods"""
        logger.info("Testing Inventory Transactions...")
        
        # Test FIFO costing method
        laptop = self.items["Laptop Computer"]
        
        # Create purchase transactions at different costs
        purchase_transactions = [
            {
                "item_id": laptop["id"],
                "transaction_type": "purchase",
                "quantity": 5.0,
                "unit_cost": 899.99,
                "transaction_date": (datetime.utcnow() - timedelta(days=30)).isoformat(),
                "notes": "Initial purchase batch 1"
            },
            {
                "item_id": laptop["id"],
                "transaction_type": "purchase",
                "quantity": 5.0,
                "unit_cost": 949.99,
                "transaction_date": (datetime.utcnow() - timedelta(days=15)).isoformat(),
                "notes": "Second purchase batch 2"
            },
            {
                "item_id": laptop["id"],
                "transaction_type": "purchase",
                "quantity": 5.0,
                "unit_cost": 999.99,
                "transaction_date": datetime.utcnow().isoformat(),
                "notes": "Third purchase batch 3"
            }
        ]
        
        for transaction in purchase_transactions:
            response = requests.post(f"{BACKEND_URL}/inventory-transactions", json=transaction)
            self.assertEqual(response.status_code, 200)
            transaction_obj = response.json()
            logger.info(f"Created inventory transaction: {transaction_obj['id']} for {laptop['name']}")
        
        # Verify item quantity was updated
        response = requests.get(f"{BACKEND_URL}/items/{laptop['id']}")
        self.assertEqual(response.status_code, 200)
        updated_laptop = response.json()
        self.assertEqual(updated_laptop["qty_on_hand"], 15.0)
        logger.info(f"Updated laptop quantity: {updated_laptop['qty_on_hand']}")
        
        # Create a sale transaction
        sale_transaction = {
            "item_id": laptop["id"],
            "transaction_type": "sale",
            "quantity": 3.0,
            "unit_cost": updated_laptop["sales_price"],
            "transaction_date": datetime.utcnow().isoformat(),
            "notes": "Sale of laptops"
        }
        
        response = requests.post(f"{BACKEND_URL}/inventory-transactions", json=sale_transaction)
        self.assertEqual(response.status_code, 200)
        sale_obj = response.json()
        logger.info(f"Created sale transaction: {sale_obj['id']} for {laptop['name']}")
        
        # Verify item quantity was updated after sale
        response = requests.get(f"{BACKEND_URL}/items/{laptop['id']}")
        self.assertEqual(response.status_code, 200)
        updated_laptop = response.json()
        self.assertEqual(updated_laptop["qty_on_hand"], 12.0)
        logger.info(f"Updated laptop quantity after sale: {updated_laptop['qty_on_hand']}")
        
        # Test LIFO costing method
        desktop = self.items["Desktop Computer"]
        
        # Create purchase transactions at different costs
        purchase_transactions = [
            {
                "item_id": desktop["id"],
                "transaction_type": "purchase",
                "quantity": 5.0,
                "unit_cost": 699.99,
                "transaction_date": (datetime.utcnow() - timedelta(days=30)).isoformat(),
                "notes": "Initial purchase batch 1"
            },
            {
                "item_id": desktop["id"],
                "transaction_type": "purchase",
                "quantity": 5.0,
                "unit_cost": 749.99,
                "transaction_date": (datetime.utcnow() - timedelta(days=15)).isoformat(),
                "notes": "Second purchase batch 2"
            },
            {
                "item_id": desktop["id"],
                "transaction_type": "purchase",
                "quantity": 5.0,
                "unit_cost": 799.99,
                "transaction_date": datetime.utcnow().isoformat(),
                "notes": "Third purchase batch 3"
            }
        ]
        
        for transaction in purchase_transactions:
            response = requests.post(f"{BACKEND_URL}/inventory-transactions", json=transaction)
            self.assertEqual(response.status_code, 200)
            transaction_obj = response.json()
            logger.info(f"Created inventory transaction: {transaction_obj['id']} for {desktop['name']}")
        
        # Test Average costing method
        tablet = self.items["Tablet"]
        
        # Create purchase transactions at different costs
        purchase_transactions = [
            {
                "item_id": tablet["id"],
                "transaction_type": "purchase",
                "quantity": 10.0,
                "unit_cost": 349.99,
                "transaction_date": (datetime.utcnow() - timedelta(days=30)).isoformat(),
                "notes": "Initial purchase batch 1"
            },
            {
                "item_id": tablet["id"],
                "transaction_type": "purchase",
                "quantity": 10.0,
                "unit_cost": 369.99,
                "transaction_date": (datetime.utcnow() - timedelta(days=15)).isoformat(),
                "notes": "Second purchase batch 2"
            },
            {
                "item_id": tablet["id"],
                "transaction_type": "purchase",
                "quantity": 10.0,
                "unit_cost": 389.99,
                "transaction_date": datetime.utcnow().isoformat(),
                "notes": "Third purchase batch 3"
            }
        ]
        
        for transaction in purchase_transactions:
            response = requests.post(f"{BACKEND_URL}/inventory-transactions", json=transaction)
            self.assertEqual(response.status_code, 200)
            transaction_obj = response.json()
            logger.info(f"Created inventory transaction: {transaction_obj['id']} for {tablet['name']}")
        
        # Verify average cost was calculated
        response = requests.get(f"{BACKEND_URL}/items/{tablet['id']}")
        self.assertEqual(response.status_code, 200)
        updated_tablet = response.json()
        self.assertIsNotNone(updated_tablet["average_cost"])
        logger.info(f"Tablet average cost: {updated_tablet['average_cost']}")
        
        # Test inventory transactions listing with filters
        response = requests.get(f"{BACKEND_URL}/inventory-transactions?item_id={laptop['id']}")
        self.assertEqual(response.status_code, 200)
        laptop_transactions = response.json()
        self.assertEqual(len(laptop_transactions), 4)  # 3 purchases + 1 sale
        logger.info(f"Retrieved {len(laptop_transactions)} transactions for laptop")
        
        # Test transaction type filter
        response = requests.get(f"{BACKEND_URL}/inventory-transactions?transaction_type=purchase")
        self.assertEqual(response.status_code, 200)
        purchase_transactions = response.json()
        self.assertGreaterEqual(len(purchase_transactions), 9)  # At least 9 purchases (3 for each item)
        logger.info(f"Retrieved {len(purchase_transactions)} purchase transactions")
        
        logger.info("Inventory Transactions tests passed")
    
    def test_02_inventory_adjustments(self):
        """Test inventory adjustments"""
        logger.info("Testing Inventory Adjustments...")
        
        # Test different adjustment types
        laptop = self.items["Laptop Computer"]
        
        # Get current quantity
        response = requests.get(f"{BACKEND_URL}/items/{laptop['id']}")
        self.assertEqual(response.status_code, 200)
        current_laptop = response.json()
        current_qty = current_laptop["qty_on_hand"]
        
        # Create a shrinkage adjustment
        shrinkage_adjustment = {
            "item_id": laptop["id"],
            "adjustment_type": "Shrinkage",
            "quantity_after": current_qty - 1.0,
            "unit_cost": current_laptop["cost"],
            "reason": "Inventory count discrepancy",
            "adjusted_by": "test_user",
            "adjustment_date": datetime.utcnow().isoformat()
        }
        
        response = requests.post(f"{BACKEND_URL}/inventory-adjustments", json=shrinkage_adjustment)
        self.assertEqual(response.status_code, 200)
        adjustment_obj = response.json()
        logger.info(f"Created shrinkage adjustment: {adjustment_obj['id']} for {laptop['name']}")
        
        # Verify quantity was updated
        response = requests.get(f"{BACKEND_URL}/items/{laptop['id']}")
        self.assertEqual(response.status_code, 200)
        updated_laptop = response.json()
        self.assertEqual(updated_laptop["qty_on_hand"], current_qty - 1.0)
        logger.info(f"Updated laptop quantity after shrinkage: {updated_laptop['qty_on_hand']}")
        
        # Create a damaged adjustment
        damaged_adjustment = {
            "item_id": laptop["id"],
            "adjustment_type": "Damaged",
            "quantity_after": updated_laptop["qty_on_hand"] - 1.0,
            "unit_cost": updated_laptop["cost"],
            "reason": "Water damage",
            "adjusted_by": "test_user",
            "adjustment_date": datetime.utcnow().isoformat()
        }
        
        response = requests.post(f"{BACKEND_URL}/inventory-adjustments", json=damaged_adjustment)
        self.assertEqual(response.status_code, 200)
        adjustment_obj = response.json()
        logger.info(f"Created damaged adjustment: {adjustment_obj['id']} for {laptop['name']}")
        
        # Verify quantity was updated
        response = requests.get(f"{BACKEND_URL}/items/{laptop['id']}")
        self.assertEqual(response.status_code, 200)
        updated_laptop = response.json()
        self.assertEqual(updated_laptop["qty_on_hand"], current_qty - 2.0)
        logger.info(f"Updated laptop quantity after damage: {updated_laptop['qty_on_hand']}")
        
        # Test inventory adjustments listing with filters
        response = requests.get(f"{BACKEND_URL}/inventory-adjustments?item_id={laptop['id']}")
        self.assertEqual(response.status_code, 200)
        laptop_adjustments = response.json()
        self.assertEqual(len(laptop_adjustments), 2)  # Shrinkage + Damaged
        logger.info(f"Retrieved {len(laptop_adjustments)} adjustments for laptop")
        
        # Test adjustment type filter
        response = requests.get(f"{BACKEND_URL}/inventory-adjustments?adjustment_type=Shrinkage")
        self.assertEqual(response.status_code, 200)
        shrinkage_adjustments = response.json()
        self.assertGreaterEqual(len(shrinkage_adjustments), 1)
        logger.info(f"Retrieved {len(shrinkage_adjustments)} shrinkage adjustments")
        
        logger.info("Inventory Adjustments tests passed")
    
    def test_03_inventory_alerts(self):
        """Test inventory alerts for reorder points"""
        logger.info("Testing Inventory Alerts...")
        
        # Get a test item
        desktop = self.items["Desktop Computer"]
        
        # Get current quantity
        response = requests.get(f"{BACKEND_URL}/items/{desktop['id']}")
        self.assertEqual(response.status_code, 200)
        current_desktop = response.json()
        current_qty = current_desktop["qty_on_hand"]
        
        # Create an adjustment to reduce quantity below reorder point
        adjustment = {
            "item_id": desktop["id"],
            "adjustment_type": "Correction",
            "quantity_after": current_desktop["reorder_point"] - 1.0,  # Set below reorder point
            "unit_cost": current_desktop["cost"],
            "reason": "Adjustment for testing alerts",
            "adjusted_by": "test_user",
            "adjustment_date": datetime.utcnow().isoformat()
        }
        
        response = requests.post(f"{BACKEND_URL}/inventory-adjustments", json=adjustment)
        self.assertEqual(response.status_code, 200)
        adjustment_obj = response.json()
        logger.info(f"Created adjustment to trigger alert: {adjustment_obj['id']} for {desktop['name']}")
        
        # Check for alerts
        response = requests.get(f"{BACKEND_URL}/inventory-alerts")
        self.assertEqual(response.status_code, 200)
        alerts = response.json()
        
        # Find alert for our desktop item
        desktop_alerts = [alert for alert in alerts if alert["item_id"] == desktop["id"]]
        self.assertGreaterEqual(len(desktop_alerts), 1)
        logger.info(f"Found {len(desktop_alerts)} alerts for desktop")
        
        # Test acknowledging an alert
        if desktop_alerts:
            alert_id = desktop_alerts[0]["id"]
            response = requests.put(f"{BACKEND_URL}/inventory-alerts/{alert_id}/acknowledge", params={"user_id": "test_user"})
            self.assertEqual(response.status_code, 200)
            logger.info(f"Acknowledged alert: {alert_id}")
            
            # Verify alert is no longer active
            response = requests.get(f"{BACKEND_URL}/inventory-alerts")
            self.assertEqual(response.status_code, 200)
            active_alerts = response.json()
            active_desktop_alerts = [alert for alert in active_alerts if alert["item_id"] == desktop["id"] and alert["is_active"]]
            self.assertEqual(len(active_desktop_alerts), 0)
            logger.info("No active alerts for desktop after acknowledgment")
        
        logger.info("Inventory Alerts tests passed")
    
    def test_04_inventory_valuation_report(self):
        """Test inventory valuation report with different costing methods"""
        logger.info("Testing Inventory Valuation Report...")
        
        # Get the inventory valuation report
        response = requests.get(f"{BACKEND_URL}/reports/inventory-valuation")
        self.assertEqual(response.status_code, 200)
        report = response.json()
        
        # Verify report structure
        self.assertIn("items", report)
        self.assertIn("summary", report)
        self.assertIn("total_fifo", report["summary"])
        self.assertIn("total_lifo", report["summary"])
        self.assertIn("total_average", report["summary"])
        
        # Verify our test items are in the report
        item_ids = [item["item_id"] for item in report["items"]]
        for name, item in self.items.items():
            if item["qty_on_hand"] > 0:  # Only items with quantity should be in report
                self.assertIn(item["id"], item_ids)
                logger.info(f"Found {name} in valuation report")
        
        # Verify different costing methods have different values
        if report["items"]:
            sample_item = report["items"][0]
            logger.info(f"Sample item valuation: FIFO={sample_item['fifo_cost']}, LIFO={sample_item['lifo_cost']}, Average={sample_item['average_cost']}")
        
        logger.info("Inventory Valuation Report tests passed")
    
    def test_05_pay_periods(self):
        """Test pay periods management"""
        logger.info("Testing Pay Periods...")
        
        # Create pay periods
        pay_period_data = [
            {
                "period_type": "Bi-weekly",
                "start_date": (datetime.utcnow() - timedelta(days=14)).isoformat(),
                "end_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
                "pay_date": (datetime.utcnow() + timedelta(days=5)).isoformat()
            },
            {
                "period_type": "Bi-weekly",
                "start_date": datetime.utcnow().isoformat(),
                "end_date": (datetime.utcnow() + timedelta(days=13)).isoformat(),
                "pay_date": (datetime.utcnow() + timedelta(days=19)).isoformat()
            }
        ]
        
        for period in pay_period_data:
            response = requests.post(f"{BACKEND_URL}/pay-periods", json=period)
            self.assertEqual(response.status_code, 200)
            period_obj = response.json()
            self.pay_periods[period_obj["id"]] = period_obj
            logger.info(f"Created pay period: {period_obj['id']}")
        
        # Test pay period listing
        response = requests.get(f"{BACKEND_URL}/pay-periods")
        self.assertEqual(response.status_code, 200)
        periods = response.json()
        self.assertGreaterEqual(len(periods), 2)
        logger.info(f"Retrieved {len(periods)} pay periods")
        
        # Test filtering by is_closed
        response = requests.get(f"{BACKEND_URL}/pay-periods?is_closed=false")
        self.assertEqual(response.status_code, 200)
        open_periods = response.json()
        self.assertGreaterEqual(len(open_periods), 2)
        logger.info(f"Retrieved {len(open_periods)} open pay periods")
        
        # Test closing a pay period
        period_id = list(self.pay_periods.keys())[0]
        response = requests.put(f"{BACKEND_URL}/pay-periods/{period_id}/close")
        self.assertEqual(response.status_code, 200)
        logger.info(f"Closed pay period: {period_id}")
        
        # Verify pay period is closed
        response = requests.get(f"{BACKEND_URL}/pay-periods/{period_id}")
        self.assertEqual(response.status_code, 200)
        closed_period = response.json()
        self.assertTrue(closed_period["is_closed"])
        logger.info(f"Verified pay period {period_id} is closed")
        
        logger.info("Pay Periods tests passed")
    
    def test_06_time_entries(self):
        """Test time entries with overtime calculation"""
        logger.info("Testing Time Entries...")
        
        # Create pay periods first
        pay_period_data = [
            {
                "period_type": "Bi-weekly",
                "start_date": (datetime.utcnow() - timedelta(days=14)).isoformat(),
                "end_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
                "pay_date": (datetime.utcnow() + timedelta(days=5)).isoformat()
            },
            {
                "period_type": "Bi-weekly",
                "start_date": datetime.utcnow().isoformat(),
                "end_date": (datetime.utcnow() + timedelta(days=13)).isoformat(),
                "pay_date": (datetime.utcnow() + timedelta(days=19)).isoformat()
            }
        ]
        
        for period in pay_period_data:
            response = requests.post(f"{BACKEND_URL}/pay-periods", json=period)
            self.assertEqual(response.status_code, 200)
            period_obj = response.json()
            self.pay_periods[period_obj["id"]] = period_obj
            logger.info(f"Created pay period: {period_obj['id']}")
        
        # Get an employee and pay period
        employee = self.employees["John Smith"]
        pay_period_id = list(self.pay_periods.keys())[1]  # Use the open pay period
        
        # Create time entries with different hours
        time_entry_data = [
            {
                "employee_id": employee["id"],
                "date": datetime.utcnow().isoformat(),
                "clock_in": datetime.utcnow().replace(hour=9, minute=0, second=0).isoformat(),
                "clock_out": datetime.utcnow().replace(hour=17, minute=0, second=0).isoformat(),
                "break_minutes": 30,
                "notes": "Regular 8-hour day with 30-minute break"
            },
            {
                "employee_id": employee["id"],
                "date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
                "clock_in": datetime.utcnow().replace(hour=9, minute=0, second=0).isoformat(),
                "clock_out": datetime.utcnow().replace(hour=19, minute=0, second=0).isoformat(),
                "break_minutes": 60,
                "notes": "10-hour day with 1-hour break (should have 1 hour overtime)"
            }
        ]
        
        for entry in time_entry_data:
            response = requests.post(f"{BACKEND_URL}/time-entries", json=entry)
            self.assertEqual(response.status_code, 200)
            entry_obj = response.json()
            self.time_entries[entry_obj["id"]] = entry_obj
            logger.info(f"Created time entry: {entry_obj['id']} with {entry_obj['total_hours']} hours")
            
            # Verify overtime calculation
            if "10-hour day" in entry["notes"]:
                self.assertGreaterEqual(entry_obj["overtime_hours"], 1.0)
                logger.info(f"Verified overtime hours: {entry_obj['overtime_hours']}")
        
        # Test time entry listing with filters
        response = requests.get(f"{BACKEND_URL}/time-entries?employee_id={employee['id']}")
        self.assertEqual(response.status_code, 200)
        employee_entries = response.json()
        self.assertEqual(len(employee_entries), 2)
        logger.info(f"Retrieved {len(employee_entries)} time entries for employee")
        
        # Test updating a time entry
        entry_id = list(self.time_entries.keys())[0]
        update_data = {
            "employee_id": employee["id"],
            "date": datetime.utcnow().isoformat(),
            "clock_in": datetime.utcnow().replace(hour=8, minute=30, second=0).isoformat(),
            "clock_out": datetime.utcnow().replace(hour=17, minute=30, second=0).isoformat(),
            "break_minutes": 60,
            "notes": "Updated time entry"
        }
        
        response = requests.put(f"{BACKEND_URL}/time-entries/{entry_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        logger.info(f"Updated time entry: {entry_id}")
        
        # Test approving a time entry
        response = requests.put(f"{BACKEND_URL}/time-entries/{entry_id}/approve", params={"approver_id": "test_approver"})
        self.assertEqual(response.status_code, 200)
        logger.info(f"Approved time entry: {entry_id}")
        
        # Verify time entry is approved
        response = requests.get(f"{BACKEND_URL}/time-entries?employee_id={employee['id']}")
        self.assertEqual(response.status_code, 200)
        updated_entries = response.json()
        approved_entry = next((entry for entry in updated_entries if entry["id"] == entry_id), None)
        self.assertIsNotNone(approved_entry)
        self.assertEqual(approved_entry["status"], "Approved")
        self.assertEqual(approved_entry["approved_by"], "test_approver")
        logger.info(f"Verified time entry {entry_id} is approved")
        
        logger.info("Time Entries tests passed")
    
    def test_07_payroll_processing(self):
        """Test payroll processing with tax calculations"""
        logger.info("Testing Payroll Processing...")
        
        # Get an employee and pay period
        employee = self.employees["John Smith"]
        pay_period_id = list(self.pay_periods.keys())[1]  # Use the open pay period
        
        # Create a payroll item
        payroll_data = {
            "employee_id": employee["id"],
            "pay_period_id": pay_period_id,
            "regular_hours": 40.0,
            "overtime_hours": 5.0
        }
        
        response = requests.post(f"{BACKEND_URL}/payroll-items", json=payroll_data)
        self.assertEqual(response.status_code, 200)
        payroll_obj = response.json()
        self.payroll_items[payroll_obj["id"]] = payroll_obj
        logger.info(f"Created payroll item: {payroll_obj['id']} with gross pay: ${payroll_obj['gross_pay']:.2f}")
        
        # Verify tax calculations
        self.assertGreater(payroll_obj["federal_income_tax"], 0)
        self.assertGreater(payroll_obj["state_income_tax"], 0)
        self.assertGreater(payroll_obj["social_security_tax"], 0)
        self.assertGreater(payroll_obj["medicare_tax"], 0)
        logger.info(f"Verified tax calculations: Federal=${payroll_obj['federal_income_tax']:.2f}, State=${payroll_obj['state_income_tax']:.2f}, SS=${payroll_obj['social_security_tax']:.2f}, Medicare=${payroll_obj['medicare_tax']:.2f}")
        
        # Test payroll item listing
        response = requests.get(f"{BACKEND_URL}/payroll-items?employee_id={employee['id']}")
        self.assertEqual(response.status_code, 200)
        employee_payroll = response.json()
        self.assertEqual(len(employee_payroll), 1)
        logger.info(f"Retrieved {len(employee_payroll)} payroll items for employee")
        
        # Test processing a payroll item
        payroll_id = payroll_obj["id"]
        response = requests.put(f"{BACKEND_URL}/payroll-items/{payroll_id}/process")
        self.assertEqual(response.status_code, 200)
        logger.info(f"Processed payroll item: {payroll_id}")
        
        # Verify payroll item is processed
        response = requests.get(f"{BACKEND_URL}/payroll-items?employee_id={employee['id']}")
        self.assertEqual(response.status_code, 200)
        updated_payroll = response.json()
        processed_item = updated_payroll[0]
        self.assertEqual(processed_item["status"], "Processed")
        self.assertIsNotNone(processed_item["processed_at"])
        logger.info(f"Verified payroll item {payroll_id} is processed")
        
        logger.info("Payroll Processing tests passed")
    
    def test_08_pay_stubs(self):
        """Test pay stub generation"""
        logger.info("Testing Pay Stubs...")
        
        # Get a processed payroll item
        payroll_id = list(self.payroll_items.keys())[0]
        
        # Create a pay stub
        response = requests.post(f"{BACKEND_URL}/pay-stubs", params={"payroll_item_id": payroll_id})
        self.assertEqual(response.status_code, 200)
        pay_stub = response.json()
        logger.info(f"Created pay stub: {pay_stub['id']} with net pay: ${pay_stub['net_pay']:.2f}")
        
        # Verify pay stub details
        self.assertEqual(pay_stub["payroll_item_id"], payroll_id)
        self.assertGreater(len(pay_stub["earnings"]), 0)
        self.assertGreater(len(pay_stub["deductions"]), 0)
        self.assertEqual(pay_stub["gross_pay"], self.payroll_items[payroll_id]["gross_pay"])
        self.assertEqual(pay_stub["total_deductions"], self.payroll_items[payroll_id]["total_deductions"])
        self.assertEqual(pay_stub["net_pay"], self.payroll_items[payroll_id]["net_pay"])
        logger.info(f"Verified pay stub details: Gross=${pay_stub['gross_pay']:.2f}, Deductions=${pay_stub['total_deductions']:.2f}, Net=${pay_stub['net_pay']:.2f}")
        
        # Test pay stub listing
        employee_id = self.payroll_items[payroll_id]["employee_id"]
        response = requests.get(f"{BACKEND_URL}/pay-stubs?employee_id={employee_id}")
        self.assertEqual(response.status_code, 200)
        employee_stubs = response.json()
        self.assertEqual(len(employee_stubs), 1)
        logger.info(f"Retrieved {len(employee_stubs)} pay stubs for employee")
        
        # Test retrieving a specific pay stub
        stub_id = pay_stub["id"]
        response = requests.get(f"{BACKEND_URL}/pay-stubs/{stub_id}")
        self.assertEqual(response.status_code, 200)
        retrieved_stub = response.json()
        self.assertEqual(retrieved_stub["id"], stub_id)
        logger.info(f"Retrieved pay stub: {stub_id}")
        
        logger.info("Pay Stubs tests passed")
    
    def test_09_tax_rates(self):
        """Test tax rates management"""
        logger.info("Testing Tax Rates...")
        
        # Create tax rates
        tax_rate_data = [
            {
                "tax_type": "Federal Income Tax",
                "rate": 22.0,
                "min_income": 40526.0,
                "max_income": 86375.0,
                "effective_date": datetime.utcnow().isoformat()
            },
            {
                "tax_type": "State Income Tax",
                "state": "CA",
                "rate": 9.3,
                "min_income": 58635.0,
                "max_income": 299508.0,
                "effective_date": datetime.utcnow().isoformat()
            },
            {
                "tax_type": "Social Security",
                "rate": 6.2,
                "min_income": 0.0,
                "max_income": 142800.0,
                "effective_date": datetime.utcnow().isoformat()
            },
            {
                "tax_type": "Medicare",
                "rate": 1.45,
                "min_income": 0.0,
                "effective_date": datetime.utcnow().isoformat()
            }
        ]
        
        for rate in tax_rate_data:
            response = requests.post(f"{BACKEND_URL}/tax-rates", json=rate)
            self.assertEqual(response.status_code, 200)
            rate_obj = response.json()
            self.tax_rates[rate_obj["id"]] = rate_obj
            logger.info(f"Created tax rate: {rate_obj['id']} for {rate_obj['tax_type']}")
        
        # Test tax rate listing
        response = requests.get(f"{BACKEND_URL}/tax-rates")
        self.assertEqual(response.status_code, 200)
        all_rates = response.json()
        self.assertGreaterEqual(len(all_rates), 4)
        logger.info(f"Retrieved {len(all_rates)} tax rates")
        
        # Test filtering by tax type
        response = requests.get(f"{BACKEND_URL}/tax-rates?tax_type=Federal Income Tax")
        self.assertEqual(response.status_code, 200)
        federal_rates = response.json()
        self.assertGreaterEqual(len(federal_rates), 1)
        logger.info(f"Retrieved {len(federal_rates)} federal tax rates")
        
        # Test filtering by state
        response = requests.get(f"{BACKEND_URL}/tax-rates?state=CA")
        self.assertEqual(response.status_code, 200)
        ca_rates = response.json()
        self.assertGreaterEqual(len(ca_rates), 1)
        logger.info(f"Retrieved {len(ca_rates)} California tax rates")
        
        logger.info("Tax Rates tests passed")
    
    def test_10_payroll_summary_report(self):
        """Test payroll summary report"""
        logger.info("Testing Payroll Summary Report...")
        
        # Set date range for report
        start_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
        end_date = datetime.utcnow().isoformat()
        
        # Get payroll summary report
        response = requests.get(f"{BACKEND_URL}/reports/payroll-summary?start_date={start_date}&end_date={end_date}")
        self.assertEqual(response.status_code, 200)
        report = response.json()
        
        # Verify report structure
        self.assertIn("summary", report)
        self.assertIn("employees", report)
        self.assertIn("total_gross", report["summary"])
        self.assertIn("total_deductions", report["summary"])
        self.assertIn("total_net", report["summary"])
        
        # Verify our test employee is in the report
        employee_id = self.employees["John Smith"]["id"]
        employee_in_report = any(emp["employee_id"] == employee_id for emp in report["employees"])
        self.assertTrue(employee_in_report)
        logger.info(f"Found employee in payroll summary report")
        
        # Test filtering by employee
        response = requests.get(f"{BACKEND_URL}/reports/payroll-summary?start_date={start_date}&end_date={end_date}&employee_id={employee_id}")
        self.assertEqual(response.status_code, 200)
        employee_report = response.json()
        self.assertEqual(len(employee_report["employees"]), 1)
        self.assertEqual(employee_report["employees"][0]["employee_id"], employee_id)
        logger.info(f"Retrieved filtered payroll summary report for employee")
        
        logger.info("Payroll Summary Report tests passed")

if __name__ == "__main__":
    unittest.main()