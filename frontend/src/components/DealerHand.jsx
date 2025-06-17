// src/components/DealerHand.jsx

import React from 'react';

const DealerHand = ({ hand = [], value = 0 }) => {
  return (
    <div style={{
      padding: "10px",
      textAlign: "center",
      backgroundColor: "#eee",
      border: "1px solid #ccc",
      marginBottom: "20px"
    }}>
      <h3>🃏 Dealer</h3>
      <div style={{ display: "flex", justifyContent: "center", gap: "8px" }}>
        {hand.map((card, i) => (
          <div key={i} style={{ fontSize: "18px" }}>
            {card[0]}{card[1]}
          </div>
        ))}
      </div>
      <p><strong>Total:</strong> {value}</p>
    </div>
  );
};

export default DealerHand;
