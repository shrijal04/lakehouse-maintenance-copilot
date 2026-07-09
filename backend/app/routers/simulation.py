from fastapi import APIRouter

from simulation.runner import run_occ_simulation

router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"]
)


@router.post("/start")
def start_simulation():

    return run_occ_simulation()