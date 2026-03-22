import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import API_URL from '../config/api';

const ROLES = [
  {
    key: 'admin',
    label: 'Admin',
    icon: 'fa-solid fa-shield-halved',
    color: 'from-purple-600 to-purple-800',
    border: 'border-purple-500',
    desc: 'System administrator managing institutes and platform analytics.',
    canRegister: false,
  },
  {
    key: 'institute',
    label: 'Institute',
    icon: 'fa-solid fa-building-columns',
    color: 'from-blue-600 to-blue-800',
    border: 'border-blue-500',
    desc: 'Educational institutions issuing and managing certificates.',
    canRegister: true,
  },
  {
    key: 'student',
    label: 'Student',
    icon: 'fa-solid fa-user-graduate',
    color: 'from-green-600 to-green-800',
    border: 'border-green-500',
    desc: 'Certificate holders tracking and sharing their credentials.',
    canRegister: false,
  },
  {
    key: 'verifier',
    label: 'Verifier',
    icon: 'fa-solid fa-magnifying-glass',
    color: 'from-orange-600 to-orange-800',
    border: 'border-orange-500',
    desc: 'Employers and organizations verifying certificate authenticity.',
    canRegister: true,
  },
];

const FEATURES = [
  { icon: 'fa-solid fa-link', title: 'Blockchain Secured', desc: 'Every certificate is hashed and stored on an immutable blockchain ledger.' },
  { icon: 'fa-solid fa-robot', title: 'AI Validation', desc: 'Machine learning models detect tampered or fraudulent certificates instantly.' },
  { icon: 'fa-solid fa-bolt', title: 'Instant Verification', desc: 'Upload any certificate and get a verified result in seconds.' },
  { icon: 'fa-solid fa-lock', title: 'Role-Based Access', desc: 'Separate secure portals for admins, institutes, students and verifiers.' },
  { icon: 'fa-solid fa-chart-bar', title: 'Analytics Dashboard', desc: 'Real-time insights on certificates issued, verified and flagged.' },
  { icon: 'fa-solid fa-globe', title: 'Globally Accessible', desc: 'Cloud-hosted platform accessible from anywhere in the world.' },
];

const STEPS = [
  { step: '01', icon: 'fa-solid fa-building-columns', role: 'Institute', action: 'Registers and uploads student certificates to the blockchain.' },
  { step: '02', icon: 'fa-solid fa-user-graduate', role: 'Student', action: 'Logs in to view, track and share their verified certificates.' },
  { step: '03', icon: 'fa-solid fa-magnifying-glass', role: 'Verifier', action: 'Uploads a certificate — AI + blockchain confirms authenticity instantly.' },
];

function LoginModal({ role, onClose, onSuccess }) {
  const { login } = useAuth();
  const [isRegister, setIsRegister] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({ username: '', password: '', email: '', instituteName: '', location: '', studentId: '', name: '' });

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      let endpoint, body;
      if (role.key === 'admin') {
        endpoint = '/auth/admin/login';
        body = { username: form.username, password: form.password };
      } else if (role.key === 'institute') {
        endpoint = isRegister ? '/auth/institute/register' : '/auth/institute/login';
        body = isRegister
          ? { institute_name: form.instituteName, password: form.password, email: form.email, location: form.location }
          : { username: form.email, password: form.password };
      } else if (role.key === 'student') {
        endpoint = '/auth/student/login';
        body = { username: form.studentId, password: form.password };
      } else if (role.key === 'verifier') {
        endpoint = isRegister ? '/auth/verifier/register' : '/auth/verifier/login';
        body = isRegister
          ? { username: form.username, password: form.password, email: form.email }
          : { username: form.username, password: form.password };
      }

      const res = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Failed');

      if (isRegister) {
        setIsRegister(false);
        setError('✅ Registered! Please sign in.');
      } else {
        login(data.access_token, data.role);
        onSuccess();
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const inputCls = 'w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-white/60 text-sm';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" />
      <div
        className={`relative w-full max-w-md bg-gradient-to-br ${role.color} rounded-2xl p-8 shadow-2xl border ${role.border}`}
        onClick={(e) => e.stopPropagation()}
      >
        <button onClick={onClose} className="absolute top-4 right-4 text-white/60 hover:text-white text-xl">✕</button>

        <div className="text-center mb-6">
          <div className="text-4xl mb-2"><i className={`${role.icon} text-white/90`} /></div>
          <h3 className="text-2xl font-bold text-white">{role.label} {isRegister ? 'Register' : 'Login'}</h3>
          <p className="text-white/60 text-sm mt-1">{role.desc}</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          {role.key === 'admin' && (
            <>
              <input className={inputCls} placeholder="Username" value={form.username} onChange={set('username')} required />
              <input className={inputCls} type="password" placeholder="Password" value={form.password} onChange={set('password')} required />
            </>
          )}

          {role.key === 'institute' && (
            <>
              {isRegister && (
                <>
                  <input className={inputCls} placeholder="Institute Name" value={form.instituteName} onChange={set('instituteName')} required />
                  <input className={inputCls} placeholder="Location" value={form.location} onChange={set('location')} />
                </>
              )}
              <input className={inputCls} type="email" placeholder="Email" value={form.email} onChange={set('email')} required />
              <input className={inputCls} type="password" placeholder="Password" value={form.password} onChange={set('password')} required />
            </>
          )}

          {role.key === 'student' && (
            <>
              <input className={inputCls} placeholder="Student ID (e.g. INST00001-00001)" value={form.studentId} onChange={set('studentId')} required />
              <input className={inputCls} type="password" placeholder="Password" value={form.password} onChange={set('password')} required />
            </>
          )}

          {role.key === 'verifier' && (
            <>
              <input className={inputCls} placeholder="Username" value={form.username} onChange={set('username')} required />
              {isRegister && <input className={inputCls} type="email" placeholder="Email" value={form.email} onChange={set('email')} required />}
              <input className={inputCls} type="password" placeholder="Password" value={form.password} onChange={set('password')} required />
            </>
          )}

          {error && (
            <p className={`text-sm text-center ${error.startsWith('✅') ? 'text-green-300' : 'text-red-300'}`}>{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-white text-gray-900 font-semibold rounded-lg hover:bg-white/90 transition disabled:opacity-50 mt-2"
          >
            {loading ? 'Please wait...' : isRegister ? 'Create Account' : 'Sign In'}
          </button>

          {role.canRegister && (
            <button
              type="button"
              onClick={() => { setIsRegister(!isRegister); setError(''); }}
              className="w-full text-white/70 hover:text-white text-sm text-center transition"
            >
              {isRegister ? 'Already have an account? Sign in' : "Don't have an account? Register"}
            </button>
          )}
        </form>
      </div>
    </div>
  );
}

export default function LandingPage() {
  const [activeModal, setActiveModal] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);

  const openModal = (roleKey) => setActiveModal(ROLES.find((r) => r.key === roleKey));
  const closeModal = () => setActiveModal(null);

  return (
    <div className="min-h-screen bg-gray-950 text-white font-['Inter']">

      {/* ── Navbar ── */}
      <nav className="fixed top-0 w-full z-40 bg-gray-950/80 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <i className="fa-solid fa-shield-halved text-2xl text-blue-400" />
            <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              CertiSense AI
            </span>
          </div>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-8 text-sm text-white/70">
            <a href="#features" className="hover:text-white transition">Features</a>
            <a href="#how-it-works" className="hover:text-white transition">How It Works</a>
            <a href="#login" className="hover:text-white transition">Login</a>
          </div>

          <div className="hidden md:flex items-center gap-3">
            <button onClick={() => openModal('verifier')} className="inline-flex items-center gap-2 px-4 py-2 text-sm text-white/80 hover:text-white transition">
              <i className="fa-solid fa-magnifying-glass text-xs" /> Verify Certificate
            </button>
            <button
              onClick={() => openModal('institute')}
              className="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-500 rounded-lg font-medium transition"
            >
              Get Started
            </button>
          </div>

          {/* Mobile hamburger */}
          <button className="md:hidden text-white/70" onClick={() => setMenuOpen(!menuOpen)}>
            <i className={`fas ${menuOpen ? 'fa-times' : 'fa-bars'} text-xl`} />
          </button>
        </div>

        {menuOpen && (
          <div className="md:hidden bg-gray-900 border-t border-white/10 px-6 py-4 space-y-3 text-sm">
            <a href="#features" className="block text-white/70 hover:text-white" onClick={() => setMenuOpen(false)}>Features</a>
            <a href="#how-it-works" className="block text-white/70 hover:text-white" onClick={() => setMenuOpen(false)}>How It Works</a>
            <a href="#login" className="block text-white/70 hover:text-white" onClick={() => setMenuOpen(false)}>Login</a>
          </div>
        )}
      </nav>

      {/* ── Hero ── */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
        {/* Background glow */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-5xl mx-auto px-6 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/10 border border-blue-500/30 rounded-full text-blue-400 text-sm mb-8">
            <span className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" />
            <i className="fa-solid fa-microchip text-xs" /> Powered by AI + Blockchain Technology
          </div>

          <h1 className="text-5xl md:text-7xl font-extrabold leading-tight mb-6">
            Verify Certificates
            <br />
            <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              Instantly & Securely
            </span>
          </h1>

          <p className="text-xl text-white/60 max-w-2xl mx-auto mb-10">
            CertiSense AI uses blockchain immutability and AI validation to eliminate fake certificates.
            Trusted by institutes, students and employers worldwide.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => openModal('verifier')}
              className="inline-flex items-center gap-3 px-8 py-4 bg-blue-600 hover:bg-blue-500 rounded-xl font-semibold text-lg transition shadow-lg shadow-blue-600/30"
            >
              <i className="fa-solid fa-magnifying-glass" /> Verify a Certificate
            </button>
            <button
              onClick={() => openModal('institute')}
              className="inline-flex items-center gap-3 px-8 py-4 bg-white/10 hover:bg-white/20 border border-white/20 rounded-xl font-semibold text-lg transition"
            >
              <i className="fa-solid fa-building-columns" /> Register Institute
            </button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-8 mt-20 max-w-2xl mx-auto">
            {[['500+', 'Students'], ['16+', 'Institutes'], ['750+', 'Certificates']].map(([num, label]) => (
              <div key={label} className="text-center">
                <div className="text-3xl font-bold text-white">{num}</div>
                <div className="text-white/50 text-sm mt-1">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section id="features" className="py-24 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Why CertiSense AI?</h2>
            <p className="text-white/50 text-lg max-w-xl mx-auto">
              A complete certificate lifecycle platform built for the modern world.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((f) => (
              <div key={f.title} className="p-6 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/10 transition">
                <div className="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center mb-4">
            <i className={`${f.icon} text-xl text-white`} />
          </div>
                <h3 className="text-lg font-semibold mb-2">{f.title}</h3>
                <p className="text-white/50 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── How It Works ── */}
      <section id="how-it-works" className="py-24 px-6 bg-white/[0.02]">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">How It Works</h2>
            <p className="text-white/50 text-lg">Three simple steps to a verified world.</p>
          </div>
          <div className="space-y-6">
            {STEPS.map((s) => (
              <div key={s.step} className="flex items-start gap-6 p-6 bg-white/5 border border-white/10 rounded-2xl">
                <div className="flex flex-col items-center gap-2 shrink-0 w-16">
                  <span className="text-3xl font-black text-white/10">{s.step}</span>
                  <i className={`${s.icon} text-blue-400 text-lg`} />
                </div>
                <div>
                  <div className="text-blue-400 font-semibold text-sm mb-1">{s.role}</div>
                  <p className="text-white/70">{s.action}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Login Section ── */}
      <section id="login" className="py-24 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Access Your Portal</h2>
            <p className="text-white/50 text-lg">Select your role to sign in or register.</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {ROLES.map((role) => (
              <button
                key={role.key}
                onClick={() => openModal(role.key)}
                className={`group p-8 bg-gradient-to-br ${role.color} rounded-2xl border ${role.border} hover:scale-105 transition-transform text-left shadow-lg`}
              >
                <div className="w-14 h-14 rounded-2xl bg-white/20 flex items-center justify-center mb-4">
                  <i className={`${role.icon} text-2xl text-white`} />
                </div>
                <h3 className="text-xl font-bold mb-2">{role.label}</h3>
                <p className="text-white/70 text-sm leading-relaxed mb-4">{role.desc}</p>
                <div className="flex items-center gap-2 text-white/80 text-sm font-medium group-hover:gap-3 transition-all">
                  {role.canRegister ? 'Login / Register' : 'Login'}
                  <i className="fa-solid fa-arrow-right text-xs" />
                </div>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="border-t border-white/10 py-10 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-white/40 text-sm">
          <div className="flex items-center gap-2">
            <i className="fa-solid fa-shield-halved text-blue-400" />
            <span className="font-semibold text-white/60">CertiSense AI v3.0</span>
          </div>
          <p>Built with React · FastAPI · AI Validation · Blockchain</p>
          <p>© {new Date().getFullYear()} CertiSense AI. All rights reserved.</p>
        </div>
      </footer>

      {/* ── Login Modal ── */}
      {activeModal && (
        <LoginModal role={activeModal} onClose={closeModal} onSuccess={closeModal} />
      )}
    </div>
  );
}
