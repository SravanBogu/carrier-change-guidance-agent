# Carrier Change Intelligence Agent API Contract

## Endpoint

POST /analyze

## Required request fields

- carrier
- payload

## Required response fields

- carrier
- normalized_claim
- warnings
- requires_human_review
- message

## Integration rule

Repo carrier-change-guidance-agent treats `warnings` and `requires_human_review` as authoritative.
It may explain these values but must not alter or recompute them.