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
    
class VisualSurveyResponseDetailed(VisualSurveyResponse):
    quant_pothole: int
    quant_patch: int
    quant_crack_i: int
    quant_crack_j: int

    @staticmethod
    def create(data: VisualSurvey):
        return VisualSurveyResponseDetailed(id=str(data.id), date=str(data.date), 
                            is_open=data.is_open, 
                            road_stretch_id=str(data.road_stretch_id), 
                            quant_registers=len(data.registers), 
                            status=data.registers_status(), 
                            quant_pothole=data.quant_item_by_class(1), 
                            quant_patch=data.quant_item_by_class(2), 
                            quant_crack_i=data.quant_item_by_class(3), 
                            quant_crack_j=data.quant_item_by_class(4))