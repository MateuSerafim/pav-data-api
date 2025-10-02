from fastapi import APIRouter, Depends
from app.dependences import road_stretch_service
from core.src.pavements_module.services.road_stretch import RoadStretchService
from app.contracts.pavements.road_stretch import RoadStretchRequest, RoadStretchResponse
from app.utils.result_extensions import return_response


router = APIRouter(prefix="", tags=["Infrastructures"])

@router.post("/road-stretchs")
async def set_road_stretchs(data: RoadStretchRequest,
                            service: RoadStretchService = Depends(road_stretch_service)):
    new_road = data.to_mapping()

    result = await service.add_road_stretch(new_road)
    return return_response(result, RoadStretchResponse)

@router.get("/road-stretchs")
async def get_road_stretchs(service: RoadStretchService = Depends(road_stretch_service)):
    road_list_result = await service.get_road_stretchs()
    return return_response(road_list_result, RoadStretchResponse)