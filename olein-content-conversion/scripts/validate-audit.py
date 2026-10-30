#!/usr/bin/env python3
"""監査JSONの構造と参照整合性を検査する。記事の意味判断は行わない。"""
import argparse
from datetime import date
import json
from pathlib import Path
import sys

try:
    import rfc3339_validator  # 日時検証が黙って省略されることを防ぐ。
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    print('検証には jsonschema と rfc3339-validator が必要です。scripts/requirements.txt を専用環境に導入してください。', file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]


def aggregate_status(states):
    """対象外を除き、未確認も隠さず同じ確認範囲内で集約する。"""
    return next((s for s in ['改善推奨', '判定不可', '要確認', '適切'] if s in states), '評価対象外')


def assessment_units(report, rules):
    """固定項目を、定義済みの部分確認または単一項目として展開する。"""
    units = []
    for finding, rule in zip(report['findings'], rules):
        if rule.get('checks'):
            for check, definition in zip(finding['checks'], rule['checks']):
                units.append({'id': finding['id'] + '.' + check['key'],
                              'domain': rule['domain'], 'scope': definition['scope'],
                              'status': check['status']})
        else:
            units.append({'id': finding['id'], 'domain': rule['domain'],
                          'scope': rule['assessment_scope'], 'status': finding['status']})
    return units


def load_json(path):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'JSONのキーが重複しています: {key}')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique_pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f'不正な数値: {value}')))


def validate(report):
    version = report.get('schema_version') if isinstance(report, dict) else None
    if not isinstance(version, str) or version not in {'1.0', '1.1'}:
        return ['schema_version: 対応している版は1.0と1.1です']
    schema_name = 'audit-result.v1.0.schema.json' if version == '1.0' else 'audit-result.schema.json'
    schema = load_json(ROOT / 'schemas' / schema_name)
    Draft202012Validator.check_schema(schema)
    errors = [f'{"/".join(map(str, e.absolute_path)) or "$"}: {e.message}'
              for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(report)]
    if errors:
        return errors
    rules = load_json(ROOT / 'references/audit-rules.json')['rules']
    by_rule = {r['id']: r for r in rules}
    evidence = {e['id']: e for e in report['evidence']}
    if len(evidence) != len(report['evidence']):
        errors.append('evidence IDが重複しています')
    ids = [f['id'] for f in report['findings']]
    if ids != [r['id'] for r in rules]:
        errors.append('findingsは固定18項目を重複なくA-01〜F-02順で含めてください')
        return errors

    def check_ref(eid, context, available=False):
        item = evidence.get(eid)
        if item is None:
            errors.append(f'{context}: 存在しない根拠ID {eid}')
        elif available and item['availability'] != 'available':
            errors.append(f'{context}: 未取得の資料を確認済み根拠として使用しています {eid}')
        return item

    datasets = report['datasets']
    if len({d['kind'] for d in datasets}) != len(datasets):
        errors.append('同種データセットは期間・範囲を整理して1つの記録にまとめてください')
    if {d['kind'] for d in datasets} != {'search_console', 'ga4', 'inquiries'}:
        errors.append('datasetsはsearch_console、ga4、inquiriesの取得状態をすべて記録してください')
    for d in datasets:
        source = check_ref(d['evidence_id'], d['kind'], d['status'] != 'missing')
        if source and source['source_type'] != 'analytics':
            errors.append(f'{d["kind"]}: データセットの根拠はanalyticsにしてください')
        if d['period'] and date.fromisoformat(d['period']['start']) > date.fromisoformat(d['period']['end']):
            errors.append(f'{d["kind"]}: 対象期間が逆転しています')
        if d['status'] == 'missing' and source and source['availability'] == 'available':
            errors.append(f'{d["kind"]}: missingと取得済み根拠が矛盾しています')

    for f in report['findings']:
        fid = f['id']
        if f['category'] != by_rule[fid]['category']:
            errors.append(f'{fid}: ルールのcategoryと一致しません')
        refs = f['evidence']
        for e in refs:
            check_ref(e['evidence_id'], fid,
                      f['classification'] != 'UNVERIFIED' and f['status'] != '評価対象外')
        if f['classification'] in {'FACT', 'EVALUATION', 'HYPOTHESIS'} and f['status'] != '評価対象外' and not refs:
            errors.append(f'{fid}: 判断を支える取得済み根拠が必要です')
        if f['classification'] != 'UNVERIFIED' and f['confidence'] == 'unknown':
            errors.append(f'{fid}: 確信度unknownはUNVERIFIEDに使用してください')
        if version == '1.1' and by_rule[fid].get('checks'):
            checks = f['checks']
            expected_keys = [c['key'] for c in by_rule[fid]['checks']]
            if [c['key'] for c in checks] != expected_keys:
                errors.append(f'{fid}: checksは定義済みの部分項目を重複なく定義順で含めてください')
            expected_status = aggregate_status([c['status'] for c in checks])
            if f['status'] != expected_status:
                errors.append(f'{fid}: 項目全体の状態は部分確認から{expected_status}となります')
            for c in checks:
                context = fid + '.' + c['key']
                for e in c['evidence']:
                    check_ref(e['evidence_id'], context,
                              c['classification'] != 'UNVERIFIED' and c['status'] != '評価対象外')
                if c['classification'] != 'UNVERIFIED' and c['status'] != '評価対象外' and not c['evidence']:
                    errors.append(f'{context}: 部分確認を支える取得済み根拠が必要です')
                if c['classification'] != 'UNVERIFIED' and c['confidence'] == 'unknown':
                    errors.append(f'{context}: 確信度unknownはUNVERIFIEDに使用してください')
                if (fid == 'A-01' and c['key'] == 'observed_queries' and
                        not any(d['kind'] == 'search_console' and d['status'] != 'missing' for d in datasets) and
                        c['status'] not in {'判定不可', '評価対象外'}):
                    errors.append(f'{context}: 実クエリ未取得のまま一致を評価できません')
        if f['status'] in {'適切', '評価対象外'} and (f['severity'] != 'none' or f['priority'] != 'none'):
            errors.append(f'{fid}: 適切・対象外を問題の重要度や優先度に変換しないでください')
        if f['status'] in {'判定不可', '要確認'} and f['severity'] == 'critical':
            errors.append(f'{fid}: 情報不足だけを重大問題としないでください')
        if f['severity'] == 'critical' and f['priority'] != 'P1':
            errors.append(f'{fid}: criticalにはP1を指定してください')
        if f['severity'] in {'info', 'none'} and f['priority'] != 'none':
            errors.append(f'{fid}: 情報・問題なしの項目に修正優先度を付けないでください')
        effect = f['expected_effect']
        if effect['status'] == 'observed' and f['classification'] == 'UNVERIFIED':
            errors.append(f'{fid}: 判断不可の主張を観測済み効果としないでください')
        for eid in effect['evidence_ids']:
            item = check_ref(eid, f'{fid}/expected_effect', effect['status'] == 'observed')
            if effect['status'] == 'observed' and item and item['source_type'] != 'analytics':
                errors.append(f'{fid}: 効果の観測には実測のanalytics根拠が必要です')
            if effect['status'] == 'observed' and not any(
                    d['evidence_id'] == eid and d['status'] != 'missing' for d in datasets):
                errors.append(f'{fid}: 効果の根拠を取得済みデータセットに登録してください')
        if effect['status'] == 'observed' and not effect['evidence_ids']:
            errors.append(f'{fid}: 観測済み効果には実測根拠が必要です')
        if effect['status'] != 'observed' and effect['evidence_ids']:
            errors.append(f'{fid}: 未観測効果に観測証拠を指定しないでください')
        if fid == 'E-04' and not any(d['status'] != 'missing' for d in datasets):
            if f['status'] != '判定不可' or f['classification'] != 'UNVERIFIED':
                errors.append('E-04: 実測データなしで成果を評価できません')
    domains = ['seo_content', 'conversion', 'reader_trust']
    if [s['domain'] for s in report['summaries']] != domains:
        errors.append('summariesは3領域をseo_content、conversion、reader_trustの順で指定してください')
    if version == '1.0':
        for s in report['summaries']:
            states = [f['status'] for f in report['findings'] if by_rule[f['id']]['domain'] == s['domain']]
            expected = aggregate_status(states)
            if s['status'] != expected:
                errors.append(f'{s["domain"]}: 領域状態は{expected}です。未確認や改善点を隠さないでください')
    else:
        # 部分項目が欠落・重複している場合は不完全な集約を行わない。
        if any([c['key'] for c in f.get('checks', [])] !=
               [c['key'] for c in by_rule[f['id']].get('checks', [])] for f in report['findings']):
            return errors
        units = assessment_units(report, rules)
        for s in report['summaries']:
            domain_units = [u for u in units if u['domain'] == s['domain']]
            for facet, scope in [('structure', 'structure'), ('outcomes', 'outcome')]:
                selected = [u for u in domain_units if u['scope'] == scope]
                expected = aggregate_status([u['status'] for u in selected])
                if s[facet]['status'] != expected:
                    errors.append(f'{s["domain"]}/{facet}: 確認範囲別の状態は{expected}です')
                if s[facet]['check_ids'] != [u['id'] for u in selected]:
                    errors.append(f'{s["domain"]}/{facet}: 集約対象の確認IDが一致しません')
            pending = [u['id'] for u in domain_units if u['status'] in {'判定不可', '要確認'}]
            if s['unverified_checks'] != pending:
                errors.append(f'{s["domain"]}: 未確認の部分項目・動作確認を隠さないでください')
    for change in report['revisions']:
        for fid in change['finding_ids']:
            if fid not in ids:
                errors.append(f'revisions: 不明な監査ID {fid}')
        if change['before'] == change['after']:
            errors.append('revisions: 変更前後が同一です')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path)
    args = parser.parse_args()
    try:
        errors = validate(load_json(args.report))
    except (OSError, ValueError) as exc:
        print(f'読込エラー: {exc}', file=sys.stderr)
        return 2
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print('構造・参照整合性: 合格 (内容の真偽・因果関係は別途レビューが必要です)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
