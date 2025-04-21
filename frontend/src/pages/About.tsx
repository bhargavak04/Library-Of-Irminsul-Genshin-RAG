import React from 'react';
import { Book, Users, Heart } from 'lucide-react';

export default function About() {
  return (
    <div className="min-h-screen bg-about bg-black/95 text-white p-8 ">
      <div className="max-w-4xl mx-auto pt-24">
        <h1 className="title text-4xl text-[#DEB887] mb-12 text-center">About Library of Irminsul</h1>
        
        <div className="space-y-12">
          <div className="bg-black/60 rounded-lg border border-[#DEB887]/30 p-8">
            <Book className="w-12 h-12 text-[#DEB887] mb-4" />
            <h2 className="title text-2xl text-[#DEB887] mb-4">Our Mission</h2>
            <p className="text-lg text-white/80">
              Library of Irminsul aims to be your ultimate companion in exploring the rich and 
              intricate lore of Teyvat. We strive to make the vast knowledge of Genshin Impact's 
              world accessible and engaging for all travelers.
            </p>
          </div>

          <div className="bg-black/60 rounded-lg border border-[#DEB887]/30 p-8">
            <Users className="w-12 h-12 text-[#DEB887] mb-4" />
            <h2 className="title text-2xl text-[#DEB887] mb-4">About Me (Bhargav Akshith)</h2>
            <p className="text-lg text-white/80">
              I am dedicated Genshin Impact enthusiast, researcher, and developer
              who share a passion for the game's storytelling and world-building. I work 
              tirelessly to gather, verify, and present accurate lore information.
            </p>
          </div>

          <div className="bg-black/60 rounded-lg border border-[#DEB887]/30 p-8">
            <Heart className="w-12 h-12 text-[#DEB887] mb-4" />
            <h2 className="title text-2xl text-[#DEB887] mb-4">Join Our Community</h2>
            <p className="text-lg text-white/80">
              Whether you're a casual player or a dedicated lore enthusiast, we welcome you to join 
              our community. Together, we can unravel the mysteries of Teyvat and share our 
              discoveries with fellow travelers.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}