import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import RiskIndicator from '../../components/risk/RiskIndicator';
import AlertCard from '../../components/risk/AlertCard';
import { Box, Grid, Typography, Button } from '@mui/material';
import { MAP_CENTER, MAP_ZOOM, RISK_LEVELS } from '../../config';
import axios from 'axios';

const Dashboard = () => {
  const { t } = useTranslation();
  const [riskData, setRiskData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRiskData = async () => {
      try {
        const response = await axios.get('/api/risk');
        setRiskData(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchRiskData();
    const interval = setInterval(fetchRiskData, 300000); // Refresh every 5 minutes

    return () => clearInterval(interval);
  }, []);

  const RecenterMap = ({ center }) => {
    const map = useMap();
    map.setView(center, map.getZoom());
    return null;
  };

  if (loading) return <Typography>Loading...</Typography>;
  if (error) return <Typography color="error">Error: {error}</Typography>;

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        {t('dashboard.title')}
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Box sx={{ height: '400px', borderRadius: 2, overflow: 'hidden' }}>
            <MapContainer
              center={MAP_CENTER}
              zoom={MAP_ZOOM}
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              />
              {riskData?.floodAreas && (
                <GeoJSON 
                  data={riskData.floodAreas} 
                  style={() => ({
                    fillColor: RISK_LEVELS.high.color,
                    weight: 2,
                    opacity: 1,
                    color: 'white',
                    fillOpacity: 0.7
                  })} 
                />
              )}
              <RecenterMap center={MAP_CENTER} />
            </MapContainer>
          </Box>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <RiskIndicator 
            level={riskData?.currentRisk || 'low'} 
            score={riskData?.riskScore} 
          />
          
          {riskData?.alerts?.length > 0 && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="h6" gutterBottom>
                Active Alerts
              </Typography>
              {riskData.alerts.map(alert => (
                <AlertCard key={alert.id} alert={alert} />
              ))}
            </Box>
          )}
        </Grid>
      </Grid>
      
      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center', gap: 2 }}>
        <Button 
          variant="contained" 
          color="primary"
          href="/report"
          sx={{ px: 4 }}
        >
          {t('report.button')}
        </Button>
        <Button 
          variant="outlined" 
          color="primary"
          href="/alerts"
          sx={{ px: 4 }}
        >
          View All Alerts
        </Button>
      </Box>
    </Box>
  );
};

export default Dashboard;