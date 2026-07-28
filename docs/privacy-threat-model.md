# Privacy threat model

| Threat | Prototype control | Residual work before pilot |
|---|---|---|
| Identity entered in notes | Short field and obvious-term rejection | Remove free text or deploy robust review |
| Site re-identification | Non-identifying demo codes; no coordinates | Site-code key isolation and small-cell suppression |
| Lost/shared device | No sensitive data permitted | Device encryption, authentication, remote revocation |
| Queue interception | Local-only queue; HTTPS expected | Encrypted storage and managed TLS |
| Unauthorized API access | Demonstration API contains synthetic data | Authentication, authorization, audit logging |
| Inference from aggregates | Whole-dataset counts only | Minimum cohorts, release review, differential privacy assessment |

The browser queue is inspectable by anyone with device access. It must never contain personal or child data.
