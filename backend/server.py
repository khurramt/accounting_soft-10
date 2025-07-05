from fastapi import FastAPI, APIRouter, HTTPException, Query, UploadFile, File, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import uuid
from datetime import datetime, timedelta
from enum import Enum
from decimal import Decimal
import json
import base64
import io
import csv
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import calendar
import bcrypt
import secrets

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="QBClone Accounting API", version="1.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Enums
class AccountType(str, Enum):
    ASSET = "Asset"
    LIABILITY = "Liability"
    EQUITY = "Equity"
    INCOME = "Income"
    EXPENSE = "Expense"

class TransactionType(str, Enum):
    INVOICE = "Invoice"
    SALES_RECEIPT = "Sales Receipt"
    ESTIMATE = "Estimate"
    SALES_ORDER = "Sales Order"
    CREDIT_MEMO = "Credit Memo"
    BILL = "Bill"
    PAYMENT = "Payment"
    DEPOSIT = "Deposit"
    CHECK = "Check"
    CREDIT_CARD = "Credit Card"
    TRANSFER = "Transfer"
    JOURNAL = "Journal"
    PURCHASE_ORDER = "Purchase Order"

class AccountDetailType(str, Enum):
    # Assets
    CHECKING = "Checking"
    SAVINGS = "Savings"
    ACCOUNTS_RECEIVABLE = "Accounts Receivable"
    INVENTORY = "Inventory"
    FIXED_ASSETS = "Fixed Assets"
    UNDEPOSITED_FUNDS = "Undeposited Funds"
    # Liabilities
    ACCOUNTS_PAYABLE = "Accounts Payable"
    CREDIT_CARD = "Credit Card"
    LOAN = "Loan"
    # Equity
    OWNER_EQUITY = "Owner's Equity"
    RETAINED_EARNINGS = "Retained Earnings"
    # Income
    SALES = "Sales"
    SERVICE_INCOME = "Service Income"
    # Expenses
    OFFICE_EXPENSES = "Office Expenses"
    TRAVEL = "Travel"
    MEALS = "Meals & Entertainment"

class ItemType(str, Enum):
    INVENTORY = "Inventory"
    NON_INVENTORY = "Non-Inventory"
    SERVICE = "Service"

class PaymentMethod(str, Enum):
    CASH = "Cash"
    CHECK = "Check"
    CREDIT_CARD = "Credit Card"
    ELECTRONIC = "Electronic"

class EmployeeStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    TERMINATED = "Terminated"

class PayType(str, Enum):
    HOURLY = "Hourly"
    SALARY = "Salary"
    COMMISSION = "Commission"

# Phase 5: Advanced Business Logic Enums
class CostingMethod(str, Enum):
    FIFO = "FIFO"
    LIFO = "LIFO"
    AVERAGE = "Average"

class InventoryAdjustmentType(str, Enum):
    SHRINKAGE = "Shrinkage"
    DAMAGED = "Damaged"
    CORRECTION = "Correction"
    RECOUNT = "Recount"
    OBSOLETE = "Obsolete"
    TRANSFER = "Transfer"

class PayrollStatus(str, Enum):
    PENDING = "Pending"
    PROCESSED = "Processed"
    PAID = "Paid"
    CANCELLED = "Cancelled"

class TimeEntryStatus(str, Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class PayPeriodType(str, Enum):
    WEEKLY = "Weekly"
    BIWEEKLY = "Bi-weekly"
    SEMIMONTHLY = "Semi-monthly"
    MONTHLY = "Monthly"

class TaxType(str, Enum):
    FEDERAL_INCOME = "Federal Income Tax"
    STATE_INCOME = "State Income Tax"
    SOCIAL_SECURITY = "Social Security"
    MEDICARE = "Medicare"
    UNEMPLOYMENT = "Unemployment"
    DISABILITY = "Disability"

# Data Models
class Company(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    legal_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: str = "United States"
    phone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    industry: str = "general"
    settings: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CompanyCreate(BaseModel):
    name: str
    legal_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: str = "United States"
    phone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    industry: str = "general"
    settings: Dict[str, Any] = {}

class Account(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    account_type: AccountType
    detail_type: AccountDetailType
    account_number: Optional[str] = None
    parent_id: Optional[str] = None
    balance: float = 0.0
    opening_balance: float = 0.0
    opening_balance_date: Optional[datetime] = None
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AccountCreate(BaseModel):
    name: str
    account_type: AccountType
    detail_type: AccountDetailType
    account_number: Optional[str] = None
    parent_id: Optional[str] = None
    opening_balance: float = 0.0
    opening_balance_date: Optional[datetime] = None

class Customer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    terms: Optional[str] = None
    credit_limit: Optional[float] = None
    tax_id: Optional[str] = None
    balance: float = 0.0
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CustomerCreate(BaseModel):
    name: str
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    terms: Optional[str] = None
    credit_limit: Optional[float] = None
    tax_id: Optional[str] = None

class Vendor(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    terms: Optional[str] = None
    tax_id: Optional[str] = None
    balance: float = 0.0
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class VendorCreate(BaseModel):
    name: str
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    terms: Optional[str] = None
    tax_id: Optional[str] = None

class Employee(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    title: Optional[str] = None
    ssn: Optional[str] = None
    employee_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    hire_date: Optional[datetime] = None
    pay_type: Optional[PayType] = None
    pay_rate: Optional[float] = None
    pay_schedule: Optional[str] = None
    vacation_balance: float = 0.0
    sick_balance: float = 0.0
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EmployeeCreate(BaseModel):
    name: str
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    title: Optional[str] = None
    ssn: Optional[str] = None
    employee_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    hire_date: Optional[datetime] = None
    pay_type: Optional[PayType] = None
    pay_rate: Optional[float] = None
    pay_schedule: Optional[str] = None
    vacation_balance: float = 0.0
    sick_balance: float = 0.0
    notes: Optional[str] = None

class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    item_number: Optional[str] = None
    item_type: ItemType
    description: Optional[str] = None
    sales_price: Optional[float] = None
    cost: Optional[float] = None
    income_account_id: Optional[str] = None
    expense_account_id: Optional[str] = None
    inventory_account_id: Optional[str] = None
    qty_on_hand: float = 0.0
    reorder_point: Optional[float] = None
    preferred_vendor_id: Optional[str] = None
    tax_code: Optional[str] = None
    active: bool = True
    # Phase 5: Advanced Inventory Management
    costing_method: CostingMethod = CostingMethod.FIFO
    min_stock_level: Optional[float] = None
    max_stock_level: Optional[float] = None
    average_cost: Optional[float] = None
    last_cost: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ItemCreate(BaseModel):
    name: str
    item_number: Optional[str] = None
    item_type: ItemType
    description: Optional[str] = None
    sales_price: Optional[float] = None
    cost: Optional[float] = None
    income_account_id: Optional[str] = None
    expense_account_id: Optional[str] = None
    inventory_account_id: Optional[str] = None
    qty_on_hand: float = 0.0
    reorder_point: Optional[float] = None
    preferred_vendor_id: Optional[str] = None
    tax_code: Optional[str] = None
    # Phase 5: Advanced Inventory Management
    costing_method: CostingMethod = CostingMethod.FIFO
    min_stock_level: Optional[float] = None
    max_stock_level: Optional[float] = None

class Class(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ClassCreate(BaseModel):
    name: str

class Location(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class LocationCreate(BaseModel):
    name: str

class Terms(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    days_due: int = 30
    discount_days: Optional[int] = None
    discount_percent: Optional[float] = None
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TermsCreate(BaseModel):
    name: str
    days_due: int = 30
    discount_days: Optional[int] = None
    discount_percent: Optional[float] = None

class PriceLevel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    adjustment_type: str = "Percentage"  # Percentage or Fixed
    adjustment_value: float = 0.0
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PriceLevelCreate(BaseModel):
    name: str
    adjustment_type: str = "Percentage"
    adjustment_value: float = 0.0

class LineItem(BaseModel):
    item_id: Optional[str] = None
    description: str
    quantity: float = 1.0
    rate: float = 0.0
    amount: float = 0.0
    account_id: Optional[str] = None
    class_id: Optional[str] = None
    location_id: Optional[str] = None
    tax_code: Optional[str] = None

class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    transaction_type: TransactionType
    transaction_number: Optional[str] = None
    customer_id: Optional[str] = None
    vendor_id: Optional[str] = None
    employee_id: Optional[str] = None
    date: datetime
    due_date: Optional[datetime] = None
    reference_number: Optional[str] = None
    po_number: Optional[str] = None
    terms_id: Optional[str] = None
    bill_to_address: Optional[str] = None
    ship_to_address: Optional[str] = None
    line_items: List[LineItem] = []
    subtotal: float = 0.0
    tax_rate: float = 0.0
    tax_amount: float = 0.0
    total: float = 0.0
    balance: Optional[float] = None  # For tracking unpaid amounts
    payment_method: Optional[PaymentMethod] = None
    deposit_to_account_id: Optional[str] = None
    deposit_id: Optional[str] = None  # For tracking which deposit this payment is in
    memo: Optional[str] = None
    status: str = "Open"  # Open, Paid, Voided, Partial, Deposited, etc.
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TransactionCreate(BaseModel):
    transaction_type: TransactionType
    customer_id: Optional[str] = None
    vendor_id: Optional[str] = None
    employee_id: Optional[str] = None
    date: datetime
    due_date: Optional[datetime] = None
    reference_number: Optional[str] = None
    po_number: Optional[str] = None
    terms_id: Optional[str] = None
    bill_to_address: Optional[str] = None
    ship_to_address: Optional[str] = None
    line_items: List[LineItem] = []
    tax_rate: float = 0.0
    payment_method: Optional[PaymentMethod] = None
    deposit_to_account_id: Optional[str] = None
    memo: Optional[str] = None

class JournalEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    transaction_id: str
    account_id: str
    debit: float = 0.0
    credit: float = 0.0
    description: str
    date: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MemorizedTransaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    transaction_template: Dict[str, Any]
    frequency: str = "Monthly"  # Daily, Weekly, Monthly, Quarterly, Yearly
    next_date: datetime
    end_date: Optional[datetime] = None
    auto_enter: bool = False
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MemorizedTransactionCreate(BaseModel):
    name: str
    transaction_template: Dict[str, Any]
    frequency: str = "Monthly"
    next_date: datetime
    end_date: Optional[datetime] = None
    auto_enter: bool = False

class ToDo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "Medium"  # Low, Medium, High
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ToDoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "Medium"

# Banking and Reconciliation Models
class BankTransaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    account_id: str
    date: datetime
    description: str
    amount: float
    transaction_type: str = "Unknown"  # Credit, Debit, Transfer, etc.
    reference_number: Optional[str] = None
    check_number: Optional[str] = None
    memo: Optional[str] = None
    category: Optional[str] = None
    reconciled: bool = False
    reconciliation_id: Optional[str] = None
    bank_transaction_id: Optional[str] = None  # From bank feed
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BankTransactionCreate(BaseModel):
    account_id: str
    date: datetime
    description: str
    amount: float
    transaction_type: str = "Unknown"
    reference_number: Optional[str] = None
    check_number: Optional[str] = None
    memo: Optional[str] = None
    category: Optional[str] = None

class Reconciliation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    account_id: str
    statement_date: datetime
    statement_ending_balance: float
    reconciled_balance: float
    difference: float = 0.0
    status: str = "In Progress"  # In Progress, Completed, Discrepancy
    reconciled_transactions: List[str] = []  # List of transaction IDs
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

class ReconciliationCreate(BaseModel):
    account_id: str
    statement_date: datetime
    statement_ending_balance: float
    notes: Optional[str] = None

class BankImportTransaction(BaseModel):
    date: datetime
    description: str
    amount: float
    transaction_type: str
    reference_number: Optional[str] = None
    check_number: Optional[str] = None
    category: Optional[str] = None
    balance: Optional[float] = None

class BankImportResult(BaseModel):
    total_transactions: int
    imported_transactions: int
    duplicate_transactions: int
    errors: List[str] = []
    preview_transactions: List[BankImportTransaction] = []

class AuditEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user: str
    module: str
    action: str
    record_id: str
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    full_name: str
    email: Optional[str] = None
    password_hash: str  # Store hashed password
    role: str = "User"
    active: bool = True
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    username: str
    full_name: str
    email: Optional[str] = None
    password: str
    role: str = "User"

class Role(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    permissions: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RoleCreate(BaseModel):
    name: str
    permissions: Dict[str, Any] = {}

# Phase 4: Form Customization Models
class CustomFieldType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    DROPDOWN = "dropdown"
    CHECKBOX = "checkbox"
    TEXTAREA = "textarea"

class CustomField(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    label: str
    field_type: CustomFieldType
    required: bool = False
    options: List[str] = []  # For dropdown type
    default_value: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CustomFieldCreate(BaseModel):
    name: str
    label: str
    field_type: CustomFieldType
    required: bool = False
    options: List[str] = []
    default_value: Optional[str] = None

class FormTemplate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    template_type: str  # "invoice", "estimate", "sales_receipt", etc.
    is_default: bool = False
    
    # Header Section
    header_layout: Dict[str, Any] = {}
    show_logo: bool = True
    logo_position: str = "left"  # "left", "right", "center"
    
    # Company Information
    show_company_info: bool = True
    company_info_position: str = "top-right"
    
    # Customer Information
    show_customer_info: bool = True
    customer_info_position: str = "top-left"
    
    # Line Items
    line_items_columns: List[str] = ["description", "quantity", "rate", "amount"]
    show_line_item_numbers: bool = True
    
    # Totals Section
    show_subtotal: bool = True
    show_tax: bool = True
    show_total: bool = True
    totals_position: str = "bottom-right"
    
    # Footer Section
    footer_text: Optional[str] = None
    show_terms: bool = True
    show_memo: bool = True
    
    # Custom Fields
    custom_fields: List[CustomField] = []
    
    # Styling
    primary_color: str = "#3B82F6"
    secondary_color: str = "#F3F4F6"
    font_family: str = "Inter"
    font_size: str = "12px"
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class FormTemplateCreate(BaseModel):
    name: str
    template_type: str
    is_default: bool = False
    header_layout: Dict[str, Any] = {}
    show_logo: bool = True
    logo_position: str = "left"
    show_company_info: bool = True
    company_info_position: str = "top-right"
    show_customer_info: bool = True
    customer_info_position: str = "top-left"
    line_items_columns: List[str] = ["description", "quantity", "rate", "amount"]
    show_line_item_numbers: bool = True
    show_subtotal: bool = True
    show_tax: bool = True
    show_total: bool = True
    totals_position: str = "bottom-right"
    footer_text: Optional[str] = None
    show_terms: bool = True
    show_memo: bool = True
    custom_fields: List[CustomField] = []
    primary_color: str = "#3B82F6"
    secondary_color: str = "#F3F4F6"
    font_family: str = "Inter"
    font_size: str = "12px"

class CompanyBranding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company_id: str
    logo_base64: Optional[str] = None
    logo_filename: Optional[str] = None
    logo_mime_type: Optional[str] = None
    company_name: str
    tagline: Optional[str] = None
    primary_color: str = "#3B82F6"
    secondary_color: str = "#F3F4F6"
    font_family: str = "Inter"
    letterhead_template: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CompanyBrandingCreate(BaseModel):
    company_id: str
    logo_base64: Optional[str] = None
    logo_filename: Optional[str] = None
    logo_mime_type: Optional[str] = None
    company_name: str
    tagline: Optional[str] = None
    primary_color: str = "#3B82F6"
    secondary_color: str = "#F3F4F6"
    font_family: str = "Inter"
    letterhead_template: Optional[str] = None

# Phase 4: User Management & Security Models
class Permission(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    module: str  # "accounts", "customers", "transactions", etc.
    actions: List[str] = []  # ["create", "read", "update", "delete"]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PermissionCreate(BaseModel):
    name: str
    description: str
    module: str
    actions: List[str] = []

class UserRole(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    permissions: List[str] = []  # Permission IDs
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserRoleCreate(BaseModel):
    name: str
    description: str
    permissions: List[str] = []
    is_admin: bool = False

class UserSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)

class AuditLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    action: str
    resource_type: str
    resource_id: str
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AuditLogCreate(BaseModel):
    user_id: str
    action: str
    resource_type: str
    resource_id: str
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Phase 5: Advanced Business Logic Models

# Inventory Management Models
class InventoryTransaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    item_id: str
    transaction_type: str  # "purchase", "sale", "adjustment"
    quantity: float
    unit_cost: float
    total_cost: float
    transaction_date: datetime
    reference_transaction_id: Optional[str] = None  # Link to invoice/bill
    lot_number: Optional[str] = None
    expiration_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class InventoryAdjustment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    item_id: str
    adjustment_type: InventoryAdjustmentType
    quantity_before: float
    quantity_after: float
    quantity_change: float
    unit_cost: float
    total_cost_impact: float
    reason: str
    reference_number: Optional[str] = None
    adjusted_by: str  # User ID
    adjustment_date: datetime
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class InventoryAlert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    item_id: str
    alert_type: str  # "reorder", "low_stock", "out_of_stock"
    current_quantity: float
    reorder_point: float
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None

# Payroll & HR Models
class PayPeriod(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    period_type: PayPeriodType
    start_date: datetime
    end_date: datetime
    pay_date: datetime
    is_closed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TimeEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_id: str
    date: datetime
    clock_in: datetime
    clock_out: Optional[datetime] = None
    break_minutes: int = 0
    total_hours: float = 0.0
    regular_hours: float = 0.0
    overtime_hours: float = 0.0
    status: TimeEntryStatus = TimeEntryStatus.DRAFT
    notes: Optional[str] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PayrollItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_id: str
    pay_period_id: str
    regular_hours: float = 0.0
    overtime_hours: float = 0.0
    regular_rate: float = 0.0
    overtime_rate: float = 0.0
    gross_pay: float = 0.0
    federal_income_tax: float = 0.0
    state_income_tax: float = 0.0
    social_security_tax: float = 0.0
    medicare_tax: float = 0.0
    total_deductions: float = 0.0
    net_pay: float = 0.0
    status: PayrollStatus = PayrollStatus.PENDING
    processed_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PayStub(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    payroll_item_id: str
    employee_id: str
    pay_period_id: str
    pay_date: datetime
    earnings: List[Dict[str, Any]] = []  # [{"type": "regular", "hours": 40, "rate": 15.00, "amount": 600.00}]
    deductions: List[Dict[str, Any]] = []  # [{"type": "federal_tax", "amount": 120.00}]
    gross_pay: float = 0.0
    total_deductions: float = 0.0
    net_pay: float = 0.0
    year_to_date_gross: float = 0.0
    year_to_date_deductions: float = 0.0
    year_to_date_net: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaxRate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tax_type: TaxType
    state: Optional[str] = None  # For state taxes
    rate: float  # Percentage rate
    min_income: float = 0.0
    max_income: Optional[float] = None
    effective_date: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Create models for API endpoints
class InventoryTransactionCreate(BaseModel):
    item_id: str
    transaction_type: str
    quantity: float
    unit_cost: float
    transaction_date: datetime
    reference_transaction_id: Optional[str] = None
    lot_number: Optional[str] = None
    expiration_date: Optional[datetime] = None
    notes: Optional[str] = None

class InventoryAdjustmentCreate(BaseModel):
    item_id: str
    adjustment_type: InventoryAdjustmentType
    quantity_after: float
    unit_cost: float
    reason: str
    reference_number: Optional[str] = None
    adjusted_by: str
    adjustment_date: datetime
    notes: Optional[str] = None

class PayPeriodCreate(BaseModel):
    period_type: PayPeriodType
    start_date: datetime
    end_date: datetime
    pay_date: datetime

class TimeEntryCreate(BaseModel):
    employee_id: str
    date: datetime
    clock_in: datetime
    clock_out: Optional[datetime] = None
    break_minutes: int = 0
    notes: Optional[str] = None

class PayrollItemCreate(BaseModel):
    employee_id: str
    pay_period_id: str
    regular_hours: float = 0.0
    overtime_hours: float = 0.0

class TaxRateCreate(BaseModel):
    tax_type: TaxType
    state: Optional[str] = None
    rate: float
    min_income: float = 0.0
    max_income: Optional[float] = None
    effective_date: datetime
security = HTTPBearer()

# Password hashing utilities
def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def generate_session_token() -> str:
    """Generate a secure session token"""
    return secrets.token_urlsafe(32)

# Company endpoints
@api_router.post("/company", response_model=Company)
async def create_company(company: CompanyCreate):
    company_dict = company.dict()
    company_obj = Company(**company_dict)
    await db.companies.insert_one(company_obj.dict())
    return company_obj

@api_router.get("/company", response_model=Company)
async def get_company():
    company = await db.companies.find_one()
    if not company:
        # Return default company
        return Company(name="QBClone", industry="general")
    return Company(**company)

@api_router.put("/company/{company_id}", response_model=Company)
async def update_company(company_id: str, company_update: CompanyCreate):
    company = await db.companies.find_one({"id": company_id})
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    update_data = company_update.dict()
    update_data["updated_at"] = datetime.utcnow()
    
    await db.companies.update_one({"id": company_id}, {"$set": update_data})
    updated_company = await db.companies.find_one({"id": company_id})
    return Company(**updated_company)

# Account endpoints
@api_router.post("/accounts", response_model=Account)
async def create_account(account: AccountCreate):
    account_dict = account.dict()
    account_obj = Account(**account_dict)
    
    # Insert opening balance journal entry if provided
    if account_obj.opening_balance != 0:
        journal_entry = JournalEntry(
            transaction_id=account_obj.id,
            account_id=account_obj.id,
            debit=account_obj.opening_balance if account_obj.account_type in [AccountType.ASSET, AccountType.EXPENSE] else 0,
            credit=account_obj.opening_balance if account_obj.account_type in [AccountType.LIABILITY, AccountType.EQUITY, AccountType.INCOME] else 0,
            description=f"Opening balance for {account_obj.name}",
            date=account_obj.opening_balance_date or datetime.utcnow()
        )
        await db.journal_entries.insert_one(journal_entry.dict())
        account_obj.balance = account_obj.opening_balance
    
    await db.accounts.insert_one(account_obj.dict())
    return account_obj

@api_router.get("/accounts", response_model=List[Account])
async def get_accounts():
    accounts = await db.accounts.find({"active": True}).to_list(1000)
    result = []
    for account in accounts:
        if "_id" in account:
            del account["_id"]
        result.append(Account(**account))
    return result

@api_router.get("/accounts/{account_id}", response_model=Account)
async def get_account(account_id: str):
    account = await db.accounts.find_one({"id": account_id})
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return Account(**account)

@api_router.put("/accounts/{account_id}", response_model=Account)
async def update_account(account_id: str, account_update: AccountCreate):
    account = await db.accounts.find_one({"id": account_id})
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    update_data = account_update.dict()
    update_data["updated_at"] = datetime.utcnow()
    
    await db.accounts.update_one({"id": account_id}, {"$set": update_data})
    updated_account = await db.accounts.find_one({"id": account_id})
    return Account(**updated_account)

@api_router.delete("/accounts/{account_id}")
async def delete_account(account_id: str):
    account = await db.accounts.find_one({"id": account_id})
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    await db.accounts.update_one({"id": account_id}, {"$set": {"active": False}})
    return {"message": "Account deactivated successfully"}

# Customer endpoints
@api_router.post("/customers", response_model=Customer)
async def create_customer(customer: CustomerCreate):
    customer_dict = customer.dict()
    customer_obj = Customer(**customer_dict)
    await db.customers.insert_one(customer_obj.dict())
    return customer_obj

@api_router.get("/customers", response_model=List[Customer])
async def get_customers():
    customers = await db.customers.find({"active": True}).to_list(1000)
    result = []
    for customer in customers:
        if "_id" in customer:
            del customer["_id"]
        result.append(Customer(**customer))
    return result

@api_router.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str):
    customer = await db.customers.find_one({"id": customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return Customer(**customer)

@api_router.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: str, customer_update: CustomerCreate):
    customer = await db.customers.find_one({"id": customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    update_data = customer_update.dict()
    await db.customers.update_one({"id": customer_id}, {"$set": update_data})
    updated_customer = await db.customers.find_one({"id": customer_id})
    return Customer(**updated_customer)

# Vendor endpoints
@api_router.post("/vendors", response_model=Vendor)
async def create_vendor(vendor: VendorCreate):
    vendor_dict = vendor.dict()
    vendor_obj = Vendor(**vendor_dict)
    await db.vendors.insert_one(vendor_obj.dict())
    return vendor_obj

@api_router.get("/vendors", response_model=List[Vendor])
async def get_vendors():
    vendors = await db.vendors.find({"active": True}).to_list(1000)
    result = []
    for vendor in vendors:
        if "_id" in vendor:
            del vendor["_id"]
        result.append(Vendor(**vendor))
    return result

@api_router.get("/vendors/{vendor_id}", response_model=Vendor)
async def get_vendor(vendor_id: str):
    vendor = await db.vendors.find_one({"id": vendor_id})
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return Vendor(**vendor)

@api_router.put("/vendors/{vendor_id}", response_model=Vendor)
async def update_vendor(vendor_id: str, vendor_update: VendorCreate):
    vendor = await db.vendors.find_one({"id": vendor_id})
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    update_data = vendor_update.dict()
    await db.vendors.update_one({"id": vendor_id}, {"$set": update_data})
    updated_vendor = await db.vendors.find_one({"id": vendor_id})
    return Vendor(**updated_vendor)

# Employee endpoints
@api_router.post("/employees", response_model=Employee)
async def create_employee(employee: EmployeeCreate):
    employee_dict = employee.dict()
    employee_obj = Employee(**employee_dict)
    await db.employees.insert_one(employee_obj.dict())
    return employee_obj

@api_router.get("/employees", response_model=List[Employee])
async def get_employees():
    employees = await db.employees.find({"status": {"$ne": "Terminated"}}).to_list(1000)
    return [Employee(**employee) for employee in employees]

@api_router.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: str):
    employee = await db.employees.find_one({"id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return Employee(**employee)

@api_router.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: str, employee_update: EmployeeCreate):
    employee = await db.employees.find_one({"id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = employee_update.dict()
    await db.employees.update_one({"id": employee_id}, {"$set": update_data})
    updated_employee = await db.employees.find_one({"id": employee_id})
    return Employee(**updated_employee)

# Item endpoints
@api_router.post("/items", response_model=Item)
async def create_item(item: ItemCreate):
    item_dict = item.dict()
    item_obj = Item(**item_dict)
    await db.items.insert_one(item_obj.dict())
    return item_obj

@api_router.get("/items", response_model=List[Item])
async def get_items():
    items = await db.items.find({"active": True}).to_list(1000)
    return [Item(**item) for item in items]

@api_router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    item = await db.items.find_one({"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(**item)

@api_router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item_update: ItemCreate):
    item = await db.items.find_one({"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = item_update.dict()
    await db.items.update_one({"id": item_id}, {"$set": update_data})
    updated_item = await db.items.find_one({"id": item_id})
    return Item(**updated_item)

# Class endpoints
@api_router.post("/classes", response_model=Class)
async def create_class(class_obj: ClassCreate):
    class_dict = class_obj.dict()
    class_model = Class(**class_dict)
    await db.classes.insert_one(class_model.dict())
    return class_model

@api_router.get("/classes", response_model=List[Class])
async def get_classes():
    classes = await db.classes.find({"active": True}).to_list(1000)
    return [Class(**class_item) for class_item in classes]

# Location endpoints
@api_router.post("/locations", response_model=Location)
async def create_location(location: LocationCreate):
    location_dict = location.dict()
    location_obj = Location(**location_dict)
    await db.locations.insert_one(location_obj.dict())
    return location_obj

@api_router.get("/locations", response_model=List[Location])
async def get_locations():
    locations = await db.locations.find({"active": True}).to_list(1000)
    return [Location(**location) for location in locations]

# Terms endpoints
@api_router.post("/terms", response_model=Terms)
async def create_terms(terms: TermsCreate):
    terms_dict = terms.dict()
    terms_obj = Terms(**terms_dict)
    await db.terms.insert_one(terms_obj.dict())
    return terms_obj

@api_router.get("/terms", response_model=List[Terms])
async def get_terms():
    terms = await db.terms.find({"active": True}).to_list(1000)
    return [Terms(**term) for term in terms]

# Price Level endpoints
@api_router.post("/price-levels", response_model=PriceLevel)
async def create_price_level(price_level: PriceLevelCreate):
    price_level_dict = price_level.dict()
    price_level_obj = PriceLevel(**price_level_dict)
    await db.price_levels.insert_one(price_level_obj.dict())
    return price_level_obj

@api_router.get("/price-levels", response_model=List[PriceLevel])
async def get_price_levels():
    price_levels = await db.price_levels.find({"active": True}).to_list(1000)
    return [PriceLevel(**price_level) for price_level in price_levels]

# Transaction endpoints
@api_router.post("/transactions", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate):
    transaction_dict = transaction.dict()
    
    # Calculate totals
    subtotal = sum(item.amount for item in transaction.line_items)
    tax_amount = subtotal * transaction.tax_rate / 100
    total = subtotal + tax_amount
    
    transaction_dict.update({
        "subtotal": subtotal,
        "tax_amount": tax_amount,
        "total": total,
        "balance": total,  # Initial balance equals total
        "transaction_number": f"{transaction.transaction_type.value[:3].upper()}-{str(uuid.uuid4())[:8]}"
    })
    
    transaction_obj = Transaction(**transaction_dict)
    await db.transactions.insert_one(transaction_obj.dict())
    
    # Create journal entries for double-entry bookkeeping
    await create_journal_entries(transaction_obj)
    
    return transaction_obj

@api_router.get("/transactions", response_model=List[Transaction])
async def get_transactions():
    transactions = await db.transactions.find().to_list(1000)
    result = []
    for transaction in transactions:
        # Remove MongoDB ObjectId field
        if "_id" in transaction:
            del transaction["_id"]
        result.append(Transaction(**transaction))
    return result

@api_router.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: str):
    transaction = await db.transactions.find_one({"id": transaction_id})
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return Transaction(**transaction)

@api_router.put("/transactions/{transaction_id}", response_model=Transaction)
async def update_transaction(transaction_id: str, transaction_update: TransactionCreate):
    transaction = await db.transactions.find_one({"id": transaction_id})
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    update_data = transaction_update.dict()
    update_data["updated_at"] = datetime.utcnow()
    
    # Recalculate totals
    subtotal = sum(item.amount for item in transaction_update.line_items)
    tax_amount = subtotal * transaction_update.tax_rate / 100
    total = subtotal + tax_amount
    
    update_data.update({
        "subtotal": subtotal,
        "tax_amount": tax_amount,
        "total": total
    })
    
    await db.transactions.update_one({"id": transaction_id}, {"$set": update_data})
    updated_transaction = await db.transactions.find_one({"id": transaction_id})
    return Transaction(**updated_transaction)

# Memorized Transaction endpoints
@api_router.post("/memorized-transactions", response_model=MemorizedTransaction)
async def create_memorized_transaction(memorized_transaction: MemorizedTransactionCreate):
    memorized_transaction_dict = memorized_transaction.dict()
    memorized_transaction_obj = MemorizedTransaction(**memorized_transaction_dict)
    await db.memorized_transactions.insert_one(memorized_transaction_obj.dict())
    return memorized_transaction_obj

@api_router.get("/memorized-transactions", response_model=List[MemorizedTransaction])
async def get_memorized_transactions():
    memorized_transactions = await db.memorized_transactions.find({"active": True}).to_list(1000)
    return [MemorizedTransaction(**mt) for mt in memorized_transactions]

# ToDo endpoints
@api_router.post("/todos", response_model=ToDo)
async def create_todo(todo: ToDoCreate):
    todo_dict = todo.dict()
    todo_obj = ToDo(**todo_dict)
    await db.todos.insert_one(todo_obj.dict())
    return todo_obj

@api_router.get("/todos", response_model=List[ToDo])
async def get_todos():
    todos = await db.todos.find().to_list(1000)
    return [ToDo(**todo) for todo in todos]

@api_router.put("/todos/{todo_id}", response_model=ToDo)
async def update_todo(todo_id: str, todo_update: ToDoCreate):
    todo = await db.todos.find_one({"id": todo_id})
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_data = todo_update.dict()
    await db.todos.update_one({"id": todo_id}, {"$set": update_data})
    updated_todo = await db.todos.find_one({"id": todo_id})
    return ToDo(**updated_todo)

@api_router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    await db.todos.delete_one({"id": todo_id})
    return {"message": "Todo deleted successfully"}

# Audit Trail endpoints
@api_router.get("/audit-trail", response_model=List[AuditEntry])
async def get_audit_trail():
    audit_entries = await db.audit_entries.find().sort("timestamp", -1).to_list(1000)
    return [AuditEntry(**entry) for entry in audit_entries]

# User endpoints - Basic implementation moved to advanced section below

# Role endpoints
@api_router.post("/roles", response_model=Role)
async def create_role(role: RoleCreate):
    role_dict = role.dict()
    role_obj = Role(**role_dict)
    await db.roles.insert_one(role_obj.dict())
    return role_obj

@api_router.get("/roles", response_model=List[Role])
async def get_roles():
    roles = await db.roles.find().to_list(1000)
    return [Role(**role) for role in roles]

# Journal entry endpoints
@api_router.post("/journal-entries", response_model=JournalEntry)
async def create_journal_entry(entry: JournalEntry):
    """Create a single journal entry"""
    await db.journal_entries.insert_one(entry.dict())
    
    # Update account balance
    await update_account_balance(entry.account_id)
    
    return entry

@api_router.get("/journal-entries", response_model=List[JournalEntry])
async def get_journal_entries():
    entries = await db.journal_entries.find().to_list(1000)
    result = []
    for entry in entries:
        if "_id" in entry:
            del entry["_id"]
        result.append(JournalEntry(**entry))
    return result

# Manual Journal Entry for adjustments
class ManualJournalEntry(BaseModel):
    date: datetime
    reference: Optional[str] = None
    memo: Optional[str] = None
    entries: List[Dict[str, Any]]  # List of {"account_id": str, "debit": float, "credit": float, "description": str}

@api_router.post("/manual-journal-entry")
async def create_manual_journal_entry(manual_entry: ManualJournalEntry):
    """Create multiple journal entries for manual adjustments (must be balanced)"""
    # Validate that debits equal credits
    total_debits = sum(entry.get("debit", 0) for entry in manual_entry.entries)
    total_credits = sum(entry.get("credit", 0) for entry in manual_entry.entries)
    
    if abs(total_debits - total_credits) > 0.01:  # Allow for small rounding differences
        raise HTTPException(
            status_code=400, 
            detail=f"Journal entry must be balanced. Debits: ${total_debits:.2f}, Credits: ${total_credits:.2f}"
        )
    
    if len(manual_entry.entries) < 2:
        raise HTTPException(status_code=400, detail="Journal entry must have at least 2 entries")
    
    # Create transaction ID for grouping the entries
    transaction_id = str(uuid.uuid4())
    
    # Create journal entries
    created_entries = []
    for entry_data in manual_entry.entries:
        if entry_data.get("debit", 0) == 0 and entry_data.get("credit", 0) == 0:
            continue  # Skip zero-amount entries
            
        journal_entry = JournalEntry(
            transaction_id=transaction_id,
            account_id=entry_data["account_id"],
            debit=entry_data.get("debit", 0),
            credit=entry_data.get("credit", 0),
            description=entry_data.get("description", manual_entry.memo or "Manual journal entry"),
            date=manual_entry.date
        )
        
        await db.journal_entries.insert_one(journal_entry.dict())
        
        # Update account balance
        await update_account_balance(entry_data["account_id"])
        
        created_entries.append(journal_entry)
    
    # Create a transaction record for audit purposes
    adjustment_transaction = Transaction(
        transaction_type=TransactionType.JOURNAL,
        date=manual_entry.date,
        reference_number=manual_entry.reference,
        memo=manual_entry.memo,
        total=total_debits,  # Use debits as the "total" for journal entries
        status="Posted",
        transaction_number=f"JE-{str(uuid.uuid4())[:8]}"
    )
    
    await db.transactions.insert_one(adjustment_transaction.dict())
    
    return {
        "message": "Manual journal entry created successfully",
        "transaction_id": transaction_id,
        "transaction_number": adjustment_transaction.transaction_number,
        "entries_created": len(created_entries),
        "total_debits": total_debits,
        "total_credits": total_credits,
        "entries": [entry.dict() for entry in created_entries]
    }

# Transfer funds endpoint
class TransferRequest(BaseModel):
    from_account_id: str
    to_account_id: str
    amount: float
    transfer_date: datetime
    reference_number: Optional[str] = None
    memo: Optional[str] = None

@api_router.post("/transfers")
async def transfer_funds(transfer: TransferRequest):
    """Transfer funds between accounts"""
    # Validate accounts exist and are different
    if transfer.from_account_id == transfer.to_account_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same account")
    
    from_account = await db.accounts.find_one({"id": transfer.from_account_id})
    to_account = await db.accounts.find_one({"id": transfer.to_account_id})
    
    if not from_account:
        raise HTTPException(status_code=404, detail="Source account not found")
    if not to_account:
        raise HTTPException(status_code=404, detail="Destination account not found")
    
    if transfer.amount <= 0:
        raise HTTPException(status_code=400, detail="Transfer amount must be positive")
    
    # Create transfer transaction record
    transfer_id = str(uuid.uuid4())
    transfer_transaction = Transaction(
        transaction_type=TransactionType.TRANSFER,
        date=transfer.transfer_date,
        reference_number=transfer.reference_number,
        memo=transfer.memo,
        total=transfer.amount,
        status="Posted",
        transaction_number=f"TRF-{str(uuid.uuid4())[:8]}"
    )
    
    await db.transactions.insert_one(transfer_transaction.dict())
    
    # Create journal entries for the transfer
    from_entry = JournalEntry(
        transaction_id=transfer_id,
        account_id=transfer.from_account_id,
        debit=0,
        credit=transfer.amount,
        description=f"Transfer to {to_account['name']} - {transfer.memo or 'Fund transfer'}",
        date=transfer.transfer_date
    )
    
    to_entry = JournalEntry(
        transaction_id=transfer_id,
        account_id=transfer.to_account_id,
        debit=transfer.amount,
        credit=0,
        description=f"Transfer from {from_account['name']} - {transfer.memo or 'Fund transfer'}",
        date=transfer.transfer_date
    )
    
    await db.journal_entries.insert_one(from_entry.dict())
    await db.journal_entries.insert_one(to_entry.dict())
    
    # Update account balances
    await update_account_balance(transfer.from_account_id)
    await update_account_balance(transfer.to_account_id)
    
    return {
        "message": "Transfer completed successfully", 
        "transfer_id": transfer_id,
        "transaction_number": transfer_transaction.transaction_number,
        "from_account": from_account['name'],
        "to_account": to_account['name'],
        "amount": transfer.amount,
        "date": transfer.transfer_date
    }

# Payment Processing Endpoints
@api_router.post("/payments/receive")
async def receive_payment(
    customer_id: str,
    payment_amount: float,
    payment_method: PaymentMethod,
    payment_date: datetime,
    deposit_to_account_id: str,
    invoice_applications: List[Dict[str, Any]] = [],
    memo: Optional[str] = None
):
    """Apply payment to customer invoices"""
    payment_id = str(uuid.uuid4())
    
    # Create payment transaction
    payment_transaction = Transaction(
        transaction_type=TransactionType.PAYMENT,
        customer_id=customer_id,
        date=payment_date,
        payment_method=payment_method,
        deposit_to_account_id=deposit_to_account_id,
        total=payment_amount,
        memo=memo,
        transaction_number=f"PMT-{str(uuid.uuid4())[:8]}"
    )
    
    await db.transactions.insert_one(payment_transaction.dict())
    
    # Apply payment to invoices
    remaining_payment = payment_amount
    for application in invoice_applications:
        invoice_id = application.get("invoice_id")
        applied_amount = min(application.get("amount", 0), remaining_payment)
        
        if applied_amount > 0:
            # Update invoice status and remaining balance
            invoice = await db.transactions.find_one({"id": invoice_id})
            if invoice:
                new_balance = invoice.get("balance", invoice["total"]) - applied_amount
                await db.transactions.update_one(
                    {"id": invoice_id}, 
                    {"$set": {"balance": new_balance, "status": "Paid" if new_balance <= 0 else "Partial"}}
                )
                remaining_payment -= applied_amount
    
    # Create journal entries for payment
    # Debit Bank/Undeposited Funds, Credit Accounts Receivable
    deposit_account = await db.accounts.find_one({"id": deposit_to_account_id})
    ar_account = await db.accounts.find_one({"detail_type": "Accounts Receivable"})
    
    if deposit_account:
        await db.journal_entries.insert_one(JournalEntry(
            transaction_id=payment_id,
            account_id=deposit_to_account_id,
            debit=payment_amount,
            credit=0,
            description=f"Payment received - {payment_transaction.transaction_number}",
            date=payment_date
        ).dict())
    
    if ar_account:
        await db.journal_entries.insert_one(JournalEntry(
            transaction_id=payment_id,
            account_id=ar_account["id"],
            debit=0,
            credit=payment_amount,
            description=f"Payment received - {payment_transaction.transaction_number}",
            date=payment_date
        ).dict())
    
    # Update customer balance
    customer = await db.customers.find_one({"id": customer_id})
    if customer:
        new_balance = customer.get("balance", 0) - payment_amount
        await db.customers.update_one({"id": customer_id}, {"$set": {"balance": new_balance}})
    
    return {"message": "Payment received successfully", "payment_id": payment_id}

@api_router.post("/payments/pay-bills")
async def pay_bills(
    payment_date: datetime,
    payment_account_id: str,
    payment_method: PaymentMethod,
    bill_payments: List[Dict[str, Any]],
    memo: Optional[str] = None
):
    """Pay multiple vendor bills"""
    payment_id = str(uuid.uuid4())
    total_payment_amount = sum(bp.get("amount", 0) for bp in bill_payments)
    
    # Create payment transaction
    payment_transaction = Transaction(
        transaction_type=TransactionType.PAYMENT,
        date=payment_date,
        payment_method=payment_method,
        deposit_to_account_id=payment_account_id,
        total=total_payment_amount,
        memo=memo,
        transaction_number=f"BPM-{str(uuid.uuid4())[:8]}"
    )
    
    await db.transactions.insert_one(payment_transaction.dict())
    
    # Process each bill payment
    for bill_payment in bill_payments:
        bill_id = bill_payment.get("bill_id")
        payment_amount = bill_payment.get("amount", 0)
        
        # Update bill status
        bill = await db.transactions.find_one({"id": bill_id})
        if bill:
            new_balance = bill.get("balance", bill["total"]) - payment_amount
            await db.transactions.update_one(
                {"id": bill_id}, 
                {"$set": {"balance": new_balance, "status": "Paid" if new_balance <= 0 else "Partial"}}
            )
            
            # Update vendor balance
            vendor_id = bill.get("vendor_id")
            if vendor_id:
                vendor = await db.vendors.find_one({"id": vendor_id})
                if vendor:
                    new_vendor_balance = vendor.get("balance", 0) - payment_amount
                    await db.vendors.update_one({"id": vendor_id}, {"$set": {"balance": new_vendor_balance}})
    
    # Create journal entries
    # Credit Bank Account, Debit Accounts Payable
    payment_account = await db.accounts.find_one({"id": payment_account_id})
    ap_account = await db.accounts.find_one({"detail_type": "Accounts Payable"})
    
    if payment_account:
        await db.journal_entries.insert_one(JournalEntry(
            transaction_id=payment_id,
            account_id=payment_account_id,
            debit=0,
            credit=total_payment_amount,
            description=f"Bill payment - {payment_transaction.transaction_number}",
            date=payment_date
        ).dict())
    
    if ap_account:
        await db.journal_entries.insert_one(JournalEntry(
            transaction_id=payment_id,
            account_id=ap_account["id"],
            debit=total_payment_amount,
            credit=0,
            description=f"Bill payment - {payment_transaction.transaction_number}",
            date=payment_date
        ).dict())
    
    return {"message": "Bills paid successfully", "payment_id": payment_id}

@api_router.post("/deposits")
async def make_deposit(
    deposit_date: datetime,
    deposit_to_account_id: str,
    payment_items: List[Dict[str, Any]],
    memo: Optional[str] = None
):
    """Make bank deposit from undeposited funds"""
    deposit_id = str(uuid.uuid4())
    total_deposit = sum(item.get("amount", 0) for item in payment_items)
    
    # Create deposit transaction
    deposit_transaction = Transaction(
        transaction_type=TransactionType.DEPOSIT,
        date=deposit_date,
        deposit_to_account_id=deposit_to_account_id,
        total=total_deposit,
        memo=memo,
        transaction_number=f"DEP-{str(uuid.uuid4())[:8]}"
    )
    
    await db.transactions.insert_one(deposit_transaction.dict())
    
    # Create journal entries
    # Debit Bank Account, Credit Undeposited Funds
    bank_account = await db.accounts.find_one({"id": deposit_to_account_id})
    undeposited_account = await db.accounts.find_one({"detail_type": "Undeposited Funds"})
    
    if bank_account:
        await db.journal_entries.insert_one(JournalEntry(
            transaction_id=deposit_id,
            account_id=deposit_to_account_id,
            debit=total_deposit,
            credit=0,
            description=f"Bank deposit - {deposit_transaction.transaction_number}",
            date=deposit_date
        ).dict())
    
    if undeposited_account:
        await db.journal_entries.insert_one(JournalEntry(
            transaction_id=deposit_id,
            account_id=undeposited_account["id"],
            debit=0,
            credit=total_deposit,
            description=f"Bank deposit - {deposit_transaction.transaction_number}",
            date=deposit_date
        ).dict())
    
    # Mark deposited items as deposited
    for item in payment_items:
        payment_id = item.get("payment_id")
        if payment_id:
            await db.transactions.update_one(
                {"id": payment_id},
                {"$set": {"status": "Deposited", "deposit_id": deposit_id}}
            )
    
    return {"message": "Deposit completed successfully", "deposit_id": deposit_id}

@api_router.get("/customers/{customer_id}/open-invoices")
async def get_customer_open_invoices(customer_id: str):
    """Get all open invoices for a customer"""
    invoices = await db.transactions.find({
        "customer_id": customer_id,
        "transaction_type": "Invoice",
        "status": {"$in": ["Open", "Partial"]}
    }).to_list(1000)
    
    # Convert to proper Transaction objects and calculate remaining balance
    result = []
    for invoice in invoices:
        # Remove MongoDB ObjectId field
        if "_id" in invoice:
            del invoice["_id"]
        
        # Calculate remaining balance
        if "balance" not in invoice:
            invoice["balance"] = invoice["total"]
        
        # Convert to Transaction object to ensure proper serialization
        transaction_obj = Transaction(**invoice)
        result.append(transaction_obj.dict())
    
    return result

@api_router.get("/vendors/{vendor_id}/open-bills")
async def get_vendor_open_bills(vendor_id: str):
    """Get all open bills for a vendor"""
    bills = await db.transactions.find({
        "vendor_id": vendor_id,
        "transaction_type": "Bill",
        "status": {"$in": ["Open", "Partial"]}
    }).to_list(1000)
    
    # Convert to proper Transaction objects and calculate remaining balance
    result = []
    for bill in bills:
        # Remove MongoDB ObjectId field
        if "_id" in bill:
            del bill["_id"]
        
        # Calculate remaining balance
        if "balance" not in bill:
            bill["balance"] = bill["total"]
        
        # Convert to Transaction object to ensure proper serialization
        transaction_obj = Transaction(**bill)
        result.append(transaction_obj.dict())
    
    return result

@api_router.get("/payments/undeposited")
async def get_undeposited_payments():
    """Get all payments in undeposited funds"""
    payments = await db.transactions.find({
        "transaction_type": "Payment",
        "status": {"$ne": "Deposited"}
    }).to_list(1000)
    
    # Convert to proper Transaction objects for serialization
    result = []
    for payment in payments:
        # Remove MongoDB ObjectId field
        if "_id" in payment:
            del payment["_id"]
        
        # Convert to Transaction object to ensure proper serialization
        transaction_obj = Transaction(**payment)
        result.append(transaction_obj.dict())
    
    return result

# Reports endpoints
@api_router.get("/reports/trial-balance")
async def get_trial_balance():
    accounts = await db.accounts.find({"active": True}).to_list(1000)
    
    trial_balance = []
    total_debits = 0
    total_credits = 0
    
    for account in accounts:
        balance = await calculate_account_balance(account["id"])
        account_data = {
            "account_name": account["name"],
            "account_type": account["account_type"],
            "debit": balance if balance > 0 and account["account_type"] in ["Asset", "Expense"] else 0,
            "credit": abs(balance) if balance < 0 or account["account_type"] in ["Liability", "Equity", "Income"] else 0
        }
        trial_balance.append(account_data)
        total_debits += account_data["debit"]
        total_credits += account_data["credit"]
    
    return {
        "trial_balance": trial_balance,
        "total_debits": total_debits,
        "total_credits": total_credits,
        "balanced": abs(total_debits - total_credits) < 0.01
    }

@api_router.get("/reports/balance-sheet")
async def get_balance_sheet():
    accounts = await db.accounts.find({"active": True}).to_list(1000)
    
    assets = []
    liabilities = []
    equity = []
    
    total_assets = 0
    total_liabilities = 0
    total_equity = 0
    
    for account in accounts:
        balance = await calculate_account_balance(account["id"])
        account_data = {
            "name": account["name"],
            "balance": balance
        }
        
        if account["account_type"] == "Asset":
            assets.append(account_data)
            total_assets += balance
        elif account["account_type"] == "Liability":
            liabilities.append(account_data)
            total_liabilities += balance
        elif account["account_type"] == "Equity":
            equity.append(account_data)
            total_equity += balance
    
    return {
        "assets": assets,
        "liabilities": liabilities,
        "equity": equity,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_equity": total_equity,
        "balanced": abs(total_assets - (total_liabilities + total_equity)) < 0.01
    }

@api_router.get("/reports/income-statement")
async def get_income_statement():
    accounts = await db.accounts.find({"active": True}).to_list(1000)
    
    income = []
    expenses = []
    
    total_income = 0
    total_expenses = 0
    
    for account in accounts:
        balance = await calculate_account_balance(account["id"])
        account_data = {
            "name": account["name"],
            "balance": balance
        }
        
        if account["account_type"] == "Income":
            income.append(account_data)
            total_income += balance
        elif account["account_type"] == "Expense":
            expenses.append(account_data)
            total_expenses += balance
    
    net_income = total_income - total_expenses
    
    return {
        "income": income,
        "expenses": expenses,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_income": net_income
    }

@api_router.get("/reports/ar-aging")
async def get_ar_aging():
    # Get all customers and their invoice balances
    customers = await db.customers.find({"active": True}).to_list(1000)
    invoices = await db.transactions.find({"transaction_type": "Invoice", "status": "Open"}).to_list(1000)
    
    ar_aging = []
    today = datetime.utcnow()
    
    for customer in customers:
        customer_invoices = [inv for inv in invoices if inv.get("customer_id") == customer["id"]]
        
        current = sum(inv["total"] for inv in customer_invoices if (today - inv["date"]).days <= 30)
        days_31_60 = sum(inv["total"] for inv in customer_invoices if 31 <= (today - inv["date"]).days <= 60)
        days_61_90 = sum(inv["total"] for inv in customer_invoices if 61 <= (today - inv["date"]).days <= 90)
        over_90 = sum(inv["total"] for inv in customer_invoices if (today - inv["date"]).days > 90)
        
        total_balance = current + days_31_60 + days_61_90 + over_90
        
        if total_balance > 0:
            ar_aging.append({
                "customer_name": customer["name"],
                "current": current,
                "days_31_60": days_31_60,
                "days_61_90": days_61_90,
                "over_90": over_90,
                "total": total_balance
            })
    
    return {"ar_aging": ar_aging}

@api_router.get("/reports/ap-aging")
async def get_ap_aging():
    # Get all vendors and their bill balances
    vendors = await db.vendors.find({"active": True}).to_list(1000)
    bills = await db.transactions.find({"transaction_type": "Bill", "status": "Open"}).to_list(1000)
    
    ap_aging = []
    today = datetime.utcnow()
    
    for vendor in vendors:
        vendor_bills = [bill for bill in bills if bill.get("vendor_id") == vendor["id"]]
        
        current = sum(bill["total"] for bill in vendor_bills if (today - bill["date"]).days <= 30)
        days_31_60 = sum(bill["total"] for bill in vendor_bills if 31 <= (today - bill["date"]).days <= 60)
        days_61_90 = sum(bill["total"] for bill in vendor_bills if 61 <= (today - bill["date"]).days <= 90)
        over_90 = sum(bill["total"] for bill in vendor_bills if (today - bill["date"]).days > 90)
        
        total_balance = current + days_31_60 + days_61_90 + over_90
        
        if total_balance > 0:
            ap_aging.append({
                "vendor_name": vendor["name"],
                "current": current,
                "days_31_60": days_31_60,
                "days_61_90": days_61_90,
                "over_90": over_90,
                "total": total_balance
            })
    
    return {"ap_aging": ap_aging}

# Enhanced Reports - Phase 3

# Customer/Vendor Aging Details with Drill-down
@api_router.get("/reports/customer-aging-details/{customer_id}")
async def get_customer_aging_details(customer_id: str):
    """Get detailed aging information for a specific customer with drill-down capability"""
    customer = await db.customers.find_one({"id": customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Get all open invoices for this customer
    invoices = await db.transactions.find({
        "customer_id": customer_id,
        "transaction_type": "Invoice",
        "status": "Open"
    }).to_list(1000)
    
    today = datetime.utcnow()
    aging_details = {
        "customer": Customer(**customer),
        "aging_buckets": {
            "current": [],
            "days_31_60": [],
            "days_61_90": [],
            "over_90": []
        },
        "summary": {
            "current_total": 0,
            "days_31_60_total": 0,
            "days_61_90_total": 0,
            "over_90_total": 0,
            "total_outstanding": 0
        }
    }
    
    for invoice in invoices:
        days_overdue = (today - invoice["date"]).days
        invoice_data = {
            "invoice_id": invoice["id"],
            "invoice_number": invoice.get("transaction_number", ""),
            "date": invoice["date"],
            "due_date": invoice.get("due_date"),
            "amount": invoice["total"],
            "balance": invoice.get("balance", invoice["total"]),
            "days_overdue": days_overdue
        }
        
        if days_overdue <= 30:
            aging_details["aging_buckets"]["current"].append(invoice_data)
            aging_details["summary"]["current_total"] += invoice_data["balance"]
        elif 31 <= days_overdue <= 60:
            aging_details["aging_buckets"]["days_31_60"].append(invoice_data)
            aging_details["summary"]["days_31_60_total"] += invoice_data["balance"]
        elif 61 <= days_overdue <= 90:
            aging_details["aging_buckets"]["days_61_90"].append(invoice_data)
            aging_details["summary"]["days_61_90_total"] += invoice_data["balance"]
        else:
            aging_details["aging_buckets"]["over_90"].append(invoice_data)
            aging_details["summary"]["over_90_total"] += invoice_data["balance"]
    
    aging_details["summary"]["total_outstanding"] = (
        aging_details["summary"]["current_total"] +
        aging_details["summary"]["days_31_60_total"] +
        aging_details["summary"]["days_61_90_total"] +
        aging_details["summary"]["over_90_total"]
    )
    
    return aging_details

@api_router.get("/reports/vendor-aging-details/{vendor_id}")
async def get_vendor_aging_details(vendor_id: str):
    """Get detailed aging information for a specific vendor with drill-down capability"""
    vendor = await db.vendors.find_one({"id": vendor_id})
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    # Get all open bills for this vendor
    bills = await db.transactions.find({
        "vendor_id": vendor_id,
        "transaction_type": "Bill",
        "status": "Open"
    }).to_list(1000)
    
    today = datetime.utcnow()
    aging_details = {
        "vendor": Vendor(**vendor),
        "aging_buckets": {
            "current": [],
            "days_31_60": [],
            "days_61_90": [],
            "over_90": []
        },
        "summary": {
            "current_total": 0,
            "days_31_60_total": 0,
            "days_61_90_total": 0,
            "over_90_total": 0,
            "total_outstanding": 0
        }
    }
    
    for bill in bills:
        days_overdue = (today - bill["date"]).days
        bill_data = {
            "bill_id": bill["id"],
            "bill_number": bill.get("transaction_number", ""),
            "date": bill["date"],
            "due_date": bill.get("due_date"),
            "amount": bill["total"],
            "balance": bill.get("balance", bill["total"]),
            "days_overdue": days_overdue
        }
        
        if days_overdue <= 30:
            aging_details["aging_buckets"]["current"].append(bill_data)
            aging_details["summary"]["current_total"] += bill_data["balance"]
        elif 31 <= days_overdue <= 60:
            aging_details["aging_buckets"]["days_31_60"].append(bill_data)
            aging_details["summary"]["days_31_60_total"] += bill_data["balance"]
        elif 61 <= days_overdue <= 90:
            aging_details["aging_buckets"]["days_61_90"].append(bill_data)
            aging_details["summary"]["days_61_90_total"] += bill_data["balance"]
        else:
            aging_details["aging_buckets"]["over_90"].append(bill_data)
            aging_details["summary"]["over_90_total"] += bill_data["balance"]
    
    aging_details["summary"]["total_outstanding"] = (
        aging_details["summary"]["current_total"] +
        aging_details["summary"]["days_31_60_total"] +
        aging_details["summary"]["days_61_90_total"] +
        aging_details["summary"]["over_90_total"]
    )
    
    return aging_details

# Cash Flow Projections
@api_router.get("/reports/cash-flow-projections")
async def get_cash_flow_projections(months: int = 12):
    """Generate cash flow projections based on receivables, payables, and historical data"""
    today = datetime.utcnow()
    
    # Get current cash position
    cash_accounts = await db.accounts.find({
        "detail_type": {"$in": ["Checking", "Savings"]},
        "active": True
    }).to_list(100)
    
    current_cash = 0
    for account in cash_accounts:
        current_cash += await calculate_account_balance(account["id"])
    
    # Get receivables (invoices) 
    invoices = await db.transactions.find({
        "transaction_type": "Invoice",
        "status": "Open"
    }).to_list(1000)
    
    # Get payables (bills)
    bills = await db.transactions.find({
        "transaction_type": "Bill", 
        "status": "Open"
    }).to_list(1000)
    
    # Generate monthly projections
    projections = []
    running_balance = current_cash
    
    for month_offset in range(months):
        month_start = today.replace(day=1) + timedelta(days=32*month_offset)
        month_start = month_start.replace(day=1)
        month_end = month_start.replace(day=calendar.monthrange(month_start.year, month_start.month)[1])
        
        # Calculate expected cash inflows (receivables due this month)
        expected_inflows = 0
        for invoice in invoices:
            due_date = invoice.get("due_date")
            if due_date and month_start <= due_date <= month_end:
                expected_inflows += invoice.get("balance", invoice["total"])
        
        # Calculate expected cash outflows (payables due this month)
        expected_outflows = 0
        for bill in bills:
            due_date = bill.get("due_date")
            if due_date and month_start <= due_date <= month_end:
                expected_outflows += bill.get("balance", bill["total"])
        
        # Calculate historical average for this month (simplified)
        historical_avg_inflow = expected_inflows * 0.8  # 80% collection rate assumption
        historical_avg_outflow = expected_outflows * 0.9  # 90% payment rate assumption
        
        net_cash_flow = historical_avg_inflow - historical_avg_outflow
        running_balance += net_cash_flow
        
        projections.append({
            "month": month_start.strftime("%Y-%m"),
            "month_name": month_start.strftime("%B %Y"),
            "opening_balance": running_balance - net_cash_flow,
            "expected_inflows": expected_inflows,
            "projected_inflows": historical_avg_inflow,
            "expected_outflows": expected_outflows,
            "projected_outflows": historical_avg_outflow,
            "net_cash_flow": net_cash_flow,
            "closing_balance": running_balance
        })
    
    return {
        "current_cash_position": current_cash,
        "total_receivables": sum(inv.get("balance", inv["total"]) for inv in invoices),
        "total_payables": sum(bill.get("balance", bill["total"]) for bill in bills),
        "projections": projections
    }

# Profit & Loss by Class/Location
@api_router.get("/reports/profit-loss-by-class")
async def get_profit_loss_by_class(
    start_date: str = None,
    end_date: str = None
):
    """Generate P&L report segmented by class"""
    # Set default date range if not provided
    if not start_date:
        start_date = datetime.utcnow().replace(day=1).isoformat()
    if not end_date:
        end_date = datetime.utcnow().isoformat()
    
    start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
    end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    
    # Get all classes
    classes = await db.classes.find({"active": True}).to_list(100)
    
    # Get transactions within date range
    transactions = await db.transactions.find({
        "date": {"$gte": start_dt, "$lte": end_dt}
    }).to_list(1000)
    
    # Initialize P&L structure
    pl_by_class = {}
    
    # Add "Unclassified" for transactions without class assignment
    all_classes = [{"id": None, "name": "Unclassified"}] + classes
    
    for class_item in all_classes:
        class_id = class_item["id"]
        class_name = class_item["name"]
        
        pl_by_class[class_name] = {
            "class_id": class_id,
            "class_name": class_name,
            "income": [],
            "expenses": [],
            "total_income": 0,
            "total_expenses": 0,
            "net_income": 0
        }
    
    # Process transactions
    for transaction in transactions:
        for line_item in transaction.get("line_items", []):
            class_id = line_item.get("class_id")
            class_name = next((c["name"] for c in all_classes if c["id"] == class_id), "Unclassified")
            
            if line_item.get("account_id"):
                account = await db.accounts.find_one({"id": line_item["account_id"]})
                if account:
                    amount = line_item.get("amount", 0)
                    
                    if account["account_type"] == "Income":
                        pl_by_class[class_name]["income"].append({
                            "account_name": account["name"],
                            "amount": amount,
                            "transaction_id": transaction["id"],
                            "transaction_type": transaction["transaction_type"],
                            "date": transaction["date"]
                        })
                        pl_by_class[class_name]["total_income"] += amount
                    
                    elif account["account_type"] == "Expense":
                        pl_by_class[class_name]["expenses"].append({
                            "account_name": account["name"],
                            "amount": amount,
                            "transaction_id": transaction["id"],
                            "transaction_type": transaction["transaction_type"],
                            "date": transaction["date"]
                        })
                        pl_by_class[class_name]["total_expenses"] += amount
    
    # Calculate net income for each class
    for class_name in pl_by_class:
        pl_by_class[class_name]["net_income"] = (
            pl_by_class[class_name]["total_income"] - 
            pl_by_class[class_name]["total_expenses"]
        )
    
    # Calculate totals
    total_income = sum(data["total_income"] for data in pl_by_class.values())
    total_expenses = sum(data["total_expenses"] for data in pl_by_class.values())
    total_net_income = total_income - total_expenses
    
    return {
        "report_period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "classes": pl_by_class,
        "totals": {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_income": total_net_income
        }
    }

@api_router.get("/reports/profit-loss-by-location")
async def get_profit_loss_by_location(
    start_date: str = None,
    end_date: str = None
):
    """Generate P&L report segmented by location"""
    # Set default date range if not provided
    if not start_date:
        start_date = datetime.utcnow().replace(day=1).isoformat()
    if not end_date:
        end_date = datetime.utcnow().isoformat()
    
    start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
    end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    
    # Get all locations
    locations = await db.locations.find({"active": True}).to_list(100)
    
    # Get transactions within date range
    transactions = await db.transactions.find({
        "date": {"$gte": start_dt, "$lte": end_dt}
    }).to_list(1000)
    
    # Initialize P&L structure
    pl_by_location = {}
    
    # Add "Unspecified" for transactions without location assignment
    all_locations = [{"id": None, "name": "Unspecified"}] + locations
    
    for location_item in all_locations:
        location_id = location_item["id"]
        location_name = location_item["name"]
        
        pl_by_location[location_name] = {
            "location_id": location_id,
            "location_name": location_name,
            "income": [],
            "expenses": [],
            "total_income": 0,
            "total_expenses": 0,
            "net_income": 0
        }
    
    # Process transactions
    for transaction in transactions:
        for line_item in transaction.get("line_items", []):
            location_id = line_item.get("location_id")
            location_name = next((l["name"] for l in all_locations if l["id"] == location_id), "Unspecified")
            
            if line_item.get("account_id"):
                account = await db.accounts.find_one({"id": line_item["account_id"]})
                if account:
                    amount = line_item.get("amount", 0)
                    
                    if account["account_type"] == "Income":
                        pl_by_location[location_name]["income"].append({
                            "account_name": account["name"],
                            "amount": amount,
                            "transaction_id": transaction["id"],
                            "transaction_type": transaction["transaction_type"],
                            "date": transaction["date"]
                        })
                        pl_by_location[location_name]["total_income"] += amount
                    
                    elif account["account_type"] == "Expense":
                        pl_by_location[location_name]["expenses"].append({
                            "account_name": account["name"],
                            "amount": amount,
                            "transaction_id": transaction["id"],
                            "transaction_type": transaction["transaction_type"],
                            "date": transaction["date"]
                        })
                        pl_by_location[location_name]["total_expenses"] += amount
    
    # Calculate net income for each location
    for location_name in pl_by_location:
        pl_by_location[location_name]["net_income"] = (
            pl_by_location[location_name]["total_income"] - 
            pl_by_location[location_name]["total_expenses"]
        )
    
    # Calculate totals
    total_income = sum(data["total_income"] for data in pl_by_location.values())
    total_expenses = sum(data["total_expenses"] for data in pl_by_location.values())
    total_net_income = total_income - total_expenses
    
    return {
        "report_period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "locations": pl_by_location,
        "totals": {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_income": total_net_income
        }
    }

# Dashboard Analytics API
@api_router.get("/analytics/dashboard-metrics")
async def get_dashboard_metrics():
    """Get real-time dashboard metrics and KPIs"""
    today = datetime.utcnow()
    month_start = today.replace(day=1)
    last_month_start = (month_start - timedelta(days=1)).replace(day=1)
    last_month_end = month_start - timedelta(days=1)
    
    # Get cash position
    cash_accounts = await db.accounts.find({
        "detail_type": {"$in": ["Checking", "Savings"]},
        "active": True
    }).to_list(100)
    
    total_cash = 0
    for account in cash_accounts:
        total_cash += await calculate_account_balance(account["id"])
    
    # Get A/R and A/P
    ar_account = await db.accounts.find_one({"detail_type": "Accounts Receivable"})
    ap_account = await db.accounts.find_one({"detail_type": "Accounts Payable"})
    
    total_ar = await calculate_account_balance(ar_account["id"]) if ar_account else 0
    total_ap = await calculate_account_balance(ap_account["id"]) if ap_account else 0
    
    # Get monthly income and expenses
    current_month_income = 0
    current_month_expenses = 0
    last_month_income = 0
    last_month_expenses = 0
    
    # Current month transactions
    current_month_transactions = await db.transactions.find({
        "date": {"$gte": month_start, "$lte": today}
    }).to_list(1000)
    
    for transaction in current_month_transactions:
        if transaction["transaction_type"] in ["Invoice", "Sales Receipt"]:
            current_month_income += transaction["total"]
        elif transaction["transaction_type"] in ["Bill", "Check"]:
            current_month_expenses += transaction["total"]
    
    # Last month transactions
    last_month_transactions = await db.transactions.find({
        "date": {"$gte": last_month_start, "$lte": last_month_end}
    }).to_list(1000)
    
    for transaction in last_month_transactions:
        if transaction["transaction_type"] in ["Invoice", "Sales Receipt"]:
            last_month_income += transaction["total"]
        elif transaction["transaction_type"] in ["Bill", "Check"]:
            last_month_expenses += transaction["total"]
    
    # Calculate growth rates
    income_growth = ((current_month_income - last_month_income) / last_month_income * 100) if last_month_income > 0 else 0
    expense_growth = ((current_month_expenses - last_month_expenses) / last_month_expenses * 100) if last_month_expenses > 0 else 0
    
    # Get overdue invoices
    overdue_invoices = await db.transactions.find({
        "transaction_type": "Invoice",
        "status": "Open",
        "due_date": {"$lt": today}
    }).to_list(1000)
    
    overdue_amount = sum(inv.get("balance", inv["total"]) for inv in overdue_invoices)
    
    # Get recent transactions
    recent_transactions = await db.transactions.find().sort("created_at", -1).limit(10).to_list(10)
    
    return {
        "financial_metrics": {
            "total_cash": total_cash,
            "total_ar": total_ar,
            "total_ap": total_ap,
            "working_capital": total_ar - total_ap,
            "current_month_income": current_month_income,
            "current_month_expenses": current_month_expenses,
            "current_month_profit": current_month_income - current_month_expenses,
            "income_growth_rate": income_growth,
            "expense_growth_rate": expense_growth
        },
        "alerts": {
            "overdue_invoices_count": len(overdue_invoices),
            "overdue_amount": overdue_amount,
            "cash_flow_status": "positive" if total_cash > 0 else "negative",
            "low_cash_warning": total_cash < 10000  # Configurable threshold
        },
        "recent_activity": [
            {
                "id": t["id"],
                "type": t["transaction_type"],
                "amount": t["total"],
                "date": t["date"],
                "description": t.get("memo", ""),
                "customer": t.get("customer_id", ""),
                "vendor": t.get("vendor_id", "")
            } for t in recent_transactions
        ]
    }

@api_router.get("/analytics/kpi-trends")
async def get_kpi_trends(period: str = "12months"):
    """Get KPI trends over time for dashboard charts"""
    today = datetime.utcnow()
    
    if period == "12months":
        periods = []
        for i in range(12):
            month_start = (today.replace(day=1) - timedelta(days=32*i)).replace(day=1)
            month_end = month_start.replace(day=calendar.monthrange(month_start.year, month_start.month)[1])
            periods.append({
                "start": month_start,
                "end": month_end,
                "label": month_start.strftime("%b %Y")
            })
        periods.reverse()
    
    trends = []
    
    for period_data in periods:
        # Get transactions for this period
        transactions = await db.transactions.find({
            "date": {"$gte": period_data["start"], "$lte": period_data["end"]}
        }).to_list(1000)
        
        income = sum(t["total"] for t in transactions if t["transaction_type"] in ["Invoice", "Sales Receipt"])
        expenses = sum(t["total"] for t in transactions if t["transaction_type"] in ["Bill", "Check"])
        profit = income - expenses
        
        trends.append({
            "period": period_data["label"],
            "income": income,
            "expenses": expenses,
            "profit": profit,
            "transaction_count": len(transactions)
        })
    
    return {"trends": trends}

@api_router.get("/analytics/drill-down/{metric}")
async def get_drill_down_data(metric: str, period: str = "current_month"):
    """Get drill-down data for dashboard metrics"""
    today = datetime.utcnow()
    
    if period == "current_month":
        start_date = today.replace(day=1)
        end_date = today
    elif period == "last_month":
        start_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        end_date = today.replace(day=1) - timedelta(days=1)
    else:
        # Default to current month
        start_date = today.replace(day=1)
        end_date = today
    
    if metric == "income":
        transactions = await db.transactions.find({
            "transaction_type": {"$in": ["Invoice", "Sales Receipt"]},
            "date": {"$gte": start_date, "$lte": end_date}
        }).to_list(1000)
        
        return {
            "metric": "income",
            "period": period,
            "total": sum(t["total"] for t in transactions),
            "transactions": [
                {
                    "id": t["id"],
                    "type": t["transaction_type"],
                    "amount": t["total"],
                    "date": t["date"],
                    "customer_id": t.get("customer_id"),
                    "reference": t.get("reference_number", "")
                } for t in transactions
            ]
        }
    
    elif metric == "expenses":
        transactions = await db.transactions.find({
            "transaction_type": {"$in": ["Bill", "Check"]},
            "date": {"$gte": start_date, "$lte": end_date}
        }).to_list(1000)
        
        return {
            "metric": "expenses",
            "period": period,
            "total": sum(t["total"] for t in transactions),
            "transactions": [
                {
                    "id": t["id"],
                    "type": t["transaction_type"],
                    "amount": t["total"],
                    "date": t["date"],
                    "vendor_id": t.get("vendor_id"),
                    "reference": t.get("reference_number", "")
                } for t in transactions
            ]
        }
    
    elif metric == "overdue_invoices":
        overdue_invoices = await db.transactions.find({
            "transaction_type": "Invoice",
            "status": "Open",
            "due_date": {"$lt": today}
        }).to_list(1000)
        
        return {
            "metric": "overdue_invoices",
            "period": "current",
            "total": sum(inv.get("balance", inv["total"]) for inv in overdue_invoices),
            "count": len(overdue_invoices),
            "invoices": [
                {
                    "id": inv["id"],
                    "invoice_number": inv.get("transaction_number", ""),
                    "customer_id": inv.get("customer_id"),
                    "amount": inv["total"],
                    "balance": inv.get("balance", inv["total"]),
                    "due_date": inv.get("due_date"),
                    "days_overdue": (today - inv.get("due_date", today)).days if inv.get("due_date") else 0
                } for inv in overdue_invoices
            ]
        }
    
    else:
        raise HTTPException(status_code=400, detail="Invalid metric specified")


# Helper functions
async def calculate_account_balance(account_id: str):
    """Calculate the current balance of an account from journal entries"""
    journal_entries = await db.journal_entries.find({"account_id": account_id}).to_list(1000)
    
    balance = 0
    for entry in journal_entries:
        balance += entry.get("debit", 0) - entry.get("credit", 0)
    
    return balance

async def create_journal_entries(transaction: Transaction):
    """Create journal entries for a transaction (double-entry bookkeeping)"""
    entries = []
    
    if transaction.transaction_type == TransactionType.INVOICE:
        # Debit Accounts Receivable, Credit Income accounts
        ar_account = await db.accounts.find_one({"detail_type": "Accounts Receivable"})
        if ar_account:
            entries.append(JournalEntry(
                transaction_id=transaction.id,
                account_id=ar_account["id"],
                debit=transaction.total,
                credit=0,
                description=f"Invoice - {transaction.transaction_number}",
                date=transaction.date
            ))
        
        # Credit each line item's income account
        for item in transaction.line_items:
            if item.account_id:
                entries.append(JournalEntry(
                    transaction_id=transaction.id,
                    account_id=item.account_id,
                    debit=0,
                    credit=item.amount,
                    description=f"Invoice - {item.description}",
                    date=transaction.date
                ))
    
    elif transaction.transaction_type == TransactionType.BILL:
        # Credit Accounts Payable, Debit Expense accounts
        ap_account = await db.accounts.find_one({"detail_type": "Accounts Payable"})
        if ap_account:
            entries.append(JournalEntry(
                transaction_id=transaction.id,
                account_id=ap_account["id"],
                debit=0,
                credit=transaction.total,
                description=f"Bill - {transaction.transaction_number}",
                date=transaction.date
            ))
        
        # Debit each line item's expense account
        for item in transaction.line_items:
            if item.account_id:
                entries.append(JournalEntry(
                    transaction_id=transaction.id,
                    account_id=item.account_id,
                    debit=item.amount,
                    credit=0,
                    description=f"Bill - {item.description}",
                    date=transaction.date
                ))
    
    elif transaction.transaction_type == TransactionType.SALES_RECEIPT:
        # Debit Bank/UF, Credit Income accounts
        deposit_account = await db.accounts.find_one({"id": transaction.deposit_to_account_id})
        if deposit_account:
            entries.append(JournalEntry(
                transaction_id=transaction.id,
                account_id=deposit_account["id"],
                debit=transaction.total,
                credit=0,
                description=f"Sales Receipt - {transaction.transaction_number}",
                date=transaction.date
            ))
        
        # Credit each line item's income account
        for item in transaction.line_items:
            if item.account_id:
                entries.append(JournalEntry(
                    transaction_id=transaction.id,
                    account_id=item.account_id,
                    debit=0,
                    credit=item.amount,
                    description=f"Sales Receipt - {item.description}",
                    date=transaction.date
                ))
    
    elif transaction.transaction_type == TransactionType.PAYMENT:
        # Debit Bank/UF, Credit AR
        deposit_account = await db.accounts.find_one({"id": transaction.deposit_to_account_id})
        ar_account = await db.accounts.find_one({"detail_type": "Accounts Receivable"})
        
        if deposit_account and ar_account:
            entries.append(JournalEntry(
                transaction_id=transaction.id,
                account_id=deposit_account["id"],
                debit=transaction.total,
                credit=0,
                description=f"Payment - {transaction.transaction_number}",
                date=transaction.date
            ))
            
            entries.append(JournalEntry(
                transaction_id=transaction.id,
                account_id=ar_account["id"],
                debit=0,
                credit=transaction.total,
                description=f"Payment - {transaction.transaction_number}",
                date=transaction.date
            ))
    
    elif transaction.transaction_type == TransactionType.CHECK:
        # Credit Bank, Debit Expense accounts
        if transaction.deposit_to_account_id:  # This would be the bank account being debited
            entries.append(JournalEntry(
                transaction_id=transaction.id,
                account_id=transaction.deposit_to_account_id,
                debit=0,
                credit=transaction.total,
                description=f"Check - {transaction.transaction_number}",
                date=transaction.date
            ))
        
        # Debit each line item's expense account
        for item in transaction.line_items:
            if item.account_id:
                entries.append(JournalEntry(
                    transaction_id=transaction.id,
                    account_id=item.account_id,
                    debit=item.amount,
                    credit=0,
                    description=f"Check - {item.description}",
                    date=transaction.date
                ))
    
    # Insert all journal entries
    for entry in entries:
        await db.journal_entries.insert_one(entry.dict())
    
    # Update account balances
    for entry in entries:
        await update_account_balance(entry.account_id)

async def update_account_balance(account_id: str):
    """Update account balance after journal entry"""
    balance = await calculate_account_balance(account_id)
    await db.accounts.update_one({"id": account_id}, {"$set": {"balance": balance}})

# Root endpoint
@api_router.get("/")
async def root():
    return {"message": "QBClone Accounting API", "version": "1.0"}

# Banking and Reconciliation Endpoints

# Bank Transactions endpoints
@api_router.post("/bank-transactions", response_model=BankTransaction)
async def create_bank_transaction(transaction: BankTransactionCreate):
    transaction_dict = transaction.dict()
    transaction_obj = BankTransaction(**transaction_dict)
    await db.bank_transactions.insert_one(transaction_obj.dict())
    return transaction_obj

@api_router.get("/bank-transactions", response_model=List[BankTransaction])
async def get_bank_transactions(account_id: str = Query(None)):
    query = {}
    if account_id:
        query["account_id"] = account_id
    
    transactions = await db.bank_transactions.find(query).to_list(1000)
    result = []
    for transaction in transactions:
        if "_id" in transaction:
            del transaction["_id"]
        result.append(BankTransaction(**transaction))
    return result

@api_router.put("/bank-transactions/{transaction_id}/reconcile")
async def reconcile_bank_transaction(transaction_id: str, reconciliation_id: str = None):
    update_data = {
        "reconciled": True,
        "reconciliation_id": reconciliation_id
    }
    
    result = await db.bank_transactions.update_one(
        {"id": transaction_id}, 
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Bank transaction not found")
    
    return {"message": "Transaction reconciled successfully"}

# Reconciliation endpoints
@api_router.post("/reconciliations", response_model=Reconciliation)
async def create_reconciliation(reconciliation: ReconciliationCreate):
    reconciliation_dict = reconciliation.dict()
    reconciliation_dict["reconciled_balance"] = 0.0  # Will be updated as transactions are reconciled
    reconciliation_obj = Reconciliation(**reconciliation_dict)
    await db.reconciliations.insert_one(reconciliation_obj.dict())
    return reconciliation_obj

@api_router.get("/reconciliations", response_model=List[Reconciliation])
async def get_reconciliations(account_id: str = Query(None)):
    query = {}
    if account_id:
        query["account_id"] = account_id
    
    reconciliations = await db.reconciliations.find(query).sort("created_at", -1).to_list(100)
    result = []
    for reconciliation in reconciliations:
        if "_id" in reconciliation:
            del reconciliation["_id"]
        result.append(Reconciliation(**reconciliation))
    return result

@api_router.get("/reconciliations/{reconciliation_id}", response_model=Reconciliation)
async def get_reconciliation(reconciliation_id: str):
    reconciliation = await db.reconciliations.find_one({"id": reconciliation_id})
    if not reconciliation:
        raise HTTPException(status_code=404, detail="Reconciliation not found")
    return Reconciliation(**reconciliation)

@api_router.put("/reconciliations/{reconciliation_id}")
async def update_reconciliation(reconciliation_id: str, update_data: Dict[str, Any]):
    result = await db.reconciliations.update_one(
        {"id": reconciliation_id}, 
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Reconciliation not found")
    
    updated_reconciliation = await db.reconciliations.find_one({"id": reconciliation_id})
    return Reconciliation(**updated_reconciliation)

@api_router.post("/reconciliations/{reconciliation_id}/complete")
async def complete_reconciliation(reconciliation_id: str):
    reconciliation = await db.reconciliations.find_one({"id": reconciliation_id})
    if not reconciliation:
        raise HTTPException(status_code=404, detail="Reconciliation not found")
    
    # Calculate final reconciled balance
    reconciled_transactions = await db.bank_transactions.find({
        "reconciliation_id": reconciliation_id,
        "reconciled": True
    }).to_list(1000)
    
    reconciled_balance = sum(t.get("amount", 0) for t in reconciled_transactions)
    difference = reconciliation["statement_ending_balance"] - reconciled_balance
    
    status = "Completed" if abs(difference) < 0.01 else "Discrepancy"
    
    update_data = {
        "status": status,
        "reconciled_balance": reconciled_balance,
        "difference": difference,
        "completed_at": datetime.utcnow()
    }
    
    await db.reconciliations.update_one(
        {"id": reconciliation_id}, 
        {"$set": update_data}
    )
    
    return {"message": "Reconciliation completed", "status": status, "difference": difference}

# Bank Import endpoints
@api_router.post("/bank-import/csv/{account_id}")
async def import_csv_bank_statement(account_id: str, file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        # Read CSV content
        contents = await file.read()
        content_str = contents.decode('utf-8')
        
        # Parse CSV
        csv_reader = csv.DictReader(io.StringIO(content_str))
        transactions = []
        errors = []
        
        for row_num, row in enumerate(csv_reader, 1):
            try:
                # Common CSV field mappings - flexible field detection
                date_fields = ['Date', 'Transaction Date', 'date', 'transaction_date']
                desc_fields = ['Description', 'Memo', 'description', 'memo', 'payee']
                amount_fields = ['Amount', 'amount', 'debit', 'credit']
                
                date_str = None
                description = None
                amount = None
                
                # Find date field
                for field in date_fields:
                    if field in row and row[field]:
                        date_str = row[field]
                        break
                
                # Find description field  
                for field in desc_fields:
                    if field in row and row[field]:
                        description = row[field]
                        break
                
                # Find amount field
                for field in amount_fields:
                    if field in row and row[field]:
                        amount_str = row[field].replace('$', '').replace(',', '')
                        amount = float(amount_str)
                        break
                
                if not all([date_str, description, amount is not None]):
                    errors.append(f"Row {row_num}: Missing required fields")
                    continue
                
                # Parse date
                try:
                    transaction_date = datetime.strptime(date_str, '%m/%d/%Y')
                except:
                    try:
                        transaction_date = datetime.strptime(date_str, '%Y-%m-%d')
                    except:
                        errors.append(f"Row {row_num}: Invalid date format")
                        continue
                
                transaction_type = "Credit" if amount > 0 else "Debit"
                
                transactions.append(BankImportTransaction(
                    date=transaction_date,
                    description=description,
                    amount=amount,
                    transaction_type=transaction_type,
                    reference_number=row.get('Reference', ''),
                    check_number=row.get('Check Number', ''),
                    category=row.get('Category', ''),
                    balance=float(row.get('Balance', 0)) if row.get('Balance') else None
                ))
                
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
        
        # Preview mode - return first 10 transactions for user review
        result = BankImportResult(
            total_transactions=len(transactions),
            imported_transactions=0,  # Will be set when actually imported
            duplicate_transactions=0,
            errors=errors,
            preview_transactions=transactions[:10]
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")

@api_router.post("/bank-import/qfx/{account_id}")
async def import_qfx_bank_statement(account_id: str, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.qfx', '.ofx')):
        raise HTTPException(status_code=400, detail="File must be QFX or OFX format")
    
    try:
        # Read QFX/OFX content
        contents = await file.read()
        content_str = contents.decode('utf-8')
        
        transactions = []
        errors = []
        
        # Parse OFX/QFX format (simplified parsing)
        lines = content_str.split('\n')
        current_transaction = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('<STMTTRN>'):
                current_transaction = {}
            elif line.startswith('</STMTTRN>'):
                if current_transaction:
                    try:
                        # Parse transaction date
                        date_str = current_transaction.get('DTPOSTED', '')
                        if len(date_str) >= 8:
                            transaction_date = datetime.strptime(date_str[:8], '%Y%m%d')
                        else:
                            raise ValueError("Invalid date")
                        
                        amount = float(current_transaction.get('TRNAMT', 0))
                        description = current_transaction.get('NAME', '') or current_transaction.get('MEMO', '')
                        
                        transaction_type = "Credit" if amount > 0 else "Debit"
                        
                        transactions.append(BankImportTransaction(
                            date=transaction_date,
                            description=description,
                            amount=amount,
                            transaction_type=transaction_type,
                            reference_number=current_transaction.get('FITID', ''),
                            check_number=current_transaction.get('CHECKNUM', ''),
                            category=current_transaction.get('MEMO', '')
                        ))
                    except Exception as e:
                        errors.append(f"Error parsing transaction: {str(e)}")
            else:
                # Parse individual fields
                if '<' in line and '>' in line:
                    start = line.find('<') + 1
                    end = line.find('>')
                    if start < end:
                        field_name = line[start:end]
                        field_value = line[end+1:].strip()
                        if field_value and not field_value.startswith('<'):
                            current_transaction[field_name] = field_value
        
        result = BankImportResult(
            total_transactions=len(transactions),
            imported_transactions=0,
            duplicate_transactions=0,
            errors=errors,
            preview_transactions=transactions[:10]
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing QFX/OFX file: {str(e)}")

@api_router.post("/bank-import/confirm/{account_id}")
async def confirm_bank_import(account_id: str, transactions: List[BankImportTransaction]):
    try:
        imported_count = 0
        duplicate_count = 0
        errors = []
        
        for transaction in transactions:
            try:
                # Check for duplicates based on date, amount, and description
                existing = await db.bank_transactions.find_one({
                    "account_id": account_id,
                    "date": transaction.date,
                    "amount": transaction.amount,
                    "description": transaction.description
                })
                
                if existing:
                    duplicate_count += 1
                    continue
                
                # Create bank transaction
                bank_transaction = BankTransaction(
                    account_id=account_id,
                    date=transaction.date,
                    description=transaction.description,
                    amount=transaction.amount,
                    transaction_type=transaction.transaction_type,
                    reference_number=transaction.reference_number,
                    check_number=transaction.check_number,
                    memo=transaction.category
                )
                
                await db.bank_transactions.insert_one(bank_transaction.dict())
                imported_count += 1
                
            except Exception as e:
                errors.append(f"Error importing transaction: {str(e)}")
        
        return {
            "imported_transactions": imported_count,
            "duplicate_transactions": duplicate_count,
            "errors": errors,
            "message": f"Successfully imported {imported_count} transactions"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing transactions: {str(e)}")

# Reconciliation Reports
@api_router.get("/reports/reconciliation/{account_id}")
async def get_reconciliation_report(account_id: str, start_date: str = None, end_date: str = None):
    try:
        query = {"account_id": account_id}
        
        if start_date:
            query["statement_date"] = {"$gte": datetime.fromisoformat(start_date)}
        if end_date:
            if "statement_date" in query:
                query["statement_date"]["$lte"] = datetime.fromisoformat(end_date)
            else:
                query["statement_date"] = {"$lte": datetime.fromisoformat(end_date)}
        
        reconciliations = await db.reconciliations.find(query).sort("statement_date", -1).to_list(100)
        
        # Get account information
        account = await db.accounts.find_one({"id": account_id})
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        report_data = {
            "account": Account(**account),
            "reconciliations": [Reconciliation(**r) for r in reconciliations],
            "summary": {
                "total_reconciliations": len(reconciliations),
                "completed_reconciliations": sum(1 for r in reconciliations if r.get("status") == "Completed"),
                "reconciliations_with_discrepancies": sum(1 for r in reconciliations if r.get("status") == "Discrepancy"),
                "average_reconciliation_time": "2.5 days"  # This would be calculated from actual data
            }
        }
        
        return report_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating reconciliation report: {str(e)}")

# Phase 4: Form Customization Endpoints

@api_router.post("/form-templates", response_model=FormTemplate)
async def create_form_template(template: FormTemplateCreate):
    """Create a new form template"""
    template_dict = template.dict()
    template_obj = FormTemplate(**template_dict)
    await db.form_templates.insert_one(template_obj.dict())
    return template_obj

@api_router.get("/form-templates", response_model=List[FormTemplate])
async def get_form_templates(template_type: Optional[str] = None):
    """Get all form templates, optionally filtered by type"""
    query = {}
    if template_type:
        query["template_type"] = template_type
    
    templates = await db.form_templates.find(query).to_list(100)
    result = []
    for template in templates:
        if "_id" in template:
            del template["_id"]
        result.append(FormTemplate(**template))
    return result

@api_router.get("/form-templates/{template_id}", response_model=FormTemplate)
async def get_form_template(template_id: str):
    """Get a specific form template"""
    template = await db.form_templates.find_one({"id": template_id})
    if not template:
        raise HTTPException(status_code=404, detail="Form template not found")
    return FormTemplate(**template)

@api_router.put("/form-templates/{template_id}", response_model=FormTemplate)
async def update_form_template(template_id: str, template_update: FormTemplateCreate):
    """Update a form template"""
    template = await db.form_templates.find_one({"id": template_id})
    if not template:
        raise HTTPException(status_code=404, detail="Form template not found")
    
    update_data = template_update.dict()
    update_data["updated_at"] = datetime.utcnow()
    
    await db.form_templates.update_one({"id": template_id}, {"$set": update_data})
    updated_template = await db.form_templates.find_one({"id": template_id})
    return FormTemplate(**updated_template)

@api_router.delete("/form-templates/{template_id}")
async def delete_form_template(template_id: str):
    """Delete a form template"""
    template = await db.form_templates.find_one({"id": template_id})
    if not template:
        raise HTTPException(status_code=404, detail="Form template not found")
    
    await db.form_templates.delete_one({"id": template_id})
    return {"message": "Form template deleted successfully"}

@api_router.post("/form-templates/{template_id}/set-default")
async def set_default_template(template_id: str):
    """Set a template as default for its type"""
    template = await db.form_templates.find_one({"id": template_id})
    if not template:
        raise HTTPException(status_code=404, detail="Form template not found")
    
    # Remove default flag from other templates of the same type
    await db.form_templates.update_many(
        {"template_type": template["template_type"]}, 
        {"$set": {"is_default": False}}
    )
    
    # Set this template as default
    await db.form_templates.update_one(
        {"id": template_id}, 
        {"$set": {"is_default": True}}
    )
    
    return {"message": "Template set as default successfully"}

# Custom Fields Endpoints
@api_router.post("/custom-fields", response_model=CustomField)
async def create_custom_field(field: CustomFieldCreate):
    """Create a new custom field"""
    field_dict = field.dict()
    field_obj = CustomField(**field_dict)
    await db.custom_fields.insert_one(field_obj.dict())
    return field_obj

@api_router.get("/custom-fields", response_model=List[CustomField])
async def get_custom_fields():
    """Get all custom fields"""
    fields = await db.custom_fields.find({}).to_list(100)
    result = []
    for field in fields:
        if "_id" in field:
            del field["_id"]
        result.append(CustomField(**field))
    return result

@api_router.get("/custom-fields/{field_id}", response_model=CustomField)
async def get_custom_field(field_id: str):
    """Get a specific custom field"""
    field = await db.custom_fields.find_one({"id": field_id})
    if not field:
        raise HTTPException(status_code=404, detail="Custom field not found")
    return CustomField(**field)

@api_router.put("/custom-fields/{field_id}", response_model=CustomField)
async def update_custom_field(field_id: str, field_update: CustomFieldCreate):
    """Update a custom field"""
    field = await db.custom_fields.find_one({"id": field_id})
    if not field:
        raise HTTPException(status_code=404, detail="Custom field not found")
    
    update_data = field_update.dict()
    await db.custom_fields.update_one({"id": field_id}, {"$set": update_data})
    updated_field = await db.custom_fields.find_one({"id": field_id})
    return CustomField(**updated_field)

@api_router.delete("/custom-fields/{field_id}")
async def delete_custom_field(field_id: str):
    """Delete a custom field"""
    field = await db.custom_fields.find_one({"id": field_id})
    if not field:
        raise HTTPException(status_code=404, detail="Custom field not found")
    
    await db.custom_fields.delete_one({"id": field_id})
    return {"message": "Custom field deleted successfully"}

# Company Branding Endpoints
@api_router.post("/company-branding", response_model=CompanyBranding)
async def create_company_branding(branding: CompanyBrandingCreate):
    """Create or update company branding"""
    branding_dict = branding.dict()
    branding_obj = CompanyBranding(**branding_dict)
    
    # Check if branding already exists for this company
    existing = await db.company_branding.find_one({"company_id": branding.company_id})
    if existing:
        # Update existing branding
        branding_dict["updated_at"] = datetime.utcnow()
        await db.company_branding.update_one(
            {"company_id": branding.company_id}, 
            {"$set": branding_dict}
        )
        updated_branding = await db.company_branding.find_one({"company_id": branding.company_id})
        return CompanyBranding(**updated_branding)
    else:
        # Create new branding
        await db.company_branding.insert_one(branding_obj.dict())
        return branding_obj

@api_router.get("/company-branding/{company_id}", response_model=CompanyBranding)
async def get_company_branding(company_id: str):
    """Get company branding"""
    branding = await db.company_branding.find_one({"company_id": company_id})
    if not branding:
        raise HTTPException(status_code=404, detail="Company branding not found")
    return CompanyBranding(**branding)

@api_router.post("/company-branding/{company_id}/upload-logo")
async def upload_company_logo(company_id: str, file: UploadFile = File(...)):
    """Upload company logo"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Read file content and encode as base64
    file_content = await file.read()
    logo_base64 = base64.b64encode(file_content).decode('utf-8')
    
    # Update or create company branding
    branding_data = {
        "company_id": company_id,
        "logo_base64": logo_base64,
        "logo_filename": file.filename,
        "logo_mime_type": file.content_type,
        "updated_at": datetime.utcnow()
    }
    
    existing = await db.company_branding.find_one({"company_id": company_id})
    if existing:
        await db.company_branding.update_one(
            {"company_id": company_id}, 
            {"$set": branding_data}
        )
    else:
        branding_data["company_name"] = "Your Company"
        branding_obj = CompanyBranding(**branding_data)
        await db.company_branding.insert_one(branding_obj.dict())
    
    return {"message": "Logo uploaded successfully", "filename": file.filename}

# Phase 4: User Management & Security Endpoints

@api_router.post("/permissions", response_model=Permission)
async def create_permission(permission: PermissionCreate):
    """Create a new permission"""
    permission_dict = permission.dict()
    permission_obj = Permission(**permission_dict)
    await db.permissions.insert_one(permission_obj.dict())
    return permission_obj

@api_router.get("/permissions", response_model=List[Permission])
async def get_permissions():
    """Get all permissions"""
    permissions = await db.permissions.find({}).to_list(100)
    result = []
    for permission in permissions:
        if "_id" in permission:
            del permission["_id"]
        result.append(Permission(**permission))
    return result

@api_router.post("/user-roles", response_model=UserRole)
async def create_user_role(role: UserRoleCreate):
    """Create a new user role"""
    role_dict = role.dict()
    role_obj = UserRole(**role_dict)
    await db.user_roles.insert_one(role_obj.dict())
    return role_obj

@api_router.get("/user-roles", response_model=List[UserRole])
async def get_user_roles():
    """Get all user roles"""
    roles = await db.user_roles.find({}).to_list(100)
    result = []
    for role in roles:
        if "_id" in role:
            del role["_id"]
        result.append(UserRole(**role))
    return result

@api_router.get("/user-roles/{role_id}", response_model=UserRole)
async def get_user_role(role_id: str):
    """Get a specific user role"""
    role = await db.user_roles.find_one({"id": role_id})
    if not role:
        raise HTTPException(status_code=404, detail="User role not found")
    return UserRole(**role)

@api_router.put("/user-roles/{role_id}", response_model=UserRole)
async def update_user_role(role_id: str, role_update: UserRoleCreate):
    """Update a user role"""
    role = await db.user_roles.find_one({"id": role_id})
    if not role:
        raise HTTPException(status_code=404, detail="User role not found")
    
    update_data = role_update.dict()
    update_data["updated_at"] = datetime.utcnow()
    
    await db.user_roles.update_one({"id": role_id}, {"$set": update_data})
    updated_role = await db.user_roles.find_one({"id": role_id})
    return UserRole(**updated_role)

@api_router.delete("/user-roles/{role_id}")
async def delete_user_role(role_id: str):
    """Delete a user role"""
    role = await db.user_roles.find_one({"id": role_id})
    if not role:
        raise HTTPException(status_code=404, detail="User role not found")
    
    await db.user_roles.delete_one({"id": role_id})
    return {"message": "User role deleted successfully"}

@api_router.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user"""
    # Check if username already exists
    existing_user = await db.users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_dict = user.dict()
    # Hash the password before storing
    password_hash = hash_password(user.password)
    user_dict.pop("password")  # Remove plain password
    user_dict["password_hash"] = password_hash  # Store hashed password
    user_obj = User(**user_dict)
    await db.users.insert_one(user_obj.dict())
    return user_obj

@api_router.get("/users", response_model=List[User])
async def get_users():
    """Get all users"""
    users = await db.users.find({"active": True}).to_list(100)
    result = []
    for user in users:
        if "_id" in user:
            del user["_id"]
        result.append(User(**user))
    return result

@api_router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get a specific user"""
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)

@api_router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: UserCreate):
    """Update a user"""
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.dict()
    await db.users.update_one({"id": user_id}, {"$set": update_data})
    updated_user = await db.users.find_one({"id": user_id})
    return User(**updated_user)

@api_router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    """Delete a user (soft delete)"""
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.users.update_one({"id": user_id}, {"$set": {"active": False}})
    return {"message": "User deactivated successfully"}

# Authentication Endpoints
class LoginRequest(BaseModel):
    username: str
    password: str

@api_router.post("/auth/login")
async def login(login_data: LoginRequest):
    """User login"""
    user = await db.users.find_one({"username": login_data.username, "active": True})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify the password using bcrypt
    if not verify_password(login_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create session token
    session_token = generate_session_token()
    session = UserSession(
        user_id=user["id"],
        session_token=session_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    
    await db.user_sessions.insert_one(session.dict())
    
    # Update last login
    await db.users.update_one({"id": user["id"]}, {"$set": {"last_login": datetime.utcnow()}})
    
    return {
        "user_id": user["id"],
        "username": user["username"],
        "full_name": user["full_name"],
        "role": user["role"],
        "session_token": session_token
    }

@api_router.post("/auth/logout")
async def logout(session_token: str):
    """User logout"""
    await db.user_sessions.delete_one({"session_token": session_token})
    return {"message": "Logged out successfully"}

@api_router.get("/auth/verify")
async def verify_session(session_token: str):
    """Verify user session"""
    session = await db.user_sessions.find_one({
        "session_token": session_token,
        "expires_at": {"$gt": datetime.utcnow()}
    })
    
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    user = await db.users.find_one({"id": session["user_id"], "active": True})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Update last activity
    await db.user_sessions.update_one(
        {"session_token": session_token},
        {"$set": {"last_activity": datetime.utcnow()}}
    )
    
    return {
        "user_id": user["id"],
        "username": user["username"],
        "full_name": user["full_name"],
        "role": user["role"]
    }

# Audit Log Endpoints
@api_router.post("/audit-log", response_model=AuditLog)
async def create_audit_log(audit_log: AuditLogCreate):
    """Create an audit log entry"""
    log_dict = audit_log.dict()
    log_obj = AuditLog(**log_dict)
    await db.audit_logs.insert_one(log_obj.dict())
    return log_obj

@api_router.get("/audit-log", response_model=List[AuditLog])
async def get_audit_logs(
    user_id: Optional[str] = None,
    resource_type: Optional[str] = None,
    action: Optional[str] = None,
    limit: int = 100
):
    """Get audit logs with optional filtering"""
    query = {}
    if user_id:
        query["user_id"] = user_id
    if resource_type:
        query["resource_type"] = resource_type
    if action:
        query["action"] = action
    
    logs = await db.audit_logs.find(query).sort("timestamp", -1).limit(limit).to_list(limit)
    result = []
    for log in logs:
        if "_id" in log:
            del log["_id"]
        result.append(AuditLog(**log))
    return result

@api_router.get("/audit-log/{resource_type}/{resource_id}", response_model=List[AuditLog])
async def get_resource_audit_logs(resource_type: str, resource_id: str):
    """Get audit logs for a specific resource"""
    logs = await db.audit_logs.find({
        "resource_type": resource_type,
        "resource_id": resource_id
    }).sort("timestamp", -1).to_list(100)
    
    result = []
    for log in logs:
        if "_id" in log:
            del log["_id"]
        result.append(AuditLog(**log))
    return result

# Default Permissions Setup
@api_router.post("/setup/default-permissions")
async def setup_default_permissions():
    """Setup default permissions and roles"""
    # Check if permissions already exist
    existing_permissions = await db.permissions.find({}).to_list(1)
    if existing_permissions:
        return {"message": "Default permissions already exist"}
    
    # Create default permissions
    default_permissions = [
        Permission(name="accounts_read", description="Read accounts", module="accounts", actions=["read"]),
        Permission(name="accounts_write", description="Write accounts", module="accounts", actions=["create", "update", "delete"]),
        Permission(name="customers_read", description="Read customers", module="customers", actions=["read"]),
        Permission(name="customers_write", description="Write customers", module="customers", actions=["create", "update", "delete"]),
        Permission(name="vendors_read", description="Read vendors", module="vendors", actions=["read"]),
        Permission(name="vendors_write", description="Write vendors", module="vendors", actions=["create", "update", "delete"]),
        Permission(name="transactions_read", description="Read transactions", module="transactions", actions=["read"]),
        Permission(name="transactions_write", description="Write transactions", module="transactions", actions=["create", "update", "delete"]),
        Permission(name="reports_read", description="Read reports", module="reports", actions=["read"]),
        Permission(name="banking_read", description="Read banking", module="banking", actions=["read"]),
        Permission(name="banking_write", description="Write banking", module="banking", actions=["create", "update", "delete"]),
        Permission(name="admin_full", description="Full admin access", module="admin", actions=["create", "read", "update", "delete"]),
    ]
    
    for permission in default_permissions:
        await db.permissions.insert_one(permission.dict())
    
    # Create default roles
    admin_permissions = [p.id for p in default_permissions]
    user_permissions = [p.id for p in default_permissions if p.name.endswith("_read")]
    
    default_roles = [
        UserRole(name="Administrator", description="Full system access", permissions=admin_permissions, is_admin=True),
        UserRole(name="Accountant", description="Full accounting access", permissions=admin_permissions[:-1]),
        UserRole(name="User", description="Basic user access", permissions=user_permissions),
    ]
    
    for role in default_roles:
        await db.user_roles.insert_one(role.dict())
    
    return {"message": "Default permissions and roles created successfully"}

# Add the router to the app
app.include_router(api_router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()