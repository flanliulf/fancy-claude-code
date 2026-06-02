---
name: review-edge-case-hunter-en
description: Exhaustively enumerate every branching path and boundary condition in code diffs, files, or functions, reporting only unhandled edge cases as a JSON array. Use when user mentions 'edge case', 'edge case hunter', 'boundary conditions', 'path analysis', 'unhandled cases', 'exhaustive review', '边界条件', '边缘情况', '路径分析', '未处理情况', '边界审查', '穷举分析', or needs orthogonal mechanical path-tracing review. Capable of scanning diffs, full files, and functions; outputs structured JSON with location, trigger condition, guard snippet, and potential consequence for each finding.
allowed-tools: Read, Grep, Glob
metadata:
  version: "1.0.0"
---

[Skill Description]
    A pure path tracer — mechanically walk every branching path and boundary condition in code diffs, full files, or functions. Report only unhandled edge cases as a structured JSON array. Orthogonal to adversarial review: method-driven, not attitude-driven.

[Core Capabilities]
    - **Exhaustive Path Enumeration**: Mechanically walk all branch paths and boundary conditions — no intuition-based guessing
    - **Diff-Scoped Analysis**: When a diff is provided, scan only diff hunks and report only boundaries directly reachable from changed lines that lack an explicit guard
    - **Full File / Function Mode**: When no diff is provided, treat the entire provided content as the scope
    - **Report Only Unhandled Paths**: Handled paths are silently discarded — zero noise in output
    - **Structured JSON Output**: Each finding contains location, trigger_condition, guard_snippet, and potential_consequence
    - **Optional Domain Focus**: Accept `also_consider` parameter to incorporate specified areas into analysis
    - **Completeness Re-validation**: Step 3 revisits every edge class from Step 2 to ensure nothing was missed

[Execution Flow]
    Sequential workflow, 4 steps. Order is mandatory — no skipping, no reordering.

    Step 1: Receive Content
        1. Load the content to review strictly from user-provided input
        2. If content is empty or cannot be decoded as text, return the following JSON and stop:
           [{"location":"N/A","trigger_condition":"Input empty or undecodable","guard_snippet":"Provide valid content to review","potential_consequence":"Review skipped — no analysis performed"}]
        3. Identify content type (code diff / full file / function) to determine scope rules:
           - diff → analyze only boundaries directly reachable within diff hunks
           - full file / function → treat entire content as scope

    Step 2: Exhaustive Path Analysis
        Walk every branching path and boundary condition within scope — report only unhandled ones.

        1. If `also_consider` input was provided, incorporate those areas into the analysis
        2. Walk all branching paths:
           - Control flow: conditionals (if/else/switch), loops, error handlers, early returns
           - Domain boundaries: where values, states, or conditions transition
        3. Derive the relevant edge classes from the content itself — don't rely on a fixed checklist. Examples:
           - Missing else/default branch
           - Unguarded inputs (null, empty, out-of-range)
           - Off-by-one loops
           - Arithmetic overflow
           - Implicit type coercion
           - Race conditions
           - Timeout gaps
        4. For each path: determine whether the content handles it
        5. Collect only unhandled paths as findings — discard handled ones silently

    Step 3: Validate Completeness
        1. Revisit every edge class identified in Step 2
        2. Add any newly found unhandled paths to findings; discard confirmed-handled ones
        3. Ensure output is complete — no edge class categories were missed

    Step 4: Present Findings
        1. Output a valid JSON array only. Each object must contain exactly these four fields:
           - location: file:start-end (or file:line when single line, or file:hunk when exact line unavailable)
           - trigger_condition: one-line description (max 15 words)
           - guard_snippet: minimal code sketch that closes the gap (single-line escaped string, no raw newlines or unescaped quotes)
           - potential_consequence: what could actually go wrong (max 15 words)
        2. No extra text, no explanations, no markdown wrapping
        3. An empty array [] is valid when no unhandled paths are found

[Notes]
    - Step execution order is mandatory — no skipping or reordering
    - Only trace paths and boundary conditions — do not comment on whether code is good or bad
    - Handled paths must be silently discarded and must not appear in output
    - Output is a pure JSON array only — no wrapping or additional text
    - An empty array [] is a valid result indicating all paths within scope are handled
    - This Skill is orthogonal to adversarial review (review-adversarial-general-en) — use both together for comprehensive coverage
