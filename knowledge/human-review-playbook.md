# Human Review Playbook

**Document status:** Approved synthetic demonstration policy  
**Applies to:** Carrier Change Intelligence demonstration environment  
**Last reviewed:** 2026-08-15

## Purpose

This playbook defines the response process when the Carrier Change Intelligence Agent API returns one or more processing warnings.

All carrier names, policies, identifiers, and examples in this document are fictional.

## Review triggers

Human review is required when:

- An unknown source field is received.
- A date value is invalid.
- Two source fields map to the same canonical field with conflicting values.
- Required business information is missing for a downstream process.
- Approved knowledge does not support an AI guidance request.

## Reviewer workflow

```text
API warning or grounded-agent fallback
    ↓
Review original carrier payload
    ↓
Confirm source meaning and intended canonical value
    ↓
Correct source data or request approved mapping change
    ↓
Record resolution according to team procedures
    ↓
Resume downstream processing when resolved
```

## Unknown-field response

Example warning:

```text
Unmapped source field: lossOccurredWhen
```

Reviewer actions:

1. Inspect the original carrier documentation or payload contract.
2. Determine whether the field has a stable and approved business meaning.
3. Do not map the field automatically based only on its name.
4. If an approved mapping is justified, submit it through the documented change-control process.
5. If the meaning remains uncertain, preserve the warning and resolve the item manually.

## Invalid-date response

Example warning:

```text
date_of_loss must use YYYY-MM-DD format
```

Reviewer actions:

1. Confirm the intended date with the carrier source.
2. Correct the date to ISO format if the source data is reliable.
3. Do not assume regional date ordering for ambiguous values.
4. Record the correction or request a corrected source payload.

## Conflicting-value response

Example warning:

```text
Conflicting values received for canonical field: date_of_loss
```

Reviewer actions:

1. Compare each original source field and value.
2. Confirm the correct value using the carrier’s approved documentation.
3. Remember that the API retains the first recognized value only as a safe temporary deterministic policy.
4. Correct the source data or submit a mapping-rule change if required.
5. Record the outcome before downstream processing continues.

## Grounded-agent safety behavior

The Carrier Change Guidance Agent may explain policy using approved knowledge sources.

The agent must:

- Preserve the Carrier Change Intelligence API result as authoritative.
- Identify relevant policy or playbook guidance when sources support the answer.
- State when knowledge is insufficient.
- Recommend human review when retrieval evidence is missing or ambiguous.

The agent must not:

- Approve or deny claims.
- Decide claim coverage, payment, liability, or fraud outcomes.
- Invent carrier field mappings.
- Override an API warning or `requires_human_review` value.

## Required fallback response

When approved knowledge does not support an answer, the agent must respond:

```text
I do not have sufficient approved information to answer that.
Please route this item for human review.
```