#!/usr/bin/env python3
"""Genera coaching/tabla-alimentos.md e incrusta el buscador en dashboard/index.html
a partir de data/tabla_alimentos.json. Ejecutar cada vez que se agregue un alimento."""
import json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(BASE, 'data/tabla_alimentos.json')))
alimentos = data['alimentos']

# --- Orden y agrupación por categoría ---
orden_cat = ["Proteina animal", "Huevos y lacteos", "Carbohidrato / tuberculo",
             "Legumbre", "Verdura", "Fruta", "Grasa", "Dulce / bebida"]
por_cat = {c: [] for c in orden_cat}
for a in alimentos:
    por_cat[a['categoria']].append(a)
for c in por_cat:
    por_cat[c].sort(key=lambda a: a['nombre'])

titulo_cat = {
    "Proteina animal": "Proteínas animales",
    "Huevos y lacteos": "Huevos y lácteos",
    "Carbohidrato / tuberculo": "Carbohidratos y tubérculos",
    "Legumbre": "Legumbres",
    "Verdura": "Verduras",
    "Fruta": "Frutas",
    "Grasa": "Grasas y untables",
    "Dulce / bebida": "Dulces, salsas y bebidas",
}

# --- Markdown ---
md = ["# Tabla de alimentos\n",
      "Valores por **100 g/ml de porción comestible**, cocida salvo que se indique. "
      "La columna «porción típica» te da el número ya calculado para una cantidad real, "
      "así no tienes que hacer la regla de tres cada vez.\n",
      "> Estimaciones de referencia (tablas de composición nutricional estándar). "
      "Sirven para decidir sobre la marcha; para el registro diario preciso, sigue mandando fotos.\n"]

for cat in orden_cat:
    items = por_cat[cat]
    if not items:
        continue
    md.append(f"## {titulo_cat[cat]}\n")
    md.append("| Alimento | kcal/100g | Proteína | Carbos | Grasa | Porción típica |")
    md.append("|---|---|---|---|---|---|")
    for a in items:
        f = a['porcion_g'] / 100
        pk, pp, pc, pg = (round(a['kcal100']*f), round(a['p100']*f,1), round(a['c100']*f,1), round(a['g100']*f,1))
        md.append(f"| {a['nombre']} | {a['kcal100']} | {a['p100']} g | {a['c100']} g | {a['g100']} g | "
                   f"{a['porcion_nota']} ({a['porcion_g']}g): **{pk} kcal**, {pp}g P, {pc}g C, {pg}g G |")
    md.append("")

md.append("---\n")
md.append("## Cómo leer esta tabla en tu día a día\n")
md.append("- **¿Cuál proteína me conviene más?** Compara kcal/100g entre las fuentes: "
          "pechuga de pollo (165) y atún (116) rinden mucho más proteína por caloría que "
          "chicharrón (520) o tocineta (541). No los elimines — solo sabes cuánto te cuestan.")
md.append("- **¿Me cabe este carbohidrato?** Mira la columna de porción típica y compárala con "
          "lo que te queda del día (te lo digo cuando registras tus comidas).")
md.append("- **¿No encuentras un alimento?** Mándamelo por chat y te doy el estimado — y lo agrego "
          "aquí para la próxima vez.")

with open(os.path.join(BASE, 'coaching/tabla-alimentos.md'), 'w') as f:
    f.write('\n'.join(md) + '\n')

# --- Incrustar en el dashboard como buscador ---
food_json = json.dumps(alimentos, ensure_ascii=False)
new_tag = f'<script id="food-table-data">window.FOOD_TABLE = {food_json};</script>'
html_path = os.path.join(BASE, 'dashboard/index.html')
html = open(html_path).read()
if '<script id="food-table-data">' in html:
    html2 = re.sub(r'<script id="food-table-data">.*?</script>', lambda m: new_tag, html, count=1, flags=re.DOTALL)
else:
    html2 = html.replace('<script id="fitfood-data">',
                          new_tag + '\n<script id="fitfood-data">', 1)
if html2 == html:
    raise SystemExit('No se pudo incrustar la tabla de alimentos en dashboard/index.html')
open(html_path, 'w').write(html2)

print(f"OK: {len(alimentos)} alimentos -> coaching/tabla-alimentos.md y dashboard/index.html")
