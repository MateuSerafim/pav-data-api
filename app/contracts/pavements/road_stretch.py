from pydantic import BaseModel, Field
from core.src.pavements_module.data_mapping.road_stretch import RoadStretchMapping
from core.src.pavements_module.domains.road_stretch import RoadStretch

class RoadStretchRequest(BaseModel):
    code:str = Field(min_length=1, max_length=RoadStretchMapping.CODE_MAX_LENGTH)
    
    lat_initial:float = Field(nullable=True)
    long_initial:float = Field(nullable=True)

    lat_final:float = Field(nullable=True)
    long_final:float = Field(nullable=True)

    def to_mapping(self) -> RoadStretchMapping:
        return RoadStretchMapping.create(self.code, self.lat_initial, self.long_initial, 
                                         self.lat_final, self.long_final)
    
class RoadStretchResponse(BaseModel):
    id: str
    code: str
    start_position: list
    end_position: list
    has_open_survey: bool
    
    @staticmethod
    def create(data: RoadStretch):
        return RoadStretchResponse(
            id=str(data.id), code=data.code, 
            start_position=data.initial_point, 
            end_position=data.final_point, 
            has_open_survey=data.has_open_survey())