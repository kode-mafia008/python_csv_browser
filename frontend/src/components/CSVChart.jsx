import React, { useState, useMemo } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

const CSVChart = ({ csvData }) => {
  const [chartType, setChartType] = useState('bar');
  const [xAxis, setXAxis] = useState('');
  const [yAxis, setYAxis] = useState('');

  // Detect numeric columns
  const numericColumns = useMemo(() => {
    if (!csvData?.columns || !csvData?.data || csvData.data.length === 0) {
      return [];
    }

    return csvData.columns.filter((column) => {
      // Check if at least 80% of non-empty values are numeric
      const values = csvData.data
        .map((row) => row[column])
        .filter((val) => val !== null && val !== undefined && val !== '');

      if (values.length === 0) return false;

      const numericCount = values.filter((val) => !isNaN(parseFloat(val))).length;
      return numericCount / values.length >= 0.8;
    });
  }, [csvData]);

  // All columns for X-axis (can be text or numeric)
  const allColumns = csvData?.columns || [];

  // Prepare chart data
  const chartData = useMemo(() => {
    if (!xAxis || !yAxis || !csvData?.data) return [];

    return csvData.data.map((row) => ({
      [xAxis]: row[xAxis],
      [yAxis]: parseFloat(row[yAxis]) || 0,
    }));
  }, [csvData, xAxis, yAxis]);

  // Set default axes when columns are available
  useMemo(() => {
    if (allColumns.length > 0 && !xAxis) {
      setXAxis(allColumns[0]);
    }
    if (numericColumns.length > 0 && !yAxis) {
      setYAxis(numericColumns[0]);
    }
  }, [allColumns, numericColumns]);

  if (!csvData || csvData.data.length === 0) {
    return (
      <div className="flex justify-center items-center h-96">
        <p className="text-gray-500">No data available for visualization</p>
      </div>
    );
  }

  if (numericColumns.length === 0) {
    return (
      <div className="flex justify-center items-center h-96">
        <p className="text-gray-500">No numeric columns found in the CSV file</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="bg-gray-50 p-4 rounded-lg">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Chart Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Chart Type
            </label>
            <select
              value={chartType}
              onChange={(e) => setChartType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="bar">Bar Chart</option>
              <option value="line">Line Chart</option>
            </select>
          </div>

          {/* X-Axis */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              X-Axis (Category)
            </label>
            <select
              value={xAxis}
              onChange={(e) => setXAxis(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {allColumns.map((column) => (
                <option key={column} value={column}>
                  {column}
                </option>
              ))}
            </select>
          </div>

          {/* Y-Axis */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Y-Axis (Numeric)
            </label>
            <select
              value={yAxis}
              onChange={(e) => setYAxis(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {numericColumns.map((column) => (
                <option key={column} value={column}>
                  {column}
                </option>
              ))}
            </select>
          </div>
        </div>

        {numericColumns.length > 0 && (
          <p className="mt-3 text-sm text-gray-600">
            Numeric columns detected: {numericColumns.join(', ')}
          </p>
        )}
      </div>

      {/* Chart */}
      {xAxis && yAxis && chartData.length > 0 && (
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {yAxis} by {xAxis}
          </h3>
          <ResponsiveContainer width="100%" height={400}>
            {chartType === 'bar' ? (
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey={xAxis} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey={yAxis} fill="#3B82F6" />
              </BarChart>
            ) : (
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey={xAxis} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey={yAxis}
                  stroke="#3B82F6"
                  strokeWidth={2}
                  dot={{ fill: '#3B82F6', r: 4 }}
                />
              </LineChart>
            )}
          </ResponsiveContainer>
        </div>
      )}

      {xAxis && yAxis && chartData.length === 0 && (
        <div className="flex justify-center items-center h-96 bg-gray-50 rounded-lg">
          <p className="text-gray-500">No valid data available for selected columns</p>
        </div>
      )}
    </div>
  );
};

export default CSVChart;
