from fastapi import APIRouter, Depends
from app.contracts.pavements.visual_survey import VisualSurveyResponse
from app.dependences import visual_survey_service
from datetime import datetime
import uuid
from core.src.pavements_module.data_mapping.visual_survey import VisualSurveyMapping
from core.src.pavements_module.services.visual_survey import VisualSurveyService
from app.utils.result_extensions import set_response

router = APIRouter(prefix="", tags=["Visual Surveys"])

@router.post("/road-stretchs/{road_strech_id}/visual_surveys")
async def create_visual_survey(road_strech_id: uuid.UUID, date: datetime,
                                visual_survey_service: VisualSurveyService\
                                  = Depends(visual_survey_service)):
    
    visual_data = VisualSurveyMapping.create(date, road_strech_id)

    add_result = await visual_survey_service.add_visual_survey(visual_data)
    
    return set_response(add_result, VisualSurveyResponse)

@router.get("/road-stretchs/{road_strech_id}/visual_surveys")
async def get_visual_surveys(road_strech_id: uuid.UUID, 
                             visual_survey_service: VisualSurveyService\
                                  = Depends(visual_survey_service)):
    query_result = await visual_survey_service.get_visual_surveys(road_strech_id)

    return set_response(query_result, VisualSurveyResponse)