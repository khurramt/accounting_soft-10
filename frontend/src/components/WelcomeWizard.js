import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const WelcomeWizard = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    // Step 1: Business Type
    business_type: '',
    business_structure: '',
    primary_activity: '',
    
    // Step 2: Company Information (Enhanced)
    company_name: '',
    legal_name: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    country: 'United States',
    phone: '',
    fax: '',
    email: '',
    website: '',
    ein: '',
    state_of_incorporation: '',
    business_start_date: '',
    fiscal_year_end: 'December',
    
    // Step 3: Business Preferences
    accounting_method: 'Accrual',
    track_inventory: false,
    have_employees: false,
    use_sales_tax: false,
    preferred_currency: 'USD',
    track_time: false,
    use_classes: false,
    use_locations: false,
    
    // Step 4: Chart of Accounts
    chart_template: 'general',
    customize_accounts: false,
    custom_accounts: [],
    
    // Step 5: Tax & Financial Settings
    tax_id: '',
    sales_tax_agency: '',
    default_bank_account: '',
    opening_balance_date: '',
    
    // Step 6: User Preferences
    default_transaction_date: 'today',
    number_format: 'US',
    date_format: 'MM/DD/YYYY',
    dashboard_layout: 'standard',
    
    // Step 7: Legacy settings
    multi_user: false,
    audit_trail: true,
    encrypt_file: false,
    password: '',
    confirm_password: ''
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [availableAccounts, setAvailableAccounts] = useState([]);

  // Business structures
  const businessStructures = [
    { id: 'sole_proprietorship', name: 'Sole Proprietorship', icon: '👤' },
    { id: 'partnership', name: 'Partnership', icon: '🤝' },
    { id: 'llc', name: 'Limited Liability Company (LLC)', icon: '🏢' },
    { id: 'corporation', name: 'Corporation', icon: '🏛️' },
    { id: 's_corp', name: 'S Corporation', icon: '📊' },
    { id: 'nonprofit', name: 'Nonprofit Organization', icon: '❤️' }
  ];

  // Business activities  
  const businessActivities = [
    { id: 'general', name: 'General Business', icon: '🏢' },
    { id: 'consulting', name: 'Consulting & Professional Services', icon: '💼' },
    { id: 'retail', name: 'Retail & E-commerce', icon: '🛍️' },
    { id: 'manufacturing', name: 'Manufacturing', icon: '🏭' },
    { id: 'construction', name: 'Construction & Contracting', icon: '🔨' },
    { id: 'restaurant', name: 'Restaurant & Food Service', icon: '🍽️' },
    { id: 'healthcare', name: 'Healthcare & Medical', icon: '🏥' },
    { id: 'real_estate', name: 'Real Estate', icon: '🏘️' },
    { id: 'automotive', name: 'Automotive Services', icon: '🚗' },
    { id: 'technology', name: 'Technology & Software', icon: '💻' },
    { id: 'education', name: 'Education & Training', icon: '🎓' },
    { id: 'nonprofit', name: 'Nonprofit', icon: '🤝' }
  ];

  // Chart of accounts templates
  const chartTemplates = [
    { id: 'general', name: 'General Business', description: 'Standard chart for most businesses' },
    { id: 'retail', name: 'Retail', description: 'Optimized for retail and inventory businesses' },
    { id: 'service', name: 'Service Business', description: 'Perfect for consulting and service companies' },
    { id: 'manufacturing', name: 'Manufacturing', description: 'Includes cost of goods and manufacturing accounts' },
    { id: 'construction', name: 'Construction', description: 'Job costing and construction-specific accounts' },
    { id: 'nonprofit', name: 'Nonprofit', description: 'Fund accounting and nonprofit requirements' }
  ];

  // Fiscal year options
  const fiscalYearOptions = [
    { value: 'January', label: 'January (Calendar Year)' },
    { value: 'February', label: 'February' },
    { value: 'March', label: 'March' },
    { value: 'April', label: 'April' },
    { value: 'May', label: 'May' },
    { value: 'June', label: 'June' },
    { value: 'July', label: 'July' },
    { value: 'August', label: 'August' },
    { value: 'September', label: 'September' },
    { value: 'October', label: 'October' },
    { value: 'November', label: 'November' },
    { value: 'December', label: 'December' }
  ];

  useEffect(() => {
    // Load existing accounts for chart of accounts customization
    loadAccounts();
  }, []);

  const loadAccounts = async () => {
    try {
      const response = await axios.get(`${API}/accounts`);
      setAvailableAccounts(response.data);
    } catch (error) {
      console.error('Error loading accounts:', error);
    }
  };

  const handleNext = () => {
    if (currentStep < 7) {
      setCurrentStep(currentStep + 1);
    } else {
      handleFinish();
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleFinish = async () => {
    setLoading(true);
    setError('');
    
    try {
      // Create company record with enhanced data
      const companyData = {
        name: formData.company_name,
        legal_name: formData.legal_name,
        address: formData.address,
        city: formData.city,
        state: formData.state,
        zip_code: formData.zip_code,
        country: formData.country,
        phone: formData.phone,
        fax: formData.fax,
        email: formData.email,
        industry: formData.primary_activity || 'general',
        settings: {
          business_type: formData.business_type,
          business_structure: formData.business_structure,
          primary_activity: formData.primary_activity,
          website: formData.website,
          ein: formData.ein,
          state_of_incorporation: formData.state_of_incorporation,
          business_start_date: formData.business_start_date,
          fiscal_year_end: formData.fiscal_year_end,
          accounting_method: formData.accounting_method,
          track_inventory: formData.track_inventory,
          have_employees: formData.have_employees,
          use_sales_tax: formData.use_sales_tax,
          preferred_currency: formData.preferred_currency,
          track_time: formData.track_time,
          use_classes: formData.use_classes,
          use_locations: formData.use_locations,
          chart_template: formData.chart_template,
          customize_accounts: formData.customize_accounts,
          tax_id: formData.tax_id,
          sales_tax_agency: formData.sales_tax_agency,
          default_bank_account: formData.default_bank_account,
          opening_balance_date: formData.opening_balance_date,
          default_transaction_date: formData.default_transaction_date,
          number_format: formData.number_format,
          date_format: formData.date_format,
          dashboard_layout: formData.dashboard_layout,
          multi_user: formData.multi_user,
          audit_trail: formData.audit_trail,
          encrypt_file: formData.encrypt_file
        }
      };

      await axios.post(`${API}/company`, companyData);
      
      // Create default chart of accounts based on template
      if (formData.chart_template && formData.chart_template !== 'general') {
        await createDefaultAccounts(formData.chart_template);
      }
      
      // Store company setup completion
      localStorage.setItem('qbclone_company_setup', 'completed');
      localStorage.setItem('qbclone_company_name', formData.company_name);
      localStorage.setItem('qbclone_setup_data', JSON.stringify(companyData.settings));
      
      onComplete();
    } catch (err) {
      setError('Failed to create company. Please try again.');
      console.error('Company creation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const createDefaultAccounts = async (template) => {
    try {
      // This would create industry-specific accounts
      // For now, we'll just ensure basic accounts exist
      const basicAccounts = [
        { name: 'Checking Account', account_type: 'Asset', detail_type: 'Checking' },
        { name: 'Accounts Receivable', account_type: 'Asset', detail_type: 'Accounts Receivable' },
        { name: 'Accounts Payable', account_type: 'Liability', detail_type: 'Accounts Payable' },
        { name: 'Sales Income', account_type: 'Income', detail_type: 'Sales' }
      ];

      for (const account of basicAccounts) {
        try {
          await axios.post(`${API}/accounts`, account);
        } catch (error) {
          console.log('Account may already exist:', account.name);
        }
      }
    } catch (error) {
      console.error('Error creating default accounts:', error);
    }
  };

  const updateFormData = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-8 rounded-t-2xl">
          <div className="flex items-center justify-center mb-6">
            <div className="w-16 h-16 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
              <span className="text-3xl font-bold">QB</span>
            </div>
          </div>
          <h1 className="text-3xl font-bold text-center mb-2">Welcome to QBClone</h1>
          <p className="text-blue-100 text-center text-lg">Let's set up your accounting system</p>
        </div>

        {/* Progress Bar */}
        <div className="px-8 py-6 bg-gray-50 border-b">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2">
              {[1, 2, 3, 4, 5, 6, 7].map((step) => (
                <div key={step} className="flex items-center">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center font-semibold text-xs ${
                    step <= currentStep 
                      ? 'bg-blue-600 text-white' 
                      : step === currentStep + 1 
                      ? 'bg-blue-200 text-blue-600' 
                      : 'bg-gray-200 text-gray-500'
                  }`}>
                    {step}
                  </div>
                  {step < 7 && (
                    <div className={`w-8 h-1 mx-1 ${
                      step < currentStep ? 'bg-blue-600' : 'bg-gray-200'
                    }`} />
                  )}
                </div>
              ))}
            </div>
            <div className="text-sm text-gray-600">
              Step {currentStep} of 7
            </div>
          </div>
          <div className="grid grid-cols-7 gap-2 text-xs text-gray-600 text-center">
            <span>Welcome</span>
            <span>Company</span>
            <span>Business</span>
            <span>Accounts</span>
            <span>Tax & Finance</span>
            <span>Preferences</span>
            <span>Review</span>
          </div>
        </div>

        {/* Content */}
        <div className="p-8">
          {currentStep === 1 && (
            <div className="space-y-6">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome & Business Type</h2>
                <p className="text-gray-600">Let's start by learning about your business</p>
              </div>
              
              {/* Business Structure */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-4">
                  What type of business structure do you have?
                </label>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {businessStructures.map((structure) => (
                    <div
                      key={structure.id}
                      onClick={() => updateFormData('business_structure', structure.id)}
                      className={`p-4 border rounded-lg cursor-pointer transition-all ${
                        formData.business_structure === structure.id
                          ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-500'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="text-center">
                        <div className="text-2xl mb-2">{structure.icon}</div>
                        <div className="font-medium text-gray-900 text-sm">{structure.name}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Primary Business Activity */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-4">
                  What's your primary business activity?
                </label>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {businessActivities.map((activity) => (
                    <div
                      key={activity.id}
                      onClick={() => updateFormData('primary_activity', activity.id)}
                      className={`p-4 border rounded-lg cursor-pointer transition-all ${
                        formData.primary_activity === activity.id
                          ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-500'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="text-center">
                        <div className="text-2xl mb-2">{activity.icon}</div>
                        <div className="font-medium text-gray-900 text-sm">{activity.name}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {currentStep === 2 && (
            <div className="space-y-6">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Company Information</h2>
                <p className="text-gray-600">Tell us about your business details</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Company Name *
                  </label>
                  <input
                    type="text"
                    value={formData.company_name}
                    onChange={(e) => updateFormData('company_name', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter company name"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Legal Name
                  </label>
                  <input
                    type="text"
                    value={formData.legal_name}
                    onChange={(e) => updateFormData('legal_name', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Legal business name"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Address
                </label>
                <input
                  type="text"
                  value={formData.address}
                  onChange={(e) => updateFormData('address', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Street address"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    City
                  </label>
                  <input
                    type="text"
                    value={formData.city}
                    onChange={(e) => updateFormData('city', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="City"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    State/Province
                  </label>
                  <input
                    type="text"
                    value={formData.state}
                    onChange={(e) => updateFormData('state', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="State"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    ZIP/Postal Code
                  </label>
                  <input
                    type="text"
                    value={formData.zip_code}
                    onChange={(e) => updateFormData('zip_code', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="ZIP code"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Phone
                  </label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => updateFormData('phone', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Phone number"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => updateFormData('email', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Email address"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Website
                  </label>
                  <input
                    type="url"
                    value={formData.website}
                    onChange={(e) => updateFormData('website', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="https://www.example.com"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    EIN (Employer Identification Number)
                  </label>
                  <input
                    type="text"
                    value={formData.ein}
                    onChange={(e) => updateFormData('ein', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="XX-XXXXXXX"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Business Start Date
                  </label>
                  <input
                    type="date"
                    value={formData.business_start_date}
                    onChange={(e) => updateFormData('business_start_date', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Fiscal Year End
                  </label>
                  <select
                    value={formData.fiscal_year_end}
                    onChange={(e) => updateFormData('fiscal_year_end', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    {fiscalYearOptions.map(option => (
                      <option key={option.value} value={option.value}>{option.label}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          )}

          {currentStep === 3 && (
            <div className="space-y-6">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Business Preferences</h2>
                <p className="text-gray-600">Configure how you want to manage your business</p>
              </div>
              
              <div className="bg-gray-50 p-6 rounded-lg">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Accounting Method</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div
                    onClick={() => updateFormData('accounting_method', 'Cash')}
                    className={`p-4 border rounded-lg cursor-pointer transition-all ${
                      formData.accounting_method === 'Cash'
                        ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-500'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <h4 className="font-medium text-gray-900">Cash Basis</h4>
                    <p className="text-sm text-gray-600 mt-1">Record income when received and expenses when paid</p>
                  </div>
                  <div
                    onClick={() => updateFormData('accounting_method', 'Accrual')}
                    className={`p-4 border rounded-lg cursor-pointer transition-all ${
                      formData.accounting_method === 'Accrual'
                        ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-500'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <h4 className="font-medium text-gray-900">Accrual Basis</h4>
                    <p className="text-sm text-gray-600 mt-1">Record income when earned and expenses when incurred</p>
                  </div>
                </div>
              </div>

              <div className="bg-gray-50 p-6 rounded-lg">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Business Features</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-4">
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        id="inventory"
                        checked={formData.track_inventory}
                        onChange={(e) => updateFormData('track_inventory', e.target.checked)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label htmlFor="inventory" className="ml-3 text-sm text-gray-700">
                        Track inventory items
                      </label>
                    </div>
                    
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        id="employees"
                        checked={formData.have_employees}
                        onChange={(e) => updateFormData('have_employees', e.target.checked)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label htmlFor="employees" className="ml-3 text-sm text-gray-700">
                        I have employees
                      </label>
                    </div>
                    
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        id="salestax"
                        checked={formData.use_sales_tax}
                        onChange={(e) => updateFormData('use_sales_tax', e.target.checked)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label htmlFor="salestax" className="ml-3 text-sm text-gray-700">
                        Charge sales tax
                      </label>
                    </div>
                    
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        id="time"
                        checked={formData.track_time}
                        onChange={(e) => updateFormData('track_time', e.target.checked)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label htmlFor="time" className="ml-3 text-sm text-gray-700">
                        Track time for projects
                      </label>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        id="classes"
                        checked={formData.use_classes}
                        onChange={(e) => updateFormData('use_classes', e.target.checked)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label htmlFor="classes" className="ml-3 text-sm text-gray-700">
                        Use classes for tracking
                      </label>
                    </div>
                    
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        id="locations"
                        checked={formData.use_locations}
                        onChange={(e) => updateFormData('use_locations', e.target.checked)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label htmlFor="locations" className="ml-3 text-sm text-gray-700">
                        Track multiple locations
                      </label>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Preferred Currency
                      </label>
                      <select
                        value={formData.preferred_currency}
                        onChange={(e) => updateFormData('preferred_currency', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="USD">US Dollar (USD)</option>
                        <option value="CAD">Canadian Dollar (CAD)</option>
                        <option value="EUR">Euro (EUR)</option>
                        <option value="GBP">British Pound (GBP)</option>
                        <option value="AUD">Australian Dollar (AUD)</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {currentStep === 4 && (
            <div className="space-y-6">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Chart of Accounts Setup</h2>
                <p className="text-gray-600">Choose the best account structure for your business</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-4">
                  Select a Chart of Accounts Template
                </label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {chartTemplates.map((template) => (
                    <div
                      key={template.id}
                      onClick={() => updateFormData('chart_template', template.id)}
                      className={`p-4 border rounded-lg cursor-pointer transition-all ${
                        formData.chart_template === template.id
                          ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-500'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <h4 className="font-medium text-gray-900">{template.name}</h4>
                      <p className="text-sm text-gray-600 mt-1">{template.description}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-blue-50 p-6 rounded-lg">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="customize"
                    checked={formData.customize_accounts}
                    onChange={(e) => updateFormData('customize_accounts', e.target.checked)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label htmlFor="customize" className="ml-3 text-sm text-blue-700 font-medium">
                    I want to customize my chart of accounts
                  </label>
                </div>
                <p className="text-sm text-blue-600 mt-2 ml-7">
                  You can always add, edit, or remove accounts after setup is complete.
                </p>
              </div>
            </div>
          )}

          {currentStep === 5 && (
            <div className="space-y-6">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Tax & Financial Settings</h2>
                <p className="text-gray-600">Configure your tax and financial preferences</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tax ID (SSN or EIN)
                  </label>
                  <input
                    type="text"
                    value={formData.tax_id}
                    onChange={(e) => updateFormData('tax_id', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="XXX-XX-XXXX or XX-XXXXXXX"
                  />
                </div>
                
                {formData.use_sales_tax && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Sales Tax Agency
                    </label>
                    <input
                      type="text"
                      value={formData.sales_tax_agency}
                      onChange={(e) => updateFormData('sales_tax_agency', e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="State Department of Revenue"
                    />
                  </div>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Default Bank Account Name
                  </label>
                  <input
                    type="text"
                    value={formData.default_bank_account}
                    onChange={(e) => updateFormData('default_bank_account', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Business Checking"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Opening Balances As Of Date
                  </label>
                  <input
                    type="date"
                    value={formData.opening_balance_date}
                    onChange={(e) => updateFormData('opening_balance_date', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div className="bg-yellow-50 p-4 rounded-lg">
                <h4 className="font-medium text-yellow-800 mb-2">💡 Tip</h4>
                <p className="text-sm text-yellow-700">
                  You can enter your account opening balances after completing the setup. 
                  Choose a date that represents when you want to start tracking your finances in QBClone.
                </p>
              </div>
            </div>
          )}

          {currentStep === 6 && (
            <div className="space-y-6">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">User Preferences</h2>
                <p className="text-gray-600">Customize how QBClone works for you</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Default Transaction Date
                  </label>
                  <select
                    value={formData.default_transaction_date}
                    onChange={(e) => updateFormData('default_transaction_date', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="today">Today's date</option>
                    <option value="last_entered">Last entered date</option>
                    <option value="blank">Leave blank</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Number Format
                  </label>
                  <select
                    value={formData.number_format}
                    onChange={(e) => updateFormData('number_format', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="US">US Format (1,234.56)</option>
                    <option value="EU">European Format (1.234,56)</option>
                    <option value="SPACE">Space Separated (1 234.56)</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Date Format
                  </label>
                  <select
                    value={formData.date_format}
                    onChange={(e) => updateFormData('date_format', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                    <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                    <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                    <option value="DD-MMM-YYYY">DD-MMM-YYYY</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Dashboard Layout
                  </label>
                  <select
                    value={formData.dashboard_layout}
                    onChange={(e) => updateFormData('dashboard_layout', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="standard">Standard Layout</option>
                    <option value="compact">Compact Layout</option>
                    <option value="detailed">Detailed Layout</option>
                  </select>
                </div>
              </div>

              <div className="bg-gray-50 p-6 rounded-lg">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Security & Access</h3>
                <div className="space-y-4">
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="multiuser"
                      checked={formData.multi_user}
                      onChange={(e) => updateFormData('multi_user', e.target.checked)}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label htmlFor="multiuser" className="ml-3 text-sm text-gray-700">
                      Enable multi-user mode
                    </label>
                  </div>
                  
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="audit"
                      checked={formData.audit_trail}
                      onChange={(e) => updateFormData('audit_trail', e.target.checked)}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label htmlFor="audit" className="ml-3 text-sm text-gray-700">
                      Enable audit trail (recommended)
                    </label>
                  </div>
                </div>
              </div>
            </div>
          )}

          {currentStep === 7 && (
            <div className="space-y-6">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Review & Complete</h2>
                <p className="text-gray-600">Review your setup and complete the configuration</p>
              </div>
              
              {/* Setup Summary */}
              <div className="bg-gray-50 p-6 rounded-lg">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Setup Summary</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Company Information</h4>
                    <p><span className="text-gray-600">Company:</span> {formData.company_name}</p>
                    <p><span className="text-gray-600">Business Type:</span> {businessStructures.find(b => b.id === formData.business_structure)?.name || 'Not selected'}</p>
                    <p><span className="text-gray-600">Activity:</span> {businessActivities.find(a => a.id === formData.primary_activity)?.name || 'Not selected'}</p>
                    <p><span className="text-gray-600">Email:</span> {formData.email || 'Not provided'}</p>
                  </div>
                  
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Business Preferences</h4>
                    <p><span className="text-gray-600">Accounting Method:</span> {formData.accounting_method}</p>
                    <p><span className="text-gray-600">Currency:</span> {formData.preferred_currency}</p>
                    <p><span className="text-gray-600">Chart Template:</span> {chartTemplates.find(c => c.id === formData.chart_template)?.name || 'General'}</p>
                    <p><span className="text-gray-600">Fiscal Year End:</span> {formData.fiscal_year_end}</p>
                  </div>
                </div>
              </div>

              {/* Feature Summary */}
              <div className="bg-blue-50 p-6 rounded-lg">
                <h3 className="text-lg font-medium text-blue-900 mb-4">Enabled Features</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-sm">
                  {formData.track_inventory && <span className="text-blue-700">✓ Inventory Tracking</span>}
                  {formData.have_employees && <span className="text-blue-700">✓ Employee Management</span>}
                  {formData.use_sales_tax && <span className="text-blue-700">✓ Sales Tax</span>}
                  {formData.track_time && <span className="text-blue-700">✓ Time Tracking</span>}
                  {formData.use_classes && <span className="text-blue-700">✓ Class Tracking</span>}
                  {formData.use_locations && <span className="text-blue-700">✓ Location Tracking</span>}
                  {formData.multi_user && <span className="text-blue-700">✓ Multi-user Access</span>}
                  {formData.audit_trail && <span className="text-blue-700">✓ Audit Trail</span>}
                </div>
              </div>

              {/* Next Steps */}
              <div className="bg-green-50 p-6 rounded-lg">
                <h3 className="text-lg font-medium text-green-900 mb-4">🎉 You're Almost Ready!</h3>
                <p className="text-green-700 mb-4">
                  After completing setup, you'll be able to:
                </p>
                <ul className="text-sm text-green-700 space-y-1">
                  <li>• Add your first customers and vendors</li>
                  <li>• Set up your chart of accounts with opening balances</li>
                  <li>• Create your first invoice or bill</li>
                  <li>• Connect your bank accounts</li>
                  <li>• Start tracking your business finances</li>
                </ul>
              </div>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
              {error}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-8 py-6 rounded-b-2xl border-t">
          <div className="flex justify-between items-center">
            <div className="flex space-x-3">
              {currentStep > 1 && (
                <button
                  onClick={handleBack}
                  className="px-6 py-3 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                  disabled={loading}
                >
                  Back
                </button>
              )}
            </div>
            
            <div className="flex space-x-3">
              <button
                onClick={() => onComplete()}
                className="px-6 py-3 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                disabled={loading}
              >
                Skip Setup
              </button>
              
              <button
                onClick={handleNext}
                className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all disabled:opacity-50"
                disabled={loading || (currentStep === 1 && (!formData.business_structure || !formData.primary_activity)) || (currentStep === 2 && !formData.company_name)}
              >
                {loading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Processing...
                  </div>
                ) : (
                  currentStep === 7 ? 'Create Company' : 'Next'
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WelcomeWizard;