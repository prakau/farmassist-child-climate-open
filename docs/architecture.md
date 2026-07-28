# Architecture

The PWA validates and stores approved observations locally. The API persists unique UUID records in SQLite and invokes the same deterministic risk package. Public output is a whole-dataset aggregate with no record-level fields. Boundaries deliberately exclude identity, health, contact, exact location, and child data. Production deployments require authenticated roles, encryption, audit logs, backup/restore, deployment review, and a stronger database.
