This project does not have Alembic configured yet.

Manual migration SQL to add the new columns on `users` table:

ALTER TABLE users
  ADD COLUMN email_verified boolean DEFAULT false NOT NULL,
  ADD COLUMN reset_token varchar(255),
  ADD COLUMN reset_token_expires_at timestamptz;

Save the above SQL and apply it to your Postgres database (psql or via your ORM migration tool).

To use Alembic, run:

1. Install Alembic: `pip install alembic`
2. `alembic init alembic`
3. Edit `alembic/env.py` to import your models and use the project's DATABASE_URL
4. Create revision: `alembic revision --autogenerate -m "add email verification fields"`
5. Apply: `alembic upgrade head`
