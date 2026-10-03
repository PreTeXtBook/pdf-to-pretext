#!/bin/bash
# Get this skill ready to work on this machine, asking nothing.
#
# Usage: setup.sh            (run it again before a new transcription: it updates PreTeXt)
#
# What it does, all inside the skill's data directory, ~/.local/share/pdf-to-pretext
# (or $XDG_DATA_HOME/pdf-to-pretext), and nowhere else:
#   - gets a clone of PreTeXtBook/pretext if no PreTeXt is found, or updates the clone it
#     got before;
#   - builds a Python environment there with PreTeXt's requirements and the packages the
#     figure scripts use (numpy, scipy, Pillow), and keeps it in step with the clone.
# A clone or a Python you named yourself (the environment, or config.local in the
# skill's directory) is used as it is and never changed.
#
# What it cannot do is install programs for the whole machine: the poppler tools, a TeX
# distribution, MuPDF's tools.  It ends with check-setup.sh, which names any of those
# that are missing and the command that installs them.
set -u
. "$(dirname "$0")/pretext-location.sh"
repository=${PRETEXT_REPOSITORY:-https://github.com/PreTeXtBook/pretext}
mkdir -p "$data"

if [ -z "$PRETEXT_HOME" ]; then
    echo "Getting PreTeXt into $data/pretext (a clone of $repository) ..."
    if git clone --quiet --depth 1 "$repository" "$data/pretext"; then
        PRETEXT_HOME=$data/pretext
    else
        echo "The clone failed.  Is git installed, and is the network reachable?"
        exit 1
    fi
elif [ "$PRETEXT_HOME" = "$data/pretext" ]; then
    echo "Updating PreTeXt in $data/pretext ..."
    git -C "$PRETEXT_HOME" pull --quiet --ff-only || echo "  (the update failed; carrying on with the clone as it is)"
else
    echo "Using your own PreTeXt at $PRETEXT_HOME; this script does not update it."
fi
echo "PreTeXt is at commit $(git -C "$PRETEXT_HOME" rev-parse --short HEAD 2>/dev/null || echo unknown)."

venv=$data/venv
runs() { "$1" "$PRETEXT_HOME/pretext/pretext" -h > /dev/null 2>&1; }
install() {
    # pip inside the environment, or, where Python was packaged without ensurepip
    # (Debian, Ubuntu), a pip from outside told to install into it
    if "$venv/bin/python3" -m pip --version > /dev/null 2>&1; then
        "$venv/bin/python3" -m pip install --quiet --disable-pip-version-check "$@"
    else
        python3 -m pip --python "$venv/bin/python3" install --quiet --disable-pip-version-check "$@"
    fi
}
if [ "$python_named" = yes ]; then
    # a Python somebody named is theirs to keep in order
    if runs "$PRETEXT_PYTHON"; then
        echo "Using the Python you named, $PRETEXT_PYTHON: it runs PreTeXt."
    else
        echo "The Python you named, $PRETEXT_PYTHON, does not run PreTeXt.  Install into it"
        echo "$PRETEXT_HOME/pretext/requirements.txt, or take its name out of the environment"
        echo "and of $skill/config.local, and this script will build one."
        exit 1
    fi
else
    # whatever python3 is on the path may run PreTeXt's help and still lack half of its
    # requirements, so the skill keeps an environment of its own
    if [ ! -x "$venv/bin/python3" ]; then
        echo "Building a Python environment in $venv ..."
        python3 -m venv "$venv" > /dev/null 2>&1 || python3 -m venv --clear --without-pip "$venv" || {
            echo "Python could not make an environment (python3 -m venv failed)."
            exit 1
        }
        echo "Installing what PreTeXt and the figure scripts need into it (a few minutes) ..."
    else
        echo "Bringing the Python environment in $venv up to date ..."
    fi
    if install -r "$PRETEXT_HOME/pretext/requirements.txt" numpy scipy pillow; then
        PRETEXT_PYTHON=$venv/bin/python3
    else
        echo "The installation failed.  Without pip this script cannot fill the environment:"
        echo "install pip for python3 (python3-pip, or python3-venv, on Debian and Ubuntu) and run it again."
        exit 1
    fi
fi
export PRETEXT_HOME PRETEXT_PYTHON
exec "$(dirname "$0")/check-setup.sh" "$@"
