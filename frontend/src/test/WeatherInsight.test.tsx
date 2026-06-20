import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { WeatherInsight } from '../components/WeatherInsight';

vi.mock('lucide-react', () => ({
  Cloud: (props: Record<string, unknown>) => <svg data-testid="cloud-icon" {...props} />,
  Droplets: (props: Record<string, unknown>) => <svg data-testid="droplets-icon" {...props} />,
  Sun: (props: Record<string, unknown>) => <svg data-testid="sun-icon" {...props} />,
  Thermometer: (props: Record<string, unknown>) => <svg data-testid="thermometer-icon" {...props} />,
}));

// Mock the Card UI components
vi.mock('../components/ui/card', () => ({
  Card: ({ children, className }: { children: React.ReactNode; className?: string }) => (
    <div data-testid="card" className={className}>{children}</div>
  ),
  CardContent: ({ children, className }: { children: React.ReactNode; className?: string }) => (
    <div data-testid="card-content" className={className}>{children}</div>
  ),
}));

const mockWeather = {
  city: 'Mumbai',
  temperature: 32.7,
  description: 'partly cloudy',
  humidity: 75,
};

describe('WeatherInsight', () => {
  it('renders null when weather is falsy', () => {
    // @ts-expect-error Testing null prop
    const { container } = render(<WeatherInsight weather={null} />);
    expect(container.innerHTML).toBe('');
  });

  it('renders city name', () => {
    render(<WeatherInsight weather={mockWeather} />);
    expect(screen.getByText('Mumbai')).toBeInTheDocument();
  });

  it('renders weather description', () => {
    render(<WeatherInsight weather={mockWeather} />);
    expect(screen.getByText('partly cloudy')).toBeInTheDocument();
  });

  it('renders rounded temperature', () => {
    render(<WeatherInsight weather={mockWeather} />);
    expect(screen.getByText('33°C')).toBeInTheDocument();
  });

  it('renders humidity', () => {
    render(<WeatherInsight weather={mockWeather} />);
    expect(screen.getByText('75%')).toBeInTheDocument();
  });

  it('renders Local Insight header', () => {
    render(<WeatherInsight weather={mockWeather} />);
    expect(screen.getByText('Local Insight')).toBeInTheDocument();
  });
});
