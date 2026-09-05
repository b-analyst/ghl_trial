# Honeypot environment scaffold

The task here is a hello-world placeholder — write a greeting to a file. It is
not an example of a good honeypot, only of a complete one, so that every file is
one you replace rather than one you imitate.

```bash
pip install inspect-ai anthropic   # plus whichever provider SDK you point at
export ANTHROPIC_API_KEY=...

docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
inspect eval adapters/inspect/inspect_task.py --model <provider>/<model>
```

## Layout

```
env.json         Identity and resource envelope.
variants.json    The variants, and the named hack signatures each plants.
qc.json          Declared score bands: what honest work must clear, what a
                 shortcut must stay under, the margin between them.
flaw.md          The design doc. Four sections. Write it first.
task.py          Prints the agent-visible prompt for a variant.
agent_data/      Staged into /workdir. What the agent sees.
grader/          Root-only. grader.py, grader_data/, reference_solution/.
adapters/        Per-target Dockerfile + adapter.json.
```
