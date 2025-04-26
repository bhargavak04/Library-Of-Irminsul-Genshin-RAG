import React, { useEffect, useState } from 'react';
import { useUser } from '@clerk/clerk-react';
// import { getUserPreferences } from '../db/schema'; // REMOVED: now using backend API
import { saveUserPreferences } from '../db/schema';

export default function Dashboard() {
  const { user } = useUser();
  const [userPreferences, setUserPreferences] = useState({
    favoriteCharacter: '',
    favoriteRegion: '',
    adventureRank: 0,
    mainTeam: [] as string[],
    preferredElement: ''
  });
  const [editMode, setEditMode] = useState(false);
  const [editPrefs, setEditPrefs] = useState({
    favoriteCharacter: '',
    favoriteRegion: '',
    adventureRank: 0,
    mainTeam: ['', '', '', ''],
    preferredElement: ''
  });
  const regions = ['Mondstadt', 'Liyue', 'Inazuma', 'Sumeru', 'Fontaine'];
  const elements = ['Pyro', 'Hydro', 'Anemo', 'Electro', 'Dendro', 'Cryo', 'Geo'];

  useEffect(() => {
    async function fetchPreferences() {
      if (!user?.id) return;
      try {
        const resp = await fetch(`https://library-of-irminsul-genshin-rag.onrender.com/api/user/preferences/${user.id}`);
        if (!resp.ok) throw new Error('Failed to fetch preferences');
        const prefs = await resp.json();
        setUserPreferences({
          favoriteCharacter: prefs.favoriteCharacter || '',
          favoriteRegion: prefs.favoriteRegion || '',
          adventureRank: prefs.adventureRank || 0,
          mainTeam: prefs.mainTeam || [],
          preferredElement: prefs.preferredElement || ''
        });
        setEditPrefs({
          favoriteCharacter: prefs.favoriteCharacter || '',
          favoriteRegion: prefs.favoriteRegion || '',
          adventureRank: prefs.adventureRank || 0,
          mainTeam: [
            prefs.mainTeam?.[0] || '',
            prefs.mainTeam?.[1] || '',
            prefs.mainTeam?.[2] || '',
            prefs.mainTeam?.[3] || ''
          ],
          preferredElement: prefs.preferredElement || ''
        });
      } catch (error) {
        console.error('Error fetching preferences:', error);
      }
    }
    fetchPreferences();
  }, [user?.id]);

  const handleEdit = () => setEditMode(true);
  const handleCancel = () => setEditMode(false);
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>, idx?: number) => {
    const { name, value } = e.target;
    if (name.startsWith('mainTeam') && idx !== undefined) {
      setEditPrefs(prev => {
        const newTeam = [...prev.mainTeam];
        newTeam[idx] = value;
        return { ...prev, mainTeam: newTeam };
      });
    } else {
      setEditPrefs(prev => ({ ...prev, [name]: value }));
    }
  };
  const handleSave = async () => {
    if (!user?.id) return;
    try {
      const prefsToSave = {
        userId: user.id,
        favoriteCharacter: editPrefs.favoriteCharacter,
        favoriteRegion: editPrefs.favoriteRegion,
        adventureRank: Number(editPrefs.adventureRank),
        mainTeam: editPrefs.mainTeam.filter(Boolean),
        preferredElement: editPrefs.preferredElement
      };
      await saveUserPreferences(prefsToSave);
      setUserPreferences({ ...prefsToSave });
      setEditMode(false);
    } catch (error) {
      alert('Failed to save preferences');
    }
  };

  return (
    <div className="min-h-screen bg-black/95 text-white p-8 bg-dboard">
      <div className="max-w-4xl mx-auto pt-24">
        <h1 className="title title-darkglow text-4xl text-[#DEB887] mb-12 text-center">
          Welcome, {user?.firstName || 'Traveler'}
        </h1>
        <div className="flex justify-center mb-8">
          {editMode ? null : (
            <button
              className="bg-[#DEB887] hover:bg-[#DEB887]/80 text-white py-2 px-6 rounded-lg shadow-md transition"
              onClick={() => setEditMode(true)}
            >
              Edit Preferences
            </button>
          )}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* User Profile Card */}
          <div className="bg-black/60 rounded-lg border border-[#DEB887]/30 p-8">
            <h2 className="text-2xl text-[#DEB887] mb-6">Profile</h2>
            <div className="space-y-4">
              <div>
                <label className="text-[#DEB887] block mb-2">Email</label>
                <p className="text-white/80">{user?.emailAddresses[0].emailAddress}</p>
              </div>
              <div>
                <label className="text-[#DEB887] block mb-2">Username</label>
                <p className="text-white/80">{user?.username || 'Not set'}</p>
              </div>
            </div>
          </div>

          {/* Game Preferences Card */}
          <div className="bg-black/60 rounded-lg border border-[#DEB887]/30 p-8">
            <h2 className="text-2xl text-[#DEB887] mb-6">Game Preferences</h2>
            {editMode ? (
              <div className="space-y-4">
                <div>
                  <label className="text-[#DEB887] block mb-2">Favorite Character</label>
                  <input
                    name="favoriteCharacter"
                    className="w-full p-2 rounded bg-black/80 text-white border border-[#DEB887]/40"
                    value={editPrefs.favoriteCharacter}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label className="text-[#DEB887] block mb-2">Favorite Region</label>
                  <select
                    name="favoriteRegion"
                    className="w-full p-2 rounded bg-black/80 text-white border border-[#DEB887]/40"
                    value={editPrefs.favoriteRegion}
                    onChange={handleChange}
                  >
                    <option value="">Select a region</option>
                    {regions.map(region => (
                      <option key={region} value={region}>{region}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-[#DEB887] block mb-2">Adventure Rank</label>
                  <input
                    name="adventureRank"
                    type="number"
                    min="1" max="60"
                    className="w-full p-2 rounded bg-black/80 text-white border border-[#DEB887]/40"
                    value={editPrefs.adventureRank}
                    onChange={handleChange}
                  />
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div>
                  <label className="text-[#DEB887] block mb-2">Favorite Character</label>
                  <p className="text-white/80">{userPreferences.favoriteCharacter}</p>
                </div>
                <div>
                  <label className="text-[#DEB887] block mb-2">Favorite Region</label>
                  <p className="text-white/80">{userPreferences.favoriteRegion}</p>
                </div>
                <div>
                  <label className="text-[#DEB887] block mb-2">Adventure Rank</label>
                  <p className="text-white/80">{userPreferences.adventureRank}</p>
                </div>
              </div>
            )}
            {editMode && (
              <div className="flex gap-4 mt-6">
                <button
                  className="bg-[#DEB887] hover:bg-[#DEB887]/80 text-white py-2 px-6 rounded-lg shadow-md transition"
                  onClick={handleSave}
                >
                  Save
                </button>
                <button
                  className="bg-gray-500 hover:bg-gray-700 text-white py-2 px-6 rounded-lg shadow-md transition"
                  onClick={handleCancel}
                >
                  Cancel
                </button>
              </div>
            )}
          </div>

          {/* Main Team Card */}
          <div className="bg-black/60 rounded-lg border border-[#DEB887]/30 p-8">
            <h2 className="text-2xl text-[#DEB887] mb-6">Main Team</h2>
            {editMode ? (
              <div className="grid grid-cols-2 gap-4">
                {editPrefs.mainTeam.map((character, idx) => (
                  <input
                    key={idx}
                    name={`mainTeam${idx}`}
                    className="text-white/80 p-2 bg-black/80 border border-[#DEB887]/40 rounded"
                    value={character}
                    onChange={e => handleChange(e, idx)}
                    placeholder={`Character ${idx + 1}`}
                  />
                ))}
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-4">
                {userPreferences.mainTeam.map((character, index) => (
                  <div key={index} className="text-white/80 p-2 bg-[#DEB887]/10 rounded">
                    {character}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Element Preference Card */}
          <div className="bg-black/60 rounded-lg border border-[#DEB887]/30 p-8">
            <h2 className="text-2xl text-[#DEB887] mb-6">Element Preference</h2>
            <div className="flex items-center justify-center h-32">
              {editMode ? (
                <select
                  name="preferredElement"
                  className="text-2xl p-2 rounded bg-black/80 text-white border border-[#DEB887]/40"
                  value={editPrefs.preferredElement}
                  onChange={handleChange}
                >
                  <option value="">Select an element</option>
                  {['Pyro', 'Hydro', 'Anemo', 'Electro', 'Dendro', 'Cryo', 'Geo'].map(el => (
                    <option key={el} value={el}>{el}</option>
                  ))}
                </select>
              ) : (
                <p className="text-2xl text-white/80">{userPreferences.preferredElement}</p>
              )}
            </div>
          </div>
        </div>
      </div>
    {/* Mobile Tab Bar */}
    <nav className="tab-bar md:hidden">
      <a href="/dashboard" className="tab-bar__item tab-bar__active">🏠<div className="text-xs">Dashboard</div></a>
      <a href="/chatbot" className="tab-bar__item">💬<div className="text-xs">Chatbot</div></a>
      <a href="/profile" className="tab-bar__item">👤<div className="text-xs">Profile</div></a>
    </nav>
  </div>
  );
}