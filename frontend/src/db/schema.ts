// import { sql } from '@vercel/postgres'; // REMOVED: DB logic moved to backend

// Removed createTables: DB logic is now handled by the backend API.

const API_BASE = "https://library-of-irminsul-genshin-rag.onrender.com";

export async function getUserPreferences(userId: string) {
  try {
    const response = await fetch(`${API_BASE}/api/user/preferences/${userId}`);
    if (!response.ok) throw new Error('Failed to fetch user preferences');
    return await response.json();
  } catch (error) {
    console.error('Error fetching user preferences:', error);
    throw error;
  }
}

export async function saveUserPreferences({ userId, favoriteCharacter, favoriteRegion, adventureRank, mainTeam, preferredElement }: { userId: string; favoriteCharacter: string; favoriteRegion: string; adventureRank: number; mainTeam: string[]; preferredElement: string; }) {
  try {
    const response = await fetch(`${API_BASE}/api/user/preferences`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId, favoriteCharacter, favoriteRegion, adventureRank, mainTeam, preferredElement })
    });
    if (!response.ok) throw new Error('Failed to save preferences');
    return await response.json();
  } catch (error) {
    console.error('Error saving user preferences:', error);
    throw error;
  }
}