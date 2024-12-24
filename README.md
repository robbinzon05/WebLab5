# WebLab5

RPS (Rock, Paper, Scissors) Online Game is a multiplayer game where players in a lobby can engage in quick matches of "Rock, Paper, Scissors." The project features real-time interactions, a simple user interface, and robust backend logic to ensure fair gameplay.

Features

Game Functionality

Multiplayer Support: Players in the same lobby can join an RPS match and play in real time.

Dynamic Lobby System: Players can join and leave lobbies without disrupting ongoing games.

Fair Play Enforcement:

Players cannot make multiple moves in the same round.

If a player exits mid-game, the other player is also notified and redirected to the home page.

Frontend

Built using Vue.js for a responsive and user-friendly interface.

Real-time updates for game states, including moves and round results.

Automatic redirection if a player leaves the game.

Backend

Developed using Django.

Implements game state tracking and robust error handling to ensure a smooth experience.

Prevents duplicate moves in the same round with server-side validations.

How It Works

Workflow

Players enter a lobby.

A game session starts when two players join a match.

Each player makes their move (Rock, Paper, or Scissors).

The backend determines the winner and updates the game state.

The game resets for the next round or ends if a player leaves.

Exiting the Game

When a player exits, the following occurs:

The exiting player triggers the stop_rps_view method.

The remaining player sees status='no_game' and is redirected to the home page.

Preventing Repeated Moves

Backend ensures fair play by checking if a user has already made a move for the current round.

If a repeated move is detected, the server responds with a 400 error.

Setup

Prerequisites

Python 3.9+

Node.js 14+

Django

Vue.js

Installation

Backend

Clone the repository:

git clone https://github.com/yourusername/rps-game.git

Navigate to the backend directory:

cd rps-game/backend

Install dependencies:

pip install -r requirements.txt

Run the server:

python manage.py runserver

Frontend

Navigate to the frontend directory:

cd rps-game/frontend

Install dependencies:

npm install

Start the development server:

npm run serve

Usage

Access the application at http://localhost:8000.

Join a lobby and start playing "Rock, Paper, Scissors"!

Follow the on-screen instructions to make moves, view results, or exit the game.

Future Enhancements

Add support for multiple lobbies.

Implement a ranking system for players.

Expand the game selection to include additional mini-games.

Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements

Special thanks to all contributors and playtesters who helped refine the project!

## Technological Stack

- **SPA -** vue3 + typescript + design system
- **REST -** DRF
- **Docker**
- **CI -** github actions/buildbot/etc...
- **Websockets**

## Backend start

```bash
python -m venv venv # create virtual environment
venv\Scripts\activate # activate virtual environment
pip install -r requirements.txt # install python dependencies

cd backend
python manage.py migrate # migrate to the database
python manage.py runserver # start the server
```

## Frontend start

```bash
cd frontend
npm install # install dependencies
npm run serve # run local dev server
```
