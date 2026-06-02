---
name: translate
track: bonus
kind: live_api
provider: Google Translate
requires_env: []
inputs: [text, target_lang, source_lang]
outputs: [translated_text]
side_effect: false
---
# translate

Translate a given text from source_lang (default auto) to target_lang (default vi).
