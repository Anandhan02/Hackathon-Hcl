import axios from "axios";

const API_URL = "http://localhost:8000/graphql";

export const graphqlRequest = async (query, variables = {}, token = null) => {
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await axios.post(API_URL, { query, variables }, { headers });

  if (res.data.errors) throw new Error(res.data.errors[0].message);
  return res.data.data; // Only the useful data
};
