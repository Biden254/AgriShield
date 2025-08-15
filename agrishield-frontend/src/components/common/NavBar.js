import React from 'react';
import { useTranslation } from 'react-i18next';
import { AppBar, Toolbar, Typography, Button, IconButton, Menu, MenuItem, useMediaQuery } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { Link, useNavigate } from 'react-router-dom';

const NavBar = () => {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const isMobile = useMediaQuery('(max-width:600px)');
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    handleMenuClose();
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          AgriShield
        </Typography>
        
        {isMobile ? (
          <>
            <IconButton
              size="large"
              edge="end"
              color="inherit"
              aria-label="menu"
              onClick={handleMenuOpen}
            >
              <MenuIcon />
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleMenuClose}
            >
              <MenuItem onClick={() => navigate('/')}>{t('nav.dashboard')}</MenuItem>
              <MenuItem onClick={() => navigate('/alerts')}>{t('nav.alerts')}</MenuItem>
              <MenuItem onClick={() => navigate('/report')}>{t('nav.report')}</MenuItem>
              <MenuItem onClick={() => navigate('/settings')}>{t('nav.settings')}</MenuItem>
              <MenuItem onClick={() => changeLanguage(i18n.language === 'en' ? 'sw' : 'en')}>
                {i18n.language === 'en' ? 'Kiswahili' : 'English'}
              </MenuItem>
            </Menu>
          </>
        ) : (
          <>
            <Button color="inherit" component={Link} to="/">{t('nav.dashboard')}</Button>
            <Button color="inherit" component={Link} to="/alerts">{t('nav.alerts')}</Button>
            <Button color="inherit" component={Link} to="/report">{t('nav.report')}</Button>
            <Button color="inherit" component={Link} to="/settings">{t('nav.settings')}</Button>
            <Button 
              color="inherit" 
              onClick={() => changeLanguage(i18n.language === 'en' ? 'sw' : 'en')}
            >
              {i18n.language === 'en' ? 'Kiswahili' : 'English'}
            </Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default NavBar;