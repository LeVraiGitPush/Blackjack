import axios from 'axios';


const BASE_URL = import.meta.env.VITE_API_URL;

export const createLobby = async (hostName) =>
  axios.post(`${BASE_URL}/lobby/create`, { host_name: hostName });

export const getLobbyInfo = async (lobbyId) =>
  axios.get(`${BASE_URL}/lobby/${lobbyId}`);

export const addFakePlayer = async (lobbyId, name) =>
  axios.post(`${BASE_URL}/lobby/${lobbyId}/add_fake`, { name });

export const assignSeat = async (lobbyId, seatIndex, player) =>
  axios.post(`${BASE_URL}/lobby/${lobbyId}/assign_seat`, {
    seat_index: seatIndex,
    player,
  });

export const startRound = async (lobbyId) =>
  axios.post(`${BASE_URL}/game/${lobbyId}/start_round`);

export const placeBet = async (lobbyId, seatId, player, amount, sideBets = {}) =>
  axios.post(`${BASE_URL}/game/${lobbyId}/seat/${seatId}/bet`, {
    player,
    amount,
    side_bets: sideBets,
  });

export const sendAction = async (lobbyId, seatId, action) =>
  axios.post(`${BASE_URL}/game/${lobbyId}/seat/${seatId}/action`, { action });
