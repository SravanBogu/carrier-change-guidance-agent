# Claims Intake Policy

**Document status:** Approved synthetic demonstration policy  
**Applies to:** Carrier Change Intelligence demonstration environment  
**Last reviewed:** 2026-08-15

## Purpose

This policy defines how the Carrier Change Intelligence Agent API processes fictional carrier claim payloads before they are used by downstream workflows.

## Processing principle

Transactional claim normalization must use deterministic, approved rules.

The system must not use an AI model to infer source-field mappings, silently correct ambiguous data, or alter canonical claim values.

## Normalization sequence

```text
Carrier payload
    ↓
Approved field alias lookup
    ↓
Canonical claim field assignment
    ↓
Date validation
    ↓
Warning collection
    ↓
Human-review decision
```

## Valid recognized fields

When a source field appears in the approved mapping reference and its value satisfies validation rules:

- Map the field to the corresponding canonical field.
- Preserve the original value when no transformation is required.
- Return no warning for that field.

## Unknown source fields

When a source field is not included in the approved mapping reference:

1. Do not add the field to the canonical claim.
2. Add a warning in this format:

```text
Unmapped source field: <field_name>
```

3. Set `requires_human_review` to `true`.

## Invalid date values

Canonical date fields must use:

```text
YYYY-MM-DD
```

When a date is invalid:

1. Set the canonical date field to `null`.
2. Add a validation warning.
3. Set `requires_human_review` to `true`.

Example invalid source value:

```text
07/30/2026
```

## Conflicting source values

A conflict occurs when two source fields map to the same canonical field but contain different values.

Example:

```json
{
  "lossdate": "2026-07-30",
  "date_of_loss": "2026-07-29"
}
```

Required behavior:

1. Preserve the first recognized value.
2. Do not silently overwrite it with the later conflicting value.
3. Add a conflict warning.
4. Set `requires_human_review` to `true`.

## Human-review requirement

The API response must set:

```json
{
  "requires_human_review": true
}
```

when one or more processing warnings occur.

Warnings are returned at the top level of the API response and are intentionally separate from the canonical normalized claim.

## AI guidance boundary

A grounded AI assistant may explain approved policy, warnings, and reviewer next steps.

The assistant must not:

- Infer unapproved aliases.
- Alter the normalized claim.
- Override API warnings.
- Change `requires_human_review`.
- Approve, deny, or adjudicate claims.