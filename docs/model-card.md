# Model card: reference environmental-risk engine

## Purpose and implementation

A deterministic threshold reference model helps trained adults interpret temperature, humidity, and soil-moisture observations. JSON configuration produces three categorical risks, a 0–100 weighted score, combined level, reasons, checks, and a disclaimer.

## Intended users and use

Researchers, implementers, and qualified agronomists may use it for supervised demonstrations and proposed pilots. It is not for autonomous decisions, emergencies, diagnosis, nutrition/health advice, child profiling, resource eligibility, punitive action, or unsupervised child use.

## Inputs and outputs

Inputs are environmental measurements plus non-identifying crop context. Outputs are heat, water, humidity-disease and combined risk, score, explanations, next checks, and limitations.

## Explainability, assumptions, and fairness

Every category maps to published thresholds. The implementation assumes valid units, representative sensor placement, and relevant local thresholds. Unequal sensor quality, crop suitability, language access, connectivity, disability access, and who can act on advice can create unequal benefit or harm.

## Limitations, known risks, and validation

This is an unvalidated reference model. It does not model crop-specific physiology, forecast weather, calibrate sensors, or predict nutrition/health outcomes. False alarms and missed risks are possible. No accuracy or impact result is claimed.

## Required evaluation and change control

Future work requires local agronomic threshold review, sensor-quality testing, retrospective and prospective evaluation, usability/accessibility testing, subgroup impact review, failure drills, and independent review. Threshold or weight changes require a versioned proposal, evidence, tests, safety review, changelog entry, and rollback plan.
