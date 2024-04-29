import { gql } from '@apollo/client';

export const GET_ALL_USERS = gql`
query MyQuery {
  users {
    ... on UserList {
      __typename
      users {
        characters {
          type {
            name
            id
            baseCharisma
            baseConstitution
            baseDexterity
            baseIntelligence
            baseStrength
            baseWisdom
            experienceRate
          }
          name
          charisma
          constitution
          dexterity
          experience
          id
          intelligence
          level
          strength
          wisdom
        }
        name
        id
        discordId
        isAdmin
      }
    }
    ... on Error {
      __typename
      message
    }
  }
}
`

export const GET_USER_BY_ID = gql`
query MyQuery {
  user {
    ... on User {
      id
      name
      characters {
        id
        level
        name
        type {
          name
        }
      }
    }
  }
}
`