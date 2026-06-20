import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { LoadingSkeleton } from '../components/LoadingSkeleton';

describe('LoadingSkeleton', () => {
  it('renders default variant', () => {
    const { container } = render(<LoadingSkeleton />);
    const el = container.firstChild as HTMLElement;
    expect(el).toBeInTheDocument();
    expect(el.className).toContain('animate-pulse');
  });

  it('renders card variant', () => {
    const { container } = render(<LoadingSkeleton variant="card" />);
    const el = container.firstChild as HTMLElement;
    expect(el.className).toContain('animate-pulse');
    expect(el.className).toContain('rounded-xl');
  });

  it('renders dashboard variant with multiple skeleton blocks', () => {
    const { container } = render(<LoadingSkeleton variant="dashboard" />);
    const el = container.firstChild as HTMLElement;
    expect(el.className).toContain('animate-pulse');
    // Dashboard has a grid with child elements
    expect(el.children.length).toBeGreaterThan(1);
  });

  it('renders text variant', () => {
    const { container } = render(<LoadingSkeleton variant="text" />);
    const el = container.firstChild as HTMLElement;
    expect(el.className).toContain('h-4');
  });
});
