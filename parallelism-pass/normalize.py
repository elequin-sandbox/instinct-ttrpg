#!/usr/bin/env python3
"""Instinct RPG card normalizer v2 - canonical keywords + unified header, no footer."""
import re, json

# ---- canonical keyword palette ----
IMPACT={'Boost':('#0F766E','#CCFBF1'),'Resolve':('#166534','#F0FDF4'),
 'Hit Dice':('#991B1B','#FEF2F2'),'Hit Die':('#991B1B','#FEF2F2'),'Threat':('#991B1B','#FEF2F2'),
 'Crit':('#B8860B','#FFFDE7'),'Toll':('#B45309','#FFFBEB'),'Miss':('#7F1D1D','#FEF2F2'),
 'Aid':('#2563EB','#EFF6FF'),'Mill':('#0C4A6E','#BAE6FD')}
VERB_COLOR=('#1D4ED8','#EFF6FF')
VERBS={'Move','Strike','Speak','Sense','Know','Focus','Enter','Exit','Read','Summon','Lift','Restrain'}
CRIT_COLOR=('#B8860B','#FFFDE7')
TYPE_COLOR={'Instinct':'#1e2540','Background':'#0f2d45','Bond':'#0f2b15','Flaw':'#3d0a0a',
 'Ancestry':'#2a1a08','Act':'#1C3A5E','React':'#0C4A6E','Item':'#92400E','Connection':'#2d1020'}
CLASS_COLOR={'Barbarian':'#9E2B2B','Fighter':'#B45309','Paladin':'#B8860B','Cleric':'#5E81AC',
 'Ranger':'#2F6B3D','Rogue':'#6C5BA8','Druid':'#5A7D2A','Warlock':'#9A2B5E',
 'Bard':'#B5388D','Wizard':'#3C3489','Monk':'#164E63'}
CHIP_WORDS={**{k:TYPE_COLOR[k] for k in ['Instinct','Background','Bond','Flaw','Ancestry','Act','React','Item']},**CLASS_COLOR}
IMPACT_ID={'Boost':'boost','Resolve':'resolve','Hit Dice':'hd','Hit Die':'hd','Threat':'threat','Crit':'crit','Toll':'toll','Miss':'miss','Aid':'aid','Mill':'mill'}
NBSP='\xa0'; RECY='↻↺'

def lighten(hexc,amt):
    r=int(hexc[1:3],16);g=int(hexc[3:5],16);b=int(hexc[5:7],16)
    r=round(r+(255-r)*amt);g=round(g+(255-g)*amt);b=round(b+(255-b)*amt)
    return '#%02x%02x%02x'%(r,g,b)
def darken(hexc,amt):
    r=int(hexc[1:3],16);g=int(hexc[3:5],16);b=int(hexc[5:7],16)
    r=round(r*(1-amt));g=round(g*(1-amt));b=round(b*(1-amt))
    return '#%02x%02x%02x'%(r,g,b)
def pill(t,kwid): return '<span class="kw kw-%s">%s</span>'%(kwid,t)
def chip(t,key): return '<span class="ix ix-%s">%s</span>'%(key.lower().replace(' ','-'),t)
def strip_tags(s): return re.sub(r'<[^>]+>','',s)
def base_of(t):
    t=t.replace(NBSP,' ').strip(); t=re.sub(r'\s*[0-9]+\s*['+RECY+r']?\s*$','',t); return re.sub(r'\s*['+RECY+r']\s*$','',t).strip()
def classify(raw):
    t=raw.replace(NBSP,' ').strip(); b=base_of(t)
    if re.fullmatch(r'[0-9]+\s*['+RECY+r']?',t): return pill(raw.strip(),'crit')
    if b in IMPACT: return pill(t,IMPACT_ID[b])
    return '<strong>%s</strong>'%t
def rename_terms(s):
    for a,bb in [(r'\bBolstered\b','Boost'),(r'\bbolstered\b','boost'),(r'\bTraits\b','Instincts'),
        (r'\bTrait\b','Instinct'),(r'\btraits\b','instincts'),(r'\btrait\b','instinct')]:
        s=re.sub(a,bb,s)
    return s
SPAN_RE=re.compile(r'<span\b[^>]*\bclass="[^"]*\btp\b[^"]*"[^>]*>(.*?)</span>',re.S)
INLINE_PILL_RE=re.compile(r'<span\b[^>]*style="[^"]*background:[^"]*"[^>]*>(.*?)</span>',re.S)
def renorm_pills(h):
    h=SPAN_RE.sub(lambda m:classify(strip_tags(m.group(1))),h)
    def r2(m):
        inner=strip_tags(m.group(1))
        if len(inner)>30 or '<' in m.group(1): return m.group(0)
        return classify(inner)
    return INLINE_PILL_RE.sub(r2,h)
SKIP_TAGS={'span','strong','em','i','a','b'}
SKIP_CLASSES={'clbl','elbl','slbl','srlbl','flbl','bf-stem-label','bf-choose','bf-type','zone-label',
 'card-subtitle','hdr','hdr-top','hdr-tag','hdr-cost','hdr-name','hdr-sub','hdr-div','tier-float','hdr-blank'}
_IMP='|'.join(sorted(IMPACT,key=len,reverse=True));_VRB='|'.join(sorted(VERBS,key=len,reverse=True))
_CHP='|'.join(sorted(CHIP_WORDS,key=len,reverse=True))
BODY_PAT=re.compile(r'(?<![\w>])(?:(?P<imp>'+_IMP+r')(?:(?P<num>\s+\d+))?|(?P<chip>'+_CHP+r'))(?![\w<])')
def _tt(seg,name):
    def cr(m):
        if m.group('imp'): return pill(m.group('imp')+(m.group('num') or ''),IMPACT_ID[m.group('imp')])
        if m.group('chip'):
            w=m.group('chip'); return w if w==name else chip(w,w)
        return m.group(0)
    return BODY_PAT.sub(cr,seg)
def transform_body(h,name):
    out=[];stack=[]
    for part in re.split(r'(<[^>]+>)',h):
        if part=='':continue
        if part.startswith('<'):
            out.append(part)
            if part.startswith('</'):
                if stack:stack.pop()
            elif not part.endswith('/>') and not re.match(r'<(br|img|hr|input)\b',part):
                tag=re.match(r'<\s*([a-zA-Z0-9]+)',part).group(1).lower()
                mc=re.search(r'class="([^"]*)"',part)
                stack.append((tag,set(mc.group(1).split()) if mc else set()))
        else:
            skip=any(t in SKIP_TAGS or (c&SKIP_CLASSES) for t,c in stack)
            out.append(part if skip else _tt(part,name))
    return ''.join(out)
def norm_body(body,name):
    return transform_body(renorm_pills(rename_terms(body)),name)

# ---- header builder (v3: light header, dark/colored text, id capsule bottom-left) ----
CAP_CSS=('display:inline-flex;align-items:center;border:1.5px solid;border-radius:4px;padding:1px 7px;'
 'font-size:9px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;'
 'font-family:system-ui,-apple-system,sans-serif;line-height:1.35;white-space:nowrap;')

ACC_KEY={'Instinct':'instinct','Background':'background','Bond':'bond','Flaw':'flaw',
 'Ancestry':'ancestry','Connection':'connection'}

def cap_n(t): return '<span class="cap cap-neutral">%s</span>'%t if t else '<span></span>'
def cap_a(t): return '<span class="cap cap-accent">%s</span>'%t if t else '<span></span>'

def header_block(type_text,type_accent,cost_text,name,subtitle=None,blank=False):
    left=cap_a(type_text) if type_accent else cap_n(type_text)
    out='<div class="hdr"><div class="hdr-top">%s%s</div>'%(left,cap_n(cost_text))
    if blank:
        out+='<div class="hdr-name hdr-blankname"><span style="opacity:.18;font-style:italic;font-weight:600;font-size:7px">name</span></div>'
    else:
        out+='<div class="hdr-name">%s</div>'%name
        if subtitle: out+='<div class="hdr-sub">%s</div>'%subtitle
    out+='</div>'
    return out

def id_tag(text): return '<div class="idtag">%s</div>'%text if text else ''
def tier_float(n): return '<div class="tier-float"><span>t%s</span></div>'%n if n else ''

def with_acc(co,key):
    return re.sub(r'class="([^"]*)"', lambda m:'class="%s acc-%s"'%(m.group(1),key), co, count=1)

BF_TYPE={'bf-bg':'Background','bf-bond':'Bond','bf-flaw':'Flaw','bf-ancestry':'Ancestry','bf-instinct':'Instinct'}

def card_open(html):
    return re.match(r'<div class="card[^"]*"[^>]*>',html).group(0)

def build(row):
    html=row['HTML']; name=row['Name']; key=row.get('Card_Key') or ''
    co=card_open(html)
    # INSTINCT
    if key.endswith('-instinct') or ('>Instinct<' in html and 'class="ch"' in html):
        mn=re.search(r'<span class="cn"[^>]*>(.*?)</span>',html,re.S); nm=strip_tags(mn.group(1)).strip() if mn else name
        i=html.find('<div class="cbody"'); j=html.rfind('<div class="cf"'); body=html[i:j] if i>=0 and j>0 else ''
        h=header_block('Instinct',True,'Act',nm)
        return with_acc('<div class="card">','instinct')+h+norm_body(body,nm)+'</div>','instinct'
    # BOON family
    mclass=re.search(r'class="card (bf-\w+)"',html)
    if mclass:
        bf=mclass.group(1); typ=BF_TYPE.get(bf,'Background')
        mn=re.search(r'<div class="bf-name"[^>]*>(.*?)</div>',html,re.S); nm=strip_tags(mn.group(1)).strip() if mn else name
        i=html.find('<div class="bf-body"'); j=html.rfind('<div class="bf-foot"'); body=html[i:j] if i>=0 and j>0 else html[i:]
        h=header_block(typ,True,'Act',nm)
        return with_acc('<div class="card '+bf+'">',ACC_KEY[typ])+h+norm_body(body,nm)+'</div>','boon'
    # CORE
    if 'core-header' in html:
        mcls=re.search(r'<span class="core-class-name"[^>]*>(.*?)</span>',html,re.S); klass=strip_tags(mcls.group(1)).strip() if mcls else ''
        mn=re.search(r'<div class="card-name"[^>]*>(.*?)</div>',html,re.S); nm=strip_tags(mn.group(1)).strip() if mn else name
        msub=re.search(r'<div class="card-subtitle"[^>]*>(.*?)</div>',html,re.S); sub=strip_tags(msub.group(1)).strip() if msub else None
        i=html.find('<div class="card-body"'); j=html.rfind('<div class="card-footer"'); body=html[i:j] if i>=0 and j>0 else ''
        h=header_block('Core',False,'',nm,subtitle=sub)
        return with_acc(co,klass.lower())+h+norm_body(body,nm)+id_tag(klass)+'</div>','core'
    # CONNECTION
    if 'class="card connection"' in html:
        i=html.find('<div class="cbody"'); j=html.rfind('<div class="cf"'); body=html[i:j] if i>=0 and j>0 else ''
        h=header_block('Connection',True,'Act','',blank=True)
        return with_acc(co,'connection')+h+norm_body(body,name)+'</div>','connection'
    # ABILITY
    mn=re.search(r'<span class="cn"[^>]*>(.*?)</span>',html,re.S); nm=strip_tags(mn.group(1)).strip() if mn else name
    mb=re.search(r'<span class="cb"[^>]*>(.*?)</span>',html,re.S); ctype=strip_tags(mb.group(1)).strip() if mb else 'Act'
    mfc=re.search(r'<span class="fclass"[^>]*>(.*?)</span>',html,re.S); klass=strip_tags(mfc.group(1)).strip() if mfc else ''
    mf=re.search(r'<span class="fright"[^>]*>(.*?)</span>',html,re.S); fr=strip_tags(mf.group(1)).strip() if mf else ''
    mt=re.search(r'Tier\s*(\d+)',fr); tier=mt.group(1) if mt else ''
    i=html.find('<div class="cbody"'); j=html.rfind('<div class="cf"'); body=html[i:j] if i>=0 and j>0 else ''
    h=header_block('Ability',False,ctype,nm)
    return with_acc(co,klass.lower())+h+norm_body(body,nm)+id_tag(klass)+tier_float(tier)+'</div>','ability'

if __name__=='__main__':
    import sys
    cur=json.load(open('current_cards.json')); keys=sys.argv[1:]; out=[]
    for r in cur:
        if keys and r.get('Card_Key') not in keys: continue
        try:
            nh,tmpl=build(r)
        except Exception as e:
            nh,tmpl='ERROR: %s'%e,'error'
        out.append({'id':r['id'],'Card_Key':r.get('Card_Key'),'Name':r['Name'],'template':tmpl,'old':r['HTML'],'new':nh})
    json.dump(out,open('normalized.json','w'))
    print('normalized %d'%len(out))
    from collections import Counter
    print(Counter(o['template'] for o in out))
    for o in out:
        if o['template']=='error': print('ERR',o['Name'],o['new'])
