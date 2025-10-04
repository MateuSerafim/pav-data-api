from pydantic import BaseModel
from core.src.pavements_module.domains.visual_survey import VisualSurvey

class VisualSurveyResponse(BaseModel):
    id: str
    date: str
    is_open: bool
    road_stretch_id:str
    quant_registers: int
    status: int
    
    @staticmethod
    def create(data: VisualSurvey):
        return VisualSurveyResponse(id=str(data.id), date=str(data.date), 
                            is_open=data.is_open, 
                            road_stretch_id=str(data.road_stretch_id), 
                            quant_registers=len(data.registers), status=data.registers_status())