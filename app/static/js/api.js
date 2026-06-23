// API utility functions
const API_BASE = '';

async function getGames(skip = 0, limit = 100) {
    const response = await fetch(`${API_BASE}/games/?skip=${skip}&limit=${limit}`);
    if (!response.ok) throw new Error('Failed to fetch games');
    return await response.json();
}

async function getGame(id) {
    const response = await fetch(`${API_BASE}/games/${id}`);
    if (!response.ok) throw new Error('Failed to fetch game');
    return await response.json();
}

async function getUser(id) {
    const response = await fetch(`${API_BASE}/users/${id}`);
    if (!response.ok) throw new Error('Failed to fetch user');
    return await response.json();
}

async function getReviews(gameId, token) {
    const response = await fetch(`${API_BASE}/reviews/game/${gameId}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    if (!response.ok) throw new Error('Failed to fetch reviews');
    return await response.json();
}

async function getUserProgress(userId, token) {
    const response = await fetch(`${API_BASE}/progress/by-user/${userId}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    if (!response.ok) throw new Error('Failed to fetch progress');
    return await response.json();
}
