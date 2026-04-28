import { MapContainer, TileLayer, GeoJSON, Tooltip } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const RiskMap = ({ geoData, riskLevels }) => {
  const mapStyle = (feature) => {
    const risk = riskLevels[feature.properties.sub_county] || 0;
    return {
      fillColor: risk > 0.8 ? '#ef4444' : risk > 0.5 ? '#f59e0b' : '#22c55e',
      weight: 1,
      opacity: 1,
      color: 'white',
      fillOpacity: 0.7,
    };
  };

  return (
    <MapContainer center={[-0.1022, 34.7617]} zoom={9} style={{ height: "500px", width: "100%" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <GeoJSON data={geoData} style={mapStyle}>
        <Tooltip sticky>Outbreak Risk Detected</Tooltip>
      </GeoJSON>
    </MapContainer>
  );
};

export default RiskMap;
