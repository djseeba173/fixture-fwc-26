# Fixture Mundial 2026 - Design System

Version: 1.0

---

# Visión del producto

Fixture Mundial 2026 será una aplicación web inspirada visualmente en la identidad oficial de la FIFA World Cup 2026.

La experiencia debe transmitir:

- Mundial
- Álbum de figuritas
- Coleccionismo
- Colores vibrantes
- Geometría moderna
- Identidad latinoamericana
- Sensación de evento global

El diseño NO debe parecer una aplicación corporativa, administrativa o un dashboard empresarial tradicional.

Debe sentirse como una mezcla entre:

- FIFA World Cup 2026
- Panini World Cup Album
- FIFA.com
- FIFA Match Center

---

# Principios de diseño

## Colorido

La aplicación debe utilizar colores vivos y contrastantes.

Evitar:

- Azules corporativos oscuros predominantes
- Interfaces monocromáticas
- Apariencia tipo ERP

Buscar:

- Bloques de color
- Formas geométricas
- Secciones diferenciadas visualmente

---

## Geometría

Inspirarse en:

- Branding oficial FWC26
- Formas triangulares
- Círculos
- Diagonales
- Mosaicos geométricos

Utilizar elementos decorativos sutiles en:

- Hero principal
- Headers
- Fondos
- Tarjetas destacadas

Nunca interferir con la legibilidad.

---

## Coleccionismo

La presencia de:

- Escudos
- Equipos
- Estadios
- Grupos

debe sentirse como una colección visual.

---

# Assets

## Logo oficial

Ruta:

```text
media/logo_fwc26.png
```

Usos:

- Navbar
- Home
- Footer
- Login
- Favicon

---

## Escudos

Ruta:

```text
media/escudos_equipos_fwc26/
```

Usos:

- Fixture
- Tablas
- Bracket
- Equipo
- Partidos

Mostrar siempre que sea posible.

Los escudos son protagonistas visuales.

---

# Paleta oficial

## FWC Green

Nombre:

Average Green

```css
#3CAC3B
```

RGB

```text
60, 172, 59
```

Uso:

- Equipos clasificados
- CTA principales
- Estados positivos
- Elementos destacados

---

## FWC Blue

Nombre:

Hermes

```css
#2A398D
```

RGB

```text
42, 57, 141
```

Uso:

- Navegación
- Links
- Encabezados
- Elementos institucionales

---

## FWC Red

Nombre:

Torch Red

```css
#E61D25
```

RGB

```text
230, 29, 37
```

Uso:

- Resultados
- Destacados
- Partidos en vivo
- Alertas

---

## FWC Light

Nombre:

Light Gray

```css
#D1D4D1
```

Uso:

- Fondos
- Bordes
- Separadores

---

## FWC Dark

Nombre:

Dark Heather Grey

```css
#474A4A
```

Uso:

- Texto
- Íconos
- Bordes fuertes

---

# Variables CSS

```css
:root {

  --fwc-green: #3CAC3B;
  --fwc-blue: #2A398D;
  --fwc-red: #E61D25;

  --fwc-light: #D1D4D1;
  --fwc-dark: #474A4A;

  --fwc-white: #FFFFFF;
  --fwc-background: #F8F9FA;

}
```

---

# Tipografía

## Principal

Inter

```css
font-family:
Inter,
system-ui,
sans-serif;
```

Características:

- Moderna
- Clara
- Excelente en tablas

---

## Secundaria

Poppins

Para:

- Títulos
- Héroes
- Encabezados

---

# Layout general

## Navbar

Altura:

```css
72px
```

Fondo:

```css
var(--fwc-white)
```

Logo alineado a la izquierda.

Menú:

- Inicio
- Grupos
- Fixture
- Bracket
- Equipos
- Estadios

---

# Home

## Hero

Debe incluir:

- Logo FWC26
- Próximo partido
- Cuenta regresiva
- Acceso al bracket

Fondo:

Patrón geométrico inspirado en FIFA 2026.

No usar fotografías.

---

## Próximos partidos

Cards con:

- Escudo local
- Escudo visitante
- Fecha
- Hora
- Estadio

---

## Resultados recientes

Cards visuales con:

```text
ARG 2 - 1 BRA
```

---

# Componentes

## Card

```css
border-radius: 16px;
```

```css
background: white;
```

```css
box-shadow:
0 4px 12px rgba(0,0,0,.08);
```

---

## Botón principal

```css
background:
var(--fwc-green);
```

Hover:

```css
transform: translateY(-2px);
```

---

## Botón secundario

```css
background:
var(--fwc-blue);
```

---

# Grupos

Visualización tipo álbum.

Ejemplo:

```text
GRUPO A

🇦🇷 Argentina
🇲🇽 México
🇯🇵 Japón
🇳🇬 Nigeria
```

---

## Tabla de posiciones

Columnas:

```text
Pos
Equipo
PJ
PG
PE
PP
GF
GC
DG
PTS
```

Clasificados:

```css
border-left:
4px solid var(--fwc-green);
```

---

# Fixture

Cada partido debe mostrar:

```text
[Escudo] Argentina

2 - 1

Brasil [Escudo]
```

Debajo:

```text
MetLife Stadium
16 Jun 2026
20:00
```

---

# Página de partido

Mostrar:

- Escudos grandes
- Resultado
- Fecha
- Hora
- Estadio

Bloque central destacado.

---

# Bracket

Elemento visual más importante del sistema.

Inspiración:

Álbum Mundial 2026.

---

## Estructura

Columnas:

```text
16avos
Octavos
Cuartos
Semifinal
Final
```

---

## Match Card

Mostrar:

```text
[ARG] Argentina

2 - 1

Brasil [BRA]
```

---

## Ganador

```css
background:
var(--fwc-green);
```

Texto:

```css
color:
white;
```

---

## Pendiente

```css
background:
white;
```

---

## Eliminado

```css
opacity:
0.65;
```

---

# Estados

## Programado

```css
background:
var(--fwc-light);
```

---

## En vivo

```css
background:
var(--fwc-red);
color:
white;
```

Badge:

```text
LIVE
```

---

## Finalizado

```css
background:
var(--fwc-green);
color:
white;
```

---

# Decoración visual

Inspirarse en el branding oficial FIFA 2026:

- Círculos
- Diagonales
- Triángulos
- Cuadrículas

Utilizar SVG decorativos.

Nunca usar imágenes rasterizadas para fondos.

---

# Ilustraciones

Estilo:

- Vectorial
- Flat
- Geométrico

Similar a:

- FIFA 2026 Brand System
- Gráficas oficiales del torneo

---

# Responsive

## Mobile

Menor a 768px

- Scroll horizontal para bracket
- Cards apiladas
- Tablas con overflow

---

## Tablet

768px a 1200px

- Bracket simplificado
- Dos columnas

---

## Desktop

Mayor a 1200px

- Bracket completo
- Grupos visibles simultáneamente

---

# Accesibilidad

Cumplir WCAG AA.

Contraste mínimo:

```text
4.5:1
```

Nunca:

- Rojo sobre verde
- Gris claro sobre blanco

---

# Estilo visual objetivo

Palabras clave:

- FIFA 2026
- Mundial
- Álbum Panini
- Colorido
- Geométrico
- Coleccionable
- Moderno
- Deportivo
- Festivo
- Internacional

---

# Referencias visuales

Assets internos:

```text
media/logo_fwc26.png
media/escudos_equipos_fwc26/*
```

Inspiración:

- FIFA World Cup 2026 Branding
- FIFA Match Center
- Álbum Panini Mundial
- FIFA Tournament Bracket
- Official FIFA Tournament Graphics

---

# Regla principal

Si existe una duda de diseño:

Elegir siempre la opción que se parezca más a una experiencia oficial FIFA World Cup 2026 y menos a una aplicación administrativa tradicional.