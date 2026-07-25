# Odoo 19 — entorno de desarrollo con Docker

## Preparación

1. Copia `.env.example` como `.env`.
2. Cambia las contraseñas de `.env` y `config/odoo.conf`.
3. Abre PowerShell en esta carpeta.
4. Ejecuta:

```powershell
docker compose pull
docker compose up -d
docker compose ps
```

5. Abre http://localhost:8069
6. Crea la base `odoo_dev`.

## Crear un módulo

```powershell
docker compose run --rm odoo odoo scaffold autonomo_core /mnt/extra-addons
```

## Ver registros

```powershell
docker compose logs -f odoo
```

## Reiniciar Odoo

```powershell
docker compose restart odoo
```

## Detener sin borrar datos

```powershell
docker compose down
```

## Volver a iniciar

```powershell
docker compose up -d
```

## AVISO

No ejecutes `docker compose down -v` salvo que quieras borrar la base de datos
y el filestore de este entorno de desarrollo.
