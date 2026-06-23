# Mechanism PRD — LLM Integration

**Modules:** `llm/{provider,claude_cli,ollama,factory,prompts,obs_text,parser}`

`LLMProvider.complete(prompt)->str` with two implementations: `ClaudeCliProvider`
(shells `claude -p` via the Gatekeeper — subscription, no API key) and
`OllamaProvider` (local HTTP via the Gatekeeper). `prompts` injects persona + the
binding free-NL contract + partial-observation prose + opponent's last message +
history. `obs_text` renders observations qualitatively (no coordinate tuples).
`parser` splits the free-NL message from the `MOVE:`/`BARRIER` token and scrubs any
leaked coordinates. **Gates:** H9, H2.
