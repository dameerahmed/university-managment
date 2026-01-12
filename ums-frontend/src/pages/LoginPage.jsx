// FILE: src/LoginPage.js
import React, { useState } from 'react';
import axios from '../api/axios';
import { useNavigate } from 'react-router-dom';
import { Mail, Lock, ArrowRight, Facebook, Twitter, Instagram } from 'lucide-react';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post('/users/login', {
        email: email,
        password: password
      });

      const { user_token, user_role, user_name } = response.data;
      localStorage.setItem('token', user_token);
      localStorage.setItem('role', user_role);
      localStorage.setItem('user_name', user_name);

      if (user_role === 'admin') navigate('/admin');
      else if (user_role === 'student') navigate('/student');
      else if (user_role === 'teacher') navigate('/teacher');
      else navigate('/');

    } catch (err) {
      console.error(err);
      setError("Invalid Email or Password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex relative overflow-hidden">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0 z-0">
        <img
          src="https://images.unsplash.com/photo-1541339907198-e08756dedf3f?q=80&w=2070&auto=format&fit=crop"
          alt="University Campus"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-black/80 via-black/60 to-black/30"></div>
      </div>

      {/* Content Container */}
      <div className="container mx-auto px-6 relative z-10 flex flex-col md:flex-row items-center justify-center h-screen gap-12 md:gap-24">

        {/* Left Side: Branding & Welcome */}
        <div className="flex-1 text-white max-w-lg hidden md:block">
          <div className="flex items-center gap-3 mb-8">
            <div className="h-12 w-12 bg-orange-500 rounded-xl flex items-center justify-center font-bold text-2xl shadow-lg shadow-orange-500/20">U</div>
            <span className="text-2xl font-bold tracking-tight">UMS Portal</span>
          </div>
          <h1 className="text-6xl font-black tracking-tight leading-tight mb-6">
            Welcome <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-amber-200">Back</span>
          </h1>
          <p className="text-lg text-gray-300 leading-relaxed mb-8">
            Access your university dashboard to manage students, track progress, and stay updated with the latest announcements.
          </p>
          <div className="flex gap-4">
            <div className="h-10 w-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors cursor-pointer backdrop-blur-sm">
              <Facebook size={20} />
            </div>
            <div className="h-10 w-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors cursor-pointer backdrop-blur-sm">
              <Twitter size={20} />
            </div>
            <div className="h-10 w-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors cursor-pointer backdrop-blur-sm">
              <Instagram size={20} />
            </div>
          </div>
        </div>

        {/* Right Side: Login Form */}
        <div className="flex-1 w-full max-w-md">
          <div className="bg-black/40 backdrop-blur-xl p-8 md:p-10 rounded-3xl border border-white/10 shadow-2xl">
            <h2 className="text-3xl font-bold text-white mb-2">Sign In</h2>
            <p className="text-gray-400 mb-8">Enter your credentials to access your account</p>

            {error && (
              <div className="bg-red-500/10 border border-red-500/20 text-red-200 p-4 rounded-xl mb-6 text-sm flex items-center gap-2">
                ⚠️ {error}
              </div>
            )}

            <form onSubmit={handleLogin} className="space-y-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300 ml-1">Email Address</label>
                <div className="relative group">
                  <Mail className="absolute left-4 top-3.5 text-gray-500 group-focus-within:text-orange-400 transition-colors" size={20} />
                  <input
                    type="email"
                    className="w-full bg-white/5 border border-white/10 focus:border-orange-500/50 rounded-xl px-12 py-3.5 text-white placeholder-gray-500 outline-none transition-all focus:bg-white/10"
                    placeholder="admin@email.com"
                    value={email} onChange={(e) => setEmail(e.target.value)} required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300 ml-1">Password</label>
                <div className="relative group">
                  <Lock className="absolute left-4 top-3.5 text-gray-500 group-focus-within:text-orange-400 transition-colors" size={20} />
                  <input
                    type="password"
                    className="w-full bg-white/5 border border-white/10 focus:border-orange-500/50 rounded-xl px-12 py-3.5 text-white placeholder-gray-500 outline-none transition-all focus:bg-white/10"
                    placeholder="••••••••"
                    value={password} onChange={(e) => setPassword(e.target.value)} required
                  />
                </div>
              </div>

              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center gap-2 cursor-pointer group">
                  <input type="checkbox" className="rounded border-gray-600 bg-transparent text-orange-500 focus:ring-offset-0 focus:ring-0" />
                  <span className="text-gray-400 group-hover:text-gray-300 transition-colors">Remember me</span>
                </label>
                <a href="#" className="text-orange-400 hover:text-orange-300 transition-colors font-medium">Forgot Password?</a>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold py-4 rounded-xl shadow-lg shadow-orange-500/20 flex items-center justify-center gap-2 transition-all hover:scale-[1.02] active:scale-[0.98]"
              >
                {loading ? (
                  <div className="h-5 w-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <>Sign In Now <ArrowRight size={20} /></>
                )}
              </button>
            </form>

            <p className="text-center text-gray-500 text-sm mt-8">
              By clicking sign in, you agree to our <br />
              <a href="#" className="text-gray-400 hover:text-white transition-colors underline decoration-gray-600">Terms of Service</a> and <a href="#" className="text-gray-400 hover:text-white transition-colors underline decoration-gray-600">Privacy Policy</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;