# FactCheck AI

FactCheck AI is a full-stack web application that verifies news, claims, and statements using AI and trusted external data sources. It analyzes user input, retrieves supporting evidence, and generates a verdict with confidence and reliability scores.

## Features

- AI-based claim verification
- Real-time news fetching
- Research-backed evidence integration
- Confidence and reliability scoring
- Claim history tracking
- Clean and responsive user interface

## Tech Stack

Frontend:
- React (Vite)
- Axios
- CSS

Backend:
- FastAPI
- Python
- SQLAlchemy
- SQLite

APIs Used:
- Google Gemini API
- GNews API
- Semantic Scholar API

## Project Structure

factcheck/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── App.jsx
│   └── package.json
│
└── README.md

## Installation and Setup

### 1. Clone the Repository

git clone https://github.com/Joel-pixel006/factcheck.git
cd factcheck

### 2. Backend Setup

cd backend

Create virtual environment:

python -m venv venv

Activate environment:

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

### 3. Environment Variables

Create a .env file inside backend folder and add:

GEMINI_API_KEY=your_gemini_api_key
GNEWS_API_KEY=your_gnews_api_key
SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_key
DATABASE_URL=sqlite:///./factcheck.db

### 4. Run Backend Server

uvicorn main:app --reload

Backend will run at:
http://127.0.0.1:8000

### 5. Frontend Setup

Open new terminal:

cd frontend

Install dependencies:

npm install

Run frontend:

npm run dev

Frontend will run at:
http://localhost:5173

## API Endpoints

POST /check
- Input: { "text": "your claim" }
- Output: verdict, confidence, reliability, articles, analysis

GET /history
- Returns previously checked claims

DELETE /history
- Clears stored history

## Deployment

Frontend (Vercel):
- Deploy React app
- Connect to backend URL

Backend (Render):
- Deploy FastAPI server
- Add environment variables in Render dashboard

## CORS Configuration

Ensure backend allows frontend requests:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Security

- Do not commit .env file
- Keep API keys private
- Use environment variables for all sensitive data

## Notes

- Backend must be running for frontend to work
- API rate limits may affect responses
- Results depend on available external data sources

## Future Improvements

- User authentication
- Better UI/UX enhancements
- Advanced fact-checking models
- Multi-language support

## Author

Joel Jose
B.Tech AI & Data Science

GitHub:
https://github.com/Joel-pixel006/factcheck
