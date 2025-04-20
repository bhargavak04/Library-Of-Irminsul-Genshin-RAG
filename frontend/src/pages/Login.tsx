import React, { useState } from 'react';
import { LogIn } from 'lucide-react';

export default function Login() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="min-h-screen bg-black/95 text-white p-8">
      <div className="max-w-md mx-auto pt-24">
        <h1 className="title text-4xl text-[#DEB887] mb-12 text-center">
          {isLogin ? 'Welcome Back' : 'Join Us'}
        </h1>
        
        <div className="bg-black/60 rounded-lg border border-[#DEB887]/30 p-8">
          <form className="space-y-6">
            <div>
              <label className="block text-[#DEB887] mb-2">Email</label>
              <input
                type="email"
                className="w-full bg-black/60 border border-[#DEB887]/30 rounded-lg px-4 py-3 text-white placeholder:text-white/50 focus:outline-none focus:border-[#DEB887]"
                placeholder="your@email.com"
              />
            </div>
            
            <div>
              <label className="block text-[#DEB887] mb-2">Password</label>
              <input
                type="password"
                className="w-full bg-black/60 border border-[#DEB887]/30 rounded-lg px-4 py-3 text-white placeholder:text-white/50 focus:outline-none focus:border-[#DEB887]"
                placeholder="••••••••"
              />
            </div>

            <button type="submit" className="btn-primary w-full flex items-center justify-center gap-2">
              <LogIn className="w-5 h-5" />
              {isLogin ? 'Sign In' : 'Create Account'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <button 
              onClick={() => setIsLogin(!isLogin)}
              className="text-[#DEB887] hover:underline"
            >
              {isLogin ? "Don't have an account? Sign up" : 'Already have an account? Sign in'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}