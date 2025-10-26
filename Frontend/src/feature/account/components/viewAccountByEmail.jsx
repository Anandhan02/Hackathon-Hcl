import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAccountByEmail, clearAccountByEmail } from "../../../redux/slices/accountSlice";

const ViewAccountByEmail = () => {
  const dispatch = useDispatch();
  const { accessToken } = useSelector((state) => state.auth);
  const { account, loading, error } = useSelector((state) => state.account);

  const [email, setEmail] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!email) return;
    dispatch(fetchAccountByEmail({ email, token: accessToken }));
  };

  const handleClear = () => {
    dispatch(clearAccountByEmail());
    setEmail("");
  };

  return (
    <div className="max-w-lg mx-auto mt-10 bg-white shadow-lg rounded-xl p-8">
      <h3 className="text-xl font-semibold text-gray-800 mb-4 text-center">
         Find Account by Email
      </h3>

      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 mb-6">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter customer email"
          required
          className="flex-1 p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-5 py-2 rounded hover:bg-blue-700 transition"
        >
          {loading ? "Searching..." : "Search"}
        </button>
        <button
          type="button"
          onClick={handleClear}
          className="bg-gray-400 text-white px-5 py-2 rounded hover:bg-gray-500 transition"
        >
          Clear
        </button>
      </form>

      {/*  Results */}
      {error && <p className="text-red-600 text-center">{error}</p>}

      {account && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 text-left">
          <h4 className="text-lg font-semibold text-green-700 mb-2">
             Account Details
          </h4>
          <p><strong>ID:</strong> {account.id}</p>
          <p><strong>Account Number:</strong> {account.accountNumber}</p>
          <p><strong>Type:</strong> {account.accountType}</p>
          <p><strong>Balance:</strong> ₹{account.balance}</p>
          <p><strong>Created At:</strong> {new Date(account.createdAt).toLocaleString()}</p>
        </div>
      )}
    </div>
  );
};

export default ViewAccountByEmail;
