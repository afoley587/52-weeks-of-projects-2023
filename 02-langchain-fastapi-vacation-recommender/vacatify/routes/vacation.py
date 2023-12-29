import uuid

from fastapi import APIRouter, Request, BackgroundTasks, HTTPException

from vacatify.schemas import (
    GenerateVacationIdeaResponse,
    GetVacationIdeaResponse,
    GenerateVacationIdeaRequest,
)

from vacatify.chains.vacation import generate_vacation_idea_chain, vacations

vacation_router = APIRouter(prefix="/vacation")


@vacation_router.post(
    "/",
    summary="Generate a vacation idea.",
    responses={
        201: {"description": "Successfully initiated task."},
    },
)
async def generate_vacation(
    r: GenerateVacationIdeaRequest, background_tasks: BackgroundTasks
) -> GenerateVacationIdeaResponse:
    """Initiates a vacation generation for you."""

    idea_id = uuid.uuid4()
    background_tasks.add_task(
        generate_vacation_idea_chain,
        idea_id,
        r.favorite_season,
        r.hobbies,
        r.budget,
    )
    return GenerateVacationIdeaResponse(id=idea_id, completed=False)


@vacation_router.get(
    "/{id}",
    summary="Get the generated a vacation idea.",
    responses={
        200: {"description": "Successfully fetched vacation."},
        404: {"description": "Vacation not found."},
    },
)
async def get_vacation(r: Request, id: uuid.UUID) -> GetVacationIdeaResponse:
    """Returns the vacation generation for you."""
    if id in vacations:
        vacay = vacations[id]
        return GetVacationIdeaResponse(
            id=vacay.id, completed=vacay.completed, idea=vacay.idea
        )
    raise HTTPException(status_code=404, detail="ID not found")
