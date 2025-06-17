// src/components/GameTable.jsx

import React, { useEffect, useState } from 'react';
import {
  getLobbyInfo,
  startRound,
  assignSeat
} from '../api/gameAPI';
import Seat from './Seat';
import DealerHand from './DealerHand';
import BalanceDisplay from './BalanceDisplay';

const GameTable = ({ lobbyId, playerName }) => {
  const [players, setPlayers] = useState([]);
  const [seats, setSeats] = useState(Array(7).fill(null));
  const [dealer, setDealer] = useState({ hand: [], value: 0 });
  const [statusMsg, setStatusMsg] = useState("");
  const [balances, setBalances] = useState({});

  const fetchLobby = async () => {
    try {
      const res = await getLobbyInfo(lobbyId);
      const playersList = res.data.players || [];
      setPlayers(playersList);

      // TODO: replace this with backend-provided seat state
      setSeats([
        { name: playerName, hand: [], value: 0, status: "waiting" },
        { name: "Bot42", hand: [], value: 0, status: "waiting" },
        ...Array(5).fill(null),
      ]);

      setBalances({
        [playerName]: 1000,
        Bot42: 1000,
      });
    } catch (err) {
      console.error("Error fetching lobby info", err);
    }
  };

  useEffect(() => {
    fetchLobby();
  }, [lobbyId]);

  const handleStartRound = async () => {
    try {
      await startRound(lobbyId);
      setStatusMsg("🎲 Round started!");
      fetchLobby();
    } catch (err) {
      setStatusMsg("❌ Failed to start round");
    }
  };

  const handleAssignSeat = async (index) => {
    try {
      await assignSeat(lobbyId, index, playerName);
      setStatusMsg(`✅ You took Seat ${index + 1}`);
      fetchLobby();
    } catch (err) {
      setStatusMsg("❌ Seat assignment failed");
    }
  };

  return (
    <div>
      <h2>🎰 Blackjack Table – Lobby <code>{lobbyId}</code></h2>
      <p>Logged in as: <strong>{playerName}</strong></p>

      <DealerHand hand={dealer.hand} value={dealer.value} />

      <div style={{ display: "flex", justifyContent: "center", flexWrap: "wrap", gap: "15px" }}>
        {seats.map((seat, index) => (
          <div key={index} style={{ textAlign: "center" }}>
            <Seat
              seatId={index}
              occupant={seat?.name}
              hand={seat?.hand || []}
              value={seat?.value || 0}
              status={seat?.status || "waiting"}
              isUserSeat={seat?.name === playerName}
              lobbyId={lobbyId}
              onUpdate={(data) => {
                const updatedSeats = [...seats];
                updatedSeats[index] = {
                  ...updatedSeats[index],
                  ...data,
                };
                setSeats(updatedSeats);
              }}
            />
            {!seat && (
              <button onClick={() => handleAssignSeat(index)}>
                Claim Seat {index + 1}
              </button>
            )}
          </div>
        ))}
      </div>

      <button onClick={handleStartRound} style={{ marginTop: "20px" }}>
        ▶️ Start Round
      </button>

      <p>{statusMsg}</p>

      <BalanceDisplay playerName={playerName} balance={balances[playerName] || 0} />

      <h3>Players in Lobby:</h3>
      <ul>
        {players.map((p) => (
          <li key={p}>{p}</li>
        ))}
      </ul>
    </div>
  );
};

export default GameTable;

