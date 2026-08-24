# SchemaGatedAI

SchemaGatedAI incrementally inspects streamed JSON from a local model. For top-level object schemas it rejects forbidden property names as soon as the key and colon arrive—before the value or response finishes—then performs strict required-field and primitive-type validation at completion.

```bash
printf '{"kind":"item","power":7}' | python -m schemagatedai examples/schema.json
```

The dependency-free 0.1.0 subset supports top-level objects, `properties`, `required`, `additionalProperties`, and primitive JSON types. It enforces a byte ceiling and rejects data after the root value. Nested value schemas, numeric ranges, unions, and full JSON Schema semantics are explicitly not implemented yet; use a full validator after this early gate when those features matter.

## Test

`python -m unittest discover -s tests -v`

## Fund more development

Donations increase RequiredTruth development production. See [SUPPORT.md](SUPPORT.md); confirmed donors may claim a transaction hash in an issue and request a specific direction.

Apache-2.0 licensed.


## Install and run

```sh
chmod +x install.sh run.sh
./install.sh
./run.sh --help
```
