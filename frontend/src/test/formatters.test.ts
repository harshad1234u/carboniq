import { describe, it, expect } from 'vitest';
import { formatCO2, formatMoney, formatPercentage, formatDate } from '../utils/formatters';

describe('formatCO2', () => {
  it('formats a whole number', () => {
    expect(formatCO2(350)).toContain('350');
    expect(formatCO2(350)).toContain('kg CO₂');
  });

  it('formats a decimal with max 1 fraction digit', () => {
    const result = formatCO2(123.456);
    expect(result).toContain('kg CO₂');
    // Should round to 1 decimal
    expect(result).toMatch(/123\.5|123\.4/);
  });

  it('formats zero', () => {
    expect(formatCO2(0)).toContain('0');
    expect(formatCO2(0)).toContain('kg CO₂');
  });

  it('formats large numbers with locale separators', () => {
    const result = formatCO2(1500);
    expect(result).toContain('kg CO₂');
  });
});

describe('formatMoney', () => {
  it('formats with rupee symbol', () => {
    expect(formatMoney(500)).toBe('₹500');
  });

  it('formats zero', () => {
    expect(formatMoney(0)).toBe('₹0');
  });

  it('rounds decimals to whole number', () => {
    const result = formatMoney(199.99);
    expect(result).toBe('₹200');
  });
});

describe('formatPercentage', () => {
  it('formats with percent sign', () => {
    expect(formatPercentage(25)).toBe('25%');
  });

  it('formats decimal percentages', () => {
    const result = formatPercentage(33.33);
    expect(result).toMatch(/33\.3%/);
  });

  it('formats zero', () => {
    expect(formatPercentage(0)).toBe('0%');
  });

  it('formats 100%', () => {
    expect(formatPercentage(100)).toBe('100%');
  });
});

describe('formatDate', () => {
  it('formats an ISO date string', () => {
    const result = formatDate('2026-06-19T12:00:00Z');
    expect(result).toContain('Jun');
    expect(result).toContain('19');
    expect(result).toContain('2026');
  });

  it('formats a simple date string', () => {
    const result = formatDate('2026-01-01');
    expect(result).toContain('Jan');
    expect(result).toContain('2026');
  });
});
