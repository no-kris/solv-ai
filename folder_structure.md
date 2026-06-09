```
solv-ai/
├── frontend/                    # React + TypeScript
│   ├── src/
│   │   ├── components/   # Reusable React components
│   │   ├── pages/        # Page routes
│   │   ├── types/        # Shared Typescript interfaces
│   │   ├── services/     # API calls to backend
│   │   ├── styles/       # CSS styles
│   │   └── main.tsx
│   ├── .gitignore
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts   
│   ├── index.html
│   └── ...
│
├── backend/                      # FastAPI + Python
│   ├── app/
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── routes/
│   │   ├── services/
│   │   ├── prompts/
│   │   └── utils/
│   ├── requirements.txt
│   ├── .env.example               # Example env vars
│   └── README.md
```
