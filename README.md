
# Tixstern

**Book the moment. Own the experience.**

Tixstern is a backend-focused concert ticketing platform designed to demonstrate concurrency-safe ticket reservations, reliable booking workflows, and measurable read-performance improvements through caching.

## Planned Technology Stack

- Backend: Python, FastAPI, SQLAlchemy 2.x
- Database: PostgreSQL
- Caching: Redis
- Migrations: Alembic
- Frontend: React, TypeScript, Vite, Tailwind CSS
- Testing: pytest, HTTPX, and Locust or k6
- Development: Git, GitHub, Docker Compose

## Project Status

Currently in Phase 0: project setup.

## Core Engineering Goals

1. Prevent overselling through concurrency-safe inventory allocation.
2. Improve suitable event-read performance through Redis caching.
3. Implement reliable reservations, expiry, and idempotent operations.
4. Verify behavior through automated tests and reproducible benchmarks.

Payments will be simulated in the initial version.
