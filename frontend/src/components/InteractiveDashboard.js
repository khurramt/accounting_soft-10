import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const InteractiveDashboard = () => {
  const [dashboardMetrics, setDashboardMetrics] = useState(null);
  const [kpiTrends, setKpiTrends] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedWidget, setSelectedWidget] = useState(null);
  const [drillDownData, setDrillDownData] = useState(null);
  const [customLayout, setCustomLayout] = useState([
    'financial-overview',
    'kpi-cards',
    'alerts',
    'cash-flow-chart',
    'trends-chart',
    'recent-activity'
  ]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [metricsResponse, trendsResponse] = await Promise.all([
        axios.get(`${API}/analytics/dashboard-metrics`),
        axios.get(`${API}/analytics/kpi-trends?period=12months`)
      ]);
      
      setDashboardMetrics(metricsResponse.data);
      setKpiTrends(trendsResponse.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDrillDown = async (metric, period = 'current_month') => {
    try {
      const response = await axios.get(`${API}/analytics/drill-down/${metric}?period=${period}`);
      setDrillDownData(response.data);
      setSelectedWidget(metric);
    } catch (error) {
      console.error('Error fetching drill-down data:', error);
    }
  };

  const closeDrillDown = () => {
    setSelectedWidget(null);
    setDrillDownData(null);
  };

  const FinancialOverviewWidget = () => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Financial Overview</h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">
            ${dashboardMetrics?.financial_metrics?.total_cash?.toLocaleString() || 0}
          </div>
          <div className="text-sm text-gray-600">Cash Position</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">
            ${dashboardMetrics?.financial_metrics?.total_ar?.toLocaleString() || 0}
          </div>
          <div className="text-sm text-gray-600">Accounts Receivable</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-red-600">
            ${dashboardMetrics?.financial_metrics?.total_ap?.toLocaleString() || 0}
          </div>
          <div className="text-sm text-gray-600">Accounts Payable</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-purple-600">
            ${dashboardMetrics?.financial_metrics?.working_capital?.toLocaleString() || 0}
          </div>
          <div className="text-sm text-gray-600">Working Capital</div>
        </div>
      </div>
    </div>
  );

  const KPICardsWidget = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {/* Monthly Income */}
      <div 
        className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg shadow-sm p-6 text-white cursor-pointer hover:shadow-lg transition-shadow"
        onClick={() => handleDrillDown('income')}
      >
        <div className="flex items-center justify-between">
          <div>
            <p className="text-green-100">Monthly Income</p>
            <p className="text-2xl font-bold">
              ${dashboardMetrics?.financial_metrics?.current_month_income?.toLocaleString() || 0}
            </p>
            <p className="text-sm text-green-100">
              {dashboardMetrics?.financial_metrics?.income_growth_rate > 0 ? '↑' : '↓'} 
              {Math.abs(dashboardMetrics?.financial_metrics?.income_growth_rate || 0).toFixed(1)}%
            </p>
          </div>
          <div className="text-3xl">💰</div>
        </div>
      </div>

      {/* Monthly Expenses */}
      <div 
        className="bg-gradient-to-r from-red-500 to-red-600 rounded-lg shadow-sm p-6 text-white cursor-pointer hover:shadow-lg transition-shadow"
        onClick={() => handleDrillDown('expenses')}
      >
        <div className="flex items-center justify-between">
          <div>
            <p className="text-red-100">Monthly Expenses</p>
            <p className="text-2xl font-bold">
              ${dashboardMetrics?.financial_metrics?.current_month_expenses?.toLocaleString() || 0}
            </p>
            <p className="text-sm text-red-100">
              {dashboardMetrics?.financial_metrics?.expense_growth_rate > 0 ? '↑' : '↓'} 
              {Math.abs(dashboardMetrics?.financial_metrics?.expense_growth_rate || 0).toFixed(1)}%
            </p>
          </div>
          <div className="text-3xl">💸</div>
        </div>
      </div>

      {/* Net Profit */}
      <div className={`bg-gradient-to-r ${
        (dashboardMetrics?.financial_metrics?.current_month_profit || 0) >= 0 
          ? 'from-blue-500 to-blue-600' 
          : 'from-orange-500 to-orange-600'
      } rounded-lg shadow-sm p-6 text-white`}>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-blue-100">Net Profit</p>
            <p className="text-2xl font-bold">
              ${dashboardMetrics?.financial_metrics?.current_month_profit?.toLocaleString() || 0}
            </p>
            <p className="text-sm text-blue-100">This Month</p>
          </div>
          <div className="text-3xl">📈</div>
        </div>
      </div>

      {/* Overdue Invoices */}
      <div 
        className="bg-gradient-to-r from-yellow-500 to-yellow-600 rounded-lg shadow-sm p-6 text-white cursor-pointer hover:shadow-lg transition-shadow"
        onClick={() => handleDrillDown('overdue_invoices')}
      >
        <div className="flex items-center justify-between">
          <div>
            <p className="text-yellow-100">Overdue Invoices</p>
            <p className="text-2xl font-bold">
              {dashboardMetrics?.alerts?.overdue_invoices_count || 0}
            </p>
            <p className="text-sm text-yellow-100">
              ${dashboardMetrics?.alerts?.overdue_amount?.toLocaleString() || 0}
            </p>
          </div>
          <div className="text-3xl">⚠️</div>
        </div>
      </div>
    </div>
  );

  const AlertsWidget = () => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Alerts & Notifications</h3>
      <div className="space-y-3">
        {dashboardMetrics?.alerts?.low_cash_warning && (
          <div className="flex items-center space-x-3 p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="text-red-500 text-xl">⚠️</div>
            <div>
              <p className="font-medium text-red-800">Low Cash Warning</p>
              <p className="text-sm text-red-600">Cash position is below recommended threshold</p>
            </div>
          </div>
        )}
        
        {(dashboardMetrics?.alerts?.overdue_invoices_count || 0) > 0 && (
          <div className="flex items-center space-x-3 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="text-yellow-500 text-xl">📋</div>
            <div>
              <p className="font-medium text-yellow-800">Overdue Invoices</p>
              <p className="text-sm text-yellow-600">
                {dashboardMetrics.alerts.overdue_invoices_count} invoices are overdue
              </p>
            </div>
          </div>
        )}

        <div className={`flex items-center space-x-3 p-3 rounded-lg ${
          dashboardMetrics?.alerts?.cash_flow_status === 'positive' 
            ? 'bg-green-50 border border-green-200' 
            : 'bg-red-50 border border-red-200'
        }`}>
          <div className={`text-xl ${
            dashboardMetrics?.alerts?.cash_flow_status === 'positive' ? 'text-green-500' : 'text-red-500'
          }`}>
            {dashboardMetrics?.alerts?.cash_flow_status === 'positive' ? '✅' : '❌'}
          </div>
          <div>
            <p className={`font-medium ${
              dashboardMetrics?.alerts?.cash_flow_status === 'positive' ? 'text-green-800' : 'text-red-800'
            }`}>
              Cash Flow Status
            </p>
            <p className={`text-sm ${
              dashboardMetrics?.alerts?.cash_flow_status === 'positive' ? 'text-green-600' : 'text-red-600'
            }`}>
              {dashboardMetrics?.alerts?.cash_flow_status === 'positive' ? 'Healthy' : 'Needs Attention'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  const TrendsChartWidget = () => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">12-Month Trends</h3>
      {kpiTrends?.trends && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                ${kpiTrends.trends.reduce((sum, trend) => sum + trend.income, 0).toLocaleString()}
              </div>
              <div className="text-sm text-green-600">Total Income (12mo)</div>
            </div>
            <div className="p-4 bg-red-50 rounded-lg">
              <div className="text-2xl font-bold text-red-600">
                ${kpiTrends.trends.reduce((sum, trend) => sum + trend.expenses, 0).toLocaleString()}
              </div>
              <div className="text-sm text-red-600">Total Expenses (12mo)</div>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                ${kpiTrends.trends.reduce((sum, trend) => sum + trend.profit, 0).toLocaleString()}
              </div>
              <div className="text-sm text-blue-600">Total Profit (12mo)</div>
            </div>
          </div>

          {/* Simple trend visualization */}
          <div className="mt-6">
            <div className="flex items-end space-x-1 h-32">
              {kpiTrends.trends.map((trend, index) => {
                const maxProfit = Math.max(...kpiTrends.trends.map(t => t.profit));
                const height = maxProfit > 0 ? (trend.profit / maxProfit) * 100 : 0;
                return (
                  <div key={index} className="flex-1 flex flex-col items-center">
                    <div 
                      className={`w-full rounded-t ${trend.profit >= 0 ? 'bg-green-400' : 'bg-red-400'}`}
                      style={{ height: `${Math.abs(height)}%`, minHeight: '4px' }}
                      title={`${trend.period}: $${trend.profit.toLocaleString()}`}
                    ></div>
                    <div className="text-xs text-gray-500 mt-1 transform -rotate-45 origin-left">
                      {trend.period.slice(0, 3)}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );

  const RecentActivityWidget = () => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
      <div className="space-y-3">
        {dashboardMetrics?.recent_activity?.slice(0, 5).map((activity, index) => (
          <div key={index} className="flex items-center space-x-3 p-3 border border-gray-100 rounded-lg">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">
                {activity.type} - ${activity.amount.toLocaleString()}
              </p>
              <p className="text-xs text-gray-500">
                {new Date(activity.date).toLocaleDateString()}
              </p>
            </div>
          </div>
        )) || (
          <p className="text-gray-500 text-center py-4">No recent activity</p>
        )}
      </div>
    </div>
  );

  // Drill-down modal
  const DrillDownModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            {selectedWidget === 'income' ? 'Income Details' :
             selectedWidget === 'expenses' ? 'Expense Details' :
             selectedWidget === 'overdue_invoices' ? 'Overdue Invoices' : 'Details'}
          </h3>
          <button
            onClick={closeDrillDown}
            className="text-gray-400 hover:text-gray-600"
          >
            ✕
          </button>
        </div>

        {drillDownData && (
          <div className="space-y-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                ${drillDownData.total?.toLocaleString() || 0}
              </div>
              <div className="text-sm text-gray-600">
                Total {selectedWidget} for {drillDownData.period}
              </div>
              {drillDownData.count && (
                <div className="text-sm text-gray-600">
                  {drillDownData.count} transactions
                </div>
              )}
            </div>

            <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      {selectedWidget === 'overdue_invoices' ? 'Invoice #' : 'Type'}
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Amount
                    </th>
                    {selectedWidget === 'overdue_invoices' && (
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Days Overdue
                      </th>
                    )}
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {(drillDownData.transactions || drillDownData.invoices || []).map((item, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {item.type || item.invoice_number}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {new Date(item.date || item.due_date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                        ${(item.amount || item.balance).toLocaleString()}
                      </td>
                      {selectedWidget === 'overdue_invoices' && (
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600 text-right">
                          {item.days_overdue} days
                        </td>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Dashboard Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Interactive Dashboard</h2>
          <p className="text-gray-600">Real-time business intelligence and analytics</p>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={fetchDashboardData}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            🔄 Refresh
          </button>
          <button className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors">
            ⚙️ Customize
          </button>
        </div>
      </div>

      {/* Dashboard Widgets */}
      <div className="space-y-6">
        {customLayout.includes('financial-overview') && <FinancialOverviewWidget />}
        {customLayout.includes('kpi-cards') && <KPICardsWidget />}
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {customLayout.includes('alerts') && (
            <div className="lg:col-span-1">
              <AlertsWidget />
            </div>
          )}
          {customLayout.includes('trends-chart') && (
            <div className="lg:col-span-1">
              <TrendsChartWidget />
            </div>
          )}
        </div>

        {customLayout.includes('recent-activity') && <RecentActivityWidget />}
      </div>

      {/* Drill-down Modal */}
      {selectedWidget && drillDownData && <DrillDownModal />}
    </div>
  );
};

export default InteractiveDashboard;