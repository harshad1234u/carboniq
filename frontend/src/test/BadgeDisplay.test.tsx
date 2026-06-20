import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BadgeDisplay } from '../components/BadgeDisplay';

vi.mock('lucide-react', () => ({
  Award: (props: Record<string, unknown>) => <svg data-testid="award-icon" {...props} />,
}));

vi.mock('../utils/formatters', () => ({
  formatDate: (date: string) => `formatted:${date}`,
}));

const mockBadges = [
  {
    id: '1',
    badge_name: 'First Step',
    badge_description: 'Completed your first calculation.',
    earned_at: '2026-06-15',
  },
  {
    id: '2',
    badge_name: 'Eco Warrior',
    badge_description: 'Completed 5 challenges.',
    earned_at: '2026-06-18',
  },
];

describe('BadgeDisplay', () => {
  it('renders empty state when no badges', () => {
    render(<BadgeDisplay badges={[]} />);
    expect(screen.getByText('Complete challenges to earn badges!')).toBeInTheDocument();
  });

  it('renders empty state when badges is undefined', () => {
    // @ts-expect-error Testing undefined prop
    render(<BadgeDisplay badges={undefined} />);
    expect(screen.getByText('Complete challenges to earn badges!')).toBeInTheDocument();
  });

  it('renders badge names', () => {
    render(<BadgeDisplay badges={mockBadges} />);
    expect(screen.getByText('First Step')).toBeInTheDocument();
    expect(screen.getByText('Eco Warrior')).toBeInTheDocument();
  });

  it('renders badge descriptions', () => {
    render(<BadgeDisplay badges={mockBadges} />);
    expect(screen.getByText('Completed your first calculation.')).toBeInTheDocument();
    expect(screen.getByText('Completed 5 challenges.')).toBeInTheDocument();
  });

  it('renders formatted earned dates', () => {
    render(<BadgeDisplay badges={mockBadges} />);
    expect(screen.getByText('Earned formatted:2026-06-15')).toBeInTheDocument();
    expect(screen.getByText('Earned formatted:2026-06-18')).toBeInTheDocument();
  });

  it('renders correct number of badges', () => {
    render(<BadgeDisplay badges={mockBadges} />);
    const awardIcons = screen.getAllByTestId('award-icon');
    // 2 badges rendered (each has an Award icon)
    expect(awardIcons.length).toBe(2);
  });
});
