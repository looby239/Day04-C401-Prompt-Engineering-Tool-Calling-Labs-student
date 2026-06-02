---
name: github_search
track: bonus
kind: live_api
provider: GitHub Search API
requires_env: [GITHUB_TOKEN]
inputs: [query, limit, sort]
outputs: [items]
side_effect: false
---
# github_search

Search for repositories on GitHub. Returns a list of repositories with their name, description, URL, stars, and language.
