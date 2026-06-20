import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { formatCO2 } from '../utils/formatters';

interface FootprintBreakdownProps {
  transport: number;
  electricity: number;
  food: number;
  flights: number;
  total: number;
}

const COLORS = ['#3b82f6', '#eab308', '#22c55e', '#a855f7'];

export function FootprintBreakdown({ transport, electricity, food, flights, total }: FootprintBreakdownProps) {
  const data = [
    { name: 'Transport', value: transport },
    { name: 'Electricity', value: electricity },
    { name: 'Food', value: food },
    { name: 'Flights', value: flights },
  ].filter(item => item.value > 0);

  return (
    <div className="h-[300px] w-full relative">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={90}
            paddingAngle={5}
            dataKey="value"
            stroke="none"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip 
            formatter={(value: number) => [formatCO2(value as number), 'Emissions']}
            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px' }}
            itemStyle={{ color: '#f8fafc' }}
          />
          <Legend verticalAlign="bottom" height={36} wrapperStyle={{ paddingTop: '20px' }}/>
        </PieChart>
      </ResponsiveContainer>
      <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none mt-[-20px]">
        <span className="text-xs text-slate-400">Total</span>
        <span className="font-bold text-lg">{formatCO2(total)}</span>
      </div>
    </div>
  );
}
