import json,os,sys,urllib.error,urllib.request,time
E=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL")
N=50000
V={0:0,1:100,2:320,3:330,4:500,5:900,6:20000}
P=[[0]*64 for _ in range(7)]
for i in range(64):
    r,f=divmod(i,8)
    P[1][i]=(r*10+f)//10
    P[2][i]=((7-r)*10+f)//10
D=[-1,-10,-11,-9,1,10,11,9]
K=[-8,-19,-21,-12,8,19,21,12]
def B(f):
    b=[0]*128;p=0
    for c in f.split()[0]:
        if c=="/":continue
        if c.isdigit():p+=int(c)
        else:b[p]="pnbrqkPNBRQK".index(c)+1;p+=1
    return b
def M(b,s):
    m=[];c=1 if s else -1;o=6 if s else 0;p=b[4+96*c]
    for i in range(128):
        p=b[i]
        if p*c<=0:continue
        t=abs(p)
        if t==1:
            if b[i+10*c]==0:
                m.append((i,i+10*c))
                if (i//16==1 if s else i//16==6) and b[i+20*c]==0:m.append((i,i+20*c))
            for d in[-1,1]:
                if b[i+11*c]*d*c>0 or(i%16==0 and d==-1)or(i%16==7 and d==1):m.append((i,i+11*c))
                if b[i+9*c]*d*c>0 or(i%16==7 and d==-1)or(i%16==0 and d==1):m.append((i,i+9*c))
        elif t==2:
            for d in K:
                j=i+d
                if 0<=j<128 and(j&0x88)==0 and b[j]*c<=0:m.append((i,j))
        else:
            for d in D[4:]if t==3 else D[:4]if t==4 else D:
                j=i
                while 1:
                    j+=d
                    if j&0x88 or not(0<=j<128):break
                    if b[j]*c>0:break
                    m.append((i,j))
                    if b[j]*c<0:break
    return m
def S(b,f,t):
    b=b[:];p=b[f];b[t]=p;b[f]=0
    if abs(p)==1 and(t//16==7 if p>0 else t//16==0):b[t]=6 if p>0 else -6
    if p==5 and abs(f-t)==2:b[5 if p>0 else 91]=0;b[3 if p>0 else 91]=5 if p>0 else -5
    return b
def Eval(b):
    v=0
    for i,p in enumerate(b):
        if p:
            c=1 if p>0 else -1
            t=abs(p)
            v+=c*(V[t]+(P[t][i]if t<7 else 0))
    return v
def AB(b,a,be,d,n):
    if d==0 or n[0]>=N:return Eval(b),None
    ms=M(b,1)
    if not ms:return -20000,None
    ms.sort(key=lambda m:(b[m[1]]*(-1 if b[m[0]]>0 else 1)>0,V[abs(b[m[1]])]if b[m[1]]else 0,abs(b[m[0]])) if b[m[0]]>0 else(b[m[1]]*1>0,V[abs(b[m[1]])]if b[m[1]]else 0,abs(b[m[0]])))
    bm=None
    for f,t in ms:
        n[0]+=1
        if n[0]>=N:break
        v=-AB(S(b,f,t),-be,-a,d-1,n)[0]
        if v>a:
            a=v;bm=(f,t)
            if a>=be:break
    return a,bm
def U(m):
    return"abcdefgh"[m[0]%16]+str(8-m[0]//16)+"abcdefgh"[m[1]%16]+str(8-m[1]//16)
def P(path,j):
    r=urllib.request.Request(E+path,data=json.dumps(j).encode(),headers={"content-type":"application/json"})
    try:
        with urllib.request.urlopen(r)as res:return json.load(res)
    except urllib.error.HTTPError as e:sys.exit(f"{path}:{e.code}")
while 1:
    g=P("/game",{})
    if g["status"]=="done":break
    while g["status"]=="your_move":
        b=B(g["fen"])
        _,m=AB(b,-30000,30000,3,[0])
        if not m:ms=M(b,g["colour"]=="white");m=ms[0]if ms else None
        if not m:break
        g=P("/move",{"game":g["game"],"move":U(m)})
    print(f"game {g['game']}: {g['outcome']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)