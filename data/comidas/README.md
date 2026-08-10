# Registro de comidas

Un archivo JSON por día: `AAAA-MM-DD.json`.

Cada comida se estima a partir de la foto que envías — alimento identificado, porción aproximada, calorías y macros. Las estimaciones incluyen un nivel de confianza: cuando es baja, te pregunto en lugar de adivinar.

```json
{
  "fecha": "2026-08-11",
  "comidas": [
    {
      "momento": "desayuno",
      "hora": "07:30",
      "items": [
        { "alimento": "huevos revueltos", "porcion_g": 150, "kcal": 220, "proteina_g": 19, "carbs_g": 2, "grasa_g": 15 }
      ],
      "confianza": "alta",
      "origen": "foto"
    }
  ],
  "totales": { "kcal": 220, "proteina_g": 19, "carbs_g": 2, "grasa_g": 15 },
  "objetivo": { "kcal": null, "proteina_g": null },
  "notas": ""
}
```

La estimación por foto tiene un margen de error real (±15–20 % es normal). No importa tanto como parece: el ajuste semanal corrige la desviación acumulada usando la tendencia de peso, que es un dato objetivo. Lo que sí importa es **registrar todos los días**, incluidos los malos — un día sin registrar es información perdida, no un día que no contó.
