import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { MapContainer, TileLayer, GeoJSON, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import RiskIndicator from "../../components/risk/RiskIndicator";
import AlertCard from "../../components/risk/AlertCard";
import { Box, Grid, Typography, Button, CircularProgress } from "@mui/material";
import { MAP_CENTER, MAP_ZOOM, RISK_LEVELS } from "../../config";
import axios from "axios";

const Dashboard = () => {
  const { t } = useTranslation();
  const [riskData, setRiskData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // ✅ Auto-fetch risk data on mount & every 5 mins
  useEffect(() => {
    const fetchRiskData = async () => {
      try {
        const token = localStorage.getItem("access_token"); // JWT auth support
        const response = await axios.get("/api/risk/", {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        });
        setRiskData(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchRiskData();
    const interval = setInterval(fetchRiskData, 300000); // Refresh every 5 mins

    return () => clearInterval(interval);
  }, []);

  // ✅ Utility to recenter map when MAP_CENTER changes
  const RecenterMap = ({ center }) => {
    const map = useMap();
    map.setView(center);
    return null;
  };

  // ✅ Loading state
  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", mt: 5 }}>
        <CircularProgress />
      </Box>
    );
  }

  // ✅ Error state
  if (error) {
    return (
      <Typography color="error" sx={{ mt: 3, textAlign: "center" }}>
        {t("dashboard.error")}: {error}
      </Typography>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* ✅ Title */}
      <Typography variant="h4" gutterBottom>
        {t("dashboard.title")}
      </Typography>

      <Grid container spacing={3}>
        {/* ✅ Map Section */}
        <Grid item xs={12} md={8}>
          <Box sx={{ height: "400px", borderRadius: 2, overflow: "hidden" }}>
            <MapContainer
              center={MAP_CENTER}
              zoom={MAP_ZOOM}
              style={{ height: "100%", width: "100%" }}
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
                    color: "white",
                    fillOpacity: 0.7,
                  })}
                />
              )}
              <RecenterMap center={MAP_CENTER} />
            </MapContainer>
          </Box>
        </Grid>

        {/* ✅ Risk & Alerts Section */}
        <Grid item xs={12} md={4}>
          <RiskIndicator
            level={riskData?.currentRisk || "low"}
            score={riskData?.riskScore}
          />

          {riskData?.alerts?.length > 0 && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="h6" gutterBottom>
                {t("dashboard.active_alerts")}
              </Typography>
              {riskData.alerts.map((alert) => (
                <AlertCard key={alert.id} alert={alert} />
              ))}
            </Box>
          )}
        </Grid>
      </Grid>

      {/* ✅ Action Buttons */}
      <Box sx={{ mt: 3, display: "flex", justifyContent: "center", gap: 2 }}>
        <Button
          variant="contained"
          color="primary"
          href="/report"
          sx={{ px: 4 }}
        >
          {t("report.button")}
        </Button>
        <Button
          variant="outlined"
          color="primary"
          href="/alerts"
          sx={{ px: 4 }}
        >
          {t("dashboard.view_alerts")}
        </Button>
      </Box>
    </Box>
  );
};

export default Dashboard;
