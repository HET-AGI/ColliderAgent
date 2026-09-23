# Literature and Data Search Reference

How to find, read, and verify particle physics literature and experimental data. All API recipes below were tested against the live services (2026-09); they need no authentication.

Shell note: use **absolute paths** (or a single compound command) in the recipes — the working directory may not persist between shell calls.

## 1. Sources and What Each Is Authoritative For

| Source | Use it for | Access |
|--------|-----------|--------|
| **INSPIRE-HEP** | Finding papers, citation counts, arXiv ↔ journal mapping, verifying citations | REST API (Section 2) |
| **arXiv** | Newest preprints, abstracts, full text, **TeX source** (exact Lagrangians) | API + direct URLs (Section 3) |
| **HEPData** | Digitized experimental results: binned distributions, backgrounds, limits, cut-flows, efficiencies | REST API (Section 4) |
| **PDG** — `https://pdg.lbl.gov/` | World averages, particle properties, review articles, summary of search limits | `WebFetch` |
| **HFLAV** — `https://hflav.web.cern.ch/` | Flavour averages ($R_{D^{(*)}}$, lifetimes, mixing, ...) | `WebFetch` |
| **LHC Higgs Working Group** — `https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG` | Reference cross sections and branching ratios of an SM-like Higgs boson **at any mass** (Yellow Report 4, arXiv:1610.07922): BR tables at `.../LHCPhysics/CERNYellowReportPageBR`, cross sections for 10 GeV–3 TeV at `.../LHCPhysics/CERNYellowReportPageBSMAt13TeV`. Needed for every extra-scalar study | `WebFetch` |
| **LHC SUSY Cross Section Working Group** — `https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections` | Reference (NNLO+NNLL) pair-production cross sections for coloured scalars and fermions (squarks, gluinos, stops) and electroweakinos vs mass — the normalization for any new coloured or electroweak state with the same quantum numbers | `WebFetch`, then re-read raw page |
| **PDG reviews** (dark matter, leptoquarks, $Z'$, ...) — e.g. `https://pdg.lbl.gov/2025/reviews/rpp2025-rev-dark-matter.pdf` | Conventions and standard inputs of a field (halo parameters, nuclear inputs), status summaries | `curl -o` + `Read` (PDF) |
| **Experiment public results** — CMS: `https://cms-results.web.cern.ch/cms-results/public-results/publications/`; ATLAS: `https://twiki.cern.ch/twiki/bin/view/AtlasPublic`; LHCb: `https://lhcbproject.web.cern.ch/Publications/LHCbProjectPublic/Summary_all.html` | Latest results including preliminary ones (CONF notes / PAS), summary plots | `WebFetch` |

`WebSearch` is good for orientation but weak for "what is the latest experimental status" — it tends to return theory papers. For status questions use INSPIRE collaboration queries (Section 5) and the public-results pages. Use the APIs for anything you will cite.

`WebFetch` returns a model-written summary of the page, not the page. Use it to locate information; before quoting a **number**, re-read the raw page (`curl -s <url>` and `grep`). PDG review articles are PDFs, which `WebFetch` may not parse: download with `curl -sL -o <file>.pdf` and read with the `Read` tool (or `pdftotext`), or use the pdgLive HTML pages.

## 2. INSPIRE-HEP API

Base: `https://inspirehep.net/api/literature`

Parameters: `q` (query, URL-encoded), `sort` (`mostcited` | `mostrecent`), `size` (results per page), `fields` (comma-separated metadata fields — always set it, full records are huge).

### Look up / verify papers by arXiv ID (one or many per call)

```bash
curl -s "https://inspirehep.net/api/literature?q=arxiv:1603.04993%20or%20arxiv:1711.10391&size=25&fields=titles,authors.full_name,collaborations,arxiv_eprints,publication_info,citation_count,control_number" \
| python3 -c "
import json,sys
for h in json.load(sys.stdin)['hits']['hits']:
    m=h['metadata']
    # titles[0] is often the journal's MathML version ('<math ...>'): prefer a plain-text one
    title=next((t['title'] for t in m['titles'] if '<math' not in t['title']), m['titles'][0]['title'])
    who=[a['full_name'] for a in m.get('authors',[])][:3] or [c['value'] for c in m.get('collaborations',[])]
    print(m['control_number'], '|', (m.get('arxiv_eprints') or [{}])[0].get('value'), '|', title, '|', who, '| cites:', m.get('citation_count'))"
```

Batch your verifications: joining IDs with `or` checks a whole reference list in one call. IDs missing from the output do not exist on INSPIRE.

`control_number` is the INSPIRE record ID — it is also the key for HEPData records (`ins<control_number>`) and for citation chasing.

### Search

```bash
# Most-cited papers on a topic (free-text query)
curl -s "https://inspirehep.net/api/literature?q=leptoquark%20B%20anomalies&sort=mostcited&size=10&fields=titles,arxiv_eprints,citation_count,earliest_date"

# Recent papers: title word + date filter
curl -s "https://inspirehep.net/api/literature?q=t%20leptoquark%20and%20de%20%3E%202025&sort=mostrecent&size=10&fields=titles,arxiv_eprints,citation_count,earliest_date"
```

### Query syntax cheat-sheet

| Query | Meaning |
|-------|---------|
| `leptoquark B anomalies` | free text — good recall for distinctive words |
| `t leptoquark` / `t "95 GeV"` | word / exact phrase in title |
| `a Greljo` | author |
| `cn CMS` | collaboration |
| `arxiv:1603.04993` | by arXiv ID (`arxiv:A or arxiv:B` for several) |
| `de > 2024` | dated after 2024 |
| `topcite 100+` | at least 100 citations |
| `refersto:recid:1428667` | papers citing the record with this INSPIRE `control_number` (citation chasing) |
| `... and ...`, `... or ...`, `not ...` | boolean combination |

Notes:
- Combine: `cn ATLAS and t leptoquark and de > 2023`, or `refersto:recid:1428667 and t muon collider`
- **Free text fails for generic or numeric topics.** A query like `95 GeV diphoton excess` sorted by `mostcited` is swamped by unrelated famous papers. When the topic contains numbers or common words, use a quoted title phrase plus a date filter: `t "95 GeV" and de > 2022`
- **Title search (`t`) cannot match symbols.** Titles store τ, μ, ν, $R_D$, $b\to c$ as LaTeX or MathML, so `t tau and t neutrino` returns nothing for "... decaying to $\tau\nu$ ...". Put only plain words in `t` (`t leptoquark`, `t resonances`) and leave the symbols to free text or to the collaboration/date filters. A zero-hit title query usually means a symbol word, not a missing paper
- **`refersto` only works with `recid`** — look up the `control_number` first. `refersto:arxiv:<id>` does not raise an error but silently returns tens of thousands of unrelated papers. Sanity check: the hit count of a `refersto:recid:` query must equal the paper's `citation_count`
- The document-type filter for reviews (`tc r`) is sparsely populated — do not rely on it. Find reviews by adding words like `review`, `guide`, `primer`, `handbook`, `status` to a query sorted by `mostcited`
- If a query returns only a handful of hits, it is too strict: drop field operators. If it returns hundreds of irrelevant hits, it is too loose: move the key phrase into the title (`t "..."`)
- Citation counts are for ordering results, not a quality measure to quote

## 3. arXiv

```bash
# Metadata by ID (comma-separated list for several)
curl -s "https://export.arxiv.org/api/query?id_list=1711.10391,1603.04993&max_results=50"

# Search (newest first) — fields: ti (title), abs (abstract), au (author), cat (category)
curl -s "https://export.arxiv.org/api/query?search_query=cat:hep-ph+AND+abs:leptoquark+AND+abs:anomalies&sortBy=submittedDate&sortOrder=descending&max_results=10"
```

The response is Atom XML (`<entry>` with `<id>`, `<title>`, `<summary>`, `<author><name>`, `<published>`). `<summary>` is the abstract — a batch `id_list` call is the cheapest way to read many abstracts, and it returns clean LaTeX (INSPIRE's `abstracts` field is often MathML). **`max_results` must be at least the number of IDs** — a smaller value silently truncates the list.

Reading a paper:
- Abstract page: `https://arxiv.org/abs/<id>` — PDF: `https://arxiv.org/pdf/<id>` (both via `WebFetch`)
- **TeX source**: `https://arxiv.org/e-print/<id>` returns a gzip tarball (or a single gzipped `.tex` for one-file submissions). Use it whenever you need an exact Lagrangian, parameter definitions, benchmark points, or table values:

```bash
D=<absolute working dir>/research/<study_label>/sources/<id>; mkdir -p "$D" && cd "$D" \
&& curl -sL -o src.tar.gz "https://arxiv.org/e-print/<id>" \
&& (tar -xzf src.tar.gz 2>/dev/null || gunzip -c src.tar.gz > main.tex) \
&& grep -n "mathcal{L}\|\\\\begin{equation}\|\\\\begin{align}\|Lagrangian" *.tex | head -40
```

Then `Read` only the relevant lines — do not load whole papers into context. Many authors use macros (`\be`, `\beq`, `\lag`, `\cL`): if the grep finds little, grep the preamble for `\newcommand` first. Not every paper prints its Lagrangian (some define the model in words or by reference): check the abstract and the grep output before spending a download on it.

## 4. HEPData

**Route**: find the experimental paper on INSPIRE → take its `control_number` → open `record/ins<control_number>`. HEPData's own free-text search (`https://www.hepdata.net/search/?q=...&format=json`) has poor precision — use it only as a last resort.

```bash
# Does a record exist? List its tables. (HTTP 404 = this paper has no HEPData record)
curl -s -w "\nHTTP %{http_code}\n" "https://www.hepdata.net/record/ins1649273?format=json" \
| python3 -c "
import json,sys
body,_,code=sys.stdin.read().rpartition('\nHTTP ')
if code.strip()!='200': sys.exit('no HEPData record (HTTP '+code.strip()+')')
for t in json.loads(body)['data_tables']:
    print(t['name'], '|', (t.get('description') or '')[:80].replace('\n',' '), '|', t['data']['csv'])"

# Download one table (formats: csv, yaml, json, root, yoda) — the table name must be fully URL-encoded
curl -sL -o "<absolute working dir>/research/<study_label>/data/ins1649273_table1.csv" "https://www.hepdata.net/download/table/ins1649273/Table%201/csv"
```

Pitfalls:
- **Table names are arbitrary strings**, often with LaTeX (`Observed limit, $\beta_{\mathrm{L}}^{23} = 0.2$`). Build the download URL yourself with `urllib.parse.quote(name, safe='')`; the `data.csv` URL given in the record JSON is not encoded and fails for such names
- **HEPData rejects Python's default `urllib` user agent** (HTTP 403). Use `curl` (also from Python via `subprocess`), or send a `User-Agent` header
- For a bulk download, loop over `data_tables` and save each table under a short sanitized file name; keep a name → file map in the data directory

Reading the tables:
- Table descriptions in the record JSON are **truncated**; the full description is in the `#: description:` header line of the downloaded CSV. Table names do not always match the paper's figure numbering — always read the description and the column headers before using a table
- A CSV file contains **several blocks** separated by blank lines (e.g. data, total background, each background component, benchmark signals). Each block has its own `#:` qualifier lines and its own column line, so a plain CSV reader breaks. Parse it like this:

```python
import csv
def read_hepdata_csv(path):
    blocks, meta, rows = [], [], []
    def flush():
        if rows: blocks.append({"meta": list(meta), "columns": rows[0], "rows": rows[1:]})
    for line in open(path):
        line = line.rstrip("\n")
        if not line.strip(): flush(); meta, rows = [], []
        elif line.startswith("#:"): meta.append(line[2:].strip())
        else: rows.append(next(csv.reader([line])))
    flush()
    return blocks   # blocks[i]["meta"][-1] names the block, e.g. 'Process,,,SM'
```

What to look for: observed events / background / uncertainty per bin (→ likelihood recast), benchmark-signal yields, efficiency or acceptance tables (→ recast validation), observed and expected cross-section limits (→ direct limit reinterpretation), cut-flows (→ selection validation).

If a search has **no HEPData record**, the numbers must be taken from the paper's tables by hand — say so in the report, and quote the table number. A very recent paper may *announce* a HEPData record (a DOI in the arXiv comment) that is not public yet: `record/ins<n>` then returns 404 and the numeric record 403. Do not work around it — take numbers from the paper's tables, or read them off a figure **stating the reading uncertainty** (e.g. "by eye, ±30%"), and list "redo with the HEPData release" as an open issue. Direct-detection collaborations often publish limit curves on their own pages, Zenodo, or GitHub instead of HEPData — check the paper's data-availability statement.

## 5. Search Strategy

1. **Orient** — a free-text or title-phrase INSPIRE search sorted by `mostcited`, plus one or two `WebSearch` queries. Identify the 1–3 standard reviews and read their abstracts.
2. **Status** — find the latest experimental result: first list the collaboration's recent papers **unfiltered** (`cn <COLLAB> and de > <year-1>`, sorted `mostrecent`) — the paper reporting an anomaly rarely has "excess" or "anomaly" in its title, and a very recent result may post-date everything you remember; then narrow with `cn <COLLAB> and t <keyword> and de > <year-2>`; the experiments' public-results pages for preliminary results; PDG/HFLAV for averages. Record measurement, SM prediction, tension, date. If no newer result is found, say so and give the query and date.
3. **Landscape** — from the reviews and the most-cited list, collect candidate models. Use `refersto:recid:<control_number>` on the key review or the key measurement paper, sorted `mostrecent`, to find what happened since. Read abstracts in batches (arXiv `id_list`).
4. **Depth** — for each serious candidate: the original paper (Lagrangian), the most recent pheno update (constraints), the most recent direct search (limits, HEPData).
5. **Novelty check** (Mode A) — see Section 5a. Record the queries used.
6. **Stop rule** — stop when new queries return papers you have already seen, or models that fall into classes you already have.

### 5a. Novelty check ("has this been proposed?")

A novelty claim is only as good as the search behind it, and a fresh anomaly can attract several papers per day. Do all of the following and log each query:

1. **The citing list is the ground truth.** Every interpretation of an experimental result cites it. Get the result's `control_number`, run `refersto:recid:<n>` (check: hit count = `citation_count`), and fetch **all** abstracts in one or two arXiv `id_list` calls, saved to a file under `tools/`
2. **Grep before you read.** Seventy abstracts cost tens of thousands of tokens. First grep the saved file for the distinguishing words of your construction (mediator type, quantum numbers, mechanism, synonyms and both spellings: `colored|coloured`, `t-channel`, `squark`, ...); read in full only the hits and a sample for the landscape
3. **Full text, not only abstracts**: INSPIRE's `ft "<phrase>"` searches the full text and combines with the citing list — `ft "colored scalar" and refersto:recid:<n>`. Use specific phrases: generic words (`"t-channel"` alone) hit many papers that merely use the vocabulary; look at each hit's title/abstract before concluding
4. **Newer than INSPIRE**: papers take days to be linked. Search arXiv abstracts over the recent submission window:

```bash
curl -s -g -G "https://export.arxiv.org/api/query" --data-urlencode 'search_query=abs:"LUX-ZEPLIN" AND submittedDate:[202609010000 TO 202609212359]' \
  --data-urlencode "sortBy=submittedDate" --data-urlencode "sortOrder=descending" --data-urlencode "max_results=100"
```
   (`-g` is required: without it curl treats `[...]` as a range and fails.) The arXiv index itself can lag by a few days — **state the date of the newest record you saw**
5. **Beyond this anomaly**: search for the construction itself (free text with its defining words, and the papers citing its parent model) to find out whether the *structure* is known, independent of the application
6. **Phrase the claim accordingly**: "no prior work found as of <date>; basis: <n> citing papers at abstract level, full-text probes <list>, arXiv listing up to <date of newest record>". Distinguish *new structure* from *known structure, new application* (see the Origin field of the report template)

**Working under a lookup budget** (when the main agent sets one): spend it in the order status → landscape → depth on the top one or two targets. Batch ID lookups and abstract reads. What the budget did not allow belongs in the report's open decisions ("a deeper pass is needed for ...") — not in guesses.

Keep a short **search log** (query → what it yielded) for the report appendix. It makes the coverage auditable.

## 6. Verification Protocol

Every reference in a report or plan must pass checks 1 and 2, and is labelled by how far check 3 went:

1. **Exists** — the arXiv ID (or DOI / report number for experimental notes) resolves via INSPIRE or arXiv in this session
2. **Matches** — the returned first author and subject are the paper you think it is. Misremembered IDs usually resolve to a real but unrelated paper, so a successful lookup alone proves nothing. (The exact title is a weaker check: preprint and journal titles sometimes differ completely.)
3. **Supports the claim** — the statement you attribute to it appears in the text you actually read. Record the **reading depth**:

| Depth | You read | May be cited for |
|-------|----------|------------------|
| `source` | the relevant part of the paper (TeX source / PDF) | anything found there: Lagrangians, benchmark points, table values (give the equation/table) |
| `abstract` | the abstract | what the abstract states: the claim, the headline numbers |
| `title` | title and authors only | the existence of a model/analysis of that kind — nothing more |
| `data` | a data table or raw web page (HEPData, twiki, collaboration page) | the numbers in it — give record/table or URL and access date |

A large set of same-topic papers cited only to map a landscape (e.g. 50 interpretations of one event) may be cited as one grouped entry listing the arXiv IDs, provided the whole set was verified in a batch lookup and its depth is stated.

Numbers (measurements, significances, limits, benchmark values) must be copied from the source, with the location (abstract / equation / table / figure) noted. Never quote a number from memory as if it were sourced. Sources contain misprints too: if a number is inconsistent with other sources, say so instead of propagating it.

Reference format in reports: `[n] First-author et al., "Title", arXiv:XXXX.XXXXX (depth: source|abstract|title) — used for: <what>`. Number the list once at the end, so that the numbering has no gaps.

## 7. Offline Fallback

If web access is unavailable (all requests fail after 2 retries):
- Proceed from your own knowledge, but tag **every** reference and number `[unverified]`
- Put a warning at the top of the report: "Generated without literature access — all citations and experimental numbers are unverified and must be checked before use"
- Report the limitation in the return summary so the main agent can inform the user
