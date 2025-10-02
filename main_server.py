from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from app.endpoints import routers_infrastructures
from app.endpoints import routers_visual_survey

fast_api_app = FastAPI(title="Pavesys - API", 
                       description="API de testes para análise de pavimentos")

fast_api_app.include_router(router=routers_infrastructures.router)
fast_api_app.include_router(router=routers_visual_survey.router)

if (__name__ == "__main__"):
    import uvicorn
    uvicorn.run("main_server:fast_api_app", host="0.0.0.0", port=8000, reload=True)