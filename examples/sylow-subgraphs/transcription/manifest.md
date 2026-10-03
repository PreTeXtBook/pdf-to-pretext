# Manifest — corpus/own/scvt (Beezer, Sylow subgraphs), transcribed from the PDF alone

Run `runs/2026-09-03-beezer-scvt`; header, policy, and effort log in `notes.md`.  Every
page of `corpus/own/scvt/paper.pdf` (10 pages: an unnumbered title page, then printed pages
1–9; PDF page N is printed page N−1) was read as an image; words come from `paper.txt`.
`source/` and `published.pdf` were not opened.  Element names verified against
`pretext/schema/pretext.rnc` at commit `59cd06c1` where noted.

Item counts for the pass-3 check: 6 sections, 1 titled `paragraphs`, 11 numbered blocks
(3 definitions, 7 theorems, 1 lemma), 1 unnumbered remark, 8 proofs, 0 numbered equations, 3 unnumbered displays, 1 figure,
0 tables, 0 footnotes, 23 bibliography entries.

## 1. Front matter

| item | content | source | PreTeXt |
|---|---|---|---|
| title | Sylow Subgraphs in Self-Complementary Vertex Transitive Graphs | title page | `article/title` (one title, two typeset lines) |
| author | Robert A. Beezer | title page | `personname` |
| department | Department of Mathematics and Computer Science | title page | `department` |
| institution | University of Puget Sound | title page | `institution` |
| location | Tacoma, Washington 98416 USA | title page | `location` |
| email | beezer@ups.edu | title page ("Email:") | `email` |
| support | This work was supported by a University of Puget Sound Martin Nelson Summer Research Award and the hospitality of the Department of Computer Science and Software Engineering at the University of Western Australia during a sabbatical visit. | unmarked footnote at the foot of printed page 1 (a `\thanks`) | `author/support` (renders in HTML and the AMS texstyle; the default LaTeX article puts it in the `\author` tabular, where this long sentence overflows and hides the name — a PreTeXt defect recorded in `notes.md`) |
| date | December 30, 2004 | title page — printed in the PDF, so it stays | `date` |
| keywords | graph theory; vertex transitive; self-complementary | printed page 1, "Keywords:" | `keywords` with three `keyword`s |
| abstract | one paragraph, printed page 1, verbatim ("Abstract:" label dropped, PreTeXt supplies its own) | | `frontmatter/abstract/p` |
| acknowledgment | "Thanks are due to Gerald Alexanderson, … is also gratefully acknowledged." | printed page 8, run-in italic heading "Acknowledgment.", small type, after the last section's text | `paragraphs` titled "Acknowledgment." at the end of Section 6 — the article schema has no acknowledgement division (front matter is `bibinfo`, `titlepage`, `abstract`; back matter is appendices, solutions, glossary, references, index, colophon) |
| excluded | page numbers; the blank space of the title page | | |

## 2. Divisions

`<!-- Original: Section N -->` before each.  No subsections.

| original | title (verbatim) | printed pages | identifier |
|---|---|---|---|
| Section 1 | Introduction | 1–3 | `section-introduction` |
| Section 2 | Definitions and Notation | 3–4 | `section-definitions-notation` |
| Section 3 | Two Basic Properties | 4 | `section-two-basic-properties` |
| Section 4 | Constructing Self-Complementary Vertex Transitive Graphs | 5–6 | `section-constructing-graphs` |
| Section 5 | Sylow Subgraphs | 6–7 | `section-sylow-subgraphs` |
| Section 6 | Recent Progress on Characterizing Self-Complementary Vertex Transitive Graphs | 8 | `section-recent-progress` |
| (run-in) | Acknowledgment. | 8 | `paragraphs-acknowledgment`, inside Section 6 |
| References | References | 8–9 | `references` |

## 3. Numbered and unnumbered items

### 3a. Theorem-like blocks (one counter, within sections; Definition 4.1 precedes Theorem 4.2; 11 numbered plus the remark)

The parenthetical after a number is the source's optional argument, here always a
citation: it becomes the block's `title`, holding `xref`s to the `biblio` entries (schema:
`title` is `TextLong`, which admits `xref`; `@detail` for "Theorem 4.5").  Every "Proof"
heading is a bold word without a period, ended by a hollow box; each becomes a `proof`
inside its theorem (none is detached).

| original | page | element | title | identifier | proof? | notes |
|---|---|---|---|---|---|---|
| Definition 2.1 | 3 | `definition` | — | `definition-vertex-transitive` | no | term "vertex transitive" upright inside the italic statement |
| Definition 2.2 | 3 | `definition` | — | `definition-self-complementary` | no | term "self-complementary" |
| Theorem 3.1 | 4 | `theorem` | [17, 22] | `theorem-order-congruent-one-mod-four` | yes | |
| Lemma 3.2 | 4 | `lemma` | [22, 17, 21] | `lemma-complementing-map-cycles` | yes | |
| Remark | 4 | `remark` | — | `remark-fixed-vertex` | no | unnumbered; `<!-- Original: unnumbered Remark, page 4 -->` |
| Definition 4.1 | 5 | `definition` | — | `definition-lexicographic-product` | no | term "lexicographic product"; the long set-builder line is inline mathematics that wrapped |
| Theorem 4.2 | 5 | `theorem` | — | `theorem-lexicographic-vertex-transitive` | yes | the prose calls 4.2 and 4.3 "propositions"; the labels say Theorem |
| Theorem 4.3 | 5 | `theorem` | — | `theorem-lexicographic-self-complementary` | yes | |
| Theorem 4.4 | 5 | `theorem` | — | `theorem-paley-graph-exists` | yes | proof has three paragraphs |
| Theorem 4.5 | 5–6 | `theorem` | [16], Theorem 4.5 → `<xref ref="biblio-rao-strongly-regular" detail="Theorem 4.5"/>` | `theorem-orders-sufficient` | yes (page 6) | |
| Theorem 5.1 | 6–7 | `theorem` | [14], Theorem 2 → `@detail="Theorem 2"` | `theorem-sylow-subgraphs` | yes, 14 paragraphs with two displays | the main result |
| Theorem 5.2 | 7 | `theorem` | [14], Theorem 1 → `@detail="Theorem 1"` | `theorem-prime-power-congruent` | yes, one sentence | |

### 3b. Displayed mathematics

No numbered equations.  Three unnumbered displays, each an `md` without `@number` and
without an id (nothing refers to them); mark each `<!-- Original: unnumbered display, page N -->`.

| page | where | mathematics |
|---|---|---|
| 6 | proof of Theorem 5.1, third paragraph | `D(P) = \{\sigma \in C(\Gamma) \mid P^{\sigma} = P, \lvert P_{x(\sigma)} \rvert = p^{n-m}\}.` |
| 7 | proof of Theorem 5.1, after "and we have" | `p^{n-m} = \lvert M_x \rvert = \lvert {M_x}^{\rho} \rvert \leq \lvert M_{x(\widetilde{\sigma})} \rvert \leq \lvert \widetilde{M}_{x(\widetilde{\sigma})} \rvert \leq p^{n-m}.` |
| 8 | Section 6, "dividing n, then" | `p^m \equiv \begin{cases} 1 \pmod{2k} & \text{if } p \text{ is odd} \\ 1 \pmod{k} & \text{if } p = 2. \end{cases}` — the original spaces "1" and "(mod 2k)" as separate columns; `cases` with two columns is the PreTeXt-native form |

Inline mathematics worth fixing now (300-dpi checks):

- printed page 1: the graph counts are set in mathematics with thin spaces:
  `<m>165\,091\,172\,592</m>`, `<m>50\,502\,031\,367\,952</m>`, `<m>5\,600</m>`; the small
  counts (720, 74, 14, 2) are plain digits.
- page 3: `\mathbf{Aut}(\Gamma)` at its definition — the original sets the whole of
  "Aut(Γ)" bold, but `\mathbf{\Gamma}` has no glyph in the AMS build's math font and
  printed as a blank (Rob, 2026-09-03), so only "Aut" is bold; page 8:
  `\mathrm{Aut}(\Gamma)` upright.
- page 3: `\{\sigma(u), \sigma(v)\} \notin E`.
- page 4: `\binom{n}{2} = \frac{n(n-1)}{2}` inline; complements `\overline{X}`,
  `\overline{\Gamma}`, `\overline{E}`; page 5: `\overline{\Gamma_1[\Gamma_2]} = \overline{\Gamma_1}\,[\overline{\Gamma_2}]`.
- page 5, Definition 4.1: `E(\Gamma_1[\Gamma_2]) = \{\,\{(u_1,u_2),(v_1,v_2)\} \mid \{u_1,v_1\} \in E_1, \text{ or } u_1 = v_1, \{u_2,v_2\} \in E_2\}.`
- page 5, proof of 4.4: `V = \{0, x, x^2, \ldots, x^{4k} = 1\}`, `E = \{\,\{u,v\} \mid u - v = x^{2s}, s \in \mathbb{Z}\,\}`, `\sigma = (0)(x\ x^2\ x^3 \ldots x^{4k})`, `\mathrm{GF}(p^r)`, `\mathrm{GF}(p^r)^{*}`, `x^2 + 2x + 2`.
- page 6: conjugation `H^{\sigma} = \sigma H \sigma^{-1}`; stabilizer `G_v = \{\sigma \in G \mid \sigma(v) = v\}`; orbit `v^G`; `\mathcal{P} = \{P \mid P \text{ is a } p-\text{group in } G, D(P) \neq \varnothing\}` — the hyphen in "p−group" is a mathematics minus in the original (the words sit inside the formula) and the empty set is the round `\varnothing` glyph; `\widetilde{\sigma}`, `\widetilde{M}`, `P^{\widetilde{\sigma}}`, `N_G(M)`.
- page 7: `x^K`, `x(\sigma)^M`, `P^{*} \setminus M`, `\langle M, g \rangle`, `\lvert G \rvert = \lvert G_v \rvert \lvert v^G \rvert`.
- page 8: `a^{-1}b \in H`, `K_n`, `S_n`, `\Gamma_i`.
- congruences everywhere: `n \equiv 1 \pmod{4}`.

### 3c. Figure

| original | page | element | identifier | notes |
|---|---|---|---|---|
| Fig. 1 | 3 | `figure` | `figure-paley-nine-vertices` | caption "A self-complementary vertex transitive graph on 9 vertices."; the label "Fig. 1" is the class's; the prose says "Figure 1" |

## 4. Numbering scheme

Sections 1–6, no subsections; theorem-like blocks on one counter within sections; the one
figure numbered globally ("Fig. 1"); no numbered equations; no footnotes (the thanks is
an unmarked note).

```xml
<numbering>
    <divisions level="1"/>
    <blocks level="1"/>
    <equations level="0"/>
    <figures level="0" distinct="yes"/>
    <footnotes level="0"/>
</numbering>
```

Expected agreement: complete, except that PreTeXt numbers the unnumbered Remark as
Remark 3.3 (blocks are always numbered).  `distinct="yes"` keeps the figure off the theorem counter
(without it PreTeXt would print "Figure 2.3" or the like); there is no table to collide.

## 5. Macros

None visible in the PDF.  Empty `docinfo/macros`; everything inline: `\overline`,
`\widetilde`, `\mathcal{P}`, `\mathbb{Z}`, `\mathrm{GF}`, `\mathrm{Aut}`, `\pmod`,
`\varnothing`, `\binom`, `\lvert…\rvert`.

## 6. Bibliography (CSL-style `biblio`, order and numbering as printed)

DOIs from Crossref (2026-09-03); numbers and wording as printed even where Crossref
differs.  Names in "family, given" form except where noted.

| key | identifier | type | fields |
|---|---|---|---|
| [1] | `biblio-chvatal-erdos-hedrlin-ramsey` | `article-journal` | Chvátal, V.; Erdös, P.; Hedrlín, Z.; "Ramsey's theorem and self-complementary graphs"; Discrete Math.; 3; 1972; 301–304; DOI `10.1016/0012-365x(72)90087-8` |
| [2] | `biblio-clapham-ramsey-bounds` | `article-journal` | Clapham, C.R.J.; "A class of self-complementary graphs and lower bounds of some Ramsey numbers"; J. Graph Theory; 3; issue 3; 1979; 287–289; DOI `10.1002/jgt.3190030311` |
| [3] | `biblio-colbourn-graph-isomorphism` | `article-journal` | Colbourn, M.J.; Colbourn, C.J.; "Graph isomorphisms and self-complementary graphs" (Crossref: "isomorphism"; keep); SIGACT News; 10; issue 1; 1978; 25–29; DOI `10.1145/1008605.1008608` |
| [4] | `biblio-froncek-rosa-siran-circulant` | `article-journal` | Fronček, D.; Rosa, A.; Širáň, J.; "The existence of selfcomplementary circulant graphs"; European J. Combin.; 17; issue 7; 1996; 625–628; DOI `10.1006/eujc.1996.0053` |
| [5] | `biblio-godsil-royle-algebraic-graph-theory` | `book` | Godsil, C.; Royle, G.; "Algebraic Graph Theory"; collection-title Graduate Texts in Mathematics; volume 207; Springer; New York; 2001; DOI `10.1007/978-1-4613-0163-9` |
| [6] | `biblio-koolen-manuscript` | `manuscript` | Koolen, J.H.; "On selfcomplementary vertex-transitive graphs"; genre Manuscript; 1997 |
| [7] | `biblio-li-vertex-transitive` | `article-journal` | Li, C.H.; "On self-complementary vertex-transitive graphs"; Comm. Algebra; 25; issue 12; 1997; 3903–3908; DOI `10.1080/00927879708826094` |
| [8] | `biblio-li-finite-graphs` | `article-journal` | Li, C.H.; "On finite graphs that are self-complementary and vertex-transitive"; Australas. J. Combin.; 18; 1998; 147–155; no DOI (journal not in Crossref) |
| [9] | `biblio-li-praeger-not-cayley` | `article-journal` | Li, C.H.; Praeger, C.E.; "Self-complementary vertex-transitive graphs need not be Cayley graphs"; Bull. London Math. Soc.; 33; issue 6; 2001; 653–661; DOI `10.1112/s0024609301008505` |
| [10] | `biblio-li-praeger-orbitals` | `article-journal` | Li, C.H.; Praeger, C.E.; "On partitioning the orbitals of a transitive permutation group"; Trans. Amer. Math. Soc.; 355; issue 2; 2003; 637–653; DOI `10.1090/s0002-9947-02-03110-0` |
| [11] | `biblio-li-praeger-homogeneous-factorisations` | `article-journal` | Li, C.H.; Praeger, C.E.; "Constructing homogenous factorisations of complete graphs and digraphs" (as printed); Graphs and Combinatorics; 18; 2002; 757-761 (hyphen as printed); DOI `10.1007/s003730200061` |
| [12] | `biblio-lovasz-shannon-capacity` | `article-journal` | Lovász, L.; "On the Shannon capacity of a graph"; IEEE Trans. Inform. Theory; 25; issue 1; 1979; 1–7; DOI `10.1109/tit.1979.1055985` |
| [13] | `biblio-luo-su-li-ramsey-bounds` | `article-journal` | three `literal` names as printed, family first: Luo Haipeng; Su Wenlong; Li Zhenchong; "The properties of self-complementary graphs and new lower bounds for diagonal Ramsey numbers"; Australas. J. Combin.; 25; 2002; 103–116; no DOI |
| [14] | `biblio-muzychuk-sylow-subgraphs` | `article-journal` | Muzychuk, M.; "On Sylow subgraphs of vertex-transitive self-complementary graphs"; Bull. London Math. Soc.; 31; 1999; 531–533; DOI `10.1112/s0024609399005925` |
| [15] | `biblio-peisert-symmetric-graphs` | `article-journal` | Peisert, W.; "All self-complementary symmetric graphs"; J. Algebra; 240; issue 1; 2001; 209–229; DOI `10.1006/jabr.2000.8714` |
| [16] | `biblio-rao-strongly-regular` | `article-journal` | Rao, S.B.; "On regular and strongly-regular self-complementary graphs"; Discrete Math.; 54; 1985; 73–82; DOI `10.1016/0012-365x(85)90063-9` |
| [17] | `biblio-ringel-selbstkomplementare` | `article-journal` | Ringel, G.; "Selbstkomplementäre Graphen"; Arch. Math.; 14; 1963; 354–358; DOI `10.1007/bf01234967` |
| [18] | `biblio-read-counting` | `article-journal` | Read, R.C.; "On the number of self-complementary graphs and digraphs"; J. London Math. Soc.; 38; 1963; 99–104; DOI `10.1112/jlms/s1-38.1.99` |
| [19] | `biblio-royle-combinatorial-data` | `webpage` | Royle, G.; "Combinatorial Data"; URL `http://www.csse.uwa.edu.au/~gordon/data.html`; accessed 2004-12-24 (the printed date) |
| [20] | `biblio-royle-personal-communication` | `document` | Royle, G.; genre "personal communication"; no title, no date |
| [21] | `biblio-suprunenko-self-complementary` | `article-journal` | Suprunenko, D.A.; "Self-complementary graphs"; Cybernetics; 21; 1985 (Crossref: 1986; keep); 559–567; DOI `10.1007/bf01074707` |
| [22] | `biblio-sachs-selbstcomplementare` | `article-journal` | Sachs, H.; "Über Selbstcomplementäre Graphen" (as printed; Crossref has "selbstkomplementäre"); Publ. Math. Debrecen; 9; 1962; 270–288; DOI `10.5486/pmd.1962.9.3-4.11` |
| [23] | `biblio-thompson-codes-to-groups` | `book` | Thompson, T.M.; "From error-correcting codes through sphere packings to simple groups"; collection-title Carus Mathematical Monographs; volume 21; Mathematical Association of America; Washington, DC; 1983; DOI `10.5948/upo9781614440215` |

Citations in the text: [19], [18], [19], [20] (page 1); [23], [3], [1, 2, 13], [13], [12],
[17, 22], [22], [16], [21], [4], [6], [7], [8], [14] (page 2); [5] (page 4); [16] (page 5);
[14] (page 6); [7, Question 3.2] → `@detail`, [9], [15], [10, 11] (page 8).  A bracket
with several numbers becomes one `xref` with space-separated `@ref` values.

## 7. Figure

Figure 1 is a vector drawing on PDF page 4 (printed page 3): nine vertices, eighteen
edges, the Paley graph on GF(9) as the text explains (center vertex 0, powers of x
clockwise from the top).  Crop with
`pdftocairo -svg|-pdf -f 4 -l 4 -r 72 -x 76 -y 56 -W 460 -H 259 -paperw 460 -paperh 259`
(ink box 79.2–532.8 × 59.5–311.5 points, widened three points); the caption starts at
y = 312 and is excluded.  File `figure-paley-nine-vertices` (both formats), `image` with a
`description` written from the drawing.  Not composite.

**Recreated in PreFigure (2026-09-04).**  The `image` now holds a `prefigure` diagram
(`network` with nine placed nodes and sixteen straight edges, plus two `path`s with a
quadratic Bézier for the edges between opposite corners, which the drawing bows to the
left of the center); the cropped original stays in `external/` as the reference.  The
drawing's line segments, parsed from the cropped SVG (whose paths carry a transform that
flips the y-axis), match the computed Paley graph exactly with the powers of <m>x</m>
placed clockwise from the top, as the prose says.  Generated assets in
`generated/prefigure/` (SVG with diagcess annotations for HTML, PDF for LaTeX).

## 8. Unreadable

Nothing.  Eleven spots were checked at 300 dpi (thin-spaced numbers, "et.al.", the
bold Aut, the binomial, both set-builder lines, the three displays, the empty-set glyph).

## 9. Text conventions for pass 2

**Verbatim quirks to preserve** (no typo correction):

- page 2: "Luo, <em>et.al.</em> [13]"; "Sach's results" twice; "the “best” graphs"
- page 3: "Fig. 1" in the caption vs "Figure 1" in prose (PreTeXt decides the label)
- page 5: "is a automorphism of"; "Rao, that shows that"
- page 6: "the order of <m>G_v</m> Thus, a Sylow" (no period); "For any <m>p</m>-group, <m>P</m> of <m>G</m>, define"; "p−group" with a minus inside the formula
- page 8: "Preisert [15]" (the reference says Peisert); "( {u, v}, {w, x} ∈ E(Γ) )" with the spaces inside the parentheses; "1-arc-transitive"
- references: "homogenous" [11]; "757-761" [11]; "Selbstcomplementäre" [22]; "Hedrlín" [1] (the text layer's combining accent is repaired to the precomposed letter — a rendering, not a change)
- line-end hyphenations to repair: tran-sitive, self-com-plementary, Theo-rem, de-signs, elemen-tary, illus-trating, re-ducible, guar-anteed, combinato-rial, self-complement-ary, con-structions, comple-menting, lexico-graphic, tran-sitive, homo-geneous, Math-ematical.  Keep the real hyphens: self-complementary, vertex-transitive (in titles), non-empty, non-zero, non-identity, number-theoretic, strongly-regular, error-correcting, 1-arc-transitive, two-element, p-group, p-subgroup, vertex-induced.

**Typography → elements:**

- Italic definitions → `term`: vertex transitive, self-complementary (page 1); circulant
  (page 2); graph, vertices, edges, automorphism, complementing map (page 3); vertex
  transitive, self-complementary (upright inside Definitions 2.1, 2.2); lexicographic
  product (Definition 4.1); symmetric, homogeneous factorization (page 8).
- Italic stress → `em`: et.al. (page 2); cyclic (page 8).
- Bold in mathematics: `\mathbf{Aut(\Gamma)}` once (page 3).
- Double quotes → `q`: “best”, “Sylow subgraphs.”  No single quotes.
- "Proof" headings → `proof` (no title).  The hollow box is PreTeXt's own.
- "Acknowledgment." → `paragraphs/title`; the two sentences are one `p`.
- "Email:" label dropped; `email` carries the address.
