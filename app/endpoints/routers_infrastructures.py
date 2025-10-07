from fastapi import APIRouter, Depends
import uuid
from app.dependences import road_stretch_service
from core.src.pavements_module.services.road_stretch import RoadStretchService
from app.contracts.pavements.road_stretch import RoadStretchRequest, RoadStretchResponse
from app.utils.result_extensions import set_response


router = APIRouter(prefix="", tags=["Infrastructures"])

CREATE_ROAD_STRETCH_SUMMARY = "Cria um trecho de rodovia."
@router.post("/road-stretchs", summary=CREATE_ROAD_STRETCH_SUMMARY)
async def set_road_stretchs(data: RoadStretchRequest,
                            service: RoadStretchService = Depends(road_stretch_service)):
    new_road = data.to_mapping()

    result = await service.add_road_stretch(new_road)
    return set_response(result, RoadStretchResponse)

GET_ROAD_STRETCH_SUMMARY = "Lista os trechos de rodovias."
@router.get("/road-stretchs", summary = GET_ROAD_STRETCH_SUMMARY)
async def get_road_stretchs(service: RoadStretchService = Depends(road_stretch_service)):
    road_list_result = await service.get_road_stretchs()
    return set_response(road_list_result, RoadStretchResponse)

DELETE_ROAD_STRETCH_SUMMARY = "Remove um trecho de rodovia."
@router.delete("/road-stretchs/{road_stretch_id}", summary=DELETE_ROAD_STRETCH_SUMMARY)
async def delete_road_stretchs(road_stretch_id: uuid.UUID, 
                               service: RoadStretchService = Depends(road_stretch_service)):
    
    delete_result = await service.delete_stretch(road_stretch_id)
    return set_response(delete_result)
    