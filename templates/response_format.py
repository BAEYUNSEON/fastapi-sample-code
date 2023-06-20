from fastapi import Response
from typing import Optional, Any
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

DEFAULT_CONTENT_TYPE = "application/json; utf-8"


def wrap_response(
        status_code: int,
        msg: Any,
        error_code: Optional[str] = None,
        content_type: Optional[str] = DEFAULT_CONTENT_TYPE):
    resp = None
    if isinstance(msg, str):
        response_obj = {
            'message': msg,
        }
        if not (200 >= status_code) or error_code:
            response_obj = {
                'errorCode': status_code,
                'errorMessage': msg,
            }
        resp = JSONResponse(content=response_obj, status_code=status_code)
    elif isinstance(msg, bytes):
        resp = Response(content=msg, media_type=content_type)
    else:
        resp = JSONResponse(content=jsonable_encoder(msg), status_code=status_code, media_type=content_type)
    return resp
