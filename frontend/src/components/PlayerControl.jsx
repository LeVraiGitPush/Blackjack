// src/components/Seat.jsx

import React from 'react';
import PlayerControl from './PlayerControl';

const Seat = ({ seatId, occupant, hand = [], value = 0, status = "waiting", isUserSeat = false, lobbyId, onUpdate }) => {
  return (
    <div
      style={{
        border: "1px solid #ccc",
        borderRadius: "8px",
        padding: "10px",
        width: "140px",
        minHeight: "160px",
        textAlign: "center",
        backgroundColor:
          status === "blackjack"
            ? "#d4ffd4"
            : status === "busted"
            ? "#ffd4d4"
            : "#fff",
      }}
    >
      <h4>Seat {seatId + 1}</h4>
      <p>
        {occupant ? <strong>{occupant}</strong> : <em>🪑 Empty</em>}
      </p>

      {hand.length > 0 && (
        <>
          <div style={{ margin: "5px 0", fontSize: "14px" }}>
            {hand.map((card, i) => (
              <div key={i}>{card[0]}{card[1]}</div>
            ))}
          </div>
          <div>
            <strong>Total:</strong> {value}
          </div>
        </>
      )}

      <p style={{ fontSize: "12px" }}>Status: {status}</p>

      {isUserSeat && (
        <PlayerControl lobbyId={lobbyId} seatId={seatId} onUpdate={onUpdate} />
      )}
    </div>
  );
};

export default Seat;
