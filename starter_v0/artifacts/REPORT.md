# Day 04 Lab v2 Report — Research Agent

## Team

- **Team**: Zone 8 - Team 5
Nguyễn Thành Lộc - 2A202600817
Đặng Tiến Quyền - 2A202600896
Trần Trung Kiên - 2A202600850
- **Provider/model**: OpenRouter / `openai/gpt-4o-mini`

## Final Metrics

- **Final version**: v3
- **Final artifact_version**: `v3+pe658de69e113+t3c77e0a487fa`
- **Best base run file**: `runs/v3_B_base_openrouter_20260602T135319192847.json`
- **Base case accuracy**: 1.0 (100%)
- **Base tool routing accuracy**: 1.0 (100%)
- **Base argument accuracy**: 1.0 (100%)
- **Group eval run file**: `runs/v3_B_group_openrouter_20260602T135538897538.json`
- **Group eval accuracy**: 1.0 (100%)
- **Chat transcript file**: `transcripts/v3_openrouter_20260602T135912332846.transcript.json`

## Version Evidence

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Initial system prompt and tool definitions | N/A | 0.65 | `runs/v0_B_base_openrouter_20260602T125543109510.json` |
| v1 | `system_prompt.md` | Adding explicit instructions for out-of-scope, missing info, confirmation, and handle mapping will improve routing and argument accuracy | 0.65 | 0.75 | `runs/v1_B_base_openrouter_20260602T130157915173.json` |
| v2 | `system_prompt.md` | Explicitly checking for URL presence in user input, forcing explicit response_type argument, and prioritizing confirmation over clarify-text will solve URL routing and boundary errors | 0.75 | 0.90 | `runs/v2_B_base_openrouter_20260602T130343289003.json` |
| v3 | `system_prompt.md` | Stripping helper words like 'tin' and 'tweet' from the query parameters, and making tool switching permanent will solve parallel naming mismatches and multi-turn tool switching retention | 0.90 | 1.00 | `runs/v3_B_base_openrouter_20260602T135319192847.json` |

## Failure Analysis

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R08_out_of_scope | out_of_scope | `send(text=...)` | Integrating math problem triggered tool invocation when it should be refused | Refuse to answer and call no tools |
| R10_missing_handle | missing_info | `timeline(screenname='sama')` | Guessed handle 'sama' when username was missing | Call `clarify` with `response_type: "text"` |
| R11_missing_url | missing_info | `fetch(url='https://example.com/article')` | Guessed URL when missing | Call `clarify` with `response_type: "text"` |
| R12_confirm_before_send | wrong_boundary | `send(text=...)` | Sent Telegram without user confirmation | Call `clarify` with `response_type: "yes_no"` |
| R13_parallel_web_and_tweets | wrong_tool | `lookup(query='tin AI', ...)` | Query extracted as 'tin AI' instead of 'AI' | Added Query Cleaning rule to strip helper words |
| R14_out_of_scope_coding | out_of_scope | `send(text=...)` | Python recursion code request triggered tool invocation | Refuse programming tasks and call no tools |
| M06_switch_tool | wrong_tool | `lookup` + `social_search` | Did not drop Twitter tool calls after explicit instruction to switch to web | Added permanent tool switching persistence rule |

## Team Eval Cases

List of cases added to `data/eval_group.json`:

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_out_of_scope_image | Asking for image generation | Refuse to answer, call no tools | PASS |
| G02_wikipedia_search | Wikipedia search for a query | call `wikipedia` tool | PASS |
| G03_arxiv_search | arXiv search for Quantum Computing | call `papers` tool | PASS |
| G04_missing_handle_tweets | Getting tweets without screenname | call `clarify` tool (`response_type: "text"`) | PASS |
| G05_send_confirmation | Posting to Telegram | call `clarify` tool (`response_type: "yes_no"`) | PASS |
| GM01_wikipedia_refinement | Wikipedia search refinement in multi-turn | call `wikipedia` with new query | PASS |
| GM02_arxiv_to_text | Finding papers then reading page text | call `paper_text` with correct arguments | PASS |
| GM03_persistent_out_of_scope | Persistent programming request | Refuse to answer, call no tools | PASS |
| GM04_clarify_name_mapping | Missing handle clarified with name | call `timeline` with handle mapping | PASS |
| GM05_papers_to_wikipedia | Switch from arXiv to Wikipedia | call `wikipedia` tool with topic | PASS |
| G06_github_search | Wikipedia search for a query | call `github_search` tool | PASS |
| GM06_github_sort_refinement | Switch from arXiv to Wikipedia | call `github_search` tool with correct args | PASS |

## Live Chat Evidence

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | "Tin tức công nghệ hôm nay có gì mới không?" | `lookup(query="công nghệ", timeframe="day", topic="news")` | `v3` | Retrieved top 5 tech news headlines from today, formatted as a markdown list with titles and links. |

## Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Wikipedia Search | `tools/wikipedia/tool.py` | Querying MediaWiki API and getting summaries for search hits. | Added search results length check to prevent empty loops. |
| GitHub Search | `tools/github_search/tool.py` | Querying GitHub API for repositories. | Added support for sorting and limit parameters. |
| UI | `app.py` | Streamlit chat UI with toggling execution trace logs. | Added try-except around completions to catch API key errors gracefully. |
| Translate Tool | `tools/translate/tool.py` | Translating text using Google Translate public API. | Handling empty inputs safely. |
| Crypto Ticker | `tools/crypto/tool.py` | Fetching real-time coin prices from Binance API. | Handling ticker mapping (e.g. BTC to BTCUSDT). |
| Weather Info | `tools/weather/tool.py` | Querying current weather details using wttr.in. | Fallback mapping for invalid locations. |

## Reflection

- **Which fixes belonged in `system_prompt.md`?**
  All routing behavior constraints, name-to-handle mappings, confirmation boundaries, out-of-scope rules, and multi-turn state persistence.
- **Which fixes belonged in `tools.yaml`?**
  Proper descriptions of parameters, default values, and enum selections for cleaner tool invocation interfaces.
- **Which failure needed manual review instead of automatic grading?**
  Refusal messages for out-of-scope requests or chat clarifications, as they require human assessment of tone and conversational helpfulness.
- **What would you improve next?**
  Adding semantic search on retrieved documents to improve answer precision, supporting async parallel API requests for faster tool runs, and expanding the GitHub tool to search for specific files or issues.
