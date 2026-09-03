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

Citations in the text are `<xref ref="biblio-farmer-zeros"/>`; a pinpoint ("[3, Theorem 2]")
uses `@detail`.  Verify against the schema before relying on any field name here.
