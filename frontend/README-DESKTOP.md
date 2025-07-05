# QBClone Desktop Application

QBClone is now available as a desktop application for Windows! This desktop version provides all the functionality of the web application with the convenience of a native desktop experience.

## Features

✅ **Complete Accounting Suite**
- Chart of Accounts Management
- Customer & Vendor Management
- Invoice and Bill Management
- Financial Reporting (Trial Balance, Balance Sheet, Income Statement)
- Banking & Reconciliation
- Payroll & HR Management
- Inventory Management with FIFO/LIFO/Average costing

✅ **Desktop Experience**
- Native Windows application
- Professional accounting software interface
- Offline data entry (connects to remote server for data sync)
- Native file dialogs and system integration

✅ **Enterprise Features**
- User Management & Role-based Access Control
- Audit Trail & Compliance
- Custom Fields & Form Templates
- Company Branding
- Advanced Reporting & Analytics

## Installation

### Prerequisites
- Windows 10 or later (64-bit)
- Internet connection (for connecting to QBClone server)

### Quick Start

1. **Download the Installer**
   - Download `QBClone-Setup-1.0.0.exe` from the releases
   
2. **Install the Application**
   - Run the installer
   - Follow the installation wizard
   - Choose installation directory
   - Create desktop shortcut (recommended)

3. **Launch QBClone**
   - Double-click the desktop shortcut or
   - Find "QBClone Accounting" in Start Menu

4. **Setup Your Company**
   - Follow the welcome wizard to set up your company
   - Configure your chart of accounts
   - Start managing your accounting!

## Development

### Building from Source

```bash
# Clone the repository
git clone <repository-url>
cd qbclone/frontend

# Install dependencies
yarn install

# Build the React application
yarn build

# Build the desktop application
yarn build-electron
```

### Development Mode

```bash
# Start the React development server
yarn start

# In another terminal, start Electron in development mode
yarn electron-dev
```

## Configuration

### Server Connection
The desktop app connects to your QBClone server instance. The server URL is configured in the `.env` file:

```
REACT_APP_BACKEND_URL=https://your-server-url.com
```

### Features
All features from the web version are available:
- **Dashboard**: Real-time financial metrics and insights
- **Chart of Accounts**: Complete account management
- **Customers & Vendors**: Contact and relationship management
- **Transactions**: All transaction types (invoices, bills, payments)
- **Banking**: Bank reconciliation and transaction import
- **Reports**: Comprehensive financial reporting suite
- **Payroll**: Employee management and payroll processing
- **Inventory**: Advanced inventory management with multiple costing methods

## Architecture

- **Frontend**: React 19 with Tailwind CSS
- **Desktop Framework**: Electron
- **Backend**: FastAPI (Python) with MongoDB
- **Packaging**: Electron Builder for Windows

## System Requirements

- **OS**: Windows 10 (64-bit) or later
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB for application, additional space for data
- **Network**: Internet connection for server communication

## Support

For technical support or questions:
- Check the documentation
- Submit issues on GitHub
- Contact support team

## Version History

### v1.0.0 (Current)
- Initial desktop release
- Complete accounting feature set
- Windows installer
- Professional UI/UX
- Server connectivity

---

**QBClone Desktop** - Professional accounting software for small and medium businesses.