export const REGISTER_USER_MUTATION = `
  mutation RegisterUser($input: RegisterInput!) {
    registerUser(input: $input) {
      accessToken
      user {
        id
        name
        email
        roles
      }
    }
  }
`;

export const LOGIN_USER_MUTATION = `
  mutation LoginUser($input: LoginInput!) {
    loginUser(input: $input) {
      accessToken
      user {
        id
        name
        email
        roles
      }
    }
  }
`;

export const CREATE_ACCOUNT_MUTATION = `
  mutation CreateAccount($input: CreateAccountInput!) {
    createAccount(input: $input) {
      id
      accountNumber
      accountType
      balance
      createdAt
    }
  }
`;
