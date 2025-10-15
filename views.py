# Description: Add your page endpoints here.

import json
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.helpers import template_renderer
from lnbits.settings import settings

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
            "public_page_tasks_creation": scrum.public_tasks,
            "public_page_delete_tasks": scrum.public_delete_tasks,
            "web_manifest": f"/scrum/manifest/{scrum_id}.webmanifest",
        },
    )


@scrum_generic_router.get("/manifest/{scrum_id}.webmanifest")
async def manifest(scrum_id: str):
    scrum = await get_scrum_by_id(scrum_id)
    if not scrum:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Scrum does not exist.")

    return {
        "short_name": "Scrum " + scrum.name,
        "name": "Scrum " + scrum.name + " - " + scrum.description,
        "icons": [
            {
                "src": (
                    settings.lnbits_custom_logo
                    if settings.lnbits_custom_logo
                    else "https://cdn.jsdelivr.net/gh/lnbits/lnbits@0.3.0/docs/logos/lnbits.png"
                ),
                "type": "image/png",
                "sizes": "900x900",
            }
        ],
        "start_url": "/scrum/" + scrum_id,
        "background_color": "#1F2234",
        "description": "Bitcoin Lightning Scrum",
        "display": "standalone",
        "scope": "/scrum/" + scrum_id,
        "theme_color": "#1F2234",
        "shortcuts": [
            {
                "name": "Scrum " + scrum.name + " - " + settings.lnbits_site_title,
                "short_name": "Scrum " + scrum.name,
                "description": "Scrum " + scrum.description + " - " + settings.lnbits_site_title,
                "url": "/scrum/" + scrum_id,
            }
        ],
    }
