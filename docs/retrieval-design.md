# Retrieval Design

## Purpose

The Carrier Change Guidance Agent uses retrieval-augmented generation (RAG) to explain Carrier Change Intelligence Agent API outcomes with approved synthetic policy knowledge.

The RAG layer does not perform transactional field normalization and does not override the API's `requires_human_review` decision.

## End-to-end flow

```text
Carrier payload + user question
    ↓
Carrier Change Intelligence Agent API
    ↓
Canonical claim + warnings + requires_human_review
    ↓
Build retrieval query from question and API warnings
    ↓
Azure AI Search hybrid retrieval
    ├── Keyword/full-text retrieval for exact terms
    └── Vector retrieval for semantic similarity
    ↓
Optional semantic ranking
    ↓
Retrieval sufficiency policy
    ↓
Foundry agent receives approved context
    ↓
Grounded explanation with sources or safe fallback
```

## Knowledge corpus

The initial corpus contains synthetic documents only:

- `carrier-field-mapping.md`
- `claims-intake-policy.md`
- `human-review-playbook.md`

## Chunking strategy

Documents are split by Markdown headings.

Each chunk preserves:

- Stable chunk ID
- Source filename
- Title
- Section heading
- Chunk index
- Text content

The small demonstration corpus does not require token-based chunking or overlap. Production sizing and overlap would be measured using an approved evaluation dataset.

## Azure AI Search index design

| Field | Type | Purpose |
|---|---|---|
| `id` | String key | Stable chunk identifier |
| `title` | String | Display and citation title |
| `content` | Searchable string | Keyword and semantic content |
| `content_vector` | Vector | Embedding representation |
| `source_file` | Filterable string | Citation source |
| `section` | Filterable string | Citation section |
| `chunk_index` | Integer | Debugging and ordering |

## Hybrid retrieval

Hybrid retrieval combines:

- Keyword search for exact source field names such as `lossOccurredWhen`
- Vector search for semantically phrased questions
- Optional semantic ranking to improve final relevance

## Retrieval sufficiency

The project does not treat a raw search score as a calibrated confidence percentage.

Retrieval is sufficient only when one or more approved sources contain usable text and citation metadata.

When retrieval is insufficient, the agent returns:

```text
I do not have sufficient approved information to answer that.
Please route this item for human review.
```

## Safety boundary

The Carrier Change Intelligence Agent API remains authoritative for:

- Canonical claim fields
- Validation warnings
- `requires_human_review`

The RAG/Foundry layer may explain those results but must not infer aliases, modify claim data, or override the API decision.