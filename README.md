# dragon-mania-mods

Repositorio de actualizaciones para el APK con actualizador. El juego lee `manifest.json` al iniciar y descarga los mods nuevos (se aplican en el siguiente arranque).

## Estructura
```
src/<id>/mod.json      definición del mod
src/<id>/assets/...    archivos que reemplazan los del juego (misma ruta)
src/<id>/classes.dex   (opcional) código; requiere "entrypoint" en mod.json
tools/build.py         empaqueta y genera manifest.json
mods/, manifest.json   generados automáticamente, no editar
```

## Añadir o actualizar contenido
1. Crea/edita `src/<id>/` (nombre solo con letras, números, `-` y `_`).
2. **Sube `version` en `mod.json`**: si no cambia, los teléfonos no descargan nada.
3. `git push` a `main`. GitHub Actions regenera `mods/` y `manifest.json`.

## mod.json
| campo | descripción |
|---|---|
| id, name, version | identificación |
| priority | mayor número gana si dos mods tocan el mismo archivo |
| enabled | `false` lo desactiva |
| entrypoint | clase `DragonMod` (solo mods con código) |
| dependencies | lista de ids requeridos |

## Seguridad
Un mod con `classes.dex` ejecuta código en cada teléfono. Activa 2FA en tu cuenta y no aceptes PRs sin revisar.
