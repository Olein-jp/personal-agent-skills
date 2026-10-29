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
    schema = load_json(ROOT / 'schemas/audit-result.schema.json')
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
    order = ['改善推奨', '判定不可', '要確認', '適切']
    for s in report['summaries']:
        states = [f['status'] for f in report['findings'] if by_rule[f['id']]['domain'] == s['domain']]
        expected = next((state for state in order if state in states), '評価対象外')
        if s['status'] != expected:
            errors.append(f'{s["domain"]}: 領域状態は{expected}です。未確認や改善点を隠さないでください')
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
