"""参照レポートの構造回帰と、不正データを使う整合性検査。意味判断は別途レビューする。"""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit_validator', ROOT / 'scripts/validate-audit.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def sample(case='A'):
    return validator.load_json(ROOT / f'tests/results/case-{case}.json')


def finding(report, fid):
    return next(f for f in report['findings'] if f['id'] == fid)


class AuditValidationTests(unittest.TestCase):
    def test_eight_reference_reports(self):
        cases = validator.load_json(ROOT / 'tests/fixtures/cases.json')
        for case in cases:
            with self.subTest(case=case['id']):
                report = sample(case['id'])
                self.assertEqual([], validator.validate(report))
                # 正規化された既知の判定の回帰検査。新たな意味判断の能力を検証しない。
                for fid, expected in case['expected'].items():
                    actual = finding(report, fid)
                    self.assertEqual(expected['classification'], actual['classification'])
                    self.assertEqual(expected['status'], actual['status'])

    def rejected(self, report, fragment=None):
        errors = validator.validate(report)
        self.assertTrue(errors)
        if fragment:
            self.assertTrue(any(fragment in e for e in errors), errors)

    def test_no_data_cannot_be_zero_score(self):
        report = sample('E')
        report['score'] = 0
        self.rejected(report, 'Additional properties')

    def test_missing_data_cannot_be_success(self):
        report = sample('E')
        f = finding(report, 'E-04')
        f.update(classification='FACT', status='適切', confidence='high', severity='none')
        self.rejected(report, '実測データなし')

    def test_unread_source_cannot_support_fact(self):
        report = sample('A')
        report['evidence'][0]['availability'] = 'unavailable'
        self.rejected(report, '未取得')

    def test_unknown_evidence_reference(self):
        report = sample()
        finding(report, 'E-01')['evidence'][0]['evidence_id'] = 'EV-NOT-FOUND'
        self.rejected(report, '存在しない根拠ID')

    def test_duplicate_evidence_id(self):
        report = sample()
        report['evidence'].append(copy.deepcopy(report['evidence'][0]))
        self.rejected(report, 'IDが重複')

    def test_duplicate_or_missing_rules(self):
        report = sample()
        report['findings'][0] = copy.deepcopy(report['findings'][1])
        self.rejected(report, '固定18項目')

    def test_order_is_stable(self):
        report = sample()
        report['findings'].reverse()
        self.rejected(report, 'A-01〜F-02順')

    def test_category_mismatch(self):
        report = sample()
        finding(report, 'E-01')['category'] = 'seo_quality'
        self.rejected(report, 'category')

    def test_unverified_cannot_be_high_confidence(self):
        report = sample()
        finding(report, 'E-04')['confidence'] = 'high'
        self.rejected(report, 'unknown')

    def test_hypothesis_cannot_be_observed_effect(self):
        report = sample('F')
        f = finding(report, 'A-01')
        f['classification'] = 'HYPOTHESIS'
        f['expected_effect'] = {'status':'observed','description':'仮説を観測扱いにした不正例','evidence_ids':['EV-GA4']}
        self.rejected(report, 'unverified')

    def test_observed_effect_requires_analytics(self):
        report = sample('F')
        finding(report, 'E-04')['expected_effect']['evidence_ids'] = ['EV-ARTICLE']
        self.rejected(report, 'analytics')

    def test_observed_effect_requires_evidence(self):
        report = sample('F')
        finding(report, 'E-04')['expected_effect']['evidence_ids'] = []
        self.rejected(report, '実測根拠')

    def test_unavailable_effect_cannot_be_observed(self):
        report = sample('F')
        next(e for e in report['evidence'] if e['id'] == 'EV-GA4')['availability'] = 'unavailable'
        self.rejected(report, '未取得')

    def test_unverified_cannot_claim_observed_effect(self):
        report = sample('F')
        finding(report, 'E-04').update(classification='UNVERIFIED', status='判定不可', confidence='unknown', severity='info')
        self.rejected(report, '判断不可')

    def test_data_acquisition_timestamp_required(self):
        report = sample('F')
        next(e for e in report['evidence'] if e['id'] == 'EV-GA4')['checked_at'] = None
        self.rejected(report)

    def test_not_applicable_is_not_penalized(self):
        report = sample('C')
        finding(report, 'E-02').update(severity='improvement', priority='P2')
        self.rejected(report, '対象外')

    def test_unknown_is_not_critical(self):
        report = sample('H')
        finding(report, 'D-01').update(severity='critical', priority='P1')
        self.rejected(report, '情報不足')

    def test_evaluation_needs_actual_evidence(self):
        report = sample('B')
        finding(report, 'C-01')['evidence'] = []
        self.rejected(report, '取得済み根拠')

    def test_summary_cannot_hide_unknowns(self):
        report = sample('E')
        report['summaries'][1]['status'] = '適切'
        self.rejected(report, '未確認や改善点')

    def test_plan_requires_proposal(self):
        report = sample('H')
        report['plan'] = None
        self.rejected(report)

    def test_audit_cannot_include_revisions(self):
        report = sample('D')
        report['mode'] = 'AUDIT'
        self.rejected(report)

    def test_revise_requires_diff(self):
        report = sample('G')
        report['revisions'] = []
        self.rejected(report)

    def test_revision_requires_known_finding(self):
        report = sample('G')
        report['revisions'][0]['finding_ids'] = ['MISSING-01']
        self.rejected(report, '不明な監査ID')

    def test_revision_must_change_content(self):
        report = sample('G')
        report['revisions'][0]['after'] = report['revisions'][0]['before']
        self.rejected(report, '変更前後')

    def test_dates_and_timezones(self):
        report = sample()
        report['created_at'] = '2026-10-29T16:00:00'
        self.rejected(report, 'date-time')

    def test_period_direction(self):
        report = sample('F')
        report['datasets'][0]['period'] = {'start':'2026-10-28','end':'2026-09-02'}
        self.rejected(report, '期間が逆転')

    def test_available_dataset_requires_period(self):
        report = sample('F')
        report['datasets'][0].update(status='available', period=None)
        self.rejected(report)

    def test_all_dataset_states_are_required(self):
        report = sample()
        report['datasets'].pop()
        self.rejected(report, '取得状態をすべて')

    def test_analytical_denominators_in_fixture(self):
        data = validator.load_json(ROOT / 'tests/fixtures/analytics-f.json')
        before, after = data['before']['ga4'], data['after']['ga4']
        self.assertAlmostEqual(0.04, before['service_transition_sessions']/before['sessions'])
        self.assertAlmostEqual(1/15, after['service_transition_sessions']/after['sessions'])
        self.assertEqual(1, after['inquiry_complete'])
        # この数値確認から因果効果の合格を導く検査は設けない。

    def test_invalid_json_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'invalid.json'
            for content in ['{"mode":"AUDIT","mode":"PLAN"}', '{"value":NaN}', '{']:
                path.write_text(content)
                p = subprocess.run([sys.executable, str(ROOT/'scripts/validate-audit.py'), str(path)], capture_output=True)
                self.assertEqual(2, p.returncode)

    def test_cli_success(self):
        p = subprocess.run([sys.executable, str(ROOT/'scripts/validate-audit.py'), str(ROOT/'tests/results/case-F.json')], capture_output=True)
        self.assertEqual(0, p.returncode, p.stderr.decode())


if __name__ == '__main__':
    unittest.main()
