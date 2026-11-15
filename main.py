import json,os,sys,urllib.error,urllib.request,struct,hashlib
U=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL")
S=int(os.environ.get("MAKEFUN_TRIAL_SEED","0"))
N=50000
D={}
K=[0]*64
H={}
V={}
P=0
def p(u,b):
    try:
        with urllib.request.urlopen(urllib.request.Request(U+u,data=json.dumps(b).encode(),headers={"content-type":"application/json"}))as r:return json.load(r)
    except urllib.error.HTTPError as e:sys.exit(f"{u}:{e.code}")
def b(f):
    B={}
    for i,r in enumerate(f.split()[0].split("/")):
        f=0
        for c in r:
            if c.isdigit():f+=int(c)
            else:B["abcdefgh"[f]+str(8-i)]=c;f+=1
    return B
def m(f,L):
    B=b(f)
    def s(m):
        v=B[m[:2]].lower();t=B.get(m[2:4])
        if not t and v=="p"and m[0]!=m[2]:t="p"
        c=V.get(t.lower(),0)if t else 0
        q=V.get(m[4],0)if len(m)==5 else 0
        return(-c,-q,V.get(v,0),m)
    return min(L,key=s)
while 1:
    g=p("/game",{})
    if g["status"]=="done":break
    while g["status"]=="your_move":
        g=p("/move",{"game":g["game"],"move":m(g["fen"],g["legal_moves"])})
    print(f"game {g['game']}: {g['outcome']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)