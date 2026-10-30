"""今回の提供ZIPの件数と率を再計算する。原データの書換え・外部送信なし。"""
import argparse
import csv
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path
import zipfile


def archive_name(info):
    if info.flag_bits & 0x800:
        return info.filename
    try:
        return info.filename.encode('cp437').decode('utf-8')
    except UnicodeError:
        return info.filename


def analyze(path):
    result = {'zip_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'tables': {}}
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            raw = z.read(info)
            reader = csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
            rows = list(reader)
            name = archive_name(info)
            entry = {'sha256': hashlib.sha256(raw).hexdigest(), 'rows': len(rows), 'columns': reader.fieldnames}
            if 'クリック数' in reader.fieldnames:
                # 空欄は欠測として残す。CSVに明示された0だけを0として読む。
                values = [(int(r['クリック数']) if r['クリック数'] else None,
                           int(r['表示回数']) if r['表示回数'] else None) for r in rows]
                complete = bool(rows) and all(c is not None and n is not None for c, n in values)
                clicks = sum(c for c, _ in values) if complete else None
                impressions = sum(n for _, n in values) if complete else None
                ctr = clicks / impressions if impressions else None
                entry.update(clicks=clicks, impressions=impressions, ctr=ctr,
                             missing_count_cells=sum(c is None for c, _ in values) + sum(n is None for _, n in values),
                             blank_ctr_cells=sum(not r['CTR'] for r in rows),
                             blank_position_cells=sum(not r['掲載順位'] for r in rows))
                bad = []
                for index, (r, (c, n)) in enumerate(zip(rows, values), 2):
                    if c is None or n is None or not r['CTR'] or n == 0:
                        continue
                    actual = Decimal(c) / Decimal(n) * 100
                    shown = Decimal(r['CTR'].rstrip('%'))
                    if abs(actual - shown) > Decimal('0.005'):
                        bad.append(index)
                entry['ctr_mismatch_csv_rows'] = bad
                if '日付' in reader.fieldnames:
                    entry['period'] = {'start': rows[0]['日付'], 'end': rows[-1]['日付']}
                    entry['first_positive_date'] = next((r['日付'] for r in rows if int(r['表示回数']) > 0), None)
                    day = next(r for r in rows if r['日付'] == '2026-10-21')
                    entry['first_positive_day'] = {'date': day['日付'], 'clicks': int(day['クリック数']),
                                                   'impressions': int(day['表示回数']),
                                                   'share_of_export_clicks': int(day['クリック数']) / clicks if clicks else None}
            else:
                entry['filters'] = dict((r['フィルタ'], r['値']) for r in rows)
            result['tables'][name] = entry
    page = result['tables']['ページ.csv']
    daily = next(v for v in result['tables'].values() if '日付' in v['columns'])
    devices = result['tables']['デバイス.csv']
    countries = result['tables']['国.csv']
    result['reconciliation'] = {
        'page_equals_daily': (page['clicks'], page['impressions']) == (daily['clicks'], daily['impressions']),
        'devices_equal_countries': (devices['clicks'], devices['impressions']) == (countries['clicks'], countries['impressions']),
        'page_minus_devices': {'clicks': page['clicks'] - devices['clicks'], 'impressions': page['impressions'] - devices['impressions']},
        'explanation': '差の原因は未特定。表の合計を混ぜない。クエリ表は1000行で、匿名クエリ・切捨て等の影響を分離できない。国別・デバイス別の差も同じ理由と断定しない。',
    }
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('zip_path', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(analyze(args.zip_path), ensure_ascii=False, indent=2) + '\n')
    print('表別の合計・CTR・空欄・丸めの整合と差分を保存。原データは変更していません。')
