"""Algorithm 1 (cycle seat graphs) as written in the paper, plus the two patches discussed in the report.
Stress test: python3 algorithm1.py"""
import random, itertools, collections
def util(L,i,seat):
    n=len(seat); k=seat.index(i); return L[i][seat[k-1]]+L[i][seat[(k+1)%n]]
def adj_block(L,seat):
    n=len(seat)
    for k in range(n):
        x,y=seat[k],seat[(k+1)%n]; sw=seat[:]; sw[k],sw[(k+1)%n]=y,x
        if util(L,x,sw)>util(L,x,seat) and util(L,y,sw)>util(L,y,seat): return k
    return None
def has_V(L,n):
    for w in range(n):
        ins=[s for s in range(n) if L[s][w]]
        for s,t in itertools.combinations(ins,2):
            if not L[s][t] and not L[t][s]: return True
    return False
def maximal_partition(L,n):
    rem=set(range(n)); parts=[]
    while rem:
        v=min(rem); P=[v]; rem.remove(v); grew=True
        while grew:
            grew=False
            for u in sorted(rem):
                if L[P[-1]][u]: P.append(u); rem.remove(u); grew=True; break
            if grew: continue
            for u in sorted(rem):
                if L[u][P[0]]: P.insert(0,u); rem.remove(u); grew=True; break
        parts.append(P)
    return parts
def minimalize(L,parts):
    ch=True
    while ch:
        ch=False
        for i,j in itertools.permutations(range(len(parts)),2):
            if L[parts[i][-1]][parts[j][0]]:
                new=parts[i]+parts[j]; parts=[p for k,p in enumerate(parts) if k not in (i,j)]+[new]; ch=True; break
    return parts
def claim1_insert(L,s,P):
    assert L[s][P[-1]]
    for j in range(len(P)-2,-1,-1):        # walk back
        if L[P[j]][s]: return P[:j+1]+[s]+P[j+1:]
        assert L[s][P[j]], "Claim 1 failed (a V exists)"
    return [s]+P
def R(L,seat): n=len(seat); return sum(L[seat[k]][seat[(k+1)%n]] for k in range(n))
stats=collections.Counter()
def case2(L,n):
    parts=minimalize(L,maximal_partition(L,n))
    for it in range(n+2):
        seat=sum(parts,[]); k=adj_block(L,seat)
        if k is None: return seat
        x,y=seat[k],seat[(k+1)%n]; p,z=seat[k-1],seat[(k+2)%n]
        pid={a:i for i,P in enumerate(parts) for a in P}; r=pid[x]; K=len(parts)
        Pr=parts[r]
        if pid[y]==r:
            assert Pr.index(y)==Pr.index(x)+1, "same path, not consecutive"
            if K==1:
                assert y==Pr[-1] and z==Pr[0] and L[y][p] and L[x][z]
                rest=claim1_insert(L,y,Pr[:-2]); assert rest[0]==z, "y prepended"
                parts=[rest+[x]]; stats['I k=1 close']+=1
                before=R(L,seat); after=R(L,sum(parts,[])); assert after>before; continue
            nxt=(r+1)%K; prv=(r-1)%K
            assert y==Pr[-1] and L[y][p] and L[x][z]
            if len(Pr)>=3:
                rest=claim1_insert(L,y,Pr[:-2]); new=rest+[x]+parts[nxt]
                parts=[P for i,P in enumerate(parts) if i not in (r,nxt)]+[new]; stats['I>=3']+=1
            else:
                Q=claim1_insert(L,y,parts[prv])
                if prv==nxt:
                    assert L[x][Q[0]]; parts=[P for i,P in enumerate(parts) if i not in (r,prv)]+[[x]+Q]
                else:
                    assert L[x][parts[nxt][0]]
                    parts=[P for i,P in enumerate(parts) if i not in (r,prv,nxt)]+[Q,[x]+parts[nxt]]
                stats['I=2']+=1
        else:
            r1=pid[y]; assert x==Pr[-1] and y==parts[r1][0]
            assert len(parts[r1])==1, "TypeII with |P_r+1|>=2"
            r2=pid[z]
            if r2!=r: raise AssertionError("TypeII with distinct P_r+2 (paper's contradiction case)")
            # gap case: k=2, tail(P_r)->head(P_r): close into cycle, rotate to start at p, prepend y
            assert K==2 and L[x][Pr[0]] and L[y][p]
            idx=Pr.index(p); cyc=Pr[idx:]+Pr[:idx]; parts=[[y]+cyc]; stats['II k=2 patch']+=1
        before=R(L,seat); parts=minimalize(L,parts); after=R(L,sum(parts,[]))
        assert after>before, ("R did not increase",before,after)
    raise AssertionError("too many repairs")
def alg1(L,n):
    if has_V(L,n):
        for w in range(n):
            ins=[s for s in range(n) if L[s][w]]
            for s,t in itertools.combinations(ins,2):
                if not L[s][t] and not L[t][s]:
                    seat=[s,w,t]; rem=[a for a in range(n) if a not in seat]
                    while rem:
                        Q=[l for l in rem if L[l][seat[-1]]]; v=(Q or rem)[0]; seat.append(v); rem.remove(v)
                    stats['case1']+=1; return seat
    stats['case2']+=1; return case2(L,n)
if __name__ == "__main__":
    random.seed(3); fails=collections.Counter(); runs=0
    for trial in range(60000):
        n=random.randint(4,9); q=random.choice([.4,.55,.7,.85])
        L=[[0 if i==j else int(random.random()<q) for j in range(n)] for i in range(n)]
        try:
            seat=alg1(L,n); runs+=1
            if adj_block(L,seat) is not None: fails['output not NS']+=1
        except AssertionError as e: fails[str(e.args[0])[:60]]+=1
    print("runs",runs,dict(stats)); print("failures",dict(fails))
