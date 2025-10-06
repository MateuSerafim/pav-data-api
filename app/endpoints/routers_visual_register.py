from fastapi import APIRouter, Depends, UploadFile, File
import uuid
import io
from fastapi.responses import StreamingResponse

from app.dependences import visual_register_service, \
  visual_survey_service, \
  file_storage_service
from core.src.pavements_module.services.visual_register import VisualRegisterService
from core.src.pavements_module.services.visual_survey import VisualSurveyService
from core.src.pavements_module.data_mapping.visual_register import VisualRegisterMapping
from core.src.files_module.image_storage_service import AzureStorageService
from app.utils.result_extensions import set_response
from app.utils.file_extensions import get_file_extensions
from core.src.utils.result import Result
from app.contracts.pavements.visual_register import VisualRegisterResponse

from app.qeue_control import send_to_queue

router = APIRouter(prefix="", tags=["Visual Register"])

@router.post("/visual-surveys/{visual_survey_id}/visual-registers")
async def create_visual_register(visual_survey_id: uuid.UUID, file: UploadFile = File(...),
                                visual_register_service: VisualRegisterService\
                                  = Depends(visual_register_service), 
                                storage_service: AzureStorageService = Depends(file_storage_service), 
                                visual_survey_service: VisualSurveyService \
                                  = Depends(visual_survey_service)):
    visual_survey_result = await visual_survey_service.get_visual_survey(visual_survey_id)
    if (visual_survey_result.is_failure()):
        return set_response(visual_survey_result)
    
    if (not visual_survey_result.value.is_open):
        return set_response(Result.failure("Não é possível adicionar registro a levantamento finalizado!"))
    
    file_name = uuid.uuid4()
    file_extensions = get_file_extensions(file.filename)
    if (file_extensions not in ["jpg", "png", "jpeg"]):
        return set_response(Result.failure(f"Tipo de arquivo inválido!"))
  
    image_data = await file.read()

    register_name = f"{visual_survey_id}/{file_name}.{file_extensions}"
  
    upload_result: Result = \
      await storage_service.upload_file("images-survey", image_data, register_name)
    if (upload_result.is_failure()):
        return set_response(upload_result)
    
    add_result = await visual_register_service.add_visual_register(
        VisualRegisterMapping.create(file_name, register_name, 0, 0, 0, visual_survey_id))
    
    if (add_result.is_failure()):
        return set_response(add_result)
    
    send_to_queue("survey-images", str(file_name))
    
    return set_response(add_result, VisualRegisterResponse)

@router.get("/visual-registers/{visual_register_id}/images")
async def get_visual_register_image(visual_register_id: uuid.UUID, 
    storage_service: AzureStorageService = Depends(file_storage_service),
    visual_register_service: VisualRegisterService= Depends(visual_register_service)):

    maybe_register: Result = await visual_register_service.get_visual_register(visual_register_id)
    if (maybe_register.is_failure()):
        set_response(maybe_register)
    
    image_stream = await storage_service.get_file("images-survey", maybe_register.value.image_url)
    if (image_stream.is_failure()):
        set_response(image_stream)
    try:
        data = await image_stream.value.readall()
        return StreamingResponse(io.BytesIO(data), 
                                 media_type="application/octet-stream", 
                                 headers={"Content-Disposition": \
                                          f"attachment; filename={maybe_register.value.image_url}"})
    except Exception as ex:
        return set_response(Result.failure(ex))
