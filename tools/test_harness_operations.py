import copy
import json
from pathlib import Path
import tempfile
import unittest
from test_acceptance_guards import module, ROOT
h = module('skills/harness-engineering/scripts/harnessctl.py', 'harnessctl')
class HarnessOperations(unittest.TestCase):
    def test_dry_apply_restore_and_conflicts(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d).resolve(); d = str(root); target = root/'old.txt'; target.write_text('before')
            plan = json.loads((ROOT/'skills/harness-engineering/assets/harness-plan.template.json').read_text())
            plan.update(run_id='fixture', allowed_roots=[d], approval_groups=['files'])
            plan['outcome'] = dict(primary_metric='files',before_state='old',target_state='new',unresolved_before=2,unresolved_target=0,expected_primary_outputs=2)
            plan['resource_budget'] = dict(max_task_launches=0,max_support_artifacts=1,max_verification_passes=1,max_low_yield_waves=1,high_cost_approved=False,cost_warning=None)
            plan['support_artifacts']=[]
            plan['operations']=[dict(id='one',action='update',target=str(target),approval_group='files',expected_sha256=h.sha256_file(target),content='after'),dict(id='two',action='create',target=str(root/'new.txt'),approval_group='files',content='new')]
            h.prepare(plan,{'files'}); self.assertEqual(target.read_text(),'before')
            drift = copy.deepcopy(plan); drift['operations'][1]['target']=str(target)
            with self.assertRaises(h.HarnessError): h.apply(drift,{'files'},root/'bad-backup')
            self.assertEqual(target.read_text(),'before')
            receipt=h.apply(plan,{'files'},root/'backup'); manifest=Path(receipt['manifest'])
            self.assertEqual(target.read_text(),'after'); target.write_text('new user work')
            with self.assertRaises(h.HarnessError): h.rollback(manifest)
            self.assertTrue((root/'new.txt').exists()); self.assertEqual(target.read_text(),'new user work')
            target.write_text('after'); h.rollback(manifest)
            self.assertEqual(target.read_text(),'before'); self.assertFalse((root/'new.txt').exists())
            self.assertEqual(h.rollback(manifest)['files'],0)
            (root/'link').symlink_to(root/'absent')
            with self.assertRaises(h.HarnessError): h.check_target(root/'link',[root])
            with self.assertRaises(h.HarnessError): h.check_target(root.parent/'outside',[root])
if __name__=='__main__': unittest.main()
