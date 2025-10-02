from fastapi import Depends
from core.src.database.db_context import get_session
from core.src.pavements_module.services.road_stretch import RoadStretchService
from core.src.pavements_module.services.visual_survey import VisualSurveyService

async def road_stretch_service(session_db = Depends(get_session)):
    return RoadStretchService(session_db)

async def visual_stretch_service(session_db = Depends(get_session)):
    return VisualSurveyService(session_db)


