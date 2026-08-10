# Integraciones: Freeletics, Garmin y Strava

Qué se puede automatizar, qué no, y cómo conectarlo.

## Resumen honesto

**No hay forma de conectarme directamente a Freeletics.** No tienen API pública — solo una interna, no documentada, que la comunidad ha aplicado ingeniería inversa ([freeletics-python](https://github.com/mkb79/freeletics-python)) y que no es una base confiable para esto. Tampoco existe un conector de Freeletics para Claude; lo verifiqué en el registro de conectores.

Pero Freeletics [sincroniza con Strava](https://www.freeletics.com/en/blog/posts/connect-strava-with-freeletics/), tu Garmin también, **y sí existe un conector de Strava para Claude**. Ese es el puente: un solo conector me da tanto tus sesiones de Freeletics como tus carreras del Garmin, de forma automática.

| Vía | Qué me da | Esfuerzo tuyo |
|-----|-----------|---------------|
| **Strava** | Qué entrenaste, cuándo, duración, frecuencia cardíaca, calorías estimadas | Configurar una vez |
| Reporte por chat | Series, repeticiones y kilos — el detalle que Strava no captura | 1 min tras entrenar fuerza |
| Export de Freeletics | Histórico completo de tus sesiones | Manual, cada varias semanas |

Usamos las dos primeras. La tercera queda por si algún día queremos el histórico completo.

---

## Configuración (una sola vez)

### 1. Freeletics → Strava

En la app de Freeletics: **Ajustes → Conexiones → activar Strava**, y autorizas.

⚠️ **Hazlo antes del Día 1.** La sincronización solo sube las actividades **desde el momento en que la activas**; lo anterior no se recupera. Como empezamos ahora, no perdemos nada — pero si lo activas en la semana 3, esas tres semanas no existirán para el análisis.

### 2. Garmin → Strava

En **Garmin Connect → Ajustes → Apps conectadas → Strava**. Tus carreras y caminatas suben solas.

### 3. Strava → Claude

Desde la configuración de conectores en claude.ai, conectas **Strava** y habilitas el conector en este chat. A partir de ahí leo tus actividades en cada check-in semanal sin que tengas que mandarme nada.

---

## Evitar duplicados

Si Garmin y Freeletics envían la misma sesión a Strava, aparece dos veces y las calorías se cuentan doble — lo que arruinaría el análisis semanal.

La regla: **una sola fuente por tipo de actividad.**

| Tipo de actividad | Fuente |
|-------------------|--------|
| Sesiones de Freeletics | Freeletics |
| Carreras y caminatas | Garmin |
| Fuerza en el gimnasio | Garmin (o registro manual por chat) |

Si usas el reloj Garmin para cronometrar una sesión de Freeletics, aparecerá duplicada. En ese caso: no inicies actividad en el reloj durante Freeletics, o borra el duplicado en Strava.

---

## Lo que Strava no me va a dar

Strava registra una sesión de fuerza como un bloque de tiempo con frecuencia cardíaca. **No sabe qué ejercicios hiciste ni cuánto peso levantaste.**

Eso importa porque el dato más valioso de estos 90 días es la progresión de tus cargas: si en un déficit calórico sigues subiendo kilos en la sentadilla, estás perdiendo grasa y conservando músculo — exactamente lo que buscas. Si las cargas se desploman, algo está mal (déficit muy agresivo, poco sueño, poca proteína) y hay que corregir antes de perder músculo.

Por eso, los días de fuerza mándame una línea rápida por chat. Algo así basta:

```
Fuerza A. Dominadas 4x6. Banca 40kg 4x8. Remo 40kg 4x10.
Militar 10kg 3x12. Laterales 5kg 3x15.
```

Los días de Freeletics no hace falta que escribas nada: eso llega solo por Strava.

---

## Export de Freeletics (opcional)

Si algún día quieres que analice tu histórico completo: **Perfil → icono de ajustes → Privacidad → Exportar datos**. Freeletics te envía el archivo y me lo pasas.

Útil sobre todo al inicio, para ver tu volumen y frecuencia de los últimos meses y calibrar mejor el punto de partida.
