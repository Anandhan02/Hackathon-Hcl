import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { logout } from "../../../redux/slices/authSlice";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import CreateAccountForm from "../../account/components/CreateAccountForm.jsx";
import ViewAccountByEmail from '../../account/components/viewAccountByEmail.jsx';

//  React Icons
import { FiLogOut, FiPlusCircle, FiClock, FiUser } from "react-icons/fi";
import { HiOutlineBanknotes, HiOutlineUserCircle } from "react-icons/hi2";

const Dashboard = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user, accessToken } = useSelector((state) => state.auth);

  const [remainingTime, setRemainingTime] = useState(0);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showAccountLookup, setShowAccountLookup] = useState(false);

  // 🕒 Decode JWT & start timer
  useEffect(() => {
    if (!accessToken) return;

    try {
      const decoded = jwtDecode(accessToken);
      const expTime = decoded.exp * 1000;
      const now = Date.now();
      const diff = Math.max(0, Math.floor((expTime - now) / 1000));

      setRemainingTime(diff);

      const interval = setInterval(() => {
        setRemainingTime((prev) => {
          if (prev <= 1) {
            clearInterval(interval);
            dispatch(logout());
            navigate("/login");
            alert("Session expired. Please log in again.");
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(interval);
    } catch (err) {
      console.error("Invalid token:", err);
      dispatch(logout());
      navigate("/login");
    }
  }, [accessToken, dispatch, navigate]);

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
  };

  const handleLogout = () => {
    dispatch(logout());
    navigate("/login");
  };

  return (
    <div className="max-w-3xl mx-auto mt-12 bg-white shadow-xl p-8 rounded-2xl text-center">
      <div className="flex flex-col items-center mb-6">
        <HiOutlineUserCircle className="text-blue-600 text-5xl mb-2" />
        <h2 className="text-3xl font-semibold">
          Welcome, {user?.name || "User"}!
        </h2>
        <p className="text-gray-600">{user?.email}</p>
      </div>

      {/* 🕒 Session Timer */}
      {remainingTime > 0 && (
        <div className="flex items-center justify-center gap-2 text-lg font-medium text-blue-600 mb-6">
          <FiClock className="text-blue-500 text-xl" />
          <span>
            Session expires in{" "}
            <span className="text-red-500 font-semibold">
              {formatTime(remainingTime)}
            </span>
          </span>
        </div>
      )}

      {/* 🔹 Action Buttons */}
      <div className="flex flex-wrap justify-center gap-4 mb-6">
        <button
          onClick={() => setShowCreateForm((prev) => !prev)}
          className="flex items-center gap-2 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          <FiPlusCircle className="text-lg" />
          {showCreateForm ? "Close Account Form" : "Create Account"}
        </button>

        <button
          onClick={() => setShowAccountLookup((prev) => !prev)}
          className="flex items-center gap-2 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition"
        >
          <HiOutlineBanknotes className="text-lg" />
          {showAccountLookup ? "Close Account View" : "View My Account"}
        </button>

        <button
          onClick={handleLogout}
          className="flex items-center gap-2 bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition"
        >
          <FiLogOut className="text-lg" />
          Logout
        </button>
      </div>

      {/* 🔹 Conditional Render Sections */}
      {showCreateForm && (
        <div className="border-t pt-6 mt-4">
          <CreateAccountForm />
        </div>
      )}

      {showAccountLookup && (
        <div className="border-t pt-6 mt-4">
          <ViewAccountByEmail />
        </div>
      )}
    </div>
  );
};

export default Dashboard;
