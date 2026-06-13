PROMPT PARA CODEX

Quiero construir una aplicación web completa para administrar y visualizar el Mundial 2026.

Contexto

En este repositorio existe información oficial del Mundial 2026 en archivos JSON:

worldcup.json
worldcup.groups.json
worldcup.teams.json
worldcup.stadiums.json
worldcup.squads.json
worldcup.quali_playoffs.json

La aplicación debe utilizar estos archivos como fuente de datos inicial.

El objetivo es recrear una experiencia similar a un fixture físico de Mundial (álbum o revista deportiva), pero totalmente interactiva y actualizable.

Stack tecnológico

Backend:

Python 3.12+
Django 5
SQLite para desarrollo
Preparado para PostgreSQL en producción

Frontend:

Django Templates
HTMX
Bootstrap 5

Testing:

pytest
pytest-django
Objetivo funcional

La aplicación debe permitir:

Visualizar grupos.
Visualizar partidos.
Ver tablas de posiciones.
Cargar resultados.
Recalcular posiciones automáticamente.
Completar automáticamente los cruces eliminatorios.
Avanzar automáticamente los ganadores.
Mostrar un bracket visual completo.
Mostrar fechas, horarios y estadios.
Administrar todo desde Django Admin.
Estructura del proyecto

Crear una estructura limpia:

project/
├── apps/
│   ├── tournaments/
│   ├── teams/
│   ├── matches/
│   ├── standings/
│   ├── brackets/
│   └── core/
│
├── services/
├── selectors/
├── management/
├── templates/
├── static/
└── tests/
Modelos
Tournament
name
year
slug
start_date
end_date
Team
name
code
fifa_code
flag_url
confederation
Group
tournament
name

Ejemplos:

A
B
C
...
L
GroupMembership
group
team
Stadium
name
city
country
capacity
Match
tournament
match_number
phase
group
stadium

date_time

home_team
away_team

home_score
away_score

extra_time_home_score
extra_time_away_score

penalty_home_score
penalty_away_score

status

status:

scheduled
live
finished
Standing
group
team

played
wins
draws
losses

goals_for
goals_against

goal_difference

points
KnockoutMatch
match_number

phase

home_source
away_source

home_team
away_team

home_score
away_score

next_match
next_slot
Fases

Utilizar enum:

GROUP
ROUND_OF_32
ROUND_OF_16
QUARTER_FINAL
SEMI_FINAL
THIRD_PLACE
FINAL
Importación de datos

Crear comando:

python manage.py import_worldcup_data

Debe:

Leer automáticamente todos los JSON existentes.
Crear equipos.
Crear grupos.
Crear estadios.
Crear partidos.
Crear relaciones.

Debe ser idempotente.

Si se ejecuta varias veces:

python manage.py import_worldcup_data

no debe duplicar datos.

Cálculo de tablas

Implementar servicio:

recalculate_group_standings(group)

Reglas:

Victoria:

3 puntos

Empate:

1 punto

Derrota:

0 puntos

Desempate:

Puntos
Diferencia de gol
Goles a favor
Clasificación automática

Cuando termina un partido:

Match.save()

debe ejecutarse:

recalculate_group_standings()

Luego:

update_group_qualifications()
Eliminación directa

La fase eliminatoria debe generarse automáticamente.

Ejemplos:

1A vs 2B
1C vs 2D
...

o según la estructura real definida en los JSON.

No hardcodear.

La lógica debe leer la estructura desde datos.

Avance automático

Cuando un partido eliminatorio finaliza:

advance_winner(match)

Debe:

Detectar ganador.
Buscar el siguiente partido.
Completar automáticamente el slot correspondiente.
Actualizar el bracket.
Bracket visual

Crear página:

/bracket/

Mostrar:

16avos
Octavos
Cuartos
Semifinales
Final

Visualmente similar a un fixture de Mundial.

Utilizar Bootstrap.

Diseño responsive.

Debe funcionar en:

Desktop
Tablet
Mobile
Vistas
Inicio
/

Mostrar:

Próximos partidos
Últimos resultados
Grupos
Acceso al bracket
Grupos
/groups/
Grupo individual
/groups/A/

Mostrar:

Equipos
Tabla
Partidos
Fixture
/fixtures/

Mostrar todos los partidos ordenados por fecha.

Partido
/matches/<id>/

Mostrar:

Equipos
Resultado
Estadio
Fecha
Estado
Bracket
/bracket/
Panel administrativo

Configurar Django Admin para:

Equipos
Grupos
Estadios
Partidos
Resultados

Permitir edición rápida.

API REST

Instalar Django REST Framework.

Endpoints:

GET /api/groups/
GET /api/teams/
GET /api/matches/
GET /api/standings/
GET /api/bracket/

Endpoint para cargar resultado:

POST /api/matches/<id>/result/
HTMX

Al guardar un resultado:

actualizar tabla del grupo
actualizar posiciones
actualizar cruces

sin recargar toda la página.

Tests

Crear tests para:

importación
cálculo de tablas
desempates
clasificación
avance de cruces
API

Cobertura mínima:

80%
Calidad de código

Aplicar:

type hints
docstrings
services
selectors
principios SOLID
consultas optimizadas
select_related
prefetch_related
Entregables

Generar:

Proyecto Django completo.
Migraciones.
Modelos.
Servicios.
Templates Bootstrap.
HTMX.
API REST.
Tests.
Comando de importación de los JSON existentes.
README con instrucciones de instalación y ejecución.

Antes de implementar, inspeccioná la estructura real de los JSON del repositorio y adaptá los modelos e importadores para que coincidan exactamente con los datos disponibles. No asumir esquemas; analizarlos primero y luego generar el código.