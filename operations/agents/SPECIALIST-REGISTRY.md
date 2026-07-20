# On-Demand Specialist Registry

Specialists are activated only when their expertise is required by an authorized task. They do not form mandatory serial gates.

| Specialist | Activation trigger | Permitted output | Must not do |
| --- | --- | --- | --- |
| Transcript Hygiene Specialist | Ingested transcript text requires cleanup, speaker-boundary review, timestamp reconciliation, or recognition-quality assessment | Corrected derived transcript artifacts, issue ledger, validation report | Alter original captures; infer speakers without evidence; promote knowledge |
| Solana Evidence Specialist | The user supplies Solana blockchain data or explicitly authorizes chain-data collection | Normalized transactions, account/program evidence, reconciliation records, verification limits | Activate without Solana data or authorization; infer ownership; promote on-chain claims beyond evidence |
| Lore and Taxonomy Specialist | Lore ingestion or an in-universe naming/classification conflict requires canonical vocabulary review | Taxonomy mappings, aliases, hierarchy decisions, conflict queue | Rewrite historical sources; apply lore authority to governance or operational history |
| Source Retrieval Specialist | A bounded campaign requires collection from a supported source family | Raw capture, provenance, retrieval ledger, exclusions, failures | Broaden the source scope; write knowledge pages |
| [Research and Gap Analyst](RESEARCH-GAP-ANALYST-CONTRACT.md) | The operator needs a cross-source inventory, a campaign identifies missing evidence, or recurring source coverage may be stale | Source-family-by-time coverage register, freshness queue, prioritized acquisition backlog, missing-artifact specification | Block routine low-risk work without cause; treat a gap as proof of absence; collect without authority |

All specialists inherit the Shared Operating Contract. Their output returns to the owning core role; specialist findings do not bypass `REVIEW`.
