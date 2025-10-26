import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { createAccount, clearNewAccount } from "../../../redux/slices/accountSlice";

const CreateAccountForm = () => {
  const dispatch = useDispatch();
  const { accessToken } = useSelector((state) => state.auth);
  const { loading, error, newAccount } = useSelector((state) => state.account);

  const [form, setForm] = useState({
    accountType: "",
    initialDeposit: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.accountType || !form.initialDeposit) return;
    dispatch(createAccount({ ...form, token: accessToken }));
  };

  useEffect(() => {
    if (newAccount) {
      const timer = setTimeout(() => dispatch(clearNewAccount()), 8000);
      return () => clearTimeout(timer);
    }
  }, [newAccount, dispatch]);

  return (
    <div className="bg-gray-50 border mt-10 p-6 rounded-xl shadow-sm">
      <h3 className="text-xl font-semibold mb-4 text-gray-800">
        🏦 Create New Account
      </h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1 font-medium">Account Type</label>
          <select
            name="accountType"
            value={form.accountType}
            onChange={handleChange}
            required
            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select Account Type</option>
            <option value="savings">Savings</option>
            <option value="current">Current</option>
            <option value="fd">Fixed Deposit</option>
          </select>
        </div>

        <div>
          <label className="block mb-1 font-medium">Initial Deposit</label>
          <input
  type="number"
  name="initialDeposit"
  value={form.initialDeposit || ""}
  onChange={(e) =>
    setForm({ ...form, initialDeposit: e.target.value.replace(/[^0-9.]/g, "") })
  }
  placeholder="Enter amount"
  required
  min="0"
  step="any"
  inputMode="decimal"
  className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
/>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
        >
          {loading ? "Creating..." : "Create Account"}
        </button>

        {error && <p className="text-red-600 mt-3 text-center">{error}</p>}
      </form>

      {newAccount && (
        <div className="mt-8 bg-green-50 border border-green-300 p-4 rounded-lg text-left">
          <h4 className="font-semibold text-green-700 mb-2">Account Created</h4>
          <p><strong>Account Number:</strong> {newAccount.accountNumber}</p>
          <p><strong>Type:</strong> {newAccount.accountType}</p>
          <p><strong>Balance:</strong> ₹{newAccount.balance}</p>
          <p><strong>Created At:</strong> {new Date(newAccount.createdAt).toLocaleString()}</p>
        </div>
      )}
    </div>
  );
};

export default CreateAccountForm;
