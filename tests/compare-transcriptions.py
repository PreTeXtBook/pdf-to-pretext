#!/usr/bin/env python3
r"""Compare a transcription with a key: structure, words, and mathematics.

Usage: compare-transcriptions.py <transcription/source/main.ptx> <key/source/main.ptx> [<directory>]

For scoring the skill against a document whose right answer is known: a round-trip case
(corpus/round-trip), where the key is the PreTeXt the PDF was built from, or a document
transcribed a second time from its source.  It prints three results.

  STRUCTURE  the sequence of sections, blocks, proofs, paragraphs, displays, and
             bibliography entries, and what each cross-reference points at.  Identifiers
             are not compared (a transcription invents its own); a target is named by
             its kind and its place in the document, "theorem 2", "biblio 5".
  WORDS      the running text, each formula counted as one token.
  FORMULAS   paired in order, then compared three ways: character for character; as TeX
             tokens; and after the equivalences below, each of which leaves the typeset
             mathematics unchanged or changes only its spacing.  What still differs is
             listed, and is what to read.

The equivalences, applied to both sides in this order:
  the document's own macros (docinfo/macros) expanded;
  \le and \leq, \ge and \geq, \ne and \neq, \lVert and \rVert and \|, \ast and *,
      \tfrac and \dfrac and \frac;
  \ldots and \cdots and \dots;
  \text{word}, \mathrm{word}, \operatorname{word} for a word of letters;
  spacing commands (~, \ , \, \; \! \quad \qquad) removed;
  \left and \right removed;
  braces around a one-token subscript or superscript, around a one-token argument of
      \mathbf and its kin, and around a group that is no command's argument;
  x^a_b written x_b^a.

With a directory as the third argument it also writes there both documents one sentence
or display to a line (canonical-*.txt, as-written.diff) and again after the equivalences
(normalized-*.txt, normalized.diff).
"""
import difflib
import os
import re
import sys
from lxml import etree

XML = "{http://www.w3.org/XML/1998/namespace}"
STRUCTURAL = ["section", "subsection", "subsubsection", "paragraphs", "theorem", "lemma", "corollary",
              "proposition", "claim", "fact", "definition", "remark", "example", "conjecture",
              "observation", "note", "convention", "question", "problem", "statement", "proof",
              "figure", "table", "sidebyside", "image", "tabular", "ol", "ul", "li", "fn",
              "p", "md", "mrow", "title", "references", "biblio", "author", "date", "abstract"]
TARGETS = STRUCTURAL + ["article"]


def load(path):
    tree = etree.parse(path)
    tree.xinclude()
    for comment in tree.xpath("//comment()"):
        parent = comment.getparent()
        if parent is None:
            continue
        tail = comment.tail or ""
        previous = comment.getprevious()
        if previous is not None:
            previous.tail = (previous.tail or "") + tail
        else:
            parent.text = (parent.text or "") + tail
        parent.remove(comment)
    return tree


def targets(tree):
    """Name every element "kind ordinal", the ordinal counted among elements of that kind.

    Returns two tables: by xml:id, for what a cross-reference points at, and by element,
    for saying where a paragraph is.  A numbered display or row is an "equation".
    """
    by_id, by_element, count = {}, {}, {}
    for e in tree.iter():
        if not isinstance(e.tag, str):
            continue
        if e.tag in ("md", "mrow") and e.get("number") != "yes":
            label = "display"
        else:
            kind = "equation" if e.tag in ("md", "mrow") else e.tag
            count[kind] = count.get(kind, 0) + 1
            label = "{} {}".format(kind, count[kind])
        by_element[e] = label
        if e.get(XML + "id"):
            by_id[e.get(XML + "id")] = label
    return by_id, by_element


# ---- mathematics -------------------------------------------------------------------

def tokens(s):
    # a control space is written "\@space" so that no token contains a blank
    return [r"\@space" if x == "\\ " else x for x in re.findall(r"\\[A-Za-z]+|\\.|[^\s]", s)]


def group(t, i):
    """The argument that starts at t[i]: a brace group's contents, or one token."""
    if i < len(t) and t[i] == "{":
        depth, j = 0, i
        while j < len(t):
            depth += {"{": 1, "}": -1}.get(t[j], 0)
            if depth == 0:
                return t[i + 1:j], j + 1
            j += 1
    return t[i:i + 1], i + 1


def macros(tree):
    """The document's macros: name -> (number of arguments, body tokens)."""
    out = {}
    text = " ".join(m.text or "" for m in tree.iter("macros"))
    t, i = tokens(text), 0
    while i < len(t):
        if t[i] in (r"\newcommand", r"\renewcommand", r"\providecommand"):
            name, i = group(t, i + 1)
            count = 0
            if i + 2 < len(t) and t[i] == "[" and t[i + 2] == "]":
                count, i = int(t[i + 1]), i + 3
            body, i = group(t, i)
            if name:
                out[name[0]] = (count, body)
        elif t[i] == r"\DeclareMathOperator":
            i += 1
            if i < len(t) and t[i] == "*":
                i += 1
            name, i = group(t, i)
            body, i = group(t, i)
            if name:
                out[name[0]] = (0, [r"\operatorname", "{"] + body + ["}"])
        else:
            i += 1
    return out


def expand(t, table, depth=0):
    """Replace each use of a macro by its body, arguments substituted."""
    if not table or depth > 8:
        return t
    out, i, changed = [], 0, False
    while i < len(t):
        if t[i] in table:
            count, body = table[t[i]]
            i += 1
            arguments = []
            for _ in range(count):
                argument, i = group(t, i)
                arguments.append(argument)
            k = 0
            while k < len(body):
                if body[k] == "#" and k + 1 < len(body) and body[k + 1].isdigit():
                    argument = arguments[int(body[k + 1]) - 1] if int(body[k + 1]) <= len(arguments) else []
                    braced = k > 0 and body[k - 1] == "{" and k + 2 < len(body) and body[k + 2] == "}"
                    out += argument if braced or len(argument) == 1 else ["{"] + argument + ["}"]
                    k += 2
                else:
                    out.append(body[k])
                    k += 1
            changed = True
        else:
            out.append(t[i])
            i += 1
    return expand(out, table, depth + 1) if changed else out


SYNONYMS = {r"\le": r"\leq", r"\ge": r"\geq", r"\ne": r"\neq", r"\lVert": r"\|", r"\rVert": r"\|",
            r"\ast": "*", r"\tfrac": r"\frac", r"\dfrac": r"\frac"}


def r_synonyms(t):
    return [SYNONYMS.get(x, x) for x in t]


def r_ellipsis(t):
    return [r"\dots" if x in (r"\ldots", r"\cdots") else x for x in t]


def r_upright_names(t):
    out, i = [], 0
    while i < len(t):
        if t[i] in (r"\text", r"\mathrm", r"\operatorname") and i + 1 < len(t) and t[i + 1] == "{":
            inner, j = group(t, i + 1)
            if inner and all(len(x) == 1 and x.isalpha() for x in inner):
                out += [r"\operatorname", "{"] + inner + ["}"]
                i = j
                continue
        out.append(t[i])
        i += 1
    return out


def r_spacing(t):
    return [x for x in t if x not in ("~", r"\@space", r"\quad", r"\qquad", r"\,", r"\;", r"\!")]


def r_sizing(t):
    return [x for x in t if x not in (r"\left", r"\right")]


TAKES_ARGUMENT = {r"\mathbf", r"\mathbb", r"\mathrm", r"\mathcal", r"\mathfrak", r"\mathsf", r"\mathit",
                  r"\text", r"\operatorname", r"\sqrt", r"\hat", r"\bar", r"\tilde", r"\vec",
                  r"\overline", r"\widehat", r"\widetilde"}


def r_braces(t):
    r"""Three brace conventions that TeX treats alike, and no others.

    A subscript or superscript that is one token needs no braces; a one-token argument
    of \mathbf and its kin may have them or not (they are added); a group that is not an
    argument of anything (it follows neither a command, nor _ or ^, nor another group)
    only limits scope, and its braces are dropped.  \frac{1}{n-1} is left alone.
    """
    out, i = [], 0
    while i < len(t):
        if t[i] in ("_", "^") and i + 3 < len(t) and t[i + 1] == "{" and t[i + 3] == "}" and t[i + 2] not in "{}":
            out += [t[i], t[i + 2]]
            i += 4
        elif t[i] in TAKES_ARGUMENT and i + 1 < len(t) and t[i + 1] not in ("{", "["):
            out += [t[i], "{", t[i + 1], "}"]
            i += 2
        else:
            out.append(t[i])
            i += 1
    t, out, stack = out, [], []
    for x in t:
        if x == "{":
            previous = out[-1] if out else "{"
            bare = not (previous in ("_", "^", "}", "{") or re.fullmatch(r"\\[A-Za-z@]+", previous))
            stack.append(bare)
            if not bare:
                out.append(x)
        elif x == "}":
            if stack and not stack.pop():
                out.append(x)
        else:
            out.append(x)
    return out


def r_script_order(t):
    out, i = list(t), 0
    while i + 3 < len(out):
        if out[i] == "^" and out[i + 2] == "_" and out[i + 1] not in "{}" and out[i + 3] not in "{}":
            out[i:i + 4] = ["_", out[i + 3], "^", out[i + 1]]
            i += 4
        else:
            i += 1
    return out


RULES = [("the document's macros expanded", None),
         ("synonyms (\\le and \\leq, \\lVert and \\|, \\ast and *, \\tfrac and \\frac)", r_synonyms),
         ("ellipsis commands (\\dots, \\ldots, \\cdots)", r_ellipsis),
         ("upright names (\\text, \\mathrm, \\operatorname)", r_upright_names),
         ("spacing commands (~, \\ , \\quad)", r_spacing),
         ("\\left and \\right", r_sizing),
         ("redundant braces", r_braces),
         ("order of subscript and superscript", r_script_order)]


def normalize(s, table):
    t = expand(tokens(s), table)
    for _, rule in RULES[1:]:
        t = rule(t)
    return " ".join(t)


def formulas(tree):
    out = []
    for e in tree.iter("m", "md", "mrow"):
        if e.tag == "md" and e.find("mrow") is not None:
            continue
        if any(a.tag in ("description", "shortdescription") for a in e.iterancestors()):
            continue  # a description is the transcriber's own words
        out.append((e.tag, "".join(e.itertext())))
    return out


# ---- text --------------------------------------------------------------------------

def pointer(e, where):
    return " ".join(where.get(r, "?" + r) for r in (e.get("ref") or "").split()) or "?"


def inline(e, where, table):
    """The content of a text element as one string; table is None for "as written"."""
    def math(body):
        return normalize(body, table) if table is not None else re.sub(r"\s+", " ", body).strip()
    flat = lambda text: re.sub(r"\s+", " ", text or "")
    parts = [flat(e.text)]
    for c in e:
        if not isinstance(c.tag, str):
            parts.append(flat(c.tail))
            continue
        if c.tag == "m":
            parts.append("$" + math("".join(c.itertext())) + "$")
        elif c.tag == "md":
            rows = c.findall("mrow") or [c]
            parts.append("\n" + "\n".join("    $$ {} $${}".format(
                math("".join(r.itertext())), "   (numbered)" if r.get("number") == "yes" else "") for r in rows) + "\n")
        elif c.tag == "xref":
            parts.append("[" + pointer(c, where) + "]")
        elif c.tag in ("q", "sq"):
            parts.append("“" + inline(c, where, table) + "”")
        elif c.tag == "nbsp":
            parts.append(" " if table is not None else "~")
        elif c.tag == "ndash":
            parts.append("–")
        elif c.tag == "mdash":
            parts.append("—")
        elif c.tag == "line":
            parts.append(inline(c, where, table) + " / ")
        elif c.tag == "fn":
            parts.append(" {footnote: " + inline(c, where, table) + "} ")
        else:
            parts.append(inline(c, where, table))
        parts.append(flat(c.tail))
    return "".join(parts)


def context(e, where, places):
    while e is not None and e.tag not in ("article", "pretext"):
        if e.tag in ("section", "subsection", "paragraphs", "proof", "biblio", "figure", "table") \
                or e.tag in STRUCTURAL[4:19]:
            return places[e] + (" -> " + pointer(e, where) if e.get("ref") else "")
        e = e.getparent()
    return "front"


def nested(e):
    """A paragraph inside a paragraph (in a list item) is read as part of the outer one."""
    return any(a.tag in ("p", "biblio", "description") for a in e.iterancestors())


def canonical(tree, where, places, table):
    lines, last = [], None
    for e in tree.iter("title", "personname", "institution", "email", "date", "p", "caption", "cell", "biblio"):
        if e.tag == "biblio":
            lines.append("== {} [{}]".format(places[e], e.get("type")))
            for f in e:
                if not isinstance(f.tag, str):
                    continue
                if f.tag in ("author", "editor", "translator"):
                    names = "; ".join(" ".join(filter(None, (n.findtext("given"), n.findtext("family"),
                                                             n.findtext("literal")))) for n in f)
                    lines.append("    {}: {}".format(f.tag, names))
                elif f.tag in ("issued", "accessed"):
                    lines.append("    {}: {}".format(f.tag, " ".join(
                        "-".join(filter(None, (d.get("year"), d.get("month"), d.get("day")))) for d in f)))
                else:
                    lines.append("    {}: {}".format(f.tag, re.sub(r"\s+", " ", "".join(f.itertext())).strip()))
            continue
        if nested(e):
            continue
        here = context(e, where, places)
        if here != last:
            lines.append("== " + here)
            last = here
        for piece in inline(e, where, table).split("\n"):
            piece = re.sub(r"\s+", " ", piece).strip()
            if not piece:
                continue
            if piece.startswith("$$"):
                lines.append("    " + piece)
            else:
                label = "" if e.tag == "p" else e.tag + ": "
                for k, sentence in enumerate(re.split(r"(?<=[.?!])\s+(?=[A-Z(])", piece)):
                    lines.append((label if k == 0 else "") + sentence)
    return lines


def words(tree, where, table):
    out = []
    for e in tree.iter("title", "p", "caption", "cell"):
        if nested(e):
            continue
        s = inline(e, where, table)
        s = re.sub(r"\$\$.*?\$\$(\s*\(numbered\))?", " § ", s)
        s = re.sub(r"\$[^$]*\$", " § ", s)
        out += re.findall(r"\[[^\]]+\]|§|[^\s§\[\]]+", s)
    return out


def structure(tree, where):
    out = []
    for e in tree.iter(*STRUCTURAL):
        if e.tag == "p" and e.getparent().tag == "li":
            continue  # an item's text may sit in the "li" itself or in a "p" inside it
        if any(a.tag in ("description", "shortdescription") for a in e.iterancestors()):
            continue  # a description is the transcriber's own words
        item = e.tag
        if e.get("number") == "yes":
            item += " numbered"
        if e.get("ref"):
            item += " -> " + pointer(e, where)
        if e.tag == "biblio":
            item += " " + (e.get("type") or "")
        out.append(item)
    return out


def main(path_a, path_b, outdir=None):
    a, b = load(path_a), load(path_b)
    (where_a, places_a), (where_b, places_b) = targets(a), targets(b)
    table_a, table_b = macros(a), macros(b)

    sa, sb = structure(a, where_a), structure(b, where_b)
    print("STRUCTURE  {} and {} elements;".format(len(sa), len(sb)), "identical" if sa == sb else "DIFFERENT")
    if sa != sb:
        for line in list(difflib.unified_diff(sa, sb, "transcription", "key", lineterm="", n=1))[:60]:
            print("   ", line)
    ra = sorted(pointer(x, where_a) for x in a.iter("xref"))
    rb = sorted(pointer(x, where_b) for x in b.iter("xref"))
    print("           cross-references: {} and {};".format(len(ra), len(rb)),
          "the same targets" if ra == rb else "DIFFERENT targets")
    unresolved = [r for r in ra if "?" in r]
    if unresolved:
        print("           unresolved in the transcription: " + ", ".join(unresolved))

    wa, wb = words(a, where_a, table_a), words(b, where_b, table_b)
    matcher = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
    changes = [op for op in matcher.get_opcodes() if op[0] != "equal"]
    print("WORDS      {} and {} tokens of running text (a formula counts as one);".format(len(wa), len(wb)),
          "identical" if not changes else "{} place(s) differ".format(len(changes)))
    for tag, i1, i2, j1, j2 in changes[:40]:
        print("    transcription: {!r}   key: {!r}   (after: {})".format(
            " ".join(wa[i1:i2]), " ".join(wb[j1:j2]), " ".join(wa[max(0, i1 - 5):i1])))

    fa, fb = formulas(a), formulas(b)
    na = [normalize(f[1], table_a) for f in fa]
    nb = [normalize(f[1], table_b) for f in fb]
    matcher = difflib.SequenceMatcher(None, na, nb, autojunk=False)
    pairs, unmatched = [], []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            pairs += list(zip(range(i1, i2), range(j1, j2)))
        else:
            unmatched.append((tag, [fa[i][1].strip() for i in range(i1, i2)], [fb[j][1].strip() for j in range(j1, j2)]))
    print("FORMULAS   {} and {}; {} paired".format(len(fa), len(fb), len(pairs)))
    print("           identical character for character: {}".format(
        sum(1 for i, j in pairs if fa[i][1].strip() == fb[j][1].strip())))
    current = [(tokens(fa[i][1]), tokens(fb[j][1])) for i, j in pairs]
    print("           identical as TeX tokens: {}".format(sum(1 for x, y in current if x == y)))
    for k, (name, rule) in enumerate(RULES):
        if k == 0:
            current = [(expand(x, table_a), expand(y, table_b)) for x, y in current]
        else:
            current = [(rule(x), rule(y)) for x, y in current]
        print("             after {:<74} {:>4}".format(name + ":", sum(1 for x, y in current if x == y)))
    residual = [(fa[i][1].strip(), fb[j][1].strip()) for (i, j), (x, y) in zip(pairs, current) if x != y]
    equivalent = len(pairs) - len(residual)
    print("           equivalent: {} of {} paired; still different: {}; in one document only: {}".format(
        equivalent, len(pairs), len(residual), sum(len(x) + len(y) for _, x, y in unmatched)))
    for x, y in residual:
        print("             transcription: {}\n             key:           {}".format(
            re.sub(r"\s+", " ", x), re.sub(r"\s+", " ", y)))
    for tag, x, y in unmatched:
        print("             only in the transcription: {}   only in the key: {}".format(x, y))

    if outdir:
        os.makedirs(outdir, exist_ok=True)
        for table_pair, stem, name in (((None, None), "canonical", "as-written.diff"),
                                       ((table_a, table_b), "normalized", "normalized.diff")):
            ca = canonical(a, where_a, places_a, table_pair[0])
            cb = canonical(b, where_b, places_b, table_pair[1])
            open(os.path.join(outdir, stem + "-transcription.txt"), "w").write("\n".join(ca) + "\n")
            open(os.path.join(outdir, stem + "-key.txt"), "w").write("\n".join(cb) + "\n")
            diff = list(difflib.unified_diff(ca, cb, "transcription", "key", lineterm="", n=1))
            open(os.path.join(outdir, name), "w").write("\n".join(diff) + "\n")
            print("{:<10} {}: {} changed line(s)".format(
                "FILES" if stem == "canonical" else "", os.path.join(outdir, name),
                sum(1 for d in diff if d[:1] in "+-" and d[:3] not in ("+++", "---"))))


if __name__ == "__main__":
    main(*sys.argv[1:4])
