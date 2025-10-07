from core.src.pavements_module.domains.visual_register import VisualRegister
from core.src.pavements_module.domains.object_register import ObjectRegister
from pydantic import BaseModel
class VisualRegisterResponse(BaseModel):
    id: str
    status: int
    survey_id: str

    @staticmethod
    def create(visual_register: VisualRegister):
        return VisualRegisterResponse(id = str(visual_register.id), 
                                      status = visual_register.process_status,
                                      survey_id = str(visual_register.visual_survey_id))
    

class VisualRegisterResponseDetailed(VisualRegisterResponse):

    objects: list

    @staticmethod
    def create(visual_register: VisualRegister):
        return VisualRegisterResponseDetailed(id = str(visual_register.id), 
                                      status = visual_register.process_status,
                                      survey_id = str(visual_register.visual_survey_id), 
                                      objects=[dict(ObjectRegistersResponse.create(o))
                                               for o in visual_register.objects])
    
class ObjectRegistersResponse(BaseModel):
    id: str
    class_type: int
    confidence: float
    coord_x1: int
    coord_y1: int
    coord_x2: int
    coord_y2: int
    @staticmethod
    def create(data: ObjectRegister):
        return ObjectRegistersResponse(id = str(data.id), class_type=data.class_type, 
            confidence=data.confidence, coord_x1=data.position[0][0], 
            coord_y1=data.position[0][1], coord_x2=data.position[1][0], 
            coord_y2=data.position[1][1])