# Frontend
This project contains the main user interface for the A-GVN system. Accessible on web browsers.
Note, currently interfaces with Backend via HTTP REST.

## Testing
Unit tests, run `npm test`
For coverage, `npm test -- --coverage`

## Directory Structure
`/agvn-app` -> Contains main frontend for AGVN Services and Utilties such as Aeros.
`/archive` -> Contains some examples and deprecated code snippets.

## How to run the Frontend
Run `npm run build && npm run start` for `/agvn-app` and `npm start` for `/aeros-app`.

Then go to `localhost:3000`.
