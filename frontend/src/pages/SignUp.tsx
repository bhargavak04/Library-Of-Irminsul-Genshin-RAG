import React from 'react';
import { SignUp } from '@clerk/clerk-react';

export default function SignUpPage() {
  return (
    <div className="min-h-screen bg-black/95 text-white p-8 bg-log">
      <div className="max-w-md mx-auto pt-24">
        <h1 className="title title-glow text-4xl text-[#DEB887] mb-12 text-center">
          Join the Adventure
        </h1>
        
        <div className="bg-black/60 rounded-lg border border-[#DEB887]/30 p-8">
          <SignUp 
            appearance={{
              elements: {
                formButtonPrimary: 'bg-[#DEB887] hover:bg-[#DEB887]/80 text-white',
                card: 'bg-transparent shadow-none',
                headerTitle: 'text-[#DEB887]',
                headerSubtitle: 'text-white/80',
                socialButtonsBlockButton: 'border-[#DEB887]/30 text-white hover:bg-[#DEB887]/10',
                socialButtonsBlockButtonText: 'text-white',
                formFieldLabel: 'text-[#DEB887]',
                formFieldInput: 'bg-black/60 border-[#DEB887]/30 text-white placeholder:text-white/50',
                footerActionLink: 'text-[#DEB887] hover:text-[#DEB887]/80',
                dividerLine: 'bg-[#DEB887]/30',
                dividerText: 'text-[#DEB887]',
                identityPreviewText: 'text-white',
                formFieldAction: 'text-[#DEB887] hover:text-[#DEB887]/80',
                otpCodeFieldInput: 'bg-black/60 border-[#DEB887]/30 text-white'
              }
            }}
            routing="path"
            path="/sign-up"
            redirectUrl="/preferences"
          />
        </div>
      </div>
      {/* Mobile Tab Bar */}
      <nav className="tab-bar md:hidden">
        <a href="/dashboard" className="tab-bar__item">🏠<div className="text-xs">Dashboard</div></a>
        <a href="/chatbot" className="tab-bar__item">💬<div className="text-xs">Chatbot</div></a>
        <a href="/profile" className="tab-bar__item tab-bar__active">👤<div className="text-xs">Profile</div></a>
      </nav>
    </div>
  );
}