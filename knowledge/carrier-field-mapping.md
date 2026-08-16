# Carrier Field Mapping Reference

**Document status:** Approved synthetic demonstration policy  
**Applies to:** Carrier Change Intelligence demonstration environment  
**Last reviewed:** 2026-08-15

## Purpose

This reference defines approved mappings from fictional carrier source payload fields to the canonical claim schema used by the Carrier Change Intelligence Agent API.

The mapping service uses deterministic rules. It does not infer unknown field meanings.

## Canonical claim fields

| Canonical field | Description | Approved source aliases |
|---|---|---|
| `claim_id` | Carrier claim identifier | `claimId`, `claim_id`, `claimNo` |
| `policy_number` | Policy identifier associated with the claim | `policyNumber`, `policy_number`, `policy_no` |
| `date_of_loss` | Date when the reported loss occurred | `lossdate`, `dateLoss`, `date_of_loss`, `incidentDate` |
| `date_reported` | Date the carrier received the report | `reportDate`, `date_reported`, `reported_at` |
| `loss_type` | Description or classification of the loss | `lossType`, `loss_type`, `incident_type` |

## Date requirements

All canonical date values must use ISO 8601 calendar-date format:

```text
YYYY-MM-DD
```

Valid example:

```text
2026-07-30
```

Invalid examples:

```text
07/30/2026
30-07-2026
July 30, 2026
```

## Mapping examples

### Northwind Mutual payload

```json
{
  "claimId": "NWM-10482",
  "policyNumber": "NWM-POL-8831",
  "lossdate": "2026-07-30",
  "lossType": "Windshield damage"
}
```

Expected canonical fields:

```json
{
  "claim_id": "NWM-10482",
  "policy_number": "NWM-POL-8831",
  "date_of_loss": "2026-07-30",
  "loss_type": "Windshield damage"
}
```

### Fabrikam Insurance payload

```json
{
  "claimNo": "FAB-77392",
  "policy_no": "FAB-PL-12009",
  "dateLoss": "2026-08-01",
  "incident_type": "Water damage"
}
```

Expected canonical fields:

```json
{
  "claim_id": "FAB-77392",
  "policy_number": "FAB-PL-12009",
  "date_of_loss": "2026-08-01",
  "loss_type": "Water damage"
}
```

## Unsupported fields

The following fictional field is not approved for automatic mapping:

```text
lossOccurredWhen
```

When an unsupported field is received:

1. Do not infer its meaning.
2. Do not add it to the canonical claim.
3. Generate an unmapped-field warning.
4. Set `requires_human_review` to `true`.
5. Route the case according to the Human Review Playbook.

## Change control

New aliases must be reviewed and approved before being added to the deterministic field-alias configuration.

The approval should confirm:

- The source field has a stable business meaning.
- The mapping does not conflict with an existing canonical field.
- Sample payloads and automated tests demonstrate the intended behavior.
- The mapping is documented before release.