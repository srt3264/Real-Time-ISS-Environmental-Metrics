// frontend/src/App.js
import React from 'react';
import SimpleTest from './SimpleTest'; // <--- THIS IS THE KEY IMPORT
import { CssBaseline, AppBar, Toolbar, Typography, Box } from '@mui/material';

function App() {
  return (
    // Box is a Material-UI component, flexGrow helps it take up available space
    <Box sx={{ flexGrow: 1 }}>
      {/* CssBaseline resets some browser default styles for Material-UI */}
      <CssBaseline />

      {/* AppBar is Material-UI's navigation bar component */}
      <AppBar position="static">
        <Toolbar>
          {/* Typography for the app title */}
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            API & WebSocket Test App
          </Typography>
        </Toolbar>
      </AppBar>

      {/* This is where your SimpleTest component is rendered */}
      <SimpleTest /> 
    </Box>
  );
}

export default App;