import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ErrorState } from '../components/ErrorState';

vi.mock('lucide-react', () => ({
  AlertCircle: (props: Record<string, unknown>) => <svg data-testid="alert-icon" {...props} />,
}));

describe('ErrorState', () => {
  it('renders error message', () => {
    render(<ErrorState message="Something broke!" />);
    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    expect(screen.getByText('Something broke!')).toBeInTheDocument();
  });

  it('renders the alert icon', () => {
    render(<ErrorState message="Error" />);
    expect(screen.getByTestId('alert-icon')).toBeInTheDocument();
  });

  it('renders retry button when onRetry is provided', () => {
    const handleRetry = vi.fn();
    render(<ErrorState message="Failed" onRetry={handleRetry} />);
    const button = screen.getByText('Try Again');
    expect(button).toBeInTheDocument();
    fireEvent.click(button);
    expect(handleRetry).toHaveBeenCalledOnce();
  });

  it('does not render retry button when onRetry is missing', () => {
    render(<ErrorState message="Error" />);
    expect(screen.queryByText('Try Again')).not.toBeInTheDocument();
  });
});
