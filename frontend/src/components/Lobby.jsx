// src/components/Lobby.jsx
import React, { useState } from 'react';
import { createLobby, addFakePlayer } from '../api/gameAPI';

const Lobby = ({ setLobbyId, setPlayerName }) => {
  const [name, setName] = useState("");

  const handleCreate = async () => {
    const res = await createLobby(name);
    setLobbyId(res.data.lobby_id);
    setPlayerName(name);
  };

  return (
    <div>
      <h2>Create Lobby</h2>
      <input
        placeholder="Your Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <button onClick={handleCreate}>🎮 Create Lobby</button>
    </div>
  );
};

export default Lobby;
