// src/App.jsx
import React from 'react';
import GameTable from './components/GameTable';

function App() {
  const lobbyId = 'demo-lobby-123'; // À adapter si tu veux un vrai ID
  const playerName = 'Jean';

  return (
    <div className="App">
      <h1>🎰 Blackjack Game Table</h1>
      <GameTable lobbyId={lobbyId} playerName={playerName} />
    </div>
  );
}

export default App;

