from fastapi import Depends
import os
from core.src.files_module.image_storage_service import AzureStorageService
from core.src.database.db_context import get_session
from core.src.pavements_module.services.road_stretch import RoadStretchService
from core.src.pavements_module.services.visual_survey import VisualSurveyService
from core.src.pavements_module.services.visual_register import VisualRegisterService

async def road_stretch_service():
    async with get_session() as session_db:
        return RoadStretchService(session_db)

async def visual_survey_service():
    async with get_session() as session_db:
        return VisualSurveyService(session_db, RoadStretchService(session_db))

def file_storage_service():
    return AzureStorageService(os.getenv("STORAGE_CONNECTION_STRING"))

async def visual_register_service():
    async with get_session() as session_db:
        return VisualRegisterService(session_db, VisualSurveyService(session_db, RoadStretchService(session_db)))


