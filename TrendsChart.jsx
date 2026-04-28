import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const TrendsChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={300}>
    <LineChart data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis yAxisId="left" label={{ value: 'Rainfall (mm)', angle: -90, position: 'insideLeft' }} />
      <YAxis yAxisId="right" orientation="right" label={{ value: 'Predicted Cases', angle: 90, position: 'insideRight' }} />
      <Tooltip />
      <Line yAxisId="left" type="monotone" dataKey="rain" stroke="#3b82f6" name="Rainfall" />
      <Line yAxisId="right" type="monotone" dataKey="cases" stroke="#ef4444" name="Predicted Cases" />
    </LineChart>
  </ResponsiveContainer>
);

export default TrendsChart;
