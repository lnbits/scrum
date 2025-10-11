# Description: Add your page endpoints here.

import json
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.helpers import template_renderer

from .crud import get_scrum_by_id, get_tasks_paginated

scrum_generic_router = APIRouter()


def scrum_renderer():
    return template_renderer(["scrum/templates"])


#######################################
##### ADD YOUR PAGE ENDPOINTS HERE ####
#######################################


# Backend admin page


@scrum_generic_router.get("/", response_class=HTMLResponse)
async def index(req: Request, user: User = Depends(check_user_exists)):
    return scrum_renderer().TemplateResponse("scrum/index.html", {"request": req, "user": user.json()})


# Frontend shareable page


@scrum_generic_router.get("/{scrum_id}")
async def scrum_public_page(req: Request, scrum_id: str):
    scrum = await get_scrum_by_id(scrum_id)
    if not scrum:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Scrum does not exist.")

    public_page_name = getattr(scrum, "name", "")
    public_page_description = getattr(scrum, "description", "")
    page = await get_tasks_paginated(scrum_ids=[scrum_id])
    payload = jsonable_encoder(page.data)
    public_page_tasks_json = json.dumps(payload)

    return scrum_renderer().TemplateResponse(
        "scrum/public_page.html",
        {
            "request": req,
            "scrum_id": scrum_id,
            "public_page_name": public_page_name,
            "public_page_description": public_page_description,
            "public_page_tasks": public_page_tasks_json,
            "public_page_assigning": scrum.public_assigning,
        },
    )
