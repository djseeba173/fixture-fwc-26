"""
Carga los resultados conocidos de la fase de grupos del Mundial 2026.
Busca los partidos por nombre de equipo (local vs visitante) y actualiza el marcador.

Uso:
    python manage.py seed_results           # aplica todos los resultados
    python manage.py seed_results --dry-run # muestra qué haría sin tocar la DB
"""
from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.matches.constants import MatchStatus
from apps.matches.models import Match
from apps.teams.models import Team

# (local, goles_local, goles_visitante, visitante)
RESULTS: list[tuple[str, int, int, str]] = [
    # ── Grupo A ──────────────────────────────────────────────
    ("México",          2, 0, "Sudáfrica"),
    ("Corea del Sur",   2, 1, "República Checa"),
    ("República Checa", 1, 1, "Sudáfrica"),
    ("México",          1, 0, "Corea del Sur"),
    # ── Grupo B ──────────────────────────────────────────────
    ("Canadá",          1, 1, "Bosnia y Herzegovina"),
    ("Catar",           1, 1, "Suiza"),
    ("Suiza",           4, 1, "Bosnia y Herzegovina"),
    ("Canadá",          6, 0, "Catar"),
    # ── Grupo C ──────────────────────────────────────────────
    ("Brasil",          1, 1, "Marruecos"),
    ("Haití",           0, 1, "Escocia"),
    ("Escocia",         0, 1, "Marruecos"),
    ("Brasil",          3, 0, "Haití"),
    # ── Grupo D ──────────────────────────────────────────────
    ("Estados Unidos",  4, 1, "Paraguay"),
    ("Australia",       2, 0, "Turquía"),
    ("Estados Unidos",  2, 0, "Australia"),
    ("Turquía",         0, 1, "Paraguay"),
    # ── Grupo E ──────────────────────────────────────────────
    ("Alemania",        7, 1, "Curazao"),
    ("Costa de Marfil", 1, 0, "Ecuador"),
    ("Alemania",        2, 1, "Costa de Marfil"),
    ("Ecuador",         0, 0, "Curazao"),
    # ── Grupo F ──────────────────────────────────────────────
    ("Países Bajos",    2, 2, "Japón"),
    ("Suecia",          5, 1, "Túnez"),
    ("Países Bajos",    5, 1, "Suecia"),
    ("Túnez",           0, 4, "Japón"),
    # ── Grupo G ──────────────────────────────────────────────
    ("Bélgica",         1, 1, "Egipto"),
    ("Irán",            2, 2, "Nueva Zelanda"),
    ("Bélgica",         0, 0, "Irán"),
    ("Nueva Zelanda",   1, 3, "Egipto"),
    # ── Grupo H ──────────────────────────────────────────────
    ("España",          0, 0, "Cabo Verde"),
    ("Arabia Saudita",  1, 1, "Uruguay"),
    ("España",          4, 0, "Arabia Saudita"),
    ("Uruguay",         2, 2, "Cabo Verde"),
    # ── Grupo I ──────────────────────────────────────────────
    ("Francia",         3, 1, "Senegal"),
    ("Irak",            1, 4, "Noruega"),
    ("Francia",         3, 0, "Irak"),
    # ── Grupo J ──────────────────────────────────────────────
    ("Argentina",       3, 0, "Argelia"),
    ("Austria",         3, 1, "Jordania"),
    ("Argentina",       2, 0, "Austria"),
    # ── Grupo K ──────────────────────────────────────────────
    ("Portugal",        1, 1, "República Democrática del Congo"),
    ("Uzbekistán",      1, 3, "Colombia"),
    # ── Grupo L ──────────────────────────────────────────────
    ("Inglaterra",      4, 2, "Croacia"),
    ("Ghana",           1, 0, "Panamá"),
]

# Aliases: nombre en español → posibles nombres en la DB (inglés/variantes)
TEAM_ALIASES: dict[str, list[str]] = {
    "México":                           ["Mexico", "México"],
    "Sudáfrica":                        ["South Africa", "Sudáfrica"],
    "Corea del Sur":                    ["South Korea", "Korea Republic", "Corea del Sur"],
    "República Checa":                  ["Czech Republic", "Czechia", "República Checa"],
    "Canadá":                           ["Canada", "Canadá"],
    "Bosnia y Herzegovina":             ["Bosnia and Herzegovina", "Bosnia-Herzegovina", "Bosnia & Herzegovina"],
    "Catar":                            ["Qatar", "Catar"],
    "Suiza":                            ["Switzerland", "Suiza"],
    "Brasil":                           ["Brazil", "Brasil"],
    "Marruecos":                        ["Morocco", "Marruecos"],
    "Escocia":                          ["Scotland", "Escocia"],
    "Haití":                            ["Haiti", "Haití"],
    "Estados Unidos":                   ["United States", "USA", "United States of America"],
    "Australia":                        ["Australia"],
    "Paraguay":                         ["Paraguay"],
    "Turquía":                          ["Turkey", "Türkiye", "Turquía"],
    "Alemania":                         ["Germany", "Alemania"],
    "Costa de Marfil":                  ["Ivory Coast", "Côte d'Ivoire", "Cote d'Ivoire", "Costa de Marfil"],
    "Ecuador":                          ["Ecuador"],
    "Curazao":                          ["Curaçao", "Curacao", "Curazao"],
    "Países Bajos":                     ["Netherlands", "Holland", "Países Bajos"],
    "Japón":                            ["Japan", "Japón"],
    "Suecia":                           ["Sweden", "Suecia"],
    "Túnez":                            ["Tunisia", "Túnez"],
    "Bélgica":                          ["Belgium", "Bélgica"],
    "Egipto":                           ["Egypt", "Egipto"],
    "Irán":                             ["Iran", "Irán"],
    "Nueva Zelanda":                    ["New Zealand", "Nueva Zelanda"],
    "España":                           ["Spain", "España"],
    "Uruguay":                          ["Uruguay"],
    "Cabo Verde":                       ["Cape Verde", "Cabo Verde"],
    "Arabia Saudita":                   ["Saudi Arabia", "Arabia Saudita"],
    "Francia":                          ["France", "Francia"],
    "Noruega":                          ["Norway", "Noruega"],
    "Senegal":                          ["Senegal"],
    "Irak":                             ["Iraq", "Irak"],
    "Argentina":                        ["Argentina"],
    "Austria":                          ["Austria"],
    "Jordania":                         ["Jordan", "Jordania"],
    "Argelia":                          ["Algeria", "Argelia"],
    "Colombia":                         ["Colombia"],
    "República Democrática del Congo":  ["DR Congo", "Democratic Republic of Congo", "Congo DR", "República Democrática del Congo"],
    "Portugal":                         ["Portugal"],
    "Uzbekistán":                       ["Uzbekistan", "Uzbekistán"],
    "Inglaterra":                       ["England", "Inglaterra"],
    "Ghana":                            ["Ghana"],
    "Panamá":                           ["Panama", "Panamá"],
    "Croacia":                          ["Croatia", "Croacia"],
}


class Command(BaseCommand):
    help = "Carga los resultados conocidos de la fase de grupos del Mundial 2026."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Muestra qué haría sin modificar la DB.")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        team_cache = self._build_team_cache()

        ok = skipped = errors = 0

        with transaction.atomic():
            for home_es, hs, aws, away_es in RESULTS:
                home = team_cache.get(home_es)
                away = team_cache.get(away_es)

                if not home:
                    self.stderr.write(f"  ⚠ Equipo no encontrado: {home_es!r}")
                    errors += 1
                    continue
                if not away:
                    self.stderr.write(f"  ⚠ Equipo no encontrado: {away_es!r}")
                    errors += 1
                    continue

                match = Match.objects.filter(home_team=home, away_team=away).first()
                if not match:
                    self.stderr.write(f"  ⚠ Partido no encontrado: {home.name} vs {away.name}")
                    errors += 1
                    continue

                if match.status == MatchStatus.FINISHED and not dry_run:
                    skipped += 1
                    continue

                label = f"{home.name} {hs}-{aws} {away.name}"
                if dry_run:
                    self.stdout.write(f"  → {label}")
                else:
                    match.home_score = hs
                    match.away_score = aws
                    match.status = MatchStatus.FINISHED
                    match.save()
                    self.stdout.write(self.style.SUCCESS(f"  ✓ {label}"))
                ok += 1

            if dry_run:
                transaction.set_rollback(True)

        suffix = " (dry-run)" if dry_run else ""
        self.stdout.write(f"\nResultado{suffix}: {ok} actualizados · {skipped} ya cargados · {errors} errores")

    def _build_team_cache(self) -> dict[str, Team | None]:
        all_teams = {t.name: t for t in Team.objects.all()}
        cache: dict[str, Team | None] = {}
        for es_name, candidates in TEAM_ALIASES.items():
            found = None
            for candidate in candidates:
                if candidate in all_teams:
                    found = all_teams[candidate]
                    break
            if not found:
                # fallback: icontains con el primer candidato
                for candidate in candidates:
                    qs = Team.objects.filter(name__icontains=candidate.split()[0])
                    if qs.count() == 1:
                        found = qs.first()
                        break
            cache[es_name] = found
        return cache
