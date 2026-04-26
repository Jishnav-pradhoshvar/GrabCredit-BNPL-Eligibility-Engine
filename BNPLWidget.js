import React, { useEffect, useState } from "react";
import { evaluateCredit } from "../services/api";

/* ── Score Ring ──────────────────────────────────────────────────── */
const R = 34, CIRC = 2 * Math.PI * R;

const ScoreRing = ({ score, status }) => {
  const offset = CIRC - (score / 100) * CIRC;
  const cls = (status || "").toLowerCase();
  return (
    <div className="ring-wrap">
      <svg className="ring-svg" viewBox="0 0 80 80">
        <circle className="ring-track" cx="40" cy="40" r={R} />
        <circle className={`ring-fill ${cls}`} cx="40" cy="40" r={R}
          strokeDasharray={CIRC} strokeDashoffset={offset} />
      </svg>
      <div className="ring-inner">
        <span className="ring-score">{score}</span>
        <span className="ring-max">/100</span>
      </div>
    </div>
  );
};

/* ── Helpers ─────────────────────────────────────────────────────── */
const tier = s => s>=80?"Excellent":s>=60?"Good":s>=40?"Fair":s>=20?"Low":"Very Low";
const label = s => s==="APPROVED"?"Approved":s==="PARTIALLY_APPROVED"?"Partial":"Rejected";
const cls   = s => s==="APPROVED"?"approved":s==="PARTIALLY_APPROVED"?"partially_approved":"rejected";

/* ── Widget ──────────────────────────────────────────────────────── */
const BNPLWidget = ({ persona }) => {
  const [result,      setResult]      = useState(null);
  const [loading,     setLoading]     = useState(false);
  const [selectedEmi, setSelectedEmi] = useState(0);

  useEffect(() => {
    if (!persona) return;
    setLoading(true);
    setResult(null);

    const t = setTimeout(() => {
      evaluateCredit(persona)
        .then(d => { setResult(d); setSelectedEmi(0); })
        .catch(e => { console.error("GrabCredit API error:", e); setResult({ error: true }); })
        .finally(() => setLoading(false));
    }, 350);
    return () => clearTimeout(t);
  }, [persona]);

  const statusCls = result ? cls(result.status) : "";

  /* Loading */
  if (loading || !result) return (
    <div className="bnpl-widget">
      <div className="widget-bar" />
      <div className="widget-header">
        <div className="widget-brand">
          <div className="widget-brand-icon">
            <svg viewBox="0 0 16 16" fill="none">
              <path d="M3 8h5M8 8l-2.5-3M8 8l-2.5 3" stroke="white" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M10 5.5h3M10 8h2.5M10 10.5h3" stroke="#10e6a8" strokeWidth="1.4" strokeLinecap="round"/>
            </svg>
          </div>
          <div>
            <div className="widget-brand-name">GrabCredit</div>
            <div className="widget-brand-sub">Pay Later</div>
          </div>
        </div>
      </div>
      <div className="widget-body">
        <div className="score-card">
          <div className="skel skel-circle" />
          <div style={{flex:1}}>
            <div className="skel skel-line w60" style={{marginBottom:8}}/>
            <div className="skel skel-line w40" />
          </div>
        </div>
        <div className="skel skel-block" />
        <div className="skel skel-line w100" />
        <div className="skel skel-line w80" />
        <div className="skel skel-line w60" />
      </div>
    </div>
  );

  /* Error */
  if (result.error) return (
    <div className="bnpl-widget">
      <div className="widget-bar" />
      <div className="widget-header">
        <div className="widget-brand">
          <div className="widget-brand-icon">
            <svg viewBox="0 0 16 16" fill="none">
              <path d="M3 8h5M8 8l-2.5-3M8 8l-2.5 3" stroke="white" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M10 5.5h3M10 8h2.5M10 10.5h3" stroke="#10e6a8" strokeWidth="1.4" strokeLinecap="round"/>
            </svg>
          </div>
          <div>
            <div className="widget-brand-name">GrabCredit</div>
            <div className="widget-brand-sub">Pay Later</div>
          </div>
        </div>
      </div>
      <div className="widget-body">
        <div className="narrative-box">
          <p>Unable to connect to the credit evaluation service. Please ensure the backend is running: <code>uvicorn app:app --port 8000</code></p>
        </div>
      </div>
    </div>
  );

  return (
    <div className={`bnpl-widget ${statusCls}`} key={persona.id}>
      <div className="widget-bar" />

      {/* Header */}
      <div className="widget-header">
        <div className="widget-brand">
          <div className="widget-brand-icon">
            <svg viewBox="0 0 16 16" fill="none">
              <path d="M3 8h5M8 8l-2.5-3M8 8l-2.5 3" stroke="white" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M10 5.5h3M10 8h2.5M10 10.5h3" stroke="#10e6a8" strokeWidth="1.4" strokeLinecap="round"/>
            </svg>
          </div>
          <div>
            <div className="widget-brand-name">GrabCredit</div>
            <div className="widget-brand-sub">Pay Later</div>
          </div>
        </div>
        <span className={`status-badge ${statusCls}`}>{label(result.status)}</span>
      </div>

      <div className="widget-body">
        {/* Score */}
        <div className="score-card">
          <ScoreRing score={result.score} status={result.status} />
          <div className="score-details">
            <div className="score-eyebrow">GrabCredit Score</div>
            <div className={`score-tier ${statusCls}`}>{tier(result.score)}</div>
            <div className="score-context">
              {persona.transaction_count > 0
                ? `${persona.transaction_count} transactions · ${Math.round(persona.account_age_days/30)} months`
                : "New user — no prior history"}
            </div>
          </div>
        </div>

        {/* Credit limit */}
        {result.credit_limit > 0 && (
          <div className="limit-row">
            <span className="limit-label">Approved Credit Line</span>
            <span className="limit-amount">₹{result.credit_limit.toLocaleString("en-IN")}</span>
          </div>
        )}

        {/* EMI plans */}
        {result.emi_plans?.length > 0 && (
          <>
            <div className="section-head">Choose EMI Plan</div>
            <div className="emi-grid">
              {result.emi_plans.map((plan, i) => (
                <div key={plan.months} id={`emi-${plan.months}`}
                  className={`emi-card ${selectedEmi === i ? "sel" : ""}`}
                  onClick={() => setSelectedEmi(i)}>
                  <div className="emi-amount">₹{plan.emi_amount.toLocaleString("en-IN")}</div>
                  <div className="emi-months">{plan.months} months</div>
                  <span className={`emi-tag ${plan.interest_rate === 0 ? "free" : "paid"}`}>
                    {plan.interest_rate === 0 ? "No Cost" : `${plan.interest_rate}% p.a.`}
                  </span>
                </div>
              ))}
            </div>
          </>
        )}

        {/* Reason codes */}
        {result.reason_codes?.length > 0 && (
          <>
            <div className="section-head">Decision Factors</div>
            <div className="reasons-list">
              {result.reason_codes.map((r, i) => (
                <div key={i} className={`reason-item ${r.type}`}
                  style={{ animationDelay: `${i * 0.06}s` }}>
                  <span className="reason-dot">
                    {r.type === "positive" ? "✓" : r.type === "neutral" ? "—" : "✕"}
                  </span>
                  <span>{r.text}</span>
                </div>
              ))}
            </div>
          </>
        )}

        {/* Narrative */}
        <div className="narrative-box">
          <p>{result.narrative}</p>
        </div>

        {/* CTA */}
        <button id="bnpl-cta"
          className={`cta-btn ${
            result.status === "APPROVED" ? "approved" :
            result.status === "PARTIALLY_APPROVED" ? "partial" : "disabled"
          }`}
          disabled={result.status === "REJECTED"}>
          {result.status === "REJECTED"
            ? "Not Eligible for Pay Later"
            : result.status === "PARTIALLY_APPROVED"
            ? `Proceed with ₹${result.credit_limit.toLocaleString("en-IN")}`
            : "Confirm & Pay with GrabCredit"}
        </button>

        {/* Security note */}
        {result.status !== "REJECTED" && (
          <div className="security-line">
            <svg viewBox="0 0 12 12" fill="none">
              <path d="M6 1L2 2.8v3.5C2 8.6 3.8 10.6 6 11c2.2-.4 4-2.4 4-4.7V2.8L6 1z"
                stroke="currentColor" strokeWidth="1.1" fill="none"/>
              <path d="M4.5 6l1 1L7.5 5" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            256-bit SSL · RBI Regulated · PCI DSS Compliant
          </div>
        )}
      </div>
    </div>
  );
};

export default BNPLWidget;