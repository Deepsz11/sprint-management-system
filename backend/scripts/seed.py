"""CLI entrypoint for seeding the database."""

from __future__ import annotations

import argparse

from app.core.logging import configure_logging, get_logger
from app.infrastructure.seed import (
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ORG_SLUG,
    seed_default_data,
)


def main() -> None:
    """Seed default data via the command line."""
    configure_logging()
    logger = get_logger("scripts.seed")

    parser = argparse.ArgumentParser(description="Seed default Sprint Outcome Tracer data.")
    parser.add_argument("--email", default=DEFAULT_ADMIN_EMAIL, help="Admin email")
    parser.add_argument(
        "--password", default=DEFAULT_ADMIN_PASSWORD, help="Admin password"
    )
    parser.add_argument("--slug", default=DEFAULT_ORG_SLUG, help="Organization slug")
    args = parser.parse_args()

    seed_default_data(
        admin_email=args.email,
        admin_password=args.password,
        organization_slug=args.slug,
    )
    logger.info("Seed complete.")


if __name__ == "__main__":
    main()