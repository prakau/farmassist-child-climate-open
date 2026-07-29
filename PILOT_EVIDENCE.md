# Prototype and field-work evidence

This document separates work already completed by JOITA BIOSEED AI PRIVATE LIMITED from the proposed UNICEF-specific child-climate and nutrition module. It is deliberately limited to evidence the company can presently support.

## Completed foundation

- An offline-first FarmAssist test build and agronomic advisory workflows.
- Programmer-led software development covering APIs, model testing, documentation, and version control.
- Field-research workflows at three farmer locations covering approximately 25 acres in Haryana.
- Structured crop-stage observations and field photographs within those research workflows.
- Laboratory and field-validation capacity relevant to proposed future evaluation.
- AgriTrust edge-hardware concepts and related industrial-design applications.
- The functional open-source reference prototype in this repository: FastAPI service, deterministic risk engine, installable dashboard, offline queue, synthetic generator, automated tests, schemas, governance, and safeguarding documentation.

## What the current software demonstration proves

The repository and demonstration show that non-personal environmental observations can be schema-validated, assessed locally against transparent thresholds, retained in an approved offline queue, synchronized when connectivity returns, and reduced to non-identifying public indicators.

The included demonstration records use the non-identifying codes `DEMO-001`, `DEMO-002`, and `DEMO-003` and are entirely synthetic. They demonstrate software behavior, not agronomic performance or field impact.

## Evidence boundary

The Haryana field-research workflows were not UNICEF school-garden pilots and did not validate this child-climate module. No active school deployment, formal implementation partner, UNICEF relationship, model-accuracy result, sensor-accuracy result, yield improvement, nutrition outcome, child-health outcome, or causal impact is claimed.

The current risk engine is a deterministic reference model. Its thresholds require crop-, location-, sensor-, and season-specific agronomic validation. Any future work involving schools or children requires safeguarding review, institutional approval, informed consent, data minimization, role-based access, retention rules, incident procedures, accountable implementation partners, and independent evaluation.

## Proposed next evidence gate

Subject to funding, approvals, and suitable partners, the next stage is a supervised evaluation that begins with synthetic tabletop tests and non-child controlled-garden testing. Predefined indicators, denominators, stopping rules, data-quality checks, and failure reporting must be approved before any real pilot.

For technical reproduction, see the [README](README.md), [pilot protocol](docs/pilot-protocol.md), [monitoring and evaluation plan](docs/monitoring-evaluation.md), and [model card](docs/model-card.md).
