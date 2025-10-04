from core.src.pavements_module.domains.visual_register import VisualRegister
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
