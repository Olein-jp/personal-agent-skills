from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,subprocess,sys,csv,io,zipfile
O=Path(__file__).resolve().parent;P=O.parent;R=O.parents[3]
prov=json.loads((O/'provenance.json').read_text());calc=json.loads((O/'calculation.json').read_text());a=json.loads((O/'audit-result.json').read_text());checks={}
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
zpath=Path(prov['source_zip']['path']);checks['original_zip_unchanged']=h(zpath)==prov['source_zip']['sha256']==calc['zip_sha256']
# 元ZIPから別途合計を計算し、保存結果の数値と照合。
with zipfile.ZipFile(zpath) as z:
 for i in z.infolist():
  name=i.filename
  if not i.flag_bits&0x800:
   try:name=name.encode('cp437').decode('utf8')
   except UnicodeError:pass
  b=z.read(i);r=list(csv.DictReader(io.StringIO(b.decode('utf-8-sig'))));t=calc['tables'][name];checks['csv_hash:'+name]=hashlib.sha256(b).hexdigest()==t['sha256']
  if r and 'クリック数'in r[0]:
   cs=sum(int(x['クリック数']) for x in r);im=sum(int(x['表示回数']) for x in r);checks['counts:'+name]=(cs,im)==(t['clicks'],t['impressions']);checks['ctr:'+name]=t['ctr']==(cs/im if im else None)
checks['empty_appearance_not_zero']=calc['tables']['検索での見え方.csv']['clicks'] is None
checks['cross_table_difference_preserved']=calc['reconciliation']['page_minus_devices']=={'clicks':1147,'impressions':70335}
checks['gsc_partial']=a['datasets'][0]['status']=='partial' and a['datasets'][0]['timezone'] is None
checks['ga4_inquiries_missing']=all(d['status']=='missing' and d['period'] is None for d in a['datasets'][1:])
checks['no_observed_improvement_effect']=all(f['expected_effect']['status']!='observed' for f in a['findings'])
for name,expected in prov['skill_files_sha256'].items():checks['skill_unchanged:'+name]=h(R/name)==expected
ret=json.loads((O/'retrieval.json').read_text());checks['article_snapshot_unchanged']=h(Path(ret['ARTICLE']['local_snapshot']))==ret['ARTICLE']['sha256'];checks['article_version_matches']=a['subject']['version']=='html-sha256:'+ret['ARTICLE']['sha256']
v=subprocess.run([sys.executable,str(R/'olein-content-conversion/scripts/validate-audit.py'),str(O/'audit-result.json')],capture_output=True,text=True);checks['audit_json_validation']=v.returncode==0
report={'checked_at':datetime.now(ZoneInfo('Asia/Tokyo')).isoformat(timespec='seconds'),'passed':all(checks.values()),'checks':checks,'audit_json_validation':{'exit_code':v.returncode,'output':v.stdout+v.stderr},'known_data_limitations':['表間差は未解消。機械検証の合格は元データ全体の整合や因果・成果を保証しない。','原本ZIPの出力日時・タイムゾーン不明。','人レビューはhuman-review-record.jsonに別保存。']}
(O/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'failed':[k for k,v in checks.items() if not v]},ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
