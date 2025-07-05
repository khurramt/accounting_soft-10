from fastapi import FastAPI, APIRouter, HTTPException, Query, UploadFile, File
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
    payment_method: Optional[PaymentMethod] = None
    deposit_to_account_id: Optional[str] = None
    memo: Optional[str] = None
    status: str = "Open"  # Open, Paid, Voided, etc.
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
    return [Account(**account) for account in accounts]

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
    return [Customer(**customer) for customer in customers]

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
    return [Vendor(**vendor) for vendor in vendors]

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
    return [Transaction(**transaction) for transaction in transactions]

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

# User endpoints
@api_router.post("/users", response_model=User)
async def create_user(user: UserCreate):
    user_dict = user.dict()
    user_dict.pop("password")  # Remove password from stored data (should be hashed)
    user_obj = User(**user_dict)
    await db.users.insert_one(user_obj.dict())
    return user_obj

@api_router.get("/users", response_model=List[User])
async def get_users():
    users = await db.users.find({"active": True}).to_list(1000)
    return [User(**user) for user in users]

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
    return [JournalEntry(**entry) for entry in entries]

# Transfer funds endpoint
@api_router.post("/transfers")
async def transfer_funds(
    from_account_id: str,
    to_account_id: str,
    amount: float,
    date: datetime,
    memo: Optional[str] = None
):
    # Create transfer transaction
    transfer_id = str(uuid.uuid4())
    
    # Create journal entries for the transfer
    from_entry = JournalEntry(
        transaction_id=transfer_id,
        account_id=from_account_id,
        debit=0,
        credit=amount,
        description=f"Transfer to account {to_account_id}",
        date=date
    )
    
    to_entry = JournalEntry(
        transaction_id=transfer_id,
        account_id=to_account_id,
        debit=amount,
        credit=0,
        description=f"Transfer from account {from_account_id}",
        date=date
    )
    
    await db.journal_entries.insert_one(from_entry.dict())
    await db.journal_entries.insert_one(to_entry.dict())
    
    # Update account balances
    await update_account_balance(from_account_id)
    await update_account_balance(to_account_id)
    
    return {"message": "Transfer completed successfully", "transfer_id": transfer_id}

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
    
    # Calculate remaining balance for each bill
    for bill in bills:
        if "balance" not in bill:
            bill["balance"] = bill["total"]
    
    return bills

@api_router.get("/payments/undeposited")
async def get_undeposited_payments():
    """Get all payments in undeposited funds"""
    payments = await db.transactions.find({
        "transaction_type": "Payment",
        "status": {"$ne": "Deposited"}
    }).to_list(1000)
    
    return payments

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