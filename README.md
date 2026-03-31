# Agent

- Gives LLMs tool access on the system and lets them run in a loop to
solve relatively complex tasks autonomously
- Uses Google's Gemini LLM

## How to use

Run the below command

```sh
uv run main.py <prompt> [--verbose]
```

- `--verbose` explicitly prints out the LLM's "thoughts", and also
prints the number of tokens used in the exchange.
- The agent loop runs a maximum of 20 times

## Planned features

- [ ] User-specified number of iterations
- [ ] Access to additional tools:
  - [ ] Recursive regex search (via `ripgrep`)
  - [ ] System manual pages (via `man`)
  - [ ] Python documentation (via `pydoc`)