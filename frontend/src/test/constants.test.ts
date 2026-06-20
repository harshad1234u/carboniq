import { describe, it, expect } from 'vitest';
import { VEHICLE_TYPES, DIET_TYPES, CARBON_SCORE_LEVELS, NAV_ITEMS } from '../utils/constants';

describe('Constants', () => {
  describe('VEHICLE_TYPES', () => {
    it('contains all expected vehicle types', () => {
      const values = VEHICLE_TYPES.map(v => v.value);
      expect(values).toContain('car_petrol');
      expect(values).toContain('car_diesel');
      expect(values).toContain('car_electric');
      expect(values).toContain('motorcycle');
      expect(values).toContain('bus');
      expect(values).toContain('train');
      expect(values).toContain('bicycle');
      expect(values).toContain('walk');
    });

    it('each type has a value and label', () => {
      VEHICLE_TYPES.forEach(v => {
        expect(v.value).toBeTruthy();
        expect(v.label).toBeTruthy();
      });
    });
  });

  describe('DIET_TYPES', () => {
    it('contains all expected diet types', () => {
      const values = DIET_TYPES.map(d => d.value);
      expect(values).toContain('meat_heavy');
      expect(values).toContain('average');
      expect(values).toContain('vegetarian');
      expect(values).toContain('vegan');
    });
  });

  describe('CARBON_SCORE_LEVELS', () => {
    it('covers the full 0-100 range', () => {
      expect(CARBON_SCORE_LEVELS[0].min).toBe(0);
      expect(CARBON_SCORE_LEVELS[CARBON_SCORE_LEVELS.length - 1].max).toBe(100);
    });

    it('has no gaps in the range', () => {
      for (let i = 1; i < CARBON_SCORE_LEVELS.length; i++) {
        expect(CARBON_SCORE_LEVELS[i].min).toBe(CARBON_SCORE_LEVELS[i - 1].max + 1);
      }
    });

    it('each level has a label, color, and bg', () => {
      CARBON_SCORE_LEVELS.forEach(l => {
        expect(l.label).toBeTruthy();
        expect(l.color).toBeTruthy();
        expect(l.bg).toBeTruthy();
      });
    });
  });

  describe('NAV_ITEMS', () => {
    it('has required navigation items', () => {
      const labels = NAV_ITEMS.map(n => n.label);
      expect(labels).toContain('Dashboard');
      expect(labels).toContain('Calculator');
      expect(labels).toContain('AI Coach');
      expect(labels).toContain('Profile');
    });

    it('each item has a path, label, and icon', () => {
      NAV_ITEMS.forEach(item => {
        expect(item.path).toMatch(/^\//);
        expect(item.label).toBeTruthy();
        expect(item.icon).toBeDefined();
      });
    });
  });
});
