interface UserData {
  user:{
    __typename: string;
    id: string;
    name: string;
    characters: Record<string, string|number>[];
    isAdmin: boolean;
  }
}

class User {
  id: string;
  name: string;
  characters: Record<string, string|number>[];
  typename: string;
  isAdmin: boolean;
  constructor(data: UserData) {
      this.typename = data.user.__typename;
      this.id = data.user.id;
      this.name = data.user.name;
      this.characters = data.user.characters;
      this.isAdmin = data.user.isAdmin;
  }
}

export { User };