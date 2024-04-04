interface LoginData {
    login: {
        __typename: string;
        token: string|undefined;
        message: string|undefined;
        name: string|undefined;
        isAdmin: boolean|undefined;
    };
}

class LoginResponse {
    token: string|undefined;
    name: string|undefined;
    message: string|undefined;
    typename: string
    isAdmin: boolean|undefined;
    constructor(data: LoginData) {
        this.typename = data.login.__typename;
        this.token = data.login.token;
        this.name = data.login.name;
        this.message = data.login.message;
        this.isAdmin = data.login.isAdmin;
    }
}

export { LoginResponse };