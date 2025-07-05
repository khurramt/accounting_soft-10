import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ReportsCenter = () => {
  const [selectedCategory, setSelectedCategory] = useState('financial');
  const [selectedReport, setSelectedReport] = useState(null);
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [customers, setCustomers] = useState([]);
  const [vendors, setVendors] = useState([]);
  const [selectedCustomer, setSelectedCustomer] = useState('');
  const [selectedVendor, setSelectedVendor] = useState('');
  const [drillDownMode, setDrillDownMode] = useState(false);
  const [filters, setFilters] = useState({
    dateFrom: '',
    dateTo: '',
    customer: '',
    vendor: '',
    account: '',
    class: '',
    location: ''
  });

  // Fetch customers and vendors for drill-down reports
  useEffect(() => {
    const fetchCustomersAndVendors = async () => {
      try {
        const [customersResponse, vendorsResponse] = await Promise.all([
          axios.get(`${API}/customers`),
          axios.get(`${API}/vendors`)
        ]);
        setCustomers(customersResponse.data);
        setVendors(vendorsResponse.data);
      } catch (error) {
        console.error('Error fetching customers/vendors:', error);
      }
    };
    
    fetchCustomersAndVendors();
  }, []);

  // Handle drill-down for customer aging details
  const loadCustomerAgingDetails = async (customerId) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/reports/customer-aging-details/${customerId}`);
      setReportData({ ...response.data, type: 'customer-aging-details' });
      setDrillDownMode(true);
    } catch (error) {
      console.error('Error loading customer aging details:', error);
      setReportData(null);
    } finally {
      setLoading(false);
    }
  };

  // Handle drill-down for vendor aging details
  const loadVendorAgingDetails = async (vendorId) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/reports/vendor-aging-details/${vendorId}`);
      setReportData({ ...response.data, type: 'vendor-aging-details' });
      setDrillDownMode(true);
    } catch (error) {
      console.error('Error loading vendor aging details:', error);
      setReportData(null);
    } finally {
      setLoading(false);
    }
  };

  // Handle drill-down for dashboard metrics
  const loadDrillDownData = async (metric, period = 'current_month') => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/analytics/drill-down/${metric}?period=${period}`);
      setReportData({ ...response.data, type: 'drill-down', originalMetric: metric });
      setDrillDownMode(true);
    } catch (error) {
      console.error('Error loading drill-down data:', error);
      setReportData(null);
    } finally {
      setLoading(false);
    }
  };

  const reportCategories = {
    financial: {
      name: 'Financial Statements',
      icon: '📊',
      reports: [
        { 
          id: 'trial-balance', 
          name: 'Trial Balance', 
          description: 'Lists all accounts with their debit and credit balances',
          icon: '⚖️'
        },
        { 
          id: 'balance-sheet', 
          name: 'Balance Sheet', 
          description: 'Shows assets, liabilities, and equity at a point in time',
          icon: '📈'
        },
        { 
          id: 'income-statement', 
          name: 'Profit & Loss', 
          description: 'Shows income and expenses over a period',
          icon: '💰'
        },
        { 
          id: 'cash-flow-projections', 
          name: 'Cash Flow Projections', 
          description: 'Projects future cash flows based on receivables and payables',
          icon: '💧'
        }
      ]
    },
    enhanced: {
      name: 'Enhanced Analytics',
      icon: '🔍',
      reports: [
        { 
          id: 'profit-loss-by-class', 
          name: 'P&L by Class', 
          description: 'Profit & Loss report segmented by class for detailed analysis',
          icon: '📊'
        },
        { 
          id: 'profit-loss-by-location', 
          name: 'P&L by Location', 
          description: 'Profit & Loss report segmented by location for performance tracking',
          icon: '📍'
        },
        { 
          id: 'dashboard-metrics', 
          name: 'Dashboard Analytics', 
          description: 'Real-time KPIs and business intelligence metrics',
          icon: '📈'
        },
        { 
          id: 'kpi-trends', 
          name: 'KPI Trends', 
          description: 'Historical trends and performance indicators over time',
          icon: '📉'
        }
      ]
    },
    sales: {
      name: 'Sales Reports',
      icon: '📈',
      reports: [
        { 
          id: 'sales-summary', 
          name: 'Sales Summary', 
          description: 'Summary of sales by customer, item, or period',
          icon: '🛍️'
        },
        { 
          id: 'ar-aging', 
          name: 'A/R Aging Summary', 
          description: 'Shows outstanding customer balances by age',
          icon: '📅'
        },
        { 
          id: 'ar-aging-details', 
          name: 'A/R Aging Details', 
          description: 'Detailed customer aging with drill-down capabilities',
          icon: '🔍'
        },
        { 
          id: 'customer-balance', 
          name: 'Customer Balance Summary', 
          description: 'Current balances for all customers',
          icon: '👥'
        },
        { 
          id: 'invoice-list', 
          name: 'Invoice List', 
          description: 'Detailed list of all invoices',
          icon: '📄'
        }
      ]
    },
    purchases: {
      name: 'Purchase Reports',
      icon: '🛒',
      reports: [
        { 
          id: 'purchase-summary', 
          name: 'Purchase Summary', 
          description: 'Summary of purchases by vendor or item',
          icon: '📦'
        },
        { 
          id: 'ap-aging', 
          name: 'A/P Aging Summary', 
          description: 'Shows outstanding vendor balances by age',
          icon: '📋'
        },
        { 
          id: 'ap-aging-details', 
          name: 'A/P Aging Details', 
          description: 'Detailed vendor aging with drill-down capabilities',
          icon: '🔍'
        },
        { 
          id: 'vendor-balance', 
          name: 'Vendor Balance Summary', 
          description: 'Current balances for all vendors',
          icon: '🏢'
        },
        { 
          id: 'bill-list', 
          name: 'Bill List', 
          description: 'Detailed list of all bills',
          icon: '🧾'
        }
      ]
    },
    inventory: {
      name: 'Inventory Reports',
      icon: '📦',
      reports: [
        { 
          id: 'inventory-valuation', 
          name: 'Inventory Valuation', 
          description: 'Current value of inventory on hand',
          icon: '💎'
        },
        { 
          id: 'stock-status', 
          name: 'Stock Status by Item', 
          description: 'Quantity on hand for each inventory item',
          icon: '📊'
        },
        { 
          id: 'inventory-turnover', 
          name: 'Inventory Turnover', 
          description: 'How quickly inventory is sold',
          icon: '🔄'
        }
      ]
    },
    employees: {
      name: 'Employee Reports',
      icon: '👥',
      reports: [
        { 
          id: 'payroll-summary', 
          name: 'Payroll Summary', 
          description: 'Summary of payroll by employee or period',
          icon: '💰'
        },
        { 
          id: 'employee-list', 
          name: 'Employee List', 
          description: 'List of all employees with contact info',
          icon: '📋'
        },
        { 
          id: 'time-tracking', 
          name: 'Time Tracking Summary', 
          description: 'Employee time tracking and productivity',
          icon: '⏰'
        }
      ]
    }
  };

  const loadReport = async (reportId) => {
    setLoading(true);
    try {
      let response;
      
      // Handle different report types and their API endpoints
      switch (reportId) {
        case 'trial-balance':
        case 'balance-sheet':
        case 'income-statement':
        case 'ar-aging':
        case 'ap-aging':
          response = await axios.get(`${API}/reports/${reportId}`, {
            params: filters
          });
          break;
        
        case 'cash-flow-projections':
          response = await axios.get(`${API}/reports/cash-flow-projections?months=12`);
          break;
        
        case 'profit-loss-by-class':
          response = await axios.get(`${API}/reports/profit-loss-by-class`, {
            params: {
              start_date: filters.dateFrom,
              end_date: filters.dateTo
            }
          });
          break;
        
        case 'profit-loss-by-location':
          response = await axios.get(`${API}/reports/profit-loss-by-location`, {
            params: {
              start_date: filters.dateFrom,
              end_date: filters.dateTo
            }
          });
          break;
        
        case 'dashboard-metrics':
          response = await axios.get(`${API}/analytics/dashboard-metrics`);
          break;
        
        case 'kpi-trends':
          response = await axios.get(`${API}/analytics/kpi-trends?period=12months`);
          break;
        
        case 'ar-aging-details':
          // This will show a customer selection interface first
          setReportData({ type: 'customer-selection', customers: [] });
          return;
        
        case 'ap-aging-details':
          // This will show a vendor selection interface first
          setReportData({ type: 'vendor-selection', vendors: [] });
          return;
        
        default:
          // For other reports, use the generic endpoint
          response = await axios.get(`${API}/reports/${reportId}`, {
            params: filters
          });
      }
      
      setReportData(response.data);
    } catch (error) {
      console.error('Error loading report:', error);
      setReportData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedReport) {
      loadReport(selectedReport.id);
    }
  }, [selectedReport, filters]);

  const exportReport = (format) => {
    // Implementation for export functionality
    console.log(`Exporting report in ${format} format`);
  };

  return (
    <div className="h-[calc(100vh-200px)] flex bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Reports Navigation */}
      <div className="w-80 border-r border-gray-200 flex flex-col">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">Reports Center</h2>
          <p className="text-gray-600 mt-1">Generate business insights and financial reports</p>
        </div>

        <div className="flex-1 overflow-y-auto p-4">
          {Object.entries(reportCategories).map(([categoryId, category]) => (
            <div key={categoryId} className="mb-6">
              <button
                onClick={() => setSelectedCategory(categoryId)}
                className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-all ${
                  selectedCategory === categoryId
                    ? 'bg-blue-100 text-blue-700'
                    : 'hover:bg-gray-100 text-gray-700'
                }`}
              >
                <span className="text-xl">{category.icon}</span>
                <span className="font-medium">{category.name}</span>
              </button>

              {selectedCategory === categoryId && (
                <div className="mt-2 ml-6 space-y-1">
                  {category.reports.map((report) => (
                    <button
                      key={report.id}
                      onClick={() => setSelectedReport(report)}
                      className={`w-full text-left p-3 rounded-lg transition-all ${
                        selectedReport?.id === report.id
                          ? 'bg-blue-50 border border-blue-200'
                          : 'hover:bg-gray-50'
                      }`}
                    >
                      <div className="flex items-start space-x-3">
                        <span className="text-lg mt-0.5">{report.icon}</span>
                        <div>
                          <div className="font-medium text-gray-900">{report.name}</div>
                          <div className="text-xs text-gray-500 mt-1">{report.description}</div>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Report Content */}
      <div className="flex-1 flex flex-col">
        {selectedReport ? (
          <>
            {/* Report Header */}
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{selectedReport.icon}</span>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{selectedReport.name}</h3>
                    <p className="text-gray-600">{selectedReport.description}</p>
                  </div>
                </div>
                
                <div className="flex space-x-2">
                  <button
                    onClick={() => loadReport(selectedReport.id)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    disabled={loading}
                  >
                    🔄 Refresh
                  </button>
                  <div className="relative">
                    <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                      📤 Export ▼
                    </button>
                    {/* Export dropdown would go here */}
                  </div>
                </div>
              </div>

              {/* Filters */}
              <div className="mt-6 grid grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">From Date</label>
                  <input
                    type="date"
                    value={filters.dateFrom}
                    onChange={(e) => setFilters(prev => ({ ...prev, dateFrom: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">To Date</label>
                  <input
                    type="date"
                    value={filters.dateTo}
                    onChange={(e) => setFilters(prev => ({ ...prev, dateTo: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Customer</label>
                  <select
                    value={filters.customer}
                    onChange={(e) => setFilters(prev => ({ ...prev, customer: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">All Customers</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Account</label>
                  <select
                    value={filters.account}
                    onChange={(e) => setFilters(prev => ({ ...prev, account: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">All Accounts</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Report Data */}
            <div className="flex-1 overflow-y-auto p-6">
              {loading ? (
                <div className="flex items-center justify-center h-64">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading report...</p>
                  </div>
                </div>
              ) : reportData ? (
                <div className="space-y-6">
                  {/* Report content based on type */}
                  {selectedReport.id === 'trial-balance' && reportData.trial_balance && (
                    <div>
                      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                        <table className="w-full">
                          <thead className="bg-gray-50">
                            <tr>
                              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Account Name
                              </th>
                              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Debit
                              </th>
                              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Credit
                              </th>
                            </tr>
                          </thead>
                          <tbody className="bg-white divide-y divide-gray-200">
                            {reportData.trial_balance.map((account, index) => (
                              <tr key={index} className="hover:bg-gray-50">
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                  {account.account_name}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                                  ${account.debit.toLocaleString()}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                                  ${account.credit.toLocaleString()}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                          <tfoot className="bg-gray-50">
                            <tr className="border-t-2 border-gray-300">
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">
                                Total
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900 text-right">
                                ${reportData.total_debits.toLocaleString()}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900 text-right">
                                ${reportData.total_credits.toLocaleString()}
                              </td>
                            </tr>
                          </tfoot>
                        </table>
                      </div>
                      
                      <div className={`mt-4 p-4 rounded-lg ${
                        reportData.balanced ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
                      }`}>
                        <div className={`flex items-center space-x-2 ${
                          reportData.balanced ? 'text-green-700' : 'text-red-700'
                        }`}>
                          <span className="text-lg">
                            {reportData.balanced ? '✅' : '❌'}
                          </span>
                          <span className="font-medium">
                            {reportData.balanced ? 'Books are balanced' : 'Books are not balanced'}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Other report types would be implemented similarly */}
                  {selectedReport.id !== 'trial-balance' && (
                    <div className="bg-gray-50 p-8 rounded-lg text-center">
                      <div className="text-4xl mb-4">{selectedReport.icon}</div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">{selectedReport.name}</h3>
                      <p className="text-gray-600">This report is being developed and will be available soon.</p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="bg-gray-50 p-8 rounded-lg text-center">
                  <div className="text-4xl mb-4">📊</div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">No Data Available</h3>
                  <p className="text-gray-600">No data found for the selected filters and date range.</p>
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <div className="text-6xl mb-4">📊</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Select a Report</h3>
              <p className="text-gray-600">Choose a report from the categories on the left to get started.</p>
              <p className="text-sm text-gray-500 mt-2">
                Reports help you understand your business performance and make informed decisions.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ReportsCenter;