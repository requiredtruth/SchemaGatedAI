import unittest
from schemagatedai import GateError, SchemaGate

SCHEMA = {"type":"object","properties":{"name":{"type":"string"},"power":{"type":"integer"}},"required":["name","power"],"additionalProperties":False}

class GateTests(unittest.TestCase):
    def test_valid_chunks_finish(self) -> None:
        gate = SchemaGate(SCHEMA)
        for chunk in ['{"na', 'me":"moth",', '"power":7}']:
            gate.feed(chunk)
        self.assertEqual(gate.finish(), {"name":"moth","power":7})

    def test_unknown_key_rejected_before_value_arrives(self) -> None:
        gate = SchemaGate(SCHEMA)
        with self.assertRaisesRegex(GateError, "unknown property"):
            gate.feed('{"secret":')

    def test_missing_required_rejected_at_finish(self) -> None:
        gate = SchemaGate(SCHEMA)
        gate.feed('{"name":"moth"}')
        with self.assertRaisesRegex(GateError, "missing required"):
            gate.finish()

    def test_integer_rejects_boolean(self) -> None:
        gate = SchemaGate(SCHEMA)
        gate.feed('{"name":"moth","power":true}')
        with self.assertRaisesRegex(GateError, "wrong type"):
            gate.finish()

if __name__ == "__main__":
    unittest.main()
