#!/usr/bin/env python3
"""Look up DOI candidates for the entries of a bibliography, at Crossref and at DataCite.

Usage: lookup-dois.py <entries.txt> [<candidates.json>]

entries.txt has one entry per line, three fields separated by " | ":

    label | title | the rest as printed (authors, journal, volume, year, arXiv number)

Crossref is asked first, with everything.  It does not hold every DOI: arXiv preprints
and the Dagstuhl proceedings (LIPIcs), among others, are registered with DataCite.  So
when no Crossref candidate carries the entry's title, DataCite is asked for the title as
a phrase; and when the entry names an arXiv identifier, the DOI arXiv gives every preprint
(10.48550/arXiv.<identifier>) is fetched and shown with its own title and authors.

A candidate whose title equals the entry's (letters and digits only, case and accents
aside) is marked "=".  That is a candidate, not yet a match: compare the authors, the
volume, and the pages with the printed entry before using the DOI, and record in the
bibliography any entry where the record and the paper disagree.
"""
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

AGENT = {"User-Agent": "pdf-to-pretext bibliography lookup"}
ARXIV = re.compile(r"arXiv[:\s]\s*([0-9]{4}\.[0-9]{4,5}|[a-z-]+(?:\.[A-Z]{2})?/[0-9]{7})", re.I)


def fetch(url):
    """The JSON at a URL, or None when it is not there; three tries."""
    for attempt in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=AGENT), timeout=40))
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return None
        except (urllib.error.URLError, TimeoutError, ValueError):
            pass
        time.sleep(3)
    return None


def key(title):
    plain = unicodedata.normalize("NFKD", title)
    return "".join(c for c in plain.lower() if c.isalnum() and not unicodedata.combining(c))


def crossref(title, rest):
    url = ("https://api.crossref.org/works?rows=3&query.bibliographic=" + urllib.parse.quote(title + " " + rest)
           + "&select=DOI,title,author,container-title,issued,volume,issue,page,type")
    found = []
    for item in ((fetch(url) or {}).get("message") or {}).get("items", []):
        authors = ", ".join(" ".join(filter(None, (a.get("given"), a.get("family")))) for a in item.get("author", []))
        year = ((item.get("issued") or {}).get("date-parts") or [[None]])[0][0]
        found.append({"source": "Crossref", "doi": item.get("DOI"), "title": "; ".join(item.get("title", [])),
                      "authors": authors,
                      "where": "{} {}({}) {} ({}) [{}]".format("; ".join(item.get("container-title", [])),
                                                               item.get("volume") or "", item.get("issue") or "",
                                                               item.get("page") or "", year, item.get("type"))})
    return found


def datacite_record(attributes, source):
    container = (attributes.get("container") or {}).get("title") or attributes.get("publisher") or ""
    if isinstance(container, dict):
        container = container.get("name", "")
    return {"source": source, "doi": attributes.get("doi"),
            "title": "; ".join(t.get("title", "") for t in attributes.get("titles", [])),
            "authors": ", ".join(c.get("name", "") for c in attributes.get("creators", [])),
            "where": "{} ({})".format(container, attributes.get("publicationYear"))}


def datacite(title):
    phrase = 'titles.title:"{}"'.format(title.replace('"', " "))
    url = "https://api.datacite.org/dois?page%5Bsize%5D=3&query=" + urllib.parse.quote(phrase)
    return [datacite_record(d["attributes"], "DataCite") for d in (fetch(url) or {}).get("data", [])]


def arxiv(identifier):
    data = (fetch("https://api.datacite.org/dois/10.48550/arXiv." + identifier) or {}).get("data")
    return [datacite_record(data["attributes"], "DataCite, arXiv " + identifier)] if data else []


def main(entries_path, json_path=None):
    everything, tally = {}, {"Crossref": [], "DataCite": [], "none": []}
    for line in open(entries_path, encoding="utf-8"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        label, title, rest = (field.strip() for field in (line.split(" | ", 2) + ["", ""])[:3])
        candidates = crossref(title, rest)
        if not any(key(c["title"]) == key(title) for c in candidates):
            candidates += datacite(title)
        identifier = ARXIV.search(line)
        if identifier:
            candidates += arxiv(identifier.group(1))
        seen = set()  # the title query and the arXiv identifier can find one record twice
        candidates = [c for c in candidates if not (c["doi"].lower() in seen or seen.add(c["doi"].lower()))]
        matched = [c for c in candidates if key(c["title"]) == key(title)]
        print("{} {}".format(label, title))
        for c in candidates:
            mark = "=" if key(c["title"]) == key(title) else " "
            print("  {} {:<10} {}\n               {} | {} | {}".format(mark, c["source"].split(",")[0], c["doi"],
                                                                      c["title"][:90], c["authors"][:70], c["where"][:80]))
        if not candidates:
            print("    nothing found")
        tally[matched[0]["source"].split(",")[0] if matched else "none"].append(label)
        everything[label] = candidates
        time.sleep(0.3)
    print()
    print("title found at Crossref: {}   at DataCite only: {}   not found: {}".format(
        len(tally["Crossref"]), len(tally["DataCite"]), len(tally["none"])))
    if tally["DataCite"]:
        print("  DataCite only: " + " ".join(tally["DataCite"]))
    if tally["none"]:
        print("  not found:     " + " ".join(tally["none"]))
    if json_path:
        json.dump(everything, open(json_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main(*sys.argv[1:3])
