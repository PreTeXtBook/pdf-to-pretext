# Sourced by the other scripts, not run.  Finds the skill's own directory and PreTeXt.
#
#   PRETEXT_HOME    a clone of PreTeXtBook/pretext; the script is its pretext/pretext
#   PRETEXT_PYTHON  the Python (3.10 or newer) that runs the script, with PreTeXt's
#                   requirements installed (pretext/requirements.txt in the clone)
#
# Nobody has to set these.  setup.sh gets a clone and builds a Python environment in
# the skill's own data directory (~/.local/share/pdf-to-pretext), and they are found
# there.  To use a clone or a Python of your own instead, name them in the environment,
# or as two shell assignments in the file config.local in the skill's directory.
# The order: the environment; config.local; a directory "pretext" beside the repository
# that holds the skill; the data directory; and, for the Python, plain python3.
# The skill's directory is found through symbolic links, so the skill may be a copy or a
# link in ~/.claude/skills.
skill=$(python3 -c 'import os, sys; print(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[1]))))' "${BASH_SOURCE[0]}")
data=${XDG_DATA_HOME:-$HOME/.local/share}/pdf-to-pretext
home_from_environment=${PRETEXT_HOME:-}
python_from_environment=${PRETEXT_PYTHON:-}
if [ -f "$skill/config.local" ]; then
    . "$skill/config.local"
fi
PRETEXT_HOME=${home_from_environment:-${PRETEXT_HOME:-}}
PRETEXT_PYTHON=${python_from_environment:-${PRETEXT_PYTHON:-}}
if [ -z "$PRETEXT_HOME" ]; then
    if [ -f "$skill/../../pretext/pretext/pretext" ]; then
        PRETEXT_HOME=$(cd "$skill/../../pretext" && pwd)
    elif [ -f "$data/pretext/pretext/pretext" ]; then
        PRETEXT_HOME=$data/pretext
    fi
fi
# whether somebody named a Python, or it is ours to provide
python_named=yes
if [ -z "$PRETEXT_PYTHON" ]; then
    python_named=no
    if [ -x "$data/venv/bin/python3" ]; then
        PRETEXT_PYTHON=$data/venv/bin/python3
    else
        PRETEXT_PYTHON=python3
    fi
fi
export PRETEXT_HOME PRETEXT_PYTHON

# Stop with directions when PreTeXt cannot be run from what was found.
require_pretext() {
    if [ -z "$PRETEXT_HOME" ] || [ ! -f "$PRETEXT_HOME/pretext/pretext" ]; then
        echo "PreTeXt was not found${PRETEXT_HOME:+ at $PRETEXT_HOME}.  Run $skill/scripts/setup.sh, which gets it." >&2
        exit 2
    fi
}

# Run the PreTeXt script with the arguments given.
pretext_script() {
    "$PRETEXT_PYTHON" "$PRETEXT_HOME/pretext/pretext" "$@"
}

# A transcription's two files, from a project directory laid out as the skill lays it out.
project_files() {
    main=$1/source/main.ptx
    publication=$1/publication/publication.ptx
    if [ ! -f "$main" ] || [ ! -f "$publication" ]; then
        echo "$1 is not a transcription project: it needs source/main.ptx and publication/publication.ptx" >&2
        exit 2
    fi
}
