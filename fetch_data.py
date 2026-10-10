import os,json,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timedelta,timezone
from pathlib import Path
BASE='https://apis.data.go.kr/B552149/reserviorWaterLevel/'
KST=timezone(timedelta(hours=9))

def query(endpoint,**params):
    key=os.environ.get('DATA_GO_KR_KEY','').strip()
    if not key: raise RuntimeError('DATA_GO_KR_KEY 인증키가 설정되지 않았습니다.')
    # Encoding 키는 이미 % 인코딩된 문자열일 수 있으므로 decoding 키 사용 권장
    q=urllib.parse.urlencode({**params,'serviceKey':key,'numOfRows':400,'pageNo':1})
    url=BASE+endpoint+'/?'+q
    req=urllib.request.Request(url,headers={'User-Agent':'WondeungReservoirMonitor/1.0'})
    try:
        with urllib.request.urlopen(req,timeout=25) as r: raw=r.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'HTTP {e.code}: '+e.read(350).decode('utf-8','replace'))
    root=ET.fromstring(raw)
    err=root.findtext('.//returnReasonCode')
    if err and err!='00':raise RuntimeError(f'API 오류 {err}: '+str(root.findtext('.//returnAuthMsg')))
    if root.find('.//OpenAPI_ServiceResponse') is not None:raise RuntimeError(raw[:350].decode('utf-8','replace'))
    return [{c.tag:c.text for c in el} for el in root.findall('.//item')]

def main():
    matches=query('reservoircode',fac_name='원등')
    matches=[r for r in matches if '원등' in (r.get('fac_name') or '') and '고흥' in (r.get('county') or '')]
    if len(matches)!=1:raise RuntimeError('고흥 원등저수지 식별 실패: '+str(matches))
    fac=matches[0]
    today=datetime.now(KST).date()
    rows=query('reservoirlevel',fac_code=fac['fac_code'],date_s=(today-timedelta(days=59)).strftime('%Y%m%d'),date_e=today.strftime('%Y%m%d'))
    rows=[r for r in rows if r.get('fac_code')==fac['fac_code'] and r.get('check_date') and r.get('water_level')]
    rows.sort(key=lambda x:x['check_date'])
    if not rows:raise RuntimeError('관측자료가 없습니다. 이전 자료를 덮어쓰지 않습니다.')
    payload={'reservoir':fac,'updated_at':datetime.now(KST).isoformat(timespec='seconds'),'source':'한국농어촌공사 농촌용수 저수지 수위정보 OpenAPI','observations':rows}
    Path(__file__).with_name('data.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    print('완료:',fac['fac_name'],len(rows),'건',rows[-1]['check_date'])
if __name__=='__main__':main()
