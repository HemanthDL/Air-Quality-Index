import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion'; // Import motion from framer-motion
import './App.css'; // Import the custom CSS for styling

function App() {
  const [city, setCity] = useState('');
  const [aqi, setAqi] = useState(null);
  const [composition, setComposition] = useState(null);
  const [cities, setcities] = useState([])




  useEffect(() => {
    fetchCities()
  }, [])

  const fetchCities = async () => {
    try {
      const response = await axios.get('http://localhost:5000/cities')

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
    try {
      const response = await axios.post('http://localhost:5000/predict', { city });
      setAqi(response.data.aqi);
      setComposition(response.data.composition);
    } catch (error) {
      console.error('Error fetching prediction:', error);
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
          <select onChange={handleCityChange} value={city} className="city-select">
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
          Get AQI Prediction
        </motion.button>
      </motion.div>

      {aqi && (
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
          <motion.h4
          style={{display:'flex',flexDirection : 'row'}}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
          >
            <p>City : </p><p style={{color : 'blue'}}>&nbsp;&nbsp;{city}</p>
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
