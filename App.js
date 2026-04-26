import React, { useState } from "react";
import BNPLWidget from "./components/BNPLWidget";

/* ── SVG Avatars ─────────────────────────────────────────────────── */
const AvatarNew = () => (
  <svg viewBox="0 0 26 26" fill="none">
    <circle cx="13" cy="9" r="4.5" fill="#f03e5a" opacity="0.15" stroke="#f03e5a" strokeWidth="1.2"/>
    <circle cx="13" cy="9" r="2.5" fill="#f03e5a" opacity="0.7"/>
    <path d="M5 22c0-4.418 3.582-8 8-8s8 3.582 8 8" stroke="#f03e5a" strokeWidth="1.4" strokeLinecap="round" opacity="0.4"/>
    <path d="M19 4l1.2 2.4L23 5" stroke="#f03e5a" strokeWidth="1.1" strokeLinecap="round" strokeLinejoin="round" opacity="0.6"/>
  </svg>
);
const AvatarSparse = () => (
  <svg viewBox="0 0 26 26" fill="none">
    <circle cx="13" cy="9" r="4.5" fill="#b45309" opacity="0.12" stroke="#b45309" strokeWidth="1.2"/>
    <circle cx="13" cy="9" r="2.5" fill="#b45309" opacity="0.6"/>
    <path d="M5 22c0-4.418 3.582-8 8-8s8 3.582 8 8" stroke="#b45309" strokeWidth="1.4" strokeLinecap="round" opacity="0.4"/>
    <rect x="18" y="4" width="5.5" height="4" rx="1" stroke="#b45309" strokeWidth="1.1" opacity="0.5"/>
    <path d="M19.5 6h2.5" stroke="#b45309" strokeWidth="1" strokeLinecap="round" opacity="0.7"/>
  </svg>
);
const AvatarAvg = () => (
  <svg viewBox="0 0 26 26" fill="none">
    <circle cx="13" cy="9" r="4.5" fill="#1a56db" opacity="0.10" stroke="#1a56db" strokeWidth="1.2"/>
    <circle cx="13" cy="9" r="2.5" fill="#1a56db" opacity="0.6"/>
    <path d="M5 22c0-4.418 3.582-8 8-8s8 3.582 8 8" stroke="#1a56db" strokeWidth="1.4" strokeLinecap="round" opacity="0.4"/>
    <polyline points="18,7 20,5 22,6.5 24,4" stroke="#1a56db" strokeWidth="1.1" strokeLinecap="round" strokeLinejoin="round" opacity="0.6"/>
  </svg>
);
const AvatarGood = () => (
  <svg viewBox="0 0 26 26" fill="none">
    <circle cx="13" cy="9" r="4.5" fill="#0d7d56" opacity="0.12" stroke="#0d7d56" strokeWidth="1.2"/>
    <circle cx="13" cy="9" r="2.5" fill="#0d7d56" opacity="0.65"/>
    <path d="M5 22c0-4.418 3.582-8 8-8s8 3.582 8 8" stroke="#0d7d56" strokeWidth="1.4" strokeLinecap="round" opacity="0.4"/>
    <circle cx="21" cy="6" r="3.5" fill="#0d7d56" opacity="0.12" stroke="#0d7d56" strokeWidth="1"/>
    <path d="M19.5 6l1.2 1.2L22.5 5" stroke="#0d7d56" strokeWidth="1.1" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);
const AvatarPower = () => (
  <svg viewBox="0 0 26 26" fill="none">
    <defs>
      <linearGradient id="pg" x1="0" y1="0" x2="1" y2="1">
        <stop stopColor="#0a6e4f"/>
        <stop offset="1" stopColor="#1a56db"/>
      </linearGradient>
    </defs>
    <circle cx="13" cy="9" r="4.5" fill="url(#pg)" opacity="0.15" stroke="url(#pg)" strokeWidth="1.2"/>
    <circle cx="13" cy="9" r="2.5" fill="url(#pg)" opacity="0.8"/>
    <path d="M5 22c0-4.418 3.582-8 8-8s8 3.582 8 8" stroke="url(#pg)" strokeWidth="1.4" strokeLinecap="round" opacity="0.4"/>
    <path d="M20 3l.8 2.5H23l-2 1.5.8 2.5L20 8l-1.6 1.5.8-2.5-2-1.5h2.2L20 3z" fill="url(#pg)" opacity="0.9"/>
  </svg>
);

const AVATARS    = [AvatarNew, AvatarSparse, AvatarAvg, AvatarGood, AvatarPower];
const BADGE_CLS  = ["badge-new","badge-sparse","badge-build","badge-trusted","badge-premium"];

/* ── Personas ────────────────────────────────────────────────────── */
const personas = [
  {
    id:"U001",name:"Arjun Mehta",label:"New User",tag:"No History",
    description:"Registered 3 days ago, zero transactions",
    avatar:"🧑‍💻",monthly_income:32000,transaction_count:0,
    repayment_ratio:0,total_gmv:0,categories_used:[],
    return_rate:0,account_age_days:3,existing_liabilities:0,
    coupon_redemption_rate:0,payment_modes:[],
  },
  {
    id:"U002",name:"Priya Sharma",label:"Low Activity",tag:"Sparse Data",
    description:"8 transactions, mixed repayment history",
    avatar:"👩‍🎓",monthly_income:28000,transaction_count:8,
    repayment_ratio:0.75,total_gmv:12400,categories_used:["Fashion","Grocery"],
    return_rate:0.25,account_age_days:120,existing_liabilities:5000,
    coupon_redemption_rate:0.6,payment_modes:["UPI"],
  },
  {
    id:"U003",name:"Rahul Verma",label:"Average User",tag:"Building Credit",
    description:"45 transactions, decent record, room to grow",
    avatar:"👨‍💼",monthly_income:55000,transaction_count:45,
    repayment_ratio:0.91,total_gmv:87500,
    categories_used:["Electronics","Fashion","Grocery","Travel"],
    return_rate:0.08,account_age_days:280,existing_liabilities:15000,
    coupon_redemption_rate:0.45,payment_modes:["UPI","Card"],
  },
  {
    id:"U004",name:"Sneha Kapoor",label:"Good Credit",tag:"Trusted",
    description:"120 transactions, excellent repayment",
    avatar:"👩‍💻",monthly_income:85000,transaction_count:120,
    repayment_ratio:0.96,total_gmv:345000,
    categories_used:["Electronics","Fashion","Grocery","Travel","Home"],
    return_rate:0.03,account_age_days:540,existing_liabilities:10000,
    coupon_redemption_rate:0.7,payment_modes:["UPI","Card","NetBanking"],
  },
  {
    id:"U005",name:"Vikram Reddy",label:"Power User",tag:"Premium",
    description:"267 transactions, near-perfect record",
    avatar:"🚀",monthly_income:150000,transaction_count:267,
    repayment_ratio:0.99,total_gmv:890000,
    categories_used:["Electronics","Fashion","Grocery","Travel","Home","Luxury"],
    return_rate:0.01,account_age_days:820,existing_liabilities:25000,
    coupon_redemption_rate:0.82,payment_modes:["UPI","Card","NetBanking","Wallet"],
  },
];

/* ── Laptop SVG ──────────────────────────────────────────────────── */
const LaptopIllustration = () => (
  <svg viewBox="0 0 320 210" fill="none" xmlns="http://www.w3.org/2000/svg" className="product-laptop-svg">
    <defs>
      <linearGradient id="lid-top" x1="30" y1="8" x2="290" y2="155" gradientUnits="userSpaceOnUse">
        <stop stopColor="#d6d3cd"/>
        <stop offset="1" stopColor="#c8c5bf"/>
      </linearGradient>
      <linearGradient id="lid-body" x1="30" y1="8" x2="290" y2="155" gradientUnits="userSpaceOnUse">
        <stop stopColor="#e2dfda"/>
        <stop offset="1" stopColor="#d0cdc8"/>
      </linearGradient>
      <linearGradient id="screen-bg" x1="40" y1="16" x2="280" y2="148" gradientUnits="userSpaceOnUse">
        <stop stopColor="#1a2744"/>
        <stop offset="0.5" stopColor="#1e3058"/>
        <stop offset="1" stopColor="#111d35"/>
      </linearGradient>
      <linearGradient id="base-grad" x1="10" y1="158" x2="310" y2="200" gradientUnits="userSpaceOnUse">
        <stop stopColor="#d0cdc8"/>
        <stop offset="1" stopColor="#bbb8b2"/>
      </linearGradient>
      <filter id="screen-glow">
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feComposite in="SourceGraphic" in2="blur" operator="over"/>
      </filter>
    </defs>

    {/* Lid outer */}
    <rect x="30" y="8" width="260" height="152" rx="10" fill="url(#lid-body)" />
    {/* Lid inner (screen face) */}
    <rect x="34" y="12" width="252" height="144" rx="8" fill="url(#lid-top)" />
    {/* Screen bezel */}
    <rect x="42" y="18" width="236" height="130" rx="6" fill="#0f0f0d" />
    {/* Screen content */}
    <rect x="46" y="22" width="228" height="122" rx="4" fill="url(#screen-bg)" />

    {/* Screen UI — browser bar */}
    <rect x="50" y="26" width="220" height="16" rx="3" fill="rgba(255,255,255,0.04)"/>
    <circle cx="58" cy="34" r="3" fill="#f03e5a" opacity="0.7"/>
    <circle cx="67" cy="34" r="3" fill="#f5a623" opacity="0.7"/>
    <circle cx="76" cy="34" r="3" fill="#10e6a8" opacity="0.7"/>
    <rect x="100" y="28.5" width="110" height="11" rx="2.5" fill="rgba(255,255,255,0.06)"/>
    <rect x="107" y="31" width="70" height="6" rx="1.5" fill="rgba(255,255,255,0.1)"/>

    {/* Screen content — product page simulation */}
    <rect x="54" y="48" width="90" height="88" rx="4" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.05)" strokeWidth="0.8"/>
    <rect x="60" y="54" width="78" height="48" rx="3" fill="rgba(78,142,255,0.08)"/>
    {/* Tiny laptop icon on screen */}
    <rect x="82" y="64" width="34" height="22" rx="2" fill="rgba(78,142,255,0.2)" stroke="rgba(78,142,255,0.4)" strokeWidth="0.7"/>
    <rect x="78" y="86" width="42" height="4" rx="1" fill="rgba(78,142,255,0.15)"/>
    <rect x="60" y="108" width="50" height="3" rx="1" fill="rgba(255,255,255,0.12)"/>
    <rect x="60" y="113" width="35" height="3" rx="1" fill="rgba(255,255,255,0.07)"/>
    <rect x="60" y="120" width="78" height="10" rx="2" fill="rgba(10,110,79,0.25)" stroke="rgba(10,110,79,0.4)" strokeWidth="0.7"/>
    <rect x="70" y="123.5" width="45" height="3" rx="1" fill="rgba(10,230,168,0.5)"/>

    {/* Right panel */}
    <rect x="152" y="48" width="118" height="38" rx="3" fill="rgba(255,255,255,0.025)" stroke="rgba(255,255,255,0.04)" strokeWidth="0.8"/>
    <rect x="158" y="54" width="60" height="5" rx="1.5" fill="rgba(255,255,255,0.12)"/>
    <rect x="158" y="62" width="40" height="4" rx="1" fill="rgba(255,255,255,0.07)"/>
    <rect x="158" y="70" width="80" height="4" rx="1" fill="rgba(255,255,255,0.05)"/>

    <rect x="152" y="92" width="55" height="22" rx="3" fill="rgba(255,255,255,0.025)"/>
    <rect x="158" y="97" width="30" height="4" rx="1" fill="rgba(78,142,255,0.3)"/>
    <rect x="158" y="104" width="20" height="3" rx="1" fill="rgba(255,255,255,0.07)"/>

    <rect x="213" y="92" width="55" height="22" rx="3" fill="rgba(255,255,255,0.025)"/>
    <rect x="219" y="97" width="30" height="4" rx="1" fill="rgba(245,166,35,0.3)"/>
    <rect x="219" y="104" width="20" height="3" rx="1" fill="rgba(255,255,255,0.07)"/>

    <rect x="152" y="120" width="116" height="10" rx="2.5" fill="rgba(10,110,79,0.25)" stroke="rgba(10,110,79,0.35)" strokeWidth="0.7"/>
    <rect x="165" y="123.5" width="70" height="3" rx="1" fill="rgba(10,230,168,0.45)"/>

    {/* Camera dot */}
    <circle cx="160" cy="15.5" r="1.5" fill="#222" stroke="rgba(255,255,255,0.08)" strokeWidth="0.5"/>

    {/* Base */}
    <path d="M10 162h300l-12 36H22L10 162z" fill="url(#base-grad)"/>
    {/* Keyboard hint */}
    <rect x="60" y="172" width="200" height="16" rx="2" fill="rgba(0,0,0,0.06)"/>
    {/* Key rows */}
    {[0,1,2,3,4,5,6,7,8,9,10,11,12].map(i => (
      <rect key={i} x={64 + i * 14} y="174" width="11" height="12" rx="1.5" fill="rgba(0,0,0,0.08)" />
    ))}
    {/* Hinge shadow */}
    <rect x="10" y="160" width="300" height="3" fill="rgba(0,0,0,0.1)" rx="1"/>
    {/* Trackpad */}
    <rect x="128" y="190" width="64" height="8" rx="2" fill="rgba(0,0,0,0.06)"/>

    {/* Logo on lid back — Apple-style center mark */}
    <circle cx="160" cy="84" r="8" fill="rgba(0,0,0,0.05)"/>
    <path d="M157 81 Q160 77 163 81 Q166 85 162 87 Q160 88 158 87 Q154 85 157 81z" fill="rgba(0,0,0,0.1)"/>
  </svg>
);

/* ── App ─────────────────────────────────────────────────────────── */
function App() {
  const [selected, setSelected] = useState(personas[3]);

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-left">
          <div className="logo-icon">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M4 10h6M10 10l-3-3.5M10 10l-3 3.5" stroke="white" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M12 6.5h4M12 10h3M12 13.5h4" stroke="#10e6a8" strokeWidth="1.6" strokeLinecap="round"/>
            </svg>
          </div>
          <span className="logo-wordmark">GrabCredit</span>
          <div className="header-pipe" />
          <span className="header-product">Pay Later Checkout</span>
        </div>

        <div className="header-right">
          <span className="header-chip">Sandbox Mode</span>
          <span className="header-chip live">
            <span className="live-dot" />
            Engine Active
          </span>
        </div>
      </header>

      <div className="main-grid">
        {/* ── Left ─────────────────────────────────────────────── */}
        <div className="left-panel">

          {/* Product */}
          <div className="product-card">
            <div className="product-stage">
              <span className="product-tag-tl">Featured</span>
              <span className="product-tag-tr">11% OFF · Today only</span>
              <LaptopIllustration />
            </div>
            <div className="product-body">
              <div className="product-eyebrow">
                Electronics · Laptop
                <div className="product-rating">
                  ★★★★★ <span>4.8 (2,341 reviews)</span>
                </div>
              </div>
              <h2 className="product-name">GrabTech Pro Laptop</h2>
              <div className="spec-row">
                {["14″ Retina Display","Apple M4 Chip","16 GB RAM","512 GB SSD","macOS Sequoia"].map(s => (
                  <span key={s} className="spec-tag">{s}</span>
                ))}
              </div>
              <div className="product-price-row">
                <span className="price-main"><span className="price-currency">₹</span>79,990</span>
                <span className="price-mrp">₹89,990</span>
                <span className="price-save">Save ₹10,000</span>
              </div>
            </div>
          </div>

          {/* Persona Selector */}
          <div className="persona-panel">
            <div className="persona-panel-head">
              <span className="persona-panel-title">Select Customer Profile</span>
              <span className="persona-panel-sub">5 test personas</span>
            </div>
            <div className="persona-list">
              {personas.map((p, i) => {
                const Av = AVATARS[i];
                return (
                  <div
                    key={p.id}
                    id={`persona-${p.id}`}
                    className={`persona-row ${selected.id === p.id ? "active" : ""}`}
                    onClick={() => setSelected(p)}
                  >
                    <div className="persona-avatar-wrap"><Av /></div>
                    <div className="persona-text">
                      <div className="persona-name">{p.name}</div>
                      <div className="persona-sub">{p.description}</div>
                    </div>
                    <span className={`persona-badge ${BADGE_CLS[i]}`}>{p.tag}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* ── Right ────────────────────────────────────────────── */}
        <div className="right-panel">
          <BNPLWidget persona={selected} />
        </div>
      </div>
    </div>
  );
}

export default App;