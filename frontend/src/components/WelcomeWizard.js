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
                <h2 className="text-2xl font-bold text-gray-900 mb-2">File Preferences</h2>
                <p className="text-gray-600">Configure your company file settings</p>
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
                      Enable Multi-user Mode
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
                      Enable Audit Trail
                    </label>
                  </div>
                  
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="encrypt"
                      checked={formData.encrypt_file}
                      onChange={(e) => updateFormData('encrypt_file', e.target.checked)}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label htmlFor="encrypt" className="ml-3 text-sm text-gray-700">
                      Encrypt Company File
                    </label>
                  </div>
                </div>
              </div>

              {formData.encrypt_file && (
                <div className="bg-blue-50 p-6 rounded-lg">
                  <h3 className="text-lg font-medium text-blue-900 mb-4">File Encryption</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-blue-700 mb-2">
                        Password
                      </label>
                      <input
                        type="password"
                        value={formData.password}
                        onChange={(e) => updateFormData('password', e.target.value)}
                        className="w-full px-4 py-3 border border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter password"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-blue-700 mb-2">
                        Confirm Password
                      </label>
                      <input
                        type="password"
                        value={formData.confirm_password}
                        onChange={(e) => updateFormData('confirm_password', e.target.value)}
                        className="w-full px-4 py-3 border border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Confirm password"
                      />
                    </div>
                  </div>
                </div>
              )}
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
                disabled={loading || (currentStep === 1 && !formData.company_name)}
              >
                {loading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Processing...
                  </div>
                ) : (
                  currentStep === 3 ? 'Finish Setup' : 'Next'
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