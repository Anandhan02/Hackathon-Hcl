import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import LoginForm from "./feature/auth/components/LoginForm.jsx";
import RegisterForm from "./feature/auth/components/RegisterForm.jsx";
import Dashboard from "./feature/auth/pages/Dashboard.jsx";
import { useSelector } from "react-redux";

const ProtectedRoute = ({ children }) => {
  const { accessToken } = useSelector((state) => state.auth);
  return accessToken ? children : <Navigate to="/login" replace />;
};

const App = () => {
  return (
    <Router>
      <ToastContainer position="top-right" autoClose={3000} />
      <Routes>
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
};

export default App;
