"""1.1の部分確認・範囲別集約と1.0互換性を検査する。意味判断のテストではない。"""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('partial_validator', ROOT/'scripts/validate-audit.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def item(report, fid):
    return next(f for f in report['findings'] if f['id'] == fid)


def report11():
    # 合成ケースを構造検査専用に加工する。実記事の意味評価として使わない。
    report = validator.load_json(ROOT/'tests/results/case-B.json')
    report.update(schema_version='1.1', rules_version='1.1')
    for f in report['findings']:
        f.update(classification='EVALUATION', status='適切', confidence='medium', severity='none', priority='none')
        f['evidence'] = [{'evidence_id':'EV-ARTICLE','location':'合成構造検査','observation':'構造検査専用の取得済み観測'}]
        f['expected_effect'] = {'status':'not_applicable','description':'成果を認定しない','evidence_ids':[]}
    for fid, keys in [('A-01',['audience_goal','observed_queries']),('E-03',['static_path','submission'])]:
        parent = item(report, fid)
        checks = []
        for key, known in zip(keys, [True, False]):
            checks.append({'key':key,'classification':'FACT' if known else 'UNVERIFIED',
                           'status':'適切' if known else '判定不可','confidence':'high' if known else 'unknown',
                           'finding':'合成の確認済み部分' if known else '未取得の部分',
                           'rationale':'確認範囲の分離を検査する合成条件',
                           'evidence':copy.deepcopy(parent['evidence']) if known else [],
                           'limitations':['意味評価・成果の認定には使わない']})
        parent.update(classification='UNVERIFIED', status='判定不可', confidence='unknown', severity='info', checks=checks)
    item(report,'E-04').update(classification='UNVERIFIED', status='判定不可', confidence='unknown', severity='info')

    def facet(status, ids):
        return {'status':status,'check_ids':ids,'reason':'確認範囲別の合成検査','limitations':['未確認の実成果・動作は別途記録']}
    # 集約器を呼んで期待値を作らず、確認したい境界条件を直接指定する。
    report['summaries'] = [
        {'domain':'seo_content','structure':facet('適切',['A-01.audience_goal','A-02','B-01','B-02','B-03','B-04','B-05']),
         'outcomes':facet('判定不可',['A-01.observed_queries']),'unverified_checks':['A-01.observed_queries'],'limitations':['検索意図未取得']},
        {'domain':'conversion','structure':facet('適切',['C-01','C-02','C-03','D-01','D-02','E-01','E-02','E-03.static_path']),
         'outcomes':facet('判定不可',['E-04']),'unverified_checks':['E-03.submission','E-04'],'limitations':['送信・実成果未検証']},
        {'domain':'reader_trust','structure':facet('適切',['F-01','F-02']),
         'outcomes':facet('評価対象外',[]),'unverified_checks':[],'limitations':['対象範囲外の成果保証なし']}]
    return report


class PartialResultsTests(unittest.TestCase):
    def rejected(self, report, fragment=None):
        errors = validator.validate(report)
        self.assertTrue(errors)
        if fragment:
            self.assertTrue(any(fragment in e for e in errors), errors)

    def test_known_structure_survives_missing_outcomes(self):
        report = report11()
        self.assertEqual([], validator.validate(report))
        self.assertEqual('適切', report['summaries'][1]['structure']['status'])
        self.assertEqual('判定不可', report['summaries'][1]['outcomes']['status'])
        self.assertIn('E-03.submission', report['summaries'][1]['unverified_checks'])

    def test_legacy_reports_remain_valid(self):
        for case in 'ABCDEFGH':
            with self.subTest(case=case):
                self.assertEqual([], validator.validate(validator.load_json(ROOT/f'tests/results/case-{case}.json')))

    def test_plan11_keeps_mode_contract(self):
        report = report11()
        report['mode'] = 'PLAN'
        report['plan'] = validator.load_json(ROOT/'tests/results/case-H.json')['plan']
        self.assertEqual([], validator.validate(report))
        report['plan'] = None
        self.rejected(report)

    def test_revise11_keeps_diff_contract(self):
        report = report11()
        report['mode'] = 'REVISE'
        report['revisions'] = validator.load_json(ROOT/'tests/results/case-G.json')['revisions']
        self.assertEqual([], validator.validate(report))
        report['revisions'] = []
        self.rejected(report)

    def test_version_mismatch(self):
        report = report11()
        report['rules_version'] = '1.0'
        self.rejected(report)

    def test_unsupported_versions(self):
        for value in ['2.0', [], None]:
            with self.subTest(value=value):
                report = report11(); report['schema_version'] = value
                self.rejected(report, 'schema_version')

    def test_required_partial_checks(self):
        report = report11(); del item(report,'E-03')['checks']
        self.rejected(report)

    def test_omitted_partial_check(self):
        report = report11(); item(report,'E-03')['checks'].pop()
        self.rejected(report, '定義済み')

    def test_duplicate_partial_check(self):
        report = report11(); item(report,'E-03')['checks'][1] = copy.deepcopy(item(report,'E-03')['checks'][0])
        self.rejected(report, '定義済み')

    def test_unknown_partial_check(self):
        report = report11(); item(report,'E-03')['checks'][1]['key'] = 'invented'
        self.rejected(report, '定義済み')

    def test_cannot_change_scope_to_hide_structure_issue(self):
        report = report11(); item(report,'E-03')['checks'][0]['scope'] = 'outcome'
        self.rejected(report, 'Additional properties')

    def test_unregistered_rule_cannot_add_checks(self):
        report = report11(); item(report,'B-01')['checks'] = copy.deepcopy(item(report,'E-03')['checks'])
        self.rejected(report)

    def test_parent_cannot_hide_unknown_part(self):
        report = report11(); item(report,'E-03').update(classification='EVALUATION',status='適切',confidence='medium')
        self.rejected(report, '項目全体')

    def test_partial_fact_requires_available_evidence(self):
        report = report11(); report['evidence'][0]['availability'] = 'unavailable'
        self.rejected(report, 'E-03.static_path')

    def test_partial_fact_requires_evidence(self):
        report = report11(); item(report,'E-03')['checks'][0]['evidence'] = []
        self.rejected(report, '部分確認を支える')

    def test_partial_unknown_cannot_be_high_confidence(self):
        report = report11(); item(report,'E-03')['checks'][1]['confidence'] = 'high'
        self.rejected(report)

    def test_partial_evidence_id_must_exist(self):
        report = report11(); item(report,'E-03')['checks'][0]['evidence'][0]['evidence_id'] = 'EV-UNKNOWN'
        self.rejected(report, '存在しない根拠ID')

    def test_outcomes_cannot_be_called_appropriate_without_data(self):
        report = report11(); report['summaries'][1]['outcomes']['status'] = '適切'
        self.rejected(report, 'outcomes')

    def test_missing_queries_cannot_be_declared_verified(self):
        report = report11()
        parent = item(report,'A-01')
        parent['checks'][1].update(classification='EVALUATION',status='適切',confidence='medium',
                                   evidence=copy.deepcopy(parent['checks'][0]['evidence']))
        parent.update(classification='EVALUATION',status='適切',confidence='medium',severity='none')
        report['summaries'][0]['outcomes']['status'] = '適切'
        report['summaries'][0]['unverified_checks'] = []
        self.rejected(report, '実クエリ未取得')

    def test_pending_behavior_cannot_be_hidden(self):
        report = report11(); report['summaries'][1]['unverified_checks'].remove('E-03.submission')
        self.rejected(report, '未確認の部分項目')

    def test_summary_cannot_omit_a_structural_unit(self):
        report = report11(); report['summaries'][1]['structure']['check_ids'].pop()
        self.rejected(report, '集約対象')

    def test_structural_issue_not_diluted_by_unknown_outcomes(self):
        report = report11()
        check = item(report,'E-03')['checks'][0]
        check.update(classification='EVALUATION',status='改善推奨',confidence='high')
        item(report,'E-03').update(classification='EVALUATION',status='改善推奨',confidence='high',severity='improvement',priority='P2')
        report['summaries'][1]['structure']['status'] = '改善推奨'
        self.assertEqual([],validator.validate(report))
        report['summaries'][1]['structure']['status'] = '適切'
        self.rejected(report, 'structure')

    def test_no_outcome_target_is_not_failure(self):
        report = report11(); report['summaries'][2]['outcomes']['status'] = '判定不可'
        self.rejected(report, '評価対象外')


if __name__ == '__main__':
    unittest.main()
