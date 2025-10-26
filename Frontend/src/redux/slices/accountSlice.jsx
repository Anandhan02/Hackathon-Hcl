import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { graphqlRequest } from "../../services/graphqlClient.js";
import { CREATE_ACCOUNT_MUTATION } from "../../graphql/mutation.js";
import { GET_ACCOUNT_BY_EMAIL } from "../../graphql/query.js";

/* ────────────────────────────────────────────────
    CREATE ACCOUNT MUTATION
──────────────────────────────────────────────── */
export const createAccount = createAsyncThunk(
  "account/createAccount",
  async ({ accountType, initialDeposit, token }, { rejectWithValue }) => {
    try {
      const variables = {
        input: {
          accountType,
          initialDeposit: parseFloat(initialDeposit),
        },
      };

      const data = await graphqlRequest(CREATE_ACCOUNT_MUTATION, variables, token);
      return data.createAccount;
    } catch (error) {
      return rejectWithValue(error.message || "Failed to create account");
    }
  }
);

/* ────────────────────────────────────────────────
    GET ACCOUNT BY EMAIL QUERY
──────────────────────────────────────────────── */
export const fetchAccountByEmail = createAsyncThunk(
  "account/fetchByEmail",
  async ({ email, token }, { rejectWithValue }) => {
    try {
      const data = await graphqlRequest(GET_ACCOUNT_BY_EMAIL, { email }, token);
      const account = data?.getAccountByEmail;
      if (!account) throw new Error("No account found for this email.");
      return account;
    } catch (error) {
      return rejectWithValue(error.message || "Failed to fetch account");
    }
  }
);

// REDUX SLICE

const accountSlice = createSlice({
  name: "account",
  initialState: {
    accounts: [],        // list of all user accounts
    newAccount: null,    // latest created account
    accountByEmail: null, // single fetched account by email
    loading: false,
    error: null,
  },
  reducers: {
    clearNewAccount: (state) => {
      state.newAccount = null;
      state.error = null;
    },
    clearAccountByEmail: (state) => {
      state.accountByEmail = null;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      /* ── Create Account ───────────────────────── */
      .addCase(createAccount.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createAccount.fulfilled, (state, action) => {
        state.loading = false;
        state.newAccount = action.payload;
        state.accounts.push(action.payload);
      })
      .addCase(createAccount.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      /* ── Get Account By Email ─────────────────── */
      .addCase(fetchAccountByEmail.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAccountByEmail.fulfilled, (state, action) => {
        state.loading = false;
        state.accountByEmail = action.payload;
      })
      .addCase(fetchAccountByEmail.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearNewAccount, clearAccountByEmail } = accountSlice.actions;
export default accountSlice.reducer;
