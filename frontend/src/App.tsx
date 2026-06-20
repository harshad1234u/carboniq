import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Layout } from './components/Layout';
import { Landing } from './pages/Landing';
import { Login } from './pages/Login';
import { Onboarding } from './pages/Onboarding';
import { Dashboard } from './pages/Dashboard';
import { Calculator } from './pages/Calculator';
import { AiCoach } from './pages/AiCoach';
import { EcoTwin } from './pages/EcoTwin';
import { Challenges } from './pages/Challenges';
import { Profile } from './pages/Profile';

import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/onboarding" element={
            <ProtectedRoute requireProfile={false}>
              <Onboarding />
            </ProtectedRoute>
          } />
          
          {/* Protected Routes with Layout */}
          <Route path="/dashboard" element={<ProtectedRoute><Layout><Dashboard /></Layout></ProtectedRoute>} />
          <Route path="/calculator" element={<ProtectedRoute><Layout><Calculator /></Layout></ProtectedRoute>} />
          <Route path="/ai-coach" element={<ProtectedRoute><Layout><AiCoach /></Layout></ProtectedRoute>} />
          <Route path="/eco-twin" element={<ProtectedRoute><Layout><EcoTwin /></Layout></ProtectedRoute>} />
          <Route path="/challenges" element={<ProtectedRoute><Layout><Challenges /></Layout></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Layout><Profile /></Layout></ProtectedRoute>} />
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
