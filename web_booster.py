# web_booster.py — Recherche web + extraction + BM25 (gratuit, sans clé API)
import os, re, string
from typing import List, Dict, Any
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

TIMEOUT = 8
MAX_RESULTS = 8
MAX_SENTENCES = 5
PER_DOMAIN = 2
DISABLE_WEB = os.environ.get("DISABLE_WEB", "0") == "1"

STOP_FR = set("""
au aux avec ce ces dans de des du elle en et eux il je la le leur lui ma maintenant
mais me même mes moi mon ni nos notre nous on ou par pas pour qu que qui sa se ses son
sur ta te tes toi ton tu un une vos votre vous c d j l m n s t y qu est plus moins tres très
aura auront aurais aurait aurions auriez auraient suis es etes êtes est sommes êtes sont ai as ont
avais avait avions aviez avaient
""".split())

STOP_EN = set("""
a an the and or of from to in on for by with as is are was were be been being that this those these
there here it its itself into over under up down very more most less least can could should would may
might not no nor do does did doing have has had having i you he she we they them my your his her our
their me him us who whom which what when where why how about above below again further then once
because until while at between among out off only same other some such own so than too s t d ll m re ve y
ain aren couldn didn doesn hadn hasn haven isn ma mightn mustn needn shan shouldn wasn weren won wouldn
""".split())

def _strip_accents(s: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn")

def _tokenize(s: str): return re.findall(r"[a-zA-ZÀ-ÿ0-9]+", _strip_accents((s or "").lower()))
def _norm_tokens(tokens): return [t for t in tokens if t not in STOP_FR and t not in STOP_EN and len(t) > 2]

def _split_sents(text: str):
    text = re.sub(r"\s+", " ", text or "").strip()
    parts = re.split(r"(?<=[\.!?])\s+", text)
    return [p.strip() for p in parts if 40 <= len(p) <= 400][:400]

def _domain(u: str) -> str:
    try: return urlparse(u).netloc.replace("www.", "")
    except Exception: return ""

class BM25:
    def __init__(self, docs, k1=1.5, b=0.75):
        import math
        self.k1,self.b=k1,b; self.docs=docs; self.N=len(docs)
        self.len=[len(d) for d in docs]; self.avg=sum(self.len)/self.N if self.N else 0.0
        self.df={}
        for d in docs:
            for w in set(d): self.df[w]=self.df.get(w,0)+1
        self.idf={w:max(0.0, math.log(((self.N-df+0.5)/(df+0.5))+1.0)) for w,df in self.df.items()}

    def score(self, q, i):
        d=self.docs[i]
        if not d: return 0.0
        tf={}
        for w in d: tf[w]=tf.get(w,0)+1
        denom=self.k1*(1-self.b+self.b*(len(d)/(self.avg+1e-9))); s=0.0
        for w in q:
            if w not in tf: continue
            idf=self.idf.get(w,0.0); s += idf*(tf[w]*(self.k1+1))/(tf[w]+denom)
        return s

    def rank(self, q, topk=10):
        scores=[self.score(q,i) for i in range(len(self.docs))]
        return sorted(range(len(self.docs)), key=lambda i:scores[i], reverse=True)[:topk]

def _search(query: str):
    if DISABLE_WEB: return []
    out=[]
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, region="wt-wt", safesearch="moderate", max_results=MAX_RESULTS):
                href = r.get("href") or r.get("link") or r.get("url") or ""
                out.append({"title": r.get("title",""), "href": href, "body": r.get("body","")})
    except Exception:
        pass
    seen=set(); uniq=[]
    for r in out:
        u=r.get("href","")
        if u and u not in seen:
            uniq.append(r); seen.add(u)
    return uniq

def _fetch_text(url: str) -> str:
    try:
        r = requests.get(url, timeout=TIMEOUT, headers={"User-Agent":"Mozilla/5.0"})
        if r.status_code != 200: return ""
        soup = BeautifulSoup(r.text, "html.parser")
        paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        return " ".join(p for p in paras if len(p.split()) >= 6)
    except Exception:
        return ""

def _build_items(links):
    items=[]
    for r in links:
        u=r.get("href","")
        if not u: continue
        txt=_fetch_text(u)
        if not txt:
            body=r.get("body","")
            if len(body)>80: items.append({"text":body,"url":u,"domain":_domain(u)})
            continue
        for s in _split_sents(txt):
            items.append({"text":s,"url":u,"domain":_domain(u)})
        if len(items)>1200: break
    return items

def _rank(query: str, items):
    if not items: return []
    docs=[_norm_tokens(_tokenize(it["text"])) for it in items]
    q=_norm_tokens(_tokenize(query)); bm=BM25(docs)
    order=bm.rank(q, topk=min(80,len(docs)))
    out=[]; used={}
    for i in order:
        it=items[i]; d=it["domain"]; used[d]=used.get(d,0)
        if used[d] >= PER_DOMAIN: continue
        # anti-redondance simple
        t=set(docs[i]); redundant=False
        for j in range(len(out)):
            o=set(_norm_tokens(_tokenize(out[j]["text"])))
            if min(len(t),len(o))==0: continue
            overlap=len(t & o)/float(min(len(t),len(o)))
            if overlap>0.7: redundant=True; break
        if redundant: continue
        out.append(it); used[d]+=1
        if len(out)>=MAX_SENTENCES: break
    return out

def web_answer(query: str) -> Dict[str, Any]:
    links=_search(query)
    items=_build_items(links)
    ranked=_rank(query, items)
    if not ranked:
        return {"answer":"Je n’ai pas trouvé de sources fiables tout de suite. Ajoute un détail (domaine/contexte) ou reformule.","sources":[]}
    answer=" ".join([r["text"] for r in ranked])
    sources=[]; seen=set()
    for r in ranked:
        if r["domain"] and r["url"] and r["domain"] not in seen:
            sources.append({"domain":r["domain"],"url":r["url"]}); seen.add(r["domain"])
    return {"answer":answer,"sources":sources}
