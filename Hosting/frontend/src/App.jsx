import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion'; // Import motion from framer-motion
import './App.css'; // Import the custom CSS for styling

function App() {
  const [city, setCity] = useState('');
  const [aqi, setAqi] = useState(null);
  const [composition, setComposition] = useState(null);
  const [cities, setcities] = useState([])
  const [loading, setLoading] = useState(false)



  useEffect(() => {
    fetchCities()
  }, [])

  const fetchCities = async () => {
    try {
      const response = await axios.get('/cities')

      setcities(response.data.cities)

    } catch (error) {
      console.error('Error fetching prediction:', error);
    }

  }


  const handleCityChange = (event) => {
    console.log(event.target.value);
    setCity(event.target.value);
  };

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const response = await axios.post('/predict', { city });
      setAqi(response.data.aqi);
      setComposition(response.data.composition);
    } catch (error) {
      console.error('Error fetching prediction:', error);
    } finally {
      setLoading(false)
    }
  };

  const handleSelectClick = () => {
    setAqi(null)
  }

  const getAqiInfo = (aqiValue) => {
    switch (aqiValue) {
      case 1:
        return { label: 'Good', color: '#2ecc71', emoji: '🟢' };     
      case 2:
        return { label: 'Fair', color: '#f1c40f', emoji: '🟡' };     
      case 3:
        return { label: 'Moderate', color: '#e67e22', emoji: '🟠' }; 
      case 4:
        return { label: 'Poor', color: '#e74c3c', emoji: '🔴' };     
      case 5:
        return { label: 'Very Poor', color: '#8e44ad', emoji: '🟣' }; 
      default:
        return { label: 'Unknown', color: 'gray', emoji: '❓' };
    }
  };


  return (
    <div className="container">
      <motion.h1
        className="title"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        Air Quality Index Prediction
      </motion.h1>
      <motion.div
        className="form-container"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 0.5 }}
      >
        <label className="city-label">
          Select City:
          <select onClick={handleSelectClick} onChange={handleCityChange} value={city} className="city-select">
            <option value="">--Select a City--</option>
            {cities.map((cityName) => (
              <option key={cityName} value={cityName}>
                {cityName}
              </option>
            ))}
          </select>
        </label>
        <motion.button
          className="submit-button"
          onClick={handleSubmit}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          transition={{ type: 'spring', stiffness: 300 }}
        >
          {loading ? "Fetching..." : "Get AQI Prediction"}
        </motion.button>
      </motion.div>

      {loading && (
        <div className="spinner"></div>
      )}

      {aqi && !loading && (
        <motion.div
          className="result-container"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 1 }}
        >
          <motion.h3
            className="aqi-result"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
          >
            Predicted AQI: {aqi}
          </motion.h3>

          <motion.div
            className="aqi-badge"
            style={{
              backgroundColor: getAqiInfo(aqi).color,
              padding: '10px 20px',
              borderRadius: '25px',
              display: 'inline-block',
              color: '#fff',
              fontWeight: 'bold',
              fontSize: '1.1rem',
              boxShadow: '0 4px 10px rgba(0,0,0,0.3)',
              margin: '10px 0'
            }}
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 300 }}
          >
            {getAqiInfo(aqi).emoji} {getAqiInfo(aqi).label}
          </motion.div>

          <motion.h4
            style={{ display: 'flex', flexDirection: 'row' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
          >
            <p>City :</p>
            <p style={{ color: 'blue' }}>&nbsp;&nbsp;{city}</p>
          </motion.h4>
          <motion.div
            className="composition-table-container"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1, delay: 1.5 }}
          >
            <h4>Air Quality Composition</h4>
            <motion.table
              className="composition-table"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1, delay: 2 }}
            >
              <thead>
                <tr>
                  <th>Component</th>
                  <th>Percentage</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(composition).map(([key, value]) => (
                  <tr key={key}>
                    <td>{key}</td>
                    <td>{value}</td>
                  </tr>
                ))}
              </tbody>
            </motion.table>
          </motion.div>
        </motion.div>
      )}
    </div>
  );
}

export default App;


