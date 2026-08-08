# Import FastAPI framework

from fastapi.middleware.cors import CORSMiddleware
from rule_classifier import classify_by_rules
from urllib import response
from fastapi import FastAPI
from dotenv import load_dotenv
import google.generativeai as genai
import joblib
from ddgs import DDGS
import os
from pathlib import Path

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
#geimini setup
def generate_gemini_analysis(claim, text):
    try:
        model=genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
    f"""
    You are an AI fact-checking assistant.

    Analyze the evidence below.

    Return exactly in this format:

    Verdict: Supported / Partially Supported / Refuted / No Evidence

    Confidence: 0-100

    Reliability: High / Medium / Low

    Summary: <maximum 2 sentences>

    Assessment: <maximum 2 sentences>

    Rules:
    - If the evidence clearly confirms the claim, return Supported.
    - If the evidence clearly disproves the claim, return Refuted.
    - If evidence is incomplete or mixed, return Partially Supported.
    - If there is no useful evidence, return No Evidence.
    - Return only the format above.
    - Do not include markdown or bullet points.

    Claim:
    {claim}

    Evidence:
    {text}
    """
)
        return response.text
    except Exception:
        return "AI service temporarily busy. Please try again later."
# Extract structured fields from Gemini response
# Extract structured fields from Gemini response
# Extract structured fields from Gemini response
def parse_gemini_response(ai_analysis):
    result = {
        "verdict": "Needs More Evidence",
        "confidence": 0,
        "reliability": "Low",
        "summary": "",
        "assessment": ""
    }

    for line in ai_analysis.split("\n"):
        line = line.strip()

        if line.startswith("Verdict:"):
            result["verdict"] = line.replace("Verdict:", "").strip()

        elif line.startswith("Confidence:"):
            value = line.replace("Confidence:", "").strip()

            try:
                result["confidence"] = int(value)
            except ValueError:
                result["confidence"] = 0

        elif line.startswith("Reliability:"):
            result["reliability"] = line.replace("Reliability:", "").strip()

        elif line.startswith("Summary:"):
            result["summary"] = line.replace("Summary:", "").strip()

        elif line.startswith("Assessment:"):
            result["assessment"] = line.replace("Assessment:", "").strip()

    return result
# Generate verdict from AI analysis
def generate_verdict_from_analysis(ai_analysis):
    analysis=ai_analysis.lower()

    if "refute" in analysis or "false" in analysis or "incorrect" in analysis or "contradict" in analysis:
        return "Refuted"

    elif "support" in analysis or "confirmed" in analysis or "true" in analysis:
        return "Supported"

    elif "partial" in analysis or "mixed" in analysis:
        return "Partially Supported"

    elif "no evidence" in analysis:
        return "No Evidence"

    return "Needs More Evidence"
def answer_question(text):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(
            f"""
            Answer this question clearly in simple words.

            Question:
            {text}
            """
        )

        return response.text
    except Exception:
        return "AI service temporarily busy. Please try again later."
def filter_articles(claim, articles):
    return articles, 0.75
def generate_opinion_response(text):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(
            f"""
            The user has given an opinion.

            Analyze the opinion and provide:
            1. Balanced viewpoint
            2. Alternative perspective
            3. Short conclusion
            Keep response under 150 words.
            Opinion:
            {text}
            """
        )

        return response.text
    except Exception:
        return "AI service temporarily busy. Please try again later."

# Import BaseModel for input validation
from pydantic import BaseModel

# Import regex for text cleaning
import re
import requests
# Create FastAPI application
app = FastAPI()
# Enable React frontend access
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://factcheck-ai-two.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#sqlite setup (placeholder)
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import DateTime
from datetime import datetime
os.makedirs("data", exist_ok=True)
DATABASE_URL="sqlite:///factcheck.db"
engine = create_engine(DATABASE_URL)
#pen = sessionlocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Think of Base as a template maker.
print("Database connected successfully.")
#This class represents a database table.
Base = declarative_base()
class ClaimHistory(Base):
    __tablename__ = "claims"
    id = Column(Integer, primary_key=True)
    claim = Column(String)
    verdict = Column(String)
    confidence = Column(Integer) 
    reliability = Column(String)
    ai_analysis = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
Base.metadata.create_all(bind=engine)
print("Claims Table Created")
# Load trained ML model
model = joblib.load("query_classifier.pkl")
# Load TF-IDF vectorizer
vectorizer = joblib.load("vectorizer.pkl")
# Common words to ignore
STOP_WORDS = {
    "the", "a", "an", "is", "are",
    "was", "were", "of", "in",
    "on", "at", "to", "for", "and"
}

# Simple evidence database
evidence_db = {
    "coffee cures cancer": "No scientific evidence found.",
    "earth revolves around sun": "Supported by scientific evidence.",
    "water boils 100 c": "Generally true at sea level."
}

# Homepage endpoint
@app.get("/")
def home():
    return {"message": "FactCheck AI is running"}

# User input structure
class Claim(BaseModel):
    text: str
# Wikipedia search (test version)
def search_wikipedia(query):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"

    headers = {
        "User-Agent": "FactCheckAI/1.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()

    return None
# Clean user text
def clean_claim(text):
    text = text.strip()
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = " ".join(text.split())
    return text
# Search articles (placeholder)
def search_articles(wiki_data):
    if not wiki_data:
        return []

    return [
        {
            "title": wiki_data.get("title", ""),
            "source": "Wikipedia",
            "summary": wiki_data.get("extract", ""),
            "url": wiki_data.get(
                "content_urls",
                {}
            ).get(
                "desktop",
                {}
            ).get(
                "page",
                ""
            )
        }
    ]
def search_news(query):
    url = (
        f"https://gnews.io/api/v4/search?"
        f"q={query}&lang=en&max=1"
        f"&apikey={GNEWS_API_KEY}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if not data.get("articles"):
        return None
    article = data["articles"][0]
    return {
        "title": article["title"],
        "source": article["source"]["name"],
        "summary": article["description"],
        "url": article["url"]
    }
def search_research(query):
    url = (
        "https://api.semanticscholar.org/graph/v1/"
        f"paper/search?query={query}&limit=1"
        "&fields=title,abstract,url"
    )

    response = requests.get(url)

    
    if response.status_code == 429:
        return None
    if response.status_code != 200:
        return None

    data = response.json()

    if not data.get("data"):
        return None

    paper = data["data"][0]

    return {
        "title": paper.get("title", ""),
        "source": "Research Paper",
        "summary": paper.get("abstract") or "No abstract available.",
        "url": paper.get("url", "")
    }
# Classify user input
def classify_claim(text):
    if text.startswith(
        ("what", "why", "how", "when",
         "where", "who", "does",
         "do", "is", "are")
    ):
        return "Question"

    if "i think" in text or "in my opinion" in text:
        return "Opinion"

    return "Fact Claim"

# Extract keywords
def extract_keywords(text):
    words = text.split()

    keywords = [
        word
        for word in words
        if word not in STOP_WORDS
    ]

    return keywords

# Search evidence
def find_evidence(claim):
    for stored_claim, evidence in evidence_db.items():
        if stored_claim in claim:
            return evidence

    return "No evidence available."
def classify_query(text):
    # Convert text to vector
    text_vector = vectorizer.transform([text])
    # Predict category
    prediction = model.predict(text_vector)
    return prediction[0]
print(classify_query("Messi"))
print(classify_query("Coffee cures cancer"))
print(classify_query("I think Ronaldo is best"))
# Search web articles
def search_web(query):
    results=[]
    ddgs=DDGS()
    search_results=ddgs.text(query,max_results=5)
    for r in search_results:
        results.append({
            "title":r["title"],
            "source":"Web Search",
            "summary":r["body"],
            "url":r["href"]
        })
    return results

# Generate verdict
def generate_verdict(evidence):
    if evidence == "No evidence available.":
        return "Unknown"

    if "No scientific evidence" in evidence:
        return "Unsupported"

    return "Supported"

# Count keywords
def keyword_count(keywords):
    return len(keywords)
# Search articles (placeholder)
def calculate_source_score(articles):
    score = 0
    for article in articles:

        if article["source"] == "Wikipedia":
            score += 80
        elif article["source"] == "Research Paper":
            score += 95        
        else:
            score += 70
    return score

def extract_sources(articles):
    sources = []

    for article in articles:
        sources.append({
            "source": article["source"],
            "category": get_source_category(article["source"]),
            "url": article["url"]
        })

    return sources
# Combine article summaries
def summarize_articles(articles):
    summaries = []
    for article in articles:
        summaries.append(article["summary"])
    return " ".join(summaries)
# Generate AI-style analysis
def generate_ai_analysis(verdict, confidence, article_count):
    if confidence >= 80:
        return f"High confidence analysis based on {article_count} reliable sources."
    if confidence >= 60:
        return f"Moderate confidence analysis based on {article_count} sources."
    return "Limited information available. Further verification recommended."

def get_source_category(source):
    if source == "Wikipedia":
        return "Knowledge Base"
    if source == "Research Paper":
        return "Scientific Source"
    return "News Source"
# Main endpoint
@app.post("/check")
def check_claim(claim: Claim):
    # Clean claim
    cleaned_claim = clean_claim(claim.text)
    # Predict query type using ML
   # First try the rule-based classifier
    query_type = classify_by_rules(claim.text)

# If no rule matched, use the ML model
    if query_type is None:
        query_type = classify_query(claim.text)
    print("Detected Query Type:", query_type)
    # If input is opinion
    if query_type == "opinion":

        opinion_answer = generate_opinion_response(cleaned_claim)

        return {
            "query_type": query_type,
            "verdict": "Opinion Analysis",
            "confidence": "N/A",
            "reliability": "N/A",
            "articles": [],
            "ai_analysis": opinion_answer,
            "sources": []
        }


    # If input is question
    if query_type == "question":
        question_answer = answer_question(cleaned_claim)

        return {
        "query_type": query_type,
        "verdict": "Question Answered",
        "confidence": "N/A",
        "reliability": "N/A",
        "articles": [],
        "ai_analysis": question_answer,
        "sources": []
        }
    # Extract keywords
    keywords = extract_keywords(cleaned_claim)
    # Create searchable text
    search_text = " ".join(keywords)
    # Search evidence
    evidence = find_evidence(search_text) 
    # Generate verdict
    verdict = generate_verdict(evidence)
    wiki_query=" ".join(keywords) if keywords else cleaned_claim
    wiki_data = search_wikipedia(wiki_query)
    news_article=search_news(wiki_query)
    research_article=search_research(wiki_query)
    web_articles = search_web(wiki_query) 
    research_status = ( 
        "Research Found" if research_article else "Rate limited or No Research Found"
    )
    
    # Count keywords
    total_keywords = keyword_count(keywords)
    articles=search_articles(wiki_data)
    if news_article:
        articles.append(news_article)
    if research_article:
        articles.append(research_article)
    # Add web search results
    articles.extend(web_articles)
    # Remove duplicate articles
    seen_urls = set()
    unique_articles = []
    for article in articles:
        if article["url"] not in seen_urls:
            unique_articles.append(article)
            seen_urls.add(article["url"])

    articles = unique_articles
    # Keep semantically relevant articles only
    articles,avg_similarity=filter_articles(cleaned_claim,articles)
    print("Average similarity:",avg_similarity)
    # Generate verdict based on evidence quality
    article_count = len(articles)
    source_score = 0
    confidence = 0
    reliability = "Low"
    ai_analysis = ""
    sources = []
    article_summary = ""
    parsed_response = {
    "verdict": "No Evidence",
    "confidence": 0,
    "reliability": "Low",
    "summary": "",
    "assessment": ""
}
    

    if article_count > 0:
        source_score = calculate_source_score(articles)
        # Confidence based on semantic relevance
       # confidence = int(avg_similarity * 100)
        article_summary = summarize_articles(articles)
        
        ai_analysis = generate_gemini_analysis(cleaned_claim, article_summary)
        # Extract structured AI response
        parsed_response=parse_gemini_response(ai_analysis)
        # Generate verdict using AI analysis
        #verdict=generate_verdict_from_analysis(ai_analysis)
        if avg_similarity >= 0.80:
            reliability = "High"
        elif avg_similarity >= 0.60:
            reliability = "Medium"
        else:
            reliability = "Low"
        sources = extract_sources(articles)
        # Use AI-generated values
        verdict=parsed_response["verdict"]
        confidence=parsed_response["confidence"]
        reliability=parsed_response["reliability"]

    if wiki_data:
        wiki_title = wiki_data.get("title", "")
        wiki_summary = wiki_data.get("extract", "")

    if query_type == "fact_claim" or query_type == "entity_search":
        db = SessionLocal()
        new_claim = ClaimHistory(
            claim=claim.text,
            verdict=verdict,
            confidence=confidence,
            reliability=reliability,
            ai_analysis=ai_analysis
        )
        db.add(new_claim)
        db.commit()
        db.close()
    db.commit()
    db.close()
    return {
        #"original_claim": claim.text,
        #"cleaned_claim": cleaned_claim,
        "claim_type": classify_claim(cleaned_claim),
        "status": "received",
        "query_type": query_type,
        "verdict": verdict,
        #"keywords": keywords,
        #"keyword_count": total_keywords,
        #"evidence": evidence,
        #"source_score": source_score,
        "article_count": article_count,
        "research_status": research_status,
        "reliability": reliability,
        "articles":articles,
        #"article_summary": article_summary,
        "summary":parsed_response["summary"],
        "assessment":parsed_response["assessment"],
        "sources": sources,
        "confidence": confidence
    }
#test endpoint to retrieve claim history
@app.get("/claims")
def get_claims():

    db = SessionLocal()

    claims = db.query(ClaimHistory).all()

    db.close()

    return claims
@app.get("/test-gemini")
def test_gemini():

    result = generate_gemini_analysis(
        "Machine learning is a branch of artificial intelligence."
    )

    return {
        "response": result
    }
# Endpoint to retrieve claim history
@app.get("/history")
def get_history():
    db=SessionLocal()
    claims = db.query(ClaimHistory).all()
    

    return [
        {
            "claim": claim.claim,
            "verdict": claim.verdict,
            "confidence": claim.confidence,
            "reliability": claim.reliability
        }
        for claim in claims
    ]
@app.delete("/history")
def clear_history():
    db=SessionLocal()
    db.query(ClaimHistory).delete()
    db.commit()
    db.close()
    return {"message": "Claim history cleared."}