from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from app.messages.messages import Messages
from app.services.factory import ServiceFactory
from app.services.sentence_creator import SentenceCreatorService

router = APIRouter()
service_factory = ServiceFactory()


async def get_create_sentence_service():
    return await service_factory.create_sentence_service()


@router.get(
    "/",
    summary="Creates a sentence based on the provided city input.",
    status_code=200
)
async def send(city: str = "", service: SentenceCreatorService = Depends(get_create_sentence_service)):
    """
    Args:  <br>
    &nbsp; &nbsp; city: A string representing a city. <br>
    &nbsp; &nbsp; service: An instance of SentenceCreatorService (injected via dependency injection).

    Returns: <br>
    &nbsp; &nbsp; A JSONResponse object containing generated sentence.

    Raises: <br>
    &nbsp; &nbsp; HTTPException: If an error occurs during sentence creation, with appropriate status code and detail.
    """
    try:
        if not city:
            raise HTTPException(status_code=400, detail=Messages.CITY_ERROR)

        sentence = await service.process_input(city)
        response = {
            "sentence": sentence
        }
        return JSONResponse(content=response)
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=Messages.NOT_FINISH_PROCESS)
