# SchemaGatedAI

SchemaGatedAI incrementally inspects streamed JSON from a local model. For top-level object schemas it rejects forbidden property names as soon as the key and colon arrive—before the value or response finishes—then performs strict required-field and primitive-type validation at completion.

```bash
printf '{"kind":"item","power":7}' | python -m schemagatedai examples/schema.json
```

The dependency-free subset supports top-level objects, `properties`, `required`, `additionalProperties`, and primitive JSON types. It enforces a byte ceiling and rejects duplicate keys and data after the root value. Nested value schemas, numeric ranges, unions, and full JSON Schema semantics are explicitly not implemented yet; use a full validator after this early gate when those features matter.

## Test

`python -m unittest discover -s tests -v`

## Fund more development

Donations increase RequiredTruth development production. See [SUPPORT.md](SUPPORT.md); confirmed donors may claim a transaction hash in an issue and request a specific direction.

Apache-2.0 licensed.


## Install and run

```sh
chmod +x install.sh run.sh
./install.sh
./run.sh
./cli.sh --help
```


## Standard launcher

`./run.sh` is the normal entry point. It runs `./install.sh` automatically when setup is missing, then opens the PySide6 control panel with live output and actions for validating a pasted or bundled payload, running the real test suite, repair, and stop. Use `./cli.sh` for stdin-based CLI operation, `./demo.sh` for the safe bundled example, and `./test.sh` to run the same tests outside the GUI.
