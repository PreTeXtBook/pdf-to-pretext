# Block classes (generated from `xsl/entities.ent`)

Regenerate with `scripts/block-classes.py pretext/xsl/entities.ent references/block-classes.md` after a `git pull` of the clone.

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

- Theorem, Lemma, Corollary, Proposition, Claim, Fact, Algorithm: the theorem class, with `statement` and `proof` children.
- Definition: `definition`.  Conjecture, Principle, Hypothesis, Assumption, Axiom: the axiom class (a statement never followed by a proof).
- Remark, Note, Observation, Warning, Convention: the remark class.  A `Notation` environment is usually a `convention` (or a `remark` titled Notation).
- Example, Question, Problem: the example class.  An open research question or conjecture posed as such: the openproblem class.
- A named result ("Theorem 2.1 (Main Theorem)") keeps the name as its `title`; "Proof of Theorem 3" is a `proof` with that `title`.
- Verify each element against `pretext/schema/pretext.rnc` before use.
