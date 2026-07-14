# Atlas Brew Combined Transcript — Transfer Status

The campaign was validated locally and promotion was initiated through the GitHub connector.

## Promoted metadata

- Campaign summary (Markdown and JSON)
- Validation report
- Checksummed manifest

## Remaining artifacts

The following files must be added from the validated campaign ZIP before this promotion can be merged:

| Path | Size | SHA-256 |
| --- | ---: | --- |
| `archive/raw/atlas-brew-combined/The_Atlas_Brew_combined_transcript.txt` | 9,119,898 bytes | `98a1658665774c3c2c53190a007a02a67fa8116ef196af5641ebb59502dfe38e` |
| `archive/normalized/atlas-brew-combined/atlas-brew-combined-normalized.md` | 8,907,995 bytes | `d72a34b76fcb2e9876c3e3d34e570c272552b9241eb1acf4cde07bc5dd03ca85` |
| `archive/normalized/atlas-brew-combined/normalization-corrections.json` | 620,631 bytes | `65f2c8006324cc7bb424928c10ac126e4300f132c2ae53ebe8c282b971c5564c` |
| `archive/source-records/atlas-brew-combined/source-records.json` | 147,127 bytes | `0d20486f5bfe16d4acf160a657907b6b85cc7f695c6ded29c1895cef2f456a7d` |
| `archive/extractions/atlas-brew-combined/extractions.json` | 79,583 bytes | `0f0b98b806d38bdd69c677dc62a0a36e4fe91ccf25415e47d3e134ac26af84e0` |
| `archive/reconciliation/atlas-brew-combined/reconciliation.json` | 37,886 bytes | `df368e82be32fd5d2afd5050b715c7644d210138d7bd25c6cafb09317e65d594` |
| `archive/proposed/knowledge/atlas-brew-combined/proposed-knowledge-deltas.json` | 12,794 bytes | `b29d40703f86be3bab599172c43982a2f91fc813e0b68b5affee120a9bcaa097` |
| `archive/proposed/graph/atlas-brew-combined/proposed-graph-deltas.json` | 12,794 bytes | `b29d40703f86be3bab599172c43982a2f91fc813e0b68b5affee120a9bcaa097` |

## Reason

The GitHub connector can create UTF-8 repository files but cannot stream local runtime files directly. The two transcript artifacts exceed the practical message-transfer limit. They must be committed from a local clone or a file-capable repository agent.

Do not merge until every manifest artifact is present and its checksum has been revalidated.
