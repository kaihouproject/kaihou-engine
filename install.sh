#!/usr/bin/env bash
set -euo pipefail

# One‑shot installer for Kaihou Engine
# Steps:
# 1. Prepare virtualenv
# 2. Activate and install package (editable) from pyproject.toml
# 3. Initialize submodules
# 4. Install spaCy language models (en, fr, es)
# 5. Completion message

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$REPO_DIR/.venv"

echo -e "\n👣 Step 1/5: Preparing virtual environment"
mkdir -p "$VENV_DIR"

if [ -d "$VENV_DIR" ]; then
  echo "✅ Virtual environment already exists"
else
  echo -e "\n🐍 Creating virtual environment"
  python3 -m venv "$VENV_DIR"
fi

echo -e "\n🔧 Step 2/5: Activating and installing package"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -e "$REPO_DIR"

# Initialize submodules if any
if git rev-parse --git-dir > /dev/null 2>&1; then
  echo -e "\n🔧 Step 3/5: Initializing submodules"
  git submodule update --init --recursive
fi

# Install spaCy models
declare -A MODELS=(
  [en]="en_core_web_sm"
  [fr]="fr_core_news_sm"
  [es]="es_core_news_sm"
)

echo -e "\n🧠 Step 4/5: Installing spaCy models"
for LANG in "${!MODELS[@]}"; do
  MODEL="${MODELS[$LANG]}"
  if python - <<'PY'
import importlib.util, sys
sys.exit(0 if importlib.util.find_spec('$MODEL') else 1)
PY
  ; then
    echo "✅ Model $MODEL already installed"
  else
    echo "📥 Downloading model $MODEL..."
    python -m spacy download "$MODEL"
  fi
done

echo -e "\n✅ Installation complete. Activate the environment with: source $VENV_DIR/bin/activate"
