from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from contextlib import asynccontextmanager
from app.dependences import file_storage_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    storage_service = file_storage_service()
    # Não coloquei como var de amb mas por ser prototipo
    container_client = storage_service.blob_service.get_container_client("images-survey")
    print(container_client)
    try:
        await container_client.create_container()
    except Exception:
        pass
    yield

fast_api_app = FastAPI(title="Pavesys - API", 
                       description="API de testes para análise de pavimentos", 
                       lifespan=lifespan)

from app.endpoints import routers_infrastructures
from app.endpoints import routers_visual_survey
from app.endpoints import routers_visual_register

fast_api_app.include_router(router=routers_infrastructures.router)
fast_api_app.include_router(router=routers_visual_survey.router)
fast_api_app.include_router(router=routers_visual_register.router)

if (__name__ == "__main__"):
    import uvicorn
    uvicorn.run("main_server:fast_api_app", host="0.0.0.0", port=8000, reload=True)