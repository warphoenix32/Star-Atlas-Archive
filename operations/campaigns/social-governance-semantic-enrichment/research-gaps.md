# Research gaps

## Governance execution

All 33 PIPs require separate primary execution evidence before an `IMPLEMENTED` or `PARTIALLY_IMPLEMENTED` state can be assigned. Candidate evidence includes official implementation reports, on-chain transactions, treasury transfers, deployed policy/product changes, and direct implementation records.

PIP-11, PIP-25, and PIP-27 lack conclusive official election winner fields in the captured portal material and remain unresolved. No winner is inferred from candidate ordering or participation totals.

## Portal lifecycle metadata

The captured portal payloads report `Proposal_Activated_Pending_Open_Voting` even where the recorded vote window has ended. This contradiction is preserved; result derivation uses the official vote totals and dates, not that stale status label.

## Missing linked media

The social export includes image and video URLs but not the media binaries. Semantic conclusions are limited to the preserved post text. Media-dependent claims require separate capture and review.

## Retweet lineage

The normalized package identifies retweets but does not preserve a separate original-author field for every reshared post. Retweets therefore prove account resharing only; underlying authorship and claims require source-lineage review.

## Unresolved social references

Unmatched handles and hashtags are listed per semantic record. They were not converted into entities without an existing canonical entity match.
