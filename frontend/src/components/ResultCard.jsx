import ArticleList from "./ArticleList";

function ResultCard({ result }) {
  if (!result) return null;

  const verdictClass = result.verdict
    .toLowerCase()
    .replace(/\s+/g, "-");

  const reliabilityClass = result.reliability
    .toLowerCase()
    .replace(/\s+/g, "-");

  return (
    <div className="result-card">

      <div className={`verdict ${verdictClass}`}>
        {result.verdict}
      </div>

      <h3>📊 Confidence Score</h3>

      <div className="progress">
        <div
          className="progress-fill"
          style={{ width: `${result.confidence}%` }}
        >
          {result.confidence}%
        </div>
      </div>

      <p>
        <strong>Reliability:</strong>{" "}
        <span className={`reliability ${reliabilityClass}`}>
          {result.reliability}
        </span>
      </p>

      <h3>📝 Summary</h3>

      <div className="summary">
        {result.summary || "No summary available."}
      </div>

      <h3>🤖 AI Assessment</h3>

      <div className="assessment">
        {result.assessment || "No assessment available."}
      </div>

      {result.articles && result.articles.length > 0 ? (
        <>
          <h3>📚 Supporting Sources</h3>
          <ArticleList articles={result.articles} />
        </>
      ) : (
        <p>No supporting articles found.</p>
      )}

    </div>
  );
}

export default ResultCard;