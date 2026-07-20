"""Build deterministic Wave 2B review artifacts."""
from __future__ import annotations
import hashlib, json, re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]; HERE=Path(__file__).resolve().parent; PACKETS=HERE/"evidence-packets"
CID="knowledge-narrative-depth-wave-2b-events-timelines-2026-07"
PAGES=[
 ("knowledge/events/Event-Evidence-Registry.md","EXPAND_AND_STANDARDIZE","QUALIFIED","R2","Event identity and evidence stages remain distinct."),
 ("knowledge/events/README.md","INDEX_REDESIGN","CANONICAL","R1","Human-first event navigation and occurrence standard."),
 ("knowledge/timeline/Community-Timeline.md","EXPAND_AND_STANDARDIZE","QUALIFIED","R2","Community chronology with source and continuity gaps."),
 ("knowledge/timeline/Corporate-Timeline.md","EXPAND_AND_STANDARDIZE","QUALIFIED","R3","Attributed corporate chronology without inferred outcomes."),
 ("knowledge/timeline/Governance-Timeline.md","EXPAND_AND_STANDARDIZE","QUALIFIED","R2","Governance stages remain separate through implementation and payment."),
 ("knowledge/timeline/Lore-Timeline.md","EXPAND_AND_STANDARDIZE","HISTORICAL","R2","Publication order remains separate from in-universe chronology."),
 ("knowledge/timeline/Master-Timeline.md","EXPAND_AND_STANDARDIZE","QUALIFIED","R2","Selective cross-domain chronology with visible gaps."),
 ("knowledge/timeline/Official-Communications-Chronology.md","EXPAND_AND_STANDARDIZE","QUALIFIED","R2","Communication-surface coverage and archival gaps."),
 ("knowledge/timeline/Product-Timeline.md","EXPAND_AND_STANDARDIZE","QUALIFIED","R2","Build-specific product states and roadmap boundaries."),
 ("knowledge/timeline/README.md","INDEX_REDESIGN","CANONICAL","R1","Human-first chronology navigation and date rules."),
 ("knowledge/timeline/Star-Atlas-Historical-Periodization.md","EXPAND_AND_STANDARDIZE","QUALIFIED","R3","Interpretive research periods remain subordinate to dated evidence."),
]
def dump(p,v): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")
def b(p): return p.read_text(encoding="utf-8").replace("\r\n","\n").encode()
def pid(s): return "KNOW-"+hashlib.sha256(s.encode()).hexdigest()[:16].upper()
def main():
 PACKETS.mkdir(parents=True,exist_ok=True); inv=[]; ledger=[]
 for path,action,status,risk,scope in PAGES:
  p=ROOT/path; ident=pid(path); name=(p.parent.name+"-README" if p.stem=="README" else p.stem)+".json"
  packet={"campaign_id":CID,"page_id":ident,"proposed_path":path,"page_action":action,"proposed_knowledge_status":status,"page_risk_score":{"R1":2,"R2":5,"R3":7}[risk],"page_risk_class":risk,"subject_entities":[],"aliases":[],"scope":scope,"material_claims":[],"known_limitations":["Material chronology remains governed by citations and limitations in the page."],"research_gaps":["See the page's open chronology questions and research-gaps metadata."],"review_required":True,"review_after":"2027-01-20"}
  dump(PACKETS/name,packet); inv.append({"page_id":ident,"path":path,"action":action,"knowledge_status":status,"risk_class":risk,"word_count":len(re.findall(r"\b[\w'-]+\b",p.read_text(encoding="utf-8"))),"sha256_utf8_lf":hashlib.sha256(b(p)).hexdigest()}); ledger.append({"page_id":ident,"path":path,"disposition":"ACCEPTED","reason":scope,"human_review_required":True})
 dump(HERE/"page-inventory.json",{"campaign_id":CID,"page_count":len(inv),"pages":inv}); dump(HERE/"revision-ledger.json",{"campaign_id":CID,"accepted":11,"deferred":0,"duplicate":0,"rejected":0,"records":ledger})
 summary={"campaign_id":CID,"status":"READY_FOR_REVIEW","pages_revised":11,"pages_created":0,"risk_distribution":dict(sorted(Counter(x[3] for x in PAGES).items())),"knowledge_status_distribution":dict(sorted(Counter(x[2] for x in PAGES).items())),"archive_evidence_rewritten":False,"semantic_evidence_rewritten":False,"graph_modified":False,"publication_modified":False}; dump(HERE/"campaign-summary.json",summary)
 (HERE/"campaign-summary.md").write_text("# Knowledge Narrative Depth Wave 2B\n\n**Status:** `READY_FOR_REVIEW`\n\nAll 11 event and timeline pages were revised. Two indexes were redesigned; nine evidence-rich chronologies were standardized without replacing their preserved entries.\n\n- Risk: R1 = 2; R2 = 7; R3 = 2\n- New knowledge pages: 0\n- Archive, semantic, graph, and publication changes: none\n",encoding="utf-8",newline="\n")
if __name__=="__main__": main()
