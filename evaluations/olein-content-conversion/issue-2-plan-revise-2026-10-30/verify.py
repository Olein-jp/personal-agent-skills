"""形式・入力保持・限定差分だけを検証する。意味の判断は人レビューへ分離。"""
from datetime import datetime
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def load(name):
    return json.loads((HERE / name).read_text())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if not self.depth:
            if tag == 'div' and 'wp-block-post-content' in dict(attrs).get('class', '').split():
                self.depth = 1
        else:
            if tag == 'div':
                self.depth += 1
            if tag in ('p', 'h2', 'h3', 'li', 'tr'):
                self.parts.append('\n')

    def handle_endtag(self, tag):
        if self.depth:
            if tag == 'div':
                self.depth -= 1
            if tag in ('p', 'h2', 'h3', 'li', 'tr'):
                self.parts.append('\n')

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)


def main():
    manifest = load('manifest.json')
    checks = {}
    for name, expected in manifest['inputs'].items():
        checks['input:' + name] = digest(HERE / name) == expected
    for name, expected in manifest['protected_files'].items():
        checks['protected:' + name] = digest(ROOT / name) == expected

    audit = load('inputs/audit-result-v1.1.json')
    plan = load('plan-result.json')
    revise = load('revise-result.json')
    checks['audit_html_version'] = audit['subject']['version'] == 'html-sha256:' + digest(HERE / 'inputs/article.html')
    checks['revise_same_version'] = revise['subject']['version'] == audit['subject']['version']
    checks['plan_brief_version'] = plan['subject']['version'] == 'sha256:' + digest(HERE / 'inputs/plan-brief.md')
    parser = ArticleParser()
    parser.feed((HERE / 'inputs/article.html').read_text())
    extracted = re.sub(r'\n\s*\n', '\n\n', ''.join(parser.parts)).strip() + '\n'
    original = (HERE / 'inputs/article.txt').read_text()
    changed = (HERE / 'revised-article.txt').read_text()
    checks['extraction_reproduced'] = extracted == original
    checks['one_revision'] = len(revise['revisions']) == 1
    revision = revise['revisions'][0]
    checks['before_exactly_once'] = original.count(revision['before']) == 1
    checks['only_declared_change'] = changed == original.replace(revision['before'], revision['after'], 1)
    checks['finding_link'] = revision['finding_ids'] == ['B-01'] and any(f['id'] == 'B-01' and f['status'] == '要確認' for f in audit['findings'])
    checks['input_findings_preserved'] = revise['findings'] == audit['findings']
    checks['no_common_changes'] = not subprocess.check_output(
        ['git', 'diff', manifest['base_commit'], '--', 'olein-content-conversion', 'olein-writing-style'],
        cwd=ROOT, text=True)

    validation = {}
    for name in ('plan-result.json', 'revise-result.json'):
        result = subprocess.run([sys.executable, str(ROOT / 'olein-content-conversion/scripts/validate-audit.py'), str(HERE / name)], capture_output=True, text=True)
        validation[name] = {'exit_code': result.returncode, 'output': result.stdout + result.stderr}
        checks['json:' + name] = result.returncode == 0

    report = {
        'checked_at': datetime.now().astimezone().isoformat(timespec='seconds'),
        'passed': all(checks.values()), 'checks': checks, 'json_validation': validation,
        'characters': {'before': len(original), 'after': len(changed), 'delta': len(changed) - len(original)},
        'limits': ['意味・実用性・文体・架空の主張の有無は人レビューで確認する。', 'ハッシュはmanifest作成時からの不変性。SEO/CV・環境動作・現行仕様の検証ではない。'],
    }
    (HERE / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'passed': report['passed'], 'failed': [key for key, value in checks.items() if not value], 'characters': report['characters']}, ensure_ascii=False))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
