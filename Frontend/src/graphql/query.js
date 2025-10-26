export const GET_ACCOUNT_BY_EMAIL = `
  query GetAccountByEmail($email: String!) {
    getAccountByEmail(email: $email) {
      id
      accountNumber
      accountType
      balance
      createdAt
    }
  }
`;