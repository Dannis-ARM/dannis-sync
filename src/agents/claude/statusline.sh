#!/bin/bash

input=$(cat)
MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(echo "$input" | jq -r '.workspace.current_dir')
BRANCH=$(echo "$input" | jq -r '.workspace.git_worktree // ""')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
INPUT_TOKENS=$(echo "$input" | jq -r '.context_window.current_usage.input_tokens // 0')
OUTPUT_TOKENS=$(echo "$input" | jq -r '.context_window.current_usage.output_tokens // 0')
CACHE_WRITE=$(echo "$input" | jq -r '.context_window.current_usage.cache_creation_input_tokens // 0')
CACHE_READ=$(echo "$input" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0')

GIT_PART=""
[ -n "$BRANCH" ] && GIT_PART=" 🌿 ${BRANCH}"
echo "[${MODEL}] 📁 ${DIR##*/}${GIT_PART}"

FILLED=$(( PCT * 20 / 100 ))
EMPTY=$(( 20 - FILLED ))
BAR=$(printf '%0.s█' $(seq 1 $FILLED 2>/dev/null))$(printf '%0.s░' $(seq 1 $EMPTY 2>/dev/null))

TOKEN_PART=""
[ "$INPUT_TOKENS" != "0" ] || [ "$OUTPUT_TOKENS" != "0" ] && {
  TOKEN_PART=" | in:${INPUT_TOKENS} out:${OUTPUT_TOKENS}"
  [ "$CACHE_WRITE" != "0" ] && TOKEN_PART="${TOKEN_PART} +cache:${CACHE_WRITE}"
  [ "$CACHE_READ" != "0" ] && TOKEN_PART="${TOKEN_PART} -cache:${CACHE_READ}"
}

echo "${BAR} ${PCT}%${TOKEN_PART}"
