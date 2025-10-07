from fastapi import APIRouter, Depends
from app.contracts.pavements.visual_survey import VisualSurveyResponse, VisualSurveyResponseDetailed
from app.dependences import visual_survey_service
from datetime import datetime
import uuid
from core.src.pavements_module.data_mapping.visual_survey import VisualSurveyMapping
from core.src.pavements_module.services.visual_survey import VisualSurveyService
from app.utils.result_extensions import set_response

router = APIRouter(prefix="", tags=["Visual Surveys"])

CREATE_VISUAL_SURVEY_SUMMARY = "Cria um levantamento para um trecho de rodovia."
CREATE_VISUAL_SURVEY_DESCRIPTION = '''
Cria um novo levantamento para um trecho de rodovia.\n 
É necessário inserir uma data válida.\n
O ato de criar um novo levantamento implica em finalizar quaisquer 
outros levantamentos presente no trecho!
'''
@router.post("/road-stretchs/{road_strech_id}/visual_surveys", 
             summary=CREATE_VISUAL_SURVEY_SUMMARY, 
             description=CREATE_VISUAL_SURVEY_DESCRIPTION)
async def create_visual_survey(road_strech_id: uuid.UUID, date: datetime,
                                visual_survey_service: VisualSurveyService\
                                  = Depends(visual_survey_service)):
    
    visual_data = VisualSurveyMapping.create(date, road_strech_id)

    add_result = await visual_survey_service.add_visual_survey(visual_data)
    
    return set_response(add_result, VisualSurveyResponse)

GET_VISUAL_SURVEYS_SUMMARY = "Retorna a lista de levantamentos para um trecho de rodovia."
CREATE_VISUAL_SURVEYS_DESCRIPTION = '''
Os status implicam:
 - 0: Em andamento - Itens ainda não analisados!
 - 1: Finalizado - Todos os itens analisados!
 - 2: Problema - Alguma análise falhou!
'''
@router.get("/road-stretchs/{road_strech_id}/visual_surveys", 
            summary=GET_VISUAL_SURVEYS_SUMMARY,
            description=CREATE_VISUAL_SURVEYS_DESCRIPTION)
async def get_visual_surveys(road_strech_id: uuid.UUID, 
                             visual_survey_service: VisualSurveyService\
                                  = Depends(visual_survey_service)):
    query_result = await visual_survey_service.get_visual_surveys(road_strech_id)

    return set_response(query_result, VisualSurveyResponse)

GET_VISUAL_SURVEY_SUMMARY = "Retorna os detalhes de um levantamento."
CREATE_VISUAL_SURVEY_DESCRIPTION = '''
status:
 - 0: Em andamento - Itens ainda não analisados!
 - 1: Finalizado - Todos os itens analisados!
 - 2: Problema - Alguma análise falhou!
'''
@router.get("/visual_surveys/{visual_survey_id}", 
            summary=GET_VISUAL_SURVEY_SUMMARY,
            description=CREATE_VISUAL_SURVEY_DESCRIPTION)
async def get_visual_surveys(visual_survey_id: uuid.UUID, 
                             visual_survey_service: VisualSurveyService\
                                  = Depends(visual_survey_service)):
    query_result = await visual_survey_service.get_visual_survey(visual_survey_id)

    return set_response(query_result, VisualSurveyResponseDetailed)

