import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import ControlPanel from './components/AI/ControlPanel';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/control-panel" element={<ControlPanel />} />
        {/* Add other routes here */}
      </Routes>
    </Router>
  );
}

export default App; 