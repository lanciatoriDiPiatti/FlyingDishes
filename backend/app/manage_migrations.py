
import argparse
from pathlib import Path
import sys

# Project root
root_dir = Path(__file__).parent
alembic_dir = root_dir / "backend" / "alembic"
alembic_ini_path = root_dir / "alembic.ini"


def main():
    """Main function to handle migration commands."""
    # This is a workaround to make the app module findable by python
    # In a real-world scenario, you would have a proper package structure
    sys.path.insert(0, str(root_dir / 'backend'))

    from app.db.session import engine
    from app.db.schema_manager import SchemaManager

    parser = argparse.ArgumentParser(description="Manage database migrations.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize Alembic.")
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-initialization, deleting existing configuration.",
    )

    # Revision command
    revision_parser = subparsers.add_parser(
        "revision", help="Create a new revision file."
    )
    revision_parser.add_argument(
        "-m", "--message", type=str, required=True, help="Revision message."
    )

    # Upgrade command
    upgrade_parser = subparsers.add_parser("upgrade", help="Upgrade to a revision.")
    upgrade_parser.add_argument(
        "revision",
        type=str,
        nargs="?",
        default="head",
        help="The revision to upgrade to.",
    )

    args = parser.parse_args()

    manager = SchemaManager(
        engine=engine, alembic_dir=alembic_dir, alembic_ini_path=alembic_ini_path
    )

    if args.command == "init":
        manager.ensure_alembic_setup(force=args.force)
        print("Alembic has been initialized.")
        print("Please check the generated files and customize if needed.")
        print("You can now generate an initial revision with:")
        print('python manage_migrations.py revision -m "Initial migration"')

    elif args.command == "revision":
        manager.generate_revision(message=args.message)

    elif args.command == "upgrade":
        manager.upgrade_schema(revision=args.revision)


if __name__ == "__main__":
    main()
