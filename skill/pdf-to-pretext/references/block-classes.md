# Block classes (generated from `xsl/entities.ent`)

PreTeXt's own list of which elements behave alike.  (For maintainers: regenerate with `scripts/block-classes.py <clone>/xsl/entities.ent references/block-classes.md` when the clone has moved.)

| class | elements |
|---|---|
| definition | `definition` |
| theorem | `theorem`, `corollary`, `lemma`, `algorithm`, `proposition`, `claim`, `fact`, `identity` |
| proof | `proof`, `argument`, `justification`, `reasoning`, `explanation` |
| axiom | `axiom`, `conjecture`, `principle`, `heuristic`, `hypothesis`, `assumption` |
| remark | `remark`, `convention`, `note`, `observation`, `warning`, `insight` |
| computation | `computation`, `technology`, `data` |
| aside | `aside`, `biographical`, `historical` |
| example | `example`, `question`, `problem` |
| project | `project`, `activity`, `exploration`, `investigation` |
| goal | `objectives`, `outcomes` |
| openproblem | `openproblem`, `openquestion`, `openconjecture` |
| figure | `figure`, `table`, `listing`, `list` |
| solution | `hint`, `answer`, `solution` |
| discussion | `context`, `discussion`, `opinion`, `status`, `suggestion` |

## Mapping a paper's environments

- Theorem, Lemma, Corollary, Proposition, Claim, Fact, Algorithm: the theorem class, with a `statement` and then its `proof`s.
- Definition: `definition`, with a `statement`.  Conjecture, Principle, Hypothesis, Assumption, Axiom: the axiom class (a `statement` never followed by a proof).
- Remark, Note, Observation, Warning, Convention: the remark class, which holds its paragraphs directly, with no `statement`.  A `Notation` environment is usually a `convention` (or a `remark` titled Notation).
- Example, Question, Problem: the example class, which may hold its paragraphs directly or a `statement`.  An open research question or conjecture posed as such: the openproblem class.
- A named result ("Theorem 2.1 (Main Theorem)") keeps the name as its `title`; "Proof of Theorem 3", set apart from its theorem, is a `proof` whose `@ref` names the theorem.
- Verify each element against `schema/pretext.rnc` in the PreTeXt clone before use.
