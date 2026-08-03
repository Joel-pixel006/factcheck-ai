import axios from "axios";
import { useState, useEffect } from "react";
import ResultCard from "./components/ResultCard";
import "./App.css";

function App() {
  const [claim, setClaim] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);

  useEffect(() => {
    loadHistory();
  }, []);

  async function loadHistory() {
    try {
      const response = await axios.get("http://127.0.0.1:8000/history");
      setHistory(response.data);
    } catch (error) {
      console.error(error);
    }
  }

  async function handleCheck() {
    if (!claim.trim()) return;

    setLoading(true);
    setError("");

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/check",
        {
          text: claim,
        }
      );

      setResult(response.data);
      loadHistory();
    } catch (error) {
      console.error(error);
      setError("Unable to verify the claim. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  async function clearHistory() {
    try {
      await axios.delete("http://127.0.0.1:8000/history");
      setHistory([]);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div className="container">

      <div className="hero">

        <h1>🔍 FactCheck AI</h1>

        <p className="subtitle">
          Verify news, claims and information using AI-powered fact checking
          with trusted sources.
        </p>

      </div>

      <textarea
        className="claim-box"
        placeholder="Example: Lionel Messi won the 2022 FIFA World Cup..."
        value={claim}
        onChange={(e) => setClaim(e.target.value)}
      />

      <button
        className="check-btn"
        onClick={handleCheck}
        disabled={loading}
      >
        {loading ? "⏳ Verifying..." : "🔎 Verify Claim"}
      </button>

      {loading && (
        <p className="loading-text">
          Searching trusted sources and analyzing evidence...
        </p>
      )}

      {error && <p className="error">{error}</p>}

      <ResultCard result={result} />

      <div className="history-card">

        <div className="history-top">

          <div>

            <h2>🕒 Recent Fact Checks</h2>

            <p className="history-subtitle">
              Your previously verified claims
            </p>

          </div>

          <button
            className="clear-btn"
            onClick={clearHistory}
          >
            🗑 Clear History
          </button>

        </div>

        {history.length === 0 ? (

          <p className="history-subtitle">
            No previous fact checks yet.
          </p>

        ) : (

          history.map((item, index) => (

            <div className="history-item" key={index}>

              <h3>📝 {item.claim}</h3>

              <div
                className={`history-verdict ${item.verdict
                  .toLowerCase()
                  .replace(/\s+/g, "-")}`}
              >
                {item.verdict}
              </div>

              <p>
                <strong>Confidence:</strong>{" "}
                {item.confidence === "N/A"
                  ? "N/A"
                  : `${item.confidence}%`}
              </p>

              <p>
                <strong>Reliability:</strong> {item.reliability}
              </p>

            </div>

          ))

        )}

      </div>

    </div>
  );
}

export default App;