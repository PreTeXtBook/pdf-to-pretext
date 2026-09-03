# pdf-to-pretext

Transcribing research articles in mathematics from PDF into PreTeXt, first by hand with
Claude Code, then as a distributable Skill (`skill/pdf-to-pretext/`) refined on a corpus of
documents with known answers.  Local only for now.

- `CLAUDE.md` — the rules and decisions that govern the work
- `TRANSITION.md` — where things stand, for the next session
- `skill/` — the deliverable: `SKILL.md`, reference files, scripts
- `corpus/` — test documents (`MANIFEST.md` lists origin and license; PDFs and sources
  are fetched by script and not committed)
- `runs/` — one directory per transcription attempt, not committed
- `evaluation/RESULTS.md` — scores over time
- `templates/` — starting points for a transcription's `main.ptx` and `publication.ptx`
- `pretext/` — a clone of PreTeXtBook/pretext used for validation and builds, not committed
