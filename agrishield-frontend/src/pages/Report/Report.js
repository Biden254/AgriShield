import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Select, 
  MenuItem, 
  FormControl, 
  InputLabel,
  Paper,
  Grid
} from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Report = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    indicatorType: '',
    description: '',
    location: '',
    urgency: 'medium'
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const indicatorTypes = [
    { value: 'river_color', label: t('report.types.river_color') },
    { value: 'bird_movement', label: t('report.types.bird_movement') },
    { value: 'fish_behavior', label: t('report.types.fish_behavior') },
    { value: 'vegetation', label: t('report.types.vegetation') },
    { value: 'other', label: t('report.types.other') }
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      await axios.post('/api/reports', formData);
      navigate('/', { state: { reportSuccess: true } });
    } catch (err) {
      setError(err.response?.data?.message || err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        {t('report.title')}
      </Typography>
      
      <Paper elevation={3} sx={{ p: 3, maxWidth: 800, mx: 'auto' }}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>{t('report.type_label')}</InputLabel>
                <Select
                  name="indicatorType"
                  value={formData.indicatorType}
                  onChange={handleChange}
                  label={t('report.type_label')}
                  required
                >
                  {indicatorTypes.map(type => (
                    <MenuItem key={type.value} value={type.value}>
                      {type.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                name="description"
                label={t('report.description_label')}
                multiline
                rows={4}
                fullWidth
                value={formData.description}
                onChange={handleChange}
                required
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                name="location"
                label={t('report.location_label')}
                fullWidth
                value={formData.location}
                onChange={handleChange}
                required
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>{t('report.urgency_label')}</InputLabel>
                <Select
                  name="urgency"
                  value={formData.urgency}
                  onChange={handleChange}
                  label={t('report.urgency_label')}
                >
                  <MenuItem value="low">{t('report.urgency_low')}</MenuItem>
                  <MenuItem value="medium">{t('report.urgency_medium')}</MenuItem>
                  <MenuItem value="high">{t('report.urgency_high')}</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                <Button 
                  variant="outlined" 
                  onClick={() => navigate('/')}
                  disabled={submitting}
                >
                  {t('common.cancel')}
                </Button>
                <Button 
                  type="submit" 
                  variant="contained" 
                  disabled={submitting}
                >
                  {submitting ? t('common.submitting') : t('common.submit')}
                </Button>
              </Box>
            </Grid>
            
            {error && (
              <Grid item xs={12}>
                <Typography color="error">{error}</Typography>
              </Grid>
            )}
          </Grid>
        </form>
      </Paper>
    </Box>
  );
};

export default Report;