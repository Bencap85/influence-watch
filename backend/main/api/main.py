from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main.api.routes.processed_article.router import router as processed_article_router
from main.api.routes.source.router import router as source_router
from main.api.routes.event.router import router as event_router
from main.api.routes.detection.router import router as detection_router
from main.api.routes.agent.router import router as agent_router
from main.api.routes.job.router import router as job_router

app = FastAPI(
    title="Influence Watch API",
    root_path="/api/v1"
)

app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["*"], # Allow all domains 
    allow_credentials=True, 
    allow_methods=["*"], # Allow all HTTP methods 
    allow_headers=["*"], # Allow all headers 
)

# Register domain routers
app.include_router(processed_article_router)
app.include_router(source_router)
app.include_router(event_router)
app.include_router(detection_router)
app.include_router(agent_router)
app.include_router(job_router)

# Local development entrypoint
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
