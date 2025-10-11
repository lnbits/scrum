# the migration file is where you build your database tables
# If you create a new release for your extension ,
# remember the migration file is like a blockchain, never edit only add!

empty_dict: dict[str, str] = {}


async def m002_scrum(db):
    """
    Initial scrum table.
    """

    await db.execute(
        f"""
        CREATE TABLE scrum.scrum (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            wallet TEXT NOT NULL,
            public_assigning BOOLEAN,
            created_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )


async def m003_tasks(db):
    """
    Initial tasks table.
    """

    await db.execute(
        f"""
        CREATE TABLE scrum.tasks (
            id TEXT PRIMARY KEY,
            scrum_id TEXT NOT NULL,
            task TEXT NOT NULL,
            assignee TEXT,
            stage TEXT NOT NULL,
            reward INT,
            paid BOOLEAN,
            complete BOOLEAN,
            notes TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )
