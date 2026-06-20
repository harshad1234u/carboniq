import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { EmptyState } from '../components/EmptyState';

// Mock lucide-react to avoid SVG rendering issues in jsdom
vi.mock('lucide-react', () => ({
  Leaf: (props: Record<string, unknown>) => <svg data-testid="leaf-icon" {...props} />,
  AlertCircle: (props: Record<string, unknown>) => <svg data-testid="alert-icon" {...props} />,
}));

describe('EmptyState', () => {
  it('renders title and description', () => {
    render(<EmptyState title="No data" description="Start tracking your footprint" />);
    expect(screen.getByText('No data')).toBeInTheDocument();
    expect(screen.getByText('Start tracking your footprint')).toBeInTheDocument();
  });

  it('renders default icon', () => {
    render(<EmptyState title="Empty" description="Nothing here" />);
    expect(screen.getByTestId('leaf-icon')).toBeInTheDocument();
  });

  it('renders action button when actionLabel and onAction are provided', () => {
    const handleAction = vi.fn();
    render(
      <EmptyState
        title="Empty"
        description="Nothing here"
        actionLabel="Get Started"
        onAction={handleAction}
      />
    );
    const button = screen.getByText('Get Started');
    expect(button).toBeInTheDocument();
    fireEvent.click(button);
    expect(handleAction).toHaveBeenCalledOnce();
  });

  it('does not render action button when actionLabel is missing', () => {
    render(<EmptyState title="Empty" description="Nothing here" />);
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });

  it('does not render action button when onAction is missing', () => {
    render(<EmptyState title="Empty" description="Nothing here" actionLabel="Click" />);
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });
});
