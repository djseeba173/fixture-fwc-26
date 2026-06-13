from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()

TEAM_ALIASES = {
    "Algeria": "argelia",
    "Belgium": "belgica",
    "Bosnia & Herzegovina": "bosnia",
    "Brazil": "brasil",
    "Croatia": "croacia",
    "Curaçao": "curazao",
    "DR Congo": "congo",
    "Egypt": "egipto",
    "England": "inglaterra",
    "France": "francia",
    "Germany": "alemania",
    "Iraq": "irak",
    "Japan": "japon",
    "Morocco": "marruecos",
    "Norway": "noruega",
    "Scotland": "escocia",
    "Spain": "espana",
    "Sweden": "suecia",
    "Switzerland": "suiza",
    "Czech Republic": "republicacheca",
    "South Africa": "sudafrica",
    "South Korea": "coreadelsur",
    "Tunisia": "tunez",
    "Turkey": "turquia",
    "United States": "usa",
    "USA": "usa",
    "Saudi Arabia": "arabiasaudita",
    "Cape Verde": "cabo_verde",
    "Côte d'Ivoire": "costa_de_marfil",
    "Ivory Coast": "costa_de_marfil",
    "New Zealand": "nuevazelanda",
    "Netherlands": "paisesbajos",
}


@register.simple_tag
def team_crest(team_or_name: object | None) -> str:
    name = getattr(team_or_name, "name", None) or str(team_or_name or "")
    slug = TEAM_ALIASES.get(name, _slugify_name(name))
    crest_path = Path(settings.BASE_DIR) / "static" / "img" / "escudos_equipos_fwc26" / f"{slug}.png"
    if crest_path.exists():
        return static(f"img/escudos_equipos_fwc26/{slug}.png")
    return static("img/crest-placeholder.svg")


@register.simple_tag
def team_label(team_or_name: object | None, fallback: str = "") -> str:
    return getattr(team_or_name, "name", None) or fallback or str(team_or_name or "")


def _slugify_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower().replace("&", " ")
    return re.sub(r"[^a-z0-9]+", "", normalized)
