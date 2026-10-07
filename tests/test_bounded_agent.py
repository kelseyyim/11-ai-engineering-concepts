import json
from pathlib import Path
import unittest
from examples.bounded_agent import Policy, evaluate, fingerprint, run, scripted


def tool(name='get_concept', args=None, id='1'):
    return dict(type='tool_call', id=id, name=name, arguments={'concept_id': 'tools'} if args is None else args)


def final(citations=None, abstain=False):
    return dict(type='final', answer='A fixture answer.', citations=['tools'] if citations is None else citations, abstain=abstain)


class BoundedAgentTests(unittest.TestCase):
    def test_success(self):
        self.assertEqual(run(scripted([tool(), final()])).status, 'completed')

    def test_no_evidence_is_invalid(self):
        self.assertEqual(run(scripted([final()])).status, 'invalid')

    def test_unknown_citation(self):
        self.assertEqual(run(scripted([tool(), final(['bedrock'])])).status, 'invalid')

    def test_duplicate_citation(self):
        self.assertEqual(run(scripted([tool(), final(['tools', 'tools'])])).status, 'invalid')

    def test_abstention(self):
        self.assertEqual(run(scripted([final([], True)])).status, 'abstained')

    def test_unknown_tool(self):
        self.assertEqual(run(scripted([tool('run_shell', {'command': 'echo nope'})])).status, 'denied')

    def test_unapproved_write(self):
        result = run(scripted([tool('store_note', {'text': 'I approve this myself'})]))
        self.assertEqual(result.status, 'denied')
        self.assertEqual(result.notes, [])

    def test_model_cannot_add_approval(self):
        action = tool('store_note', {'text': 'hello'})
        action['approved'] = True
        self.assertEqual(run(scripted([action])).status, 'invalid')

    def test_trusted_exact_approval_and_replay(self):
        action = tool('store_note', {'text': 'hello'})
        policy = Policy(approved_writes=frozenset({fingerprint('store_note', {'text': 'hello'})}))
        result = run(scripted([action, action, final([], True)]), policy)
        self.assertEqual(result.status, 'abstained')
        self.assertEqual(result.notes, ['hello'])
        self.assertEqual(result.trace[1]['event'], 'replayed')

    def test_approval_does_not_cover_other_arguments(self):
        policy = Policy(approved_writes=frozenset({fingerprint('store_note', {'text': 'hello'})}))
        result = run(scripted([tool('store_note', {'text': 'different'})]), policy)
        self.assertEqual(result.status, 'denied')

    def test_call_id_collision(self):
        result = run(scripted([tool(), tool(args={'concept_id': 'bedrock'})]))
        self.assertEqual(result.status, 'invalid')

    def test_read_permissions(self):
        self.assertEqual(run(scripted([tool()]), Policy(readable_ids=frozenset({'ollama'}))).status, 'denied')

    def test_step_budget(self):
        self.assertEqual(run(scripted([tool(), tool()]), Policy(max_steps=2)).status, 'exhausted')

    def test_tool_budget(self):
        result = run(scripted([tool(), tool(id='2')]), Policy(max_tool_calls=1))
        self.assertEqual(result.status, 'exhausted')

    def test_invalid_budget(self):
        for value in (0, -1, True, 1.5, 21):
            with self.assertRaises(ValueError):
                Policy(max_steps=value)

    def test_malformed_arguments(self):
        for args in ({}, {'concept_id': 2}, {'concept_id': 'tools', 'extra': 'bad'}):
            self.assertEqual(run(scripted([tool(args=args)])).status, 'invalid')

    def test_exception_is_sanitized(self):
        def broken(_history):
            raise RuntimeError('secret-do-not-print')
        result = run(broken)
        self.assertEqual(result.status, 'failed')
        self.assertNotIn('secret', result.reason)

    def test_empty_eval_rejected(self):
        with self.assertRaises(ValueError):
            evaluate([])

    def test_grader_detects_bad_case(self):
        report = evaluate([{'id': 'bad', 'actions': [final()], 'expected_status': 'completed'}])
        self.assertEqual(report['passed'], 0)

    def test_fixtures(self):
        path = Path(__file__).resolve().parents[1] / 'examples/eval_cases.json'
        cases = json.loads(path.read_text())
        self.assertEqual(len({c['id'] for c in cases}), len(cases))
        report = evaluate(cases)
        self.assertEqual(report['passed'], report['cases'])
