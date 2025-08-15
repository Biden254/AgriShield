import React from 'react';
import { useTranslation } from 'react-i18next';
import { Box, Typography, CircularProgress, Paper } from '@mui/material';
import { RISK_LEVELS } from '../../config';

const RiskIndicator = ({ level, score }) => {
  const { t } = useTranslation();
  const riskConfig = RISK_LEVELS[level] || RISK_LEVELS.low;

  return (
    <Paper elevation={3} sx={{ p: 3, textAlign: 'center' }}>
      <Typography variant="h6" gutterBottom>
        Current Flood Risk
      </Typography>
      
      <Box sx={{ position: 'relative', display: 'inline-flex', mb: 2 }}>
        <CircularProgress 
          variant="determinate" 
          value={score ? Math.min(score, 100) : 0} 
          size={120}
          thickness={4}
          sx={{
            color: riskConfig.color,
            '& .MuiCircularProgress-circle': {
              strokeLinecap: 'round',
            },
          }}
        />
        <Box
          sx={{
            top: 0,
            left: 0,
            bottom: 0,
            right: 0,
            position: 'absolute',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Typography variant="h4" component="div" color={riskConfig.color}>
            {t(`risk.${level}`)}
          </Typography>
        </Box>
      </Box>
      
      <Typography variant="body1" color="text.secondary">
        {score ? `Risk score: ${Math.round(score)}/100` : 'Calculating risk...'}
      </Typography>
      
      {level === 'high' && (
        <Typography variant="body2" color="error" sx={{ mt: 2 }}>
          Immediate action required! Check alerts for instructions.
        </Typography>
      )}
    </Paper>
  );
};

export default RiskIndicator;