# API reference

Interactive OpenAPI is at `/docs`; machine-readable OpenAPI is at `/openapi.json`.

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness and version |
| POST/GET | `/v1/observations` | Validate/store or list environmental records |
| POST | `/v1/risk/assess` | Explain reference risk without storage |
| GET | `/v1/sites/{site_code}/summary` | Latest non-identifying site context |
| GET | `/v1/public/indicators` | Aggregate-only public output |
| GET | `/v1/config/risk-thresholds` | Inspect model configuration |

Duplicate observation UUIDs return HTTP 409. Validation errors return 422. This alpha has no authentication and is suitable only for synthetic local demonstrations.
