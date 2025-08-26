# Migrations

## Adding Migrations

To add a new migration, use the following command:

```bash
alembic revision --autogenerate -m "Your migration message"
```

This will create a new migration script in the `migrations/versions` directory.

## Applying Migrations

To apply the latest migrations to your database, run:

```bash
alembic upgrade head
```

This will apply all pending migrations to bring your database schema up to date.

## Downgrading Migrations

To revert to a previous migration, use the following command:

```bash
alembic downgrade <revision>
```

Replace `<revision>` with the specific revision ID you want to downgrade to. You can also use `-1` to revert the last migration.
