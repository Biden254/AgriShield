export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
export const MAP_CENTER = [-0.5, 34.2]; // Budalang'i coordinates
export const MAP_ZOOM = 12;
export const RISK_LEVELS = {
  low: { color: '#4CAF50', label: 'Low Risk' },
  moderate: { color: '#FFC107', label: 'Moderate Risk' },
  high: { color: '#F44336', label: 'High Risk' }
};