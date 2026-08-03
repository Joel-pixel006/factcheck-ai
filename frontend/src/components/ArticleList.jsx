function ArticleList({ articles }) {
  if (!articles || articles.length === 0) {
    return (
      <div className="articles">
        <p>No supporting articles found.</p>
      </div>
    );
  }

  return (
    <div className="articles">

      <h3>📚 Supporting Articles</h3>

      {articles.map((article, index) => (

        <div className="article-card" key={index}>

          <h4>{article.title}</h4>

          <p className="article-source">
            <strong>Source:</strong> {article.source}
          </p>

          {article.summary && (
            <p className="article-summary">
              {article.summary}
            </p>
          )}

          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="article-link"
          >
            🔗 Read Full Article
          </a>

        </div>

      ))}

    </div>
  );
}

export default ArticleList;