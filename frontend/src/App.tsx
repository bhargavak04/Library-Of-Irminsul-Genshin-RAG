import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { MessageSquare, Search, User } from 'lucide-react';
import { ClerkProvider, SignedIn, SignedOut, useUser, SignOutButton } from '@clerk/clerk-react';
import Chatbot from './pages/Chatbot';
import About from './pages/About';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import SignUp from './pages/SignUp';
import Preferences from './pages/Preferences';

import { useNavigate } from 'react-router-dom';

function Navbar() {
  const { user } = useUser();
  const navigate = useNavigate();

  return (
    <nav className="absolute top-0 w-full p-8 flex justify-end gap-12 z-10">
      <Link to="/about" className="nav-link">About Us</Link>
      <SignedIn>
        <Link to="/chatbot" className="nav-link">Chatbot</Link>
        <Link to="/dashboard" className="nav-link">{user?.firstName || 'Dashboard'}</Link>
        <SignOutButton signOutCallback={() => navigate('/') }>
          <button className="nav-link">Logout</button>
        </SignOutButton>
      </SignedIn>
      <SignedOut>
        <Link to="/login" className="nav-link">Login</Link>
        <Link to="/sign-up" className="nav-link">Sign Up</Link>
      </SignedOut>
    </nav>
  );
}

function LandingPage() {
  return (
    <div className="min-h-screen bg-genshin flex flex-col items-center justify-center relative">

      <div className="flex flex-col items-center justify-center flex-1 w-full pt-24 md:pt-36">
        <div className="text-center space-y-8 max-w-4xl px-4 relative">
          <div className="mb-12 md:mb-16">
            <div className="decorated-title mb-8">
              <h1 className="title text-6xl text-white whitespace-nowrap" style={{ 
                textShadow: '0 0 20px rgba(0,0,0,0.7), 0 0 40px rgba(0,0,0,0.4)' 
              }}>
                Library of Irminsul
              </h1>
            </div>
            <p className="text-3xl text-white/90" style={{ 
              textShadow: '0 0 10px rgba(0,0,0,0.6)' 
            }}>
              Your Genshin Lore Companion
            </p>
          </div>
          <Link to="/chatbot" className="btn-primary inline-block text-xl tracking-wider mt-6">
            Get Started
          </Link>
        </div>
      </div>
      
      <div className="mt-40 relative w-full px-8">
        <div className="section-title mb-20">
          <h2 className="title text-4xl text-white text-center" style={{ 
            textShadow: '0 0 20px rgba(222,184,135,0.5)' 
          }}>
            Features
          </h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 max-w-6xl mx-auto">
          <div className="feature-card text-center group">
            <MessageSquare className="w-16 h-16 mb-6 mx-auto text-[#DEB887] opacity-80 group-hover:opacity-100 transition-opacity" />
            <h3 className="title text-2xl mb-4 text-[#DEB887]">Ask Akasha</h3>
            <p className="text-white/80 text-lg">Chat with our AI to learn about Genshin's vast lore and characters.</p>
          </div>
          <div className="feature-card text-center group">
            <Search className="w-16 h-16 mb-6 mx-auto text-[#DEB887] opacity-80 group-hover:opacity-100 transition-opacity" />
            <h3 className="title text-2xl mb-4 text-[#DEB887]">Search Lore</h3>
            <p className="text-white/80 text-lg">Explore detailed information about characters, weapons, and artifacts.</p>
          </div>
          <div className="feature-card text-center group">
            <User className="w-16 h-16 mb-6 mx-auto text-[#DEB887] opacity-80 group-hover:opacity-100 transition-opacity" />
            <h3 className="title text-2xl mb-4 text-[#DEB887]">Personalized</h3>
            <p className="text-white/80 text-lg">Save your favorite topics and track your learning progress.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  if (!import.meta.env.VITE_CLERK_PUBLISHABLE_KEY) {
    throw new Error('Missing Publishable Key');
  }

  return (
    <ClerkProvider publishableKey={import.meta.env.VITE_CLERK_PUBLISHABLE_KEY}>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login />} />
          <Route path="/sign-up" element={<SignUp />} />
          <Route path="/chatbot" element={
            <SignedIn>
              <Chatbot />
            </SignedIn>
          } />
          <Route path="/dashboard" element={
            <SignedIn>
              <Dashboard />
            </SignedIn>
          } />
          <Route path="/preferences" element={
            <SignedIn>
              <Preferences />
            </SignedIn>
          } />
        </Routes>
      </Router>
    </ClerkProvider>
  );
}

export default App;