# Sourced by the other scripts, not run.  Finds the skill's own directory and PreTeXt.
#
#   PRETEXT_HOME    a clone of PreTeXtBook/pretext; the script is its pretext/pretext
#   PRETEXT_PYTHON  the Python (3.10 or newer) that runs the script, with PreTeXt's
#                   requirements installed (pretext/requirements.txt in the clone)
#
# Each is taken from the environment; else from the file config.local in the skill's
# directory (two shell assignments, see check-setup.sh); else from a default: a directory
# "pretext" beside the repository that holds the skill, and plain python3.
# The skill's directory is found through symbolic links, so the skill may be installed
# as a link into ~/.claude/skills.
skill=$(python3 -c 'import os, sys; print(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[1]))))' "${BASH_SOURCE[0]}")
home_from_environment=${PRETEXT_HOME:-}
python_from_environment=${PRETEXT_PYTHON:-}
if [ -f "$skill/config.local" ]; then
    . "$skill/config.local"
fi
PRETEXT_HOME=${home_from_environment:-${PRETEXT_HOME:-}}
PRETEXT_PYTHON=${python_from_environment:-${PRETEXT_PYTHON:-python3}}
if [ -z "$PRETEXT_HOME" ] && [ -f "$skill/../../pretext/pretext/pretext" ]; then
    PRETEXT_HOME=$(cd "$skill/../../pretext" && pwd)
fi

# Stop with directions when PreTeXt cannot be run from what was found.
require_pretext() {
    if [ -z "$PRETEXT_HOME" ] || [ ! -f "$PRETEXT_HOME/pretext/pretext" ]; then
        echo "PreTeXt was not found${PRETEXT_HOME:+ at $PRETEXT_HOME}." >&2
        echo "Clone https://github.com/PreTeXtBook/pretext and name the clone in" >&2
        echo "$skill/config.local, as check-setup.sh describes." >&2
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
