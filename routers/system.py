from fastapi import APIRouter, status


router = APIRouter(
    prefix="/system",
    tags=["system"],
    responses={404: {"user": "Not authorized"}}
)


@router.get("/healthcheck", status_code=status.HTTP_200_OK)
def health_check():
    return {"health_check": "Everything OK!"}
