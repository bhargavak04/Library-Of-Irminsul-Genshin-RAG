import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '@clerk/clerk-react';
import { saveUserPreferences } from '../db/schema';

export default function Preferences() {
  const navigate = useNavigate();
  const { user } = useUser();
  
  const [preferences, setPreferences] = useState({
    favoriteCharacter: '',
    favoriteRegion: '',
    adventureRank: '',
    mainTeam1: '',
    mainTeam2: '',
    mainTeam3: '',
    mainTeam4: '',
    preferredElement: ''
  });

  const regions = ['Mondstadt', 'Liyue', 'Inazuma', 'Sumeru', 'Fontaine'];
  const elements = ['Pyro', 'Hydro', 'Anemo', 'Electro', 'Dendro', 'Cryo', 'Geo'];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      if (!user?.id) return;

      const mainTeam = [preferences.mainTeam1, preferences.mainTeam2, preferences.mainTeam3, preferences.mainTeam4].filter(Boolean);
      
      await saveUserPreferences({
        userId: user.id,
        favoriteCharacter: preferences.favoriteCharacter,
        favoriteRegion: preferences.favoriteRegion,
        adventureRank: parseInt(preferences.adventureRank),
        mainTeam,
        preferredElement: preferences.preferredElement
      });

      navigate('/dashboard');
    } catch (error) {
      console.error('Error saving preferences:', error);
      // You might want to show an error message to the user here
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setPreferences(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  return (
    <div className="min-h-screen bg-black/95 text-white p-8">
      <div className="max-w-2xl mx-auto pt-24">
        <h1 className="title text-4xl text-[#DEB887] mb-12 text-center">
          Set Your Preferences
        </h1>
        
        <form onSubmit={handleSubmit} className="bg-black/60 rounded-lg border border-[#DEB887]/30 p-8 space-y-6">
          <div>
            <label className="text-[#DEB887] block mb-2">Favorite Character</label>
            <input
              type="text"
              name="favoriteCharacter"
              value={preferences.favoriteCharacter}
              onChange={handleChange}
              className="w-full bg-black/60 border border-[#DEB887]/30 rounded-lg px-4 py-2 text-white"
              required
            />
          </div>

          <div>
            <label className="text-[#DEB887] block mb-2">Favorite Region</label>
            <select
              name="favoriteRegion"
              value={preferences.favoriteRegion}
              onChange={handleChange}
              className="w-full bg-black/60 border border-[#DEB887]/30 rounded-lg px-4 py-2 text-white"
              required
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
              type="number"
              name="adventureRank"
              value={preferences.adventureRank}
              onChange={handleChange}
              min="1"
              max="60"
              className="w-full bg-black/60 border border-[#DEB887]/30 rounded-lg px-4 py-2 text-white"
              required
            />
          </div>

          <div>
            <label className="text-[#DEB887] block mb-2">Main Team (4 Characters)</label>
            <div className="grid grid-cols-2 gap-4">
              {[1, 2, 3, 4].map(num => (
                <input
                  key={num}
                  type="text"
                  name={`mainTeam${num}`}
                  value={preferences[`mainTeam${num}` as keyof typeof preferences]}
                  onChange={handleChange}
                  placeholder={`Character ${num}`}
                  className="w-full bg-black/60 border border-[#DEB887]/30 rounded-lg px-4 py-2 text-white"
                  required
                />
              ))}
            </div>
          </div>

          <div>
            <label className="text-[#DEB887] block mb-2">Preferred Element</label>
            <select
              name="preferredElement"
              value={preferences.preferredElement}
              onChange={handleChange}
              className="w-full bg-black/60 border border-[#DEB887]/30 rounded-lg px-4 py-2 text-white"
              required
            >
              <option value="">Select an element</option>
              {elements.map(element => (
                <option key={element} value={element}>{element}</option>
              ))}
            </select>
          </div>

          <button
            type="submit"
            className="w-full bg-[#DEB887] hover:bg-[#DEB887]/80 text-white py-3 rounded-lg mt-8"
          >
            Save Preferences
          </button>
        </form>
      </div>
    </div>
  );
}