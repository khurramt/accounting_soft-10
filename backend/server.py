from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from enum import Enum
from decimal import Decimal

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
    BILL = "Bill"
    PAYMENT = "Payment"
    JOURNAL = "Journal"

class AccountDetailType(str, Enum):
    # Assets
    CHECKING = "Checking"
    SAVINGS = "Savings"
    ACCOUNTS_RECEIVABLE = "Accounts Receivable"
    INVENTORY = "Inventory"
    FIXED_ASSETS = "Fixed Assets"
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

# Data Models
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

class LineItem(BaseModel):
    description: str
    quantity: float = 1.0
    rate: float = 0.0
    amount: float = 0.0
    account_id: str

class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    transaction_type: TransactionType
    transaction_number: Optional[str] = None
    customer_id: Optional[str] = None
    vendor_id: Optional[str] = None
    date: datetime
    due_date: Optional[datetime] = None
    line_items: List[LineItem] = []
    subtotal: float = 0.0
    tax_rate: float = 0.0
    tax_amount: float = 0.0
    total: float = 0.0
    memo: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TransactionCreate(BaseModel):
    transaction_type: TransactionType
    customer_id: Optional[str] = None
    vendor_id: Optional[str] = None
    date: datetime
    due_date: Optional[datetime] = None
    line_items: List[LineItem] = []
    tax_rate: float = 0.0
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

# Account endpoints
@api_router.post("/accounts", response_model=Account)
async def create_account(account: AccountCreate):
    account_dict = account.dict()
    account_obj = Account(**account_dict)
    
    # Insert opening balance journal entry if provided
    if account_obj.opening_balance != 0:
        # Create journal entry for opening balance
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

# Journal entry endpoints
@api_router.get("/journal-entries", response_model=List[JournalEntry])
async def get_journal_entries():
    entries = await db.journal_entries.find().to_list(1000)
    return [JournalEntry(**entry) for entry in entries]

# Reports endpoints
@api_router.get("/reports/trial-balance")
async def get_trial_balance():
    # Get all accounts with their balances
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
            entries.append(JournalEntry(
                transaction_id=transaction.id,
                account_id=item.account_id,
                debit=item.amount,
                credit=0,
                description=f"Bill - {item.description}",
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