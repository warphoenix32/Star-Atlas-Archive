# Normalization Ledger

Applied uniformly to each transcript:

1. Preserved the supplied file byte-for-byte under `raw/`.
2. Generated a stable source ID from the raw SHA-256 checksum.
3. Normalized line endings.
4. Joined wrapped caption text belonging to the same timestamp.
5. Collapsed repeated whitespace inside each caption.
6. Preserved wording, caption order, and timestamps.
7. Did not infer speakers, URLs, or missing dates.
8. Recorded filename-derived dates only with an explicit evidence basis.

No semantic tagging or canonical knowledge promotion was performed.
