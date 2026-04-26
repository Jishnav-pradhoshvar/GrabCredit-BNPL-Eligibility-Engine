const API_BASE = "http://localhost:8000";

/**
 * POST /evaluate-credit — MCP-compliant credit evaluation endpoint.
 * Sends persona data as JSON, returns full BNPL decision payload.
 */
export const evaluateCredit = async (persona) => {
  const res = await fetch(`${API_BASE}/evaluate-credit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(persona),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }

  return res.json();
};