#!/bin/bash

input=$(cat)

model_name=$(echo "$input" | jq -r '.model.display_name // "Claude"')
current_dir=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // ""')
ctx_size=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')

# Self-calculate from current_usage for accurate percentage on 1M models.
# The pre-calculated used_percentage can get stuck (e.g., stays at 80% on 1M
# models even after context shrinks) until session restart.
current_usage_null=$(echo "$input" | jq -r '.context_window.current_usage == null')
if [ "$current_usage_null" = "false" ]; then
    cur_input=$(echo "$input" | jq -r '.context_window.current_usage.input_tokens // 0')
    cur_cache_create=$(echo "$input" | jq -r '.context_window.current_usage.cache_creation_input_tokens // 0')
    cur_cache_read=$(echo "$input" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0')
    used_tokens=$((cur_input + cur_cache_create + cur_cache_read))
    used_pct=$(awk -v u="$used_tokens" -v s="$ctx_size" 'BEGIN {printf "%.1f", u / s * 100}')
else
    raw_pct=$(echo "$input" | jq -r '.context_window.used_percentage // 0')
    used_pct=$(awk -v p="$raw_pct" 'BEGIN {printf "%.1f", p + 0}')
    used_tokens=$(awk -v p="$raw_pct" -v s="$ctx_size" 'BEGIN {printf "%d", p * s / 100}')
fi

used_pct_int=${used_pct%%.*}
[ -z "$used_pct_int" ] && used_pct_int=0

# Format tokens as human-readable (26.4k, 1.2M)
if [ "$used_tokens" -ge 1000000 ]; then
    token_str=$(awk -v t="$used_tokens" 'BEGIN {printf "%.1fM", t / 1000000}')
elif [ "$used_tokens" -ge 1000 ]; then
    token_str=$(awk -v t="$used_tokens" 'BEGIN {printf "%.1fk", t / 1000}')
else
    token_str="${used_tokens}"
fi

dir_name=$(basename "${current_dir:-$(pwd)}")

# Git branch (skip optional locks for performance)
git_info=""
if [ -n "$current_dir" ] && git -C "$current_dir" rev-parse --git-dir > /dev/null 2>&1; then
    branch=$(git -C "$current_dir" --no-optional-locks symbolic-ref --short HEAD 2>/dev/null || \
             git -C "$current_dir" --no-optional-locks rev-parse --short HEAD 2>/dev/null)
    [ -n "$branch" ] && git_info="\033[35m ($branch)\033[0m"
fi

if [ "$used_pct_int" -ge 80 ]; then
    ctx_color='\033[91m'
elif [ "$used_pct_int" -ge 50 ]; then
    ctx_color='\033[33m'
else
    ctx_color='\033[32m'
fi

# Layout: 🤖 model | 📁 dir (branch) | ⚡ pct% · Xk tokens
echo -e "\033[32m🤖 ${model_name}\033[0m \033[2m|\033[0m \033[36m📁 ${dir_name}\033[0m${git_info} \033[2m|\033[0m ${ctx_color}⚡ ${used_pct}%\033[0m \033[2m·\033[0m ${ctx_color}${token_str} tokens\033[0m"
