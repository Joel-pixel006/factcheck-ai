from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
semantic_model=SentenceTransformer('all-MiniLM-L6-v2')
# Convert text to vector
def get_embedding(text):
    embedding = semantic_model.encode([text])
    return embedding
# Compare similarity
def get_similarity(text1, text2):
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)
    similarity = cosine_similarity(embedding1, embedding2)
    return similarity[0][0]
# Keep relevant articles and calculate average similarity
def filter_articles(query,articles):
    filtered_articles=[]
    similarity_scores=[]
    for article in articles:
        score=get_similarity(query,article["summary"])
        if score>0.50:
            filtered_articles.append(article)
            similarity_scores.append(score)
    avg_score=sum(similarity_scores)/len(similarity_scores) if similarity_scores else 0
    return filtered_articles,avg_score
