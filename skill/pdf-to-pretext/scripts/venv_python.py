"""Let a script of this skill find the modules it needs.

A script that uses numpy, scipy, or Pillow calls ensure() before importing them.  When
the Python that started the script lacks one, the script is started again under the
skill's own Python: the one named by PRETEXT_PYTHON, or in config.local, or built by
setup.sh in the skill's data directory.  So the scripts can be run by name, whichever
python3 is first on the path.
"""
import importlib.util
import os
import re
import sys


def skill_python():
    if os.environ.get("PRETEXT_PYTHON"):
        return os.environ["PRETEXT_PYTHON"]
    skill = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    try:
        named = re.search(r"^PRETEXT_PYTHON=(.+)$", open(os.path.join(skill, "config.local")).read(), re.M)
        if named:
            return named.group(1).strip().strip("\"'")
    except OSError:
        pass
    data = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    return os.path.join(data, "pdf-to-pretext", "venv", "bin", "python3")


def ensure(*modules):
    if all(importlib.util.find_spec(m) is not None for m in modules):
        return
    python = skill_python()
    # the Python of an environment is a link to the system's, so compare the names as
    # given, not what they resolve to; the variable stops a second restart
    if os.path.exists(python) and os.path.abspath(python) != os.path.abspath(sys.executable) \
            and not os.environ.get("PDF_TO_PRETEXT_RESTARTED"):
        os.environ["PDF_TO_PRETEXT_RESTARTED"] = "1"
        os.execv(python, [python] + sys.argv)
    sys.exit("This script needs the Python modules {}.  Run scripts/setup.sh, which installs them.".format(
        ", ".join(modules)))
