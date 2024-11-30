# Julia Jakubowska AI Content Creation Platform

An AI-powered platform for generating YouTube content ideas, titles, thumbnails, and hooks in both English and Polish.

## Features

- Bilingual support (English and Polish)
- Multi-step content generation
- Modern, responsive UI
- Real-time AI-powered suggestions
- Step-by-step content creation workflow

## Tech Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS
- Backend: FastAPI, Python
- AI: OpenAI GPT-4
- Styling: Tailwind CSS, Framer Motion

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Activate the virtual environment:
```bash
source venv/bin/activate  # On Unix/macOS
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a .env file and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

6. Run the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Deployment

The application is deployed using:
- Frontend: Vercel (https://julia-jakubowska-ai.vercel.app)
- Backend: Render (https://julia-jakubowska-ai.onrender.com)

## Contributing

Feel free to submit issues and enhancement requests!
