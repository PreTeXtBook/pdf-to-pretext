# CSL-style bibliography entries (from `schema/pretext.rnc`, 2026-09-03)

A `biblio` with `@type` from the CSL vocabulary below carries structured fields, all
optional, in this fixed order (the no-style fallback renders them in this order):

`author`, `editor`, `translator`, `title`, `container-title`, `collection-title`, `genre`,
`edition`, `volume`, `number`, `issue`, `issued`, `accessed`, `page`, `page-first`,
`number-of-pages`, `publisher`, `publisher-place`, `DOI`, `ISBN`, `ISSN`, `URL`.

Types: `article`, `article-journal`, `article-magazine`, `article-newspaper`, `book`,
`chapter`, `collection`, `dataset`, `document`, `entry`, `entry-dictionary`,
`entry-encyclopedia`, `manuscript`, `paper-conference`, `patent`, `report`, `review`,
`software`, `speech`, `thesis`, `webpage`.

Names: `author`, `editor`, `translator` each hold one or more `name` elements, and a `name`
holds any of `family`, `given`, `dropping-particle`, `non-dropping-particle`, `suffix`,
`static-ordering`, or a single `literal`.  Dates: `issued` and `accessed` hold `date`
elements with `@year` (and further parts; check the schema).

Example (journal article):

```xml
<biblio xml:id="biblio-farmer-zeros" type="article-journal">
    <author><name><family>Farmer</family><given>David W.</given></name></author>
    <title>Title of the paper</title>
    <container-title>Journal Name</container-title>
    <volume>12</volume>
    <issue>3</issue>
    <issued><date year="2021"/></issued>
    <page>100-120</page>
    <DOI>10.0000/example</DOI>
</biblio>
```

DOIs: `scripts/lookup-dois.py` takes the entries as printed and lists candidates.  Crossref
does not hold every DOI.  arXiv preprints (`10.48550/arXiv.<identifier>`, one for every
preprint) and the Dagstuhl proceedings (LIPIcs, `10.4230/...`) are registered with DataCite,
which the script asks when Crossref has no candidate with the entry's title.  A title that
agrees is a candidate only: compare authors, volume, and pages, and say in a comment where
the record and the printed entry disagree (a year, a volume).  In a `DOI` element `<` and
`>` are written `&lt;` and `&gt;` (the old Wiley identifiers contain them).

As printed, in the order printed:

- A page range takes a hyphen (`100-120`), whatever dash the original prints.
- A long dash standing for a repeated author is written out as the name, with a comment
  that the original prints a dash.
- A preprint printed with "arXiv preprint arXiv:NNNN.NNNNN" where a journal would be is
  type `article` with that string as its `container-title`, so the printed words survive.
- An entry with no author prints a leading comma in PreTeXt's rendering; say so in the
  notes rather than invent an author.
- PreTeXt renders these entries in its own order and punctuation (family name first, the
  DOI at the end).  That is a difference of typography, not an error to work around.

Citations in the text are `<xref ref="biblio-farmer-zeros"/>`; several keys in one
citation ("[7, 4, 6]") are one `xref` whose `@ref` lists the targets in the printed
order.  A pinpoint ("[3, Theorem 2]") uses `@detail`.  Verify against the schema before
relying on any field name here.
