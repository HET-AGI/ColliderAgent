#!/usr/bin/env python3
"""INSPIRE-HEP query helper (uses curl; logs every query to search_log.tsv).

usage: inspire.py "<query>" [sort=mostrecent|mostcited] [size=25] [abs=1]
"""
import json, subprocess, sys, urllib.parse, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "search_log.tsv")


def main():
    q = sys.argv[1]
    opts = dict(a.split("=", 1) for a in sys.argv[2:])
    sort = opts.get("sort", "mostrecent")
    size = opts.get("size", "25")
    want_abs = opts.get("abs", "0") == "1"
    fields = "titles,authors.full_name,collaborations,arxiv_eprints,citation_count,control_number,earliest_date"
    if want_abs:
        fields += ",abstracts"
    url = ("https://inspirehep.net/api/literature?q=" + urllib.parse.quote(q)
           + "&sort=" + sort + "&size=" + size + "&fields=" + fields)
    out = subprocess.run(["curl", "-s", "--max-time", "60", url], capture_output=True, text=True).stdout
    try:
        d = json.loads(out)
    except Exception:
        print("BAD RESPONSE:", out[:500])
        return
    total = d["hits"]["total"]
    print("TOTAL HITS:", total)
    for h in d["hits"]["hits"]:
        m = h["metadata"]
        title = next((t["title"] for t in m["titles"] if "<math" not in t["title"]), m["titles"][0]["title"])
        who = [a["full_name"] for a in m.get("authors", [])][:3] or [c["value"] for c in m.get("collaborations", [])]
        col = [c["value"] for c in m.get("collaborations", [])]
        print(m["control_number"], "|", (m.get("arxiv_eprints") or [{}])[0].get("value"), "|", m.get("earliest_date"),
              "|", title, "|", who, col, "| cites:", m.get("citation_count"))
        if want_abs:
            ab = (m.get("abstracts") or [{}])[0].get("value", "")
            print("    ABS:", ab[:1500].replace("\n", " "))
    with open(LOG, "a") as f:
        f.write("\t".join([datetime.datetime.now().isoformat(timespec="seconds"), "INSPIRE", q, sort, str(total)]) + "\n")


if __name__ == "__main__":
    main()
