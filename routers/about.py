from fastapi import APIRouter, Request

from utils.template_renderer import render_template
from constants.team import TEAM_MEMBERS

router = APIRouter()


@router.get("/about")
async def serve_about(request: Request):

    return render_template(
        "about.html",
        request,
        members=TEAM_MEMBERS,
        title="About Us"
    )