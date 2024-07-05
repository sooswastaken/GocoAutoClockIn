import { useState, useEffect } from 'react';
import axios from 'axios';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { LocalizationProvider, TimePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import Checkbox from '@mui/material/Checkbox';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import './App.css';

// Create a dark theme
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});
function App() {
  const [config, setConfig] = useState({});

  useEffect(() => {
    axios.get('/config')
      .then(response => {
        let data = {
          "monday": {"enabled": true, "start": "08:35", "end": "17:30"},
          "tuesday": {"enabled": true, "start": "08:35", "end": "17:30"},
          "wednesday": {"enabled": true, "start": "08:35", "end": "17:30"},
          "thursday": {"enabled": true, "start": "08:35", "end": "17:30"},
          "friday": {"enabled": true, "start": "09:00", "end": "13:00"}
        }
                Object.keys(data).forEach(day => {
          data[day].start = new Date(`1970-01-01T${data[day].start}:00`);
          data[day].end = new Date(`1970-01-01T${data[day].end}:00`);
        });

        setConfig(data);
        console.log(response)
      })
      .catch(error => {
        console.error('Error fetching configuration:', error);
      });
  }, []);

  const saveConfig = () => {
    axios.post('/update', config)
      .then(response => {
        if (response.data.status === 'success') {
          alert('Configuration saved successfully!');
        } else {
          alert('Error saving configuration.');
        }
      })
      .catch(error => {
        console.error('Error saving configuration:', error);
      });
  };

  const testPunch = () => {
    axios.post('/test')
      .then(response => {
        if (response.data.status === 'success') {
          alert('Test punch successful!');
        } else {
          alert('Error testing punch.');
        }
      })
      .catch(error => {
        console.error('Error testing punch:', error);
      });
  };

  const handleChange = (day, field, value) => {
    setConfig(prevConfig => ({
      ...prevConfig,
      [day]: {
        ...prevConfig[day],
        [field]: field === 'enabled' ? value : value
      }
    }));
  };

    return (
    <ThemeProvider theme={darkTheme}>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <div>
          <h1>Auto Clocker Configuration</h1>
          <table style={{borderCollapse: 'collapse', border: 'none'}}>
            <thead>
              <tr>
                <th>Day</th>
                <th>On</th>
                <th>Start Time</th>
                <th>End Time</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(config).map(([day, settings]) => (
                <tr key={day}>
                  <td>{day.charAt(0).toUpperCase() + day.slice(1)}</td>
                  <td><Checkbox className="checkbox" checked={settings.enabled} onChange={e => handleChange(day, 'enabled', e.target.checked)} /></td>
                  <td>
                    <TimePicker className="time-picker"
                      value={settings.start}
                      onChange={newValue => handleChange(day, 'start', newValue)}
                      renderInput={(params) => <TextField {...params} />}
                    />
                  </td>
                  <td>
                    <TimePicker className="time-picker"
                      value={settings.end}
                      onChange={newValue => handleChange(day, 'end', newValue)}
                      renderInput={(params) => <TextField {...params} />}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <Button className="save" variant="contained" onClick={saveConfig}>Save Configuration</Button>
          <Button className="test" variant="contained" color="secondary" onClick={testPunch}>Test Punching</Button>
        </div>
      </LocalizationProvider>
    </ThemeProvider>
  );
}

export default App;
