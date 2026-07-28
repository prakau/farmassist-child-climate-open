# Deployment guide

For local evaluation use `make install`, `make test`, and `make run`; for containers use `docker compose up --build`. Never expose this alpha API publicly: it lacks authentication, authorization, encrypted browser storage, rate limiting, audit logging, managed secrets, backup/restore, and production hardening.

Before a supervised pilot, complete safeguarding and privacy reviews, use TLS, authenticated least-privilege roles, managed secrets, encrypted storage/backups, retention/deletion jobs, monitoring, incident response, dependency review, recovery tests, and institutional approval. Pin and scan production images and document responsible operators.
