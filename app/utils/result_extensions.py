from fastapi.responses import JSONResponse
from core.src.utils.result import Result
from datetime import datetime, timezone

def return_response(result: Result, class_to_convert = None):
    if result.is_failure():
        return JSONResponse(status_code=result.error_code.value, 
                            content={"error": result.error, 
                                     "response_data":str(datetime.now(tz=timezone.utc))})
    if (class_to_convert == None):
        return JSONResponse(
            content={"result": dict(result.value), 
                     "response_data":str(datetime.now(tz=timezone.utc))})
    
    if (type(result.value) == list):
        data_list = [dict(class_to_convert.create(value)) for value in result.value]
        return JSONResponse(content={"result": data_list, 
                                     "response_data":str(datetime.now(tz=timezone.utc))})
    
    return JSONResponse(content={"result": dict(class_to_convert.create(result.value)), 
                                 "response_data":str(datetime.now(tz=timezone.utc))})