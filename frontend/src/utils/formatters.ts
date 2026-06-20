export const formatCO2 = (kg: number): string => {
  return `${kg.toLocaleString(undefined, { maximumFractionDigits: 1 })} kg CO₂`;
};

export const formatMoney = (inr: number): string => {
  return `₹${inr.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
};

export const formatPercentage = (pct: number): string => {
  return `${pct.toLocaleString(undefined, { maximumFractionDigits: 1 })}%`;
};

export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};
