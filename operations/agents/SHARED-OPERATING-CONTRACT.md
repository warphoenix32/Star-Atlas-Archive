# Shared Operating Contract

## Mission

Protect the separation between preserved evidence, reviewed knowledge, and public presentation while moving work efficiently through `PRESERVE`, `DRAFT`, `REVIEW`, and `PUBLISH`.

## Rules for every agent

1. Preserve exact source identifiers, dates, timestamps, quotations, checksums, and provenance.
2. Never convert a proposal into a vote, a vote into passage, passage into implementation, an announcement into release, testing into general availability, or payment authorization into verified payment.
3. Never infer an identity, source lineage, lifecycle state, or current status when the repository cannot support it.
4. Use semantic records as discovery aids, not as sole factual authority.
5. Treat current-state claims as date-scoped and include an `as_of` date.
6. Keep archive evidence immutable. Corrections belong in derived records, reconciliation, or knowledge with explicit provenance.
7. Work only in paths authorized by the task and role contract.
8. Prefer updating an existing canonical page over creating a duplicate entity page.
9. Record gaps and conflicts rather than smoothing them out in prose.
10. Stop at the role's handoff boundary.
11. Apply `EVIDENCE-SIGNIFICANCE-STANDARD.md` to transcript and conversational evidence. Preserve out-of-scope material in the Archive, but do not promote unrelated politics, unrelated games, off-topic attacks, or sentiment-only interpretations.

## Human adjudication

Surface a decision immediately when it concerns identity resolution, conflicting authoritative sources, taxonomy migration, financial or legal interpretation, governance execution, sensitive personal information, reputational claims, R3 or R4 knowledge, or any irreversible repository action. Do not bury the decision in a final report.

The decision packet must state:

- the decision ID and question;
- the relevant evidence and its authority;
- the agent's recommendation and rationale;
- the consequences of accepting or rejecting it;
- the permitted choices, including `DEFER`;
- the safe work that can continue while the decision is pending.

## Quality floor

Every handoff must be deterministic where generation is involved, internally linked, schema-valid, free of unexplained orphan records, and accompanied by a concise report of completed work, limitations, warnings, and unresolved human decisions.
