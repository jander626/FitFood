#!/usr/bin/env python3
"""Genera dashboard/_data.js a partir de data/*.json y data/comidas/*.json.
Ejecutar antes de republicar el dashboard cada vez que haya datos nuevos.
"""
import json, glob, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(path):
    with open(os.path.join(BASE, path)) as f:
        return json.load(f)

perfil = load('data/perfil.json')
peso = load('data/peso.json')
medidas = load('data/medidas.json')
entrenos = load('data/entrenos.json')

kcal_obj = perfil['calculado']['kcal_objetivo']
tdee = perfil['calculado']['tdee_kcal']
obj_macros = {
    'proteina': perfil['calculado']['proteina_g'],
    'carbs': perfil['calculado']['carbohidratos_g'],
    'grasa': perfil['calculado']['grasa_g'],
}

# --- días con comida: sólo días de plan real (excluye día 0 / pre-plan) ---
dias = []
for path in sorted(glob.glob(os.path.join(BASE, 'data/comidas/*.json'))):
    d = load(f'data/comidas/{os.path.basename(path)}')
    if not isinstance(d.get('dia_plan'), int):
        continue  # se salta el pre-plan (11 ago)
    peso_dia = next((p['kg'] for p in peso['registros'] if p['fecha'] == d['fecha']), None)
    entreno_dia = [e for e in entrenos['registros'] if e['fecha'] == d['fecha']]
    dias.append({
        'fecha': d['fecha'],
        'dia_plan': d['dia_plan'],
        'kcal': d['totales']['kcal'],
        'proteina': d['totales']['proteina_g'],
        'carbs': d['totales']['carbs_g'],
        'grasa': d['totales']['grasa_g'],
        'gasto_estimado': tdee,
        'deficit_real': round(tdee - d['totales']['kcal'], 1),
        'peso': peso_dia,
        'entreno': bool(entreno_dia),
        'comidas': [
            {
                'momento': c['momento'],
                'items': [i['alimento'] for i in c['items']],
                'kcal': c['subtotal']['kcal'],
                'proteina': c['subtotal']['proteina_g'],
            }
            for c in d['comidas']
        ],
    })

out = {
    'objetivo': {'kcal': kcal_obj, 'tdee': tdee, **obj_macros},
    'dias': dias,
}

# Incrusta los datos directamente en dashboard/index.html (el publicador de
# Artifacts solo sirve un archivo, no puede cargar un <script src="..."> aparte).
data_json = json.dumps(out, indent=2, ensure_ascii=False)
new_tag = f'<script id="fitfood-data">window.FITFOOD_DATA = {data_json};</script>'

html_path = os.path.join(BASE, 'dashboard/index.html')
html = open(html_path).read()
html2 = re.sub(
    r'<script id="fitfood-data">.*?</script>',
    lambda m: new_tag,
    html,
    count=1,
    flags=re.DOTALL,
)
if html2 == html:
    raise SystemExit('No se encontró el tag <script id="fitfood-data"> en dashboard/index.html')
open(html_path, 'w').write(html2)

print(f"OK: {len(dias)} dias incrustados en dashboard/index.html")
