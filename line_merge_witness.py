"""Read-only bounded three-way line merge with structured conflict evidence."""
import argparse,json,pathlib,sys

def need(ok,message):
    if not ok:raise ValueError(message)

def hunks(base,variant):
    n=len(base);m=len(variant)
    dp=[[0]*(m+1) for _ in range(n+1)]
    for i in range(n-1,-1,-1):
        for j in range(m-1,-1,-1):
            dp[i][j]=1+dp[i+1][j+1] if base[i]==variant[j] else max(dp[i+1][j],dp[i][j+1])
    out=[];i=j=0;start=None;replacement=[]
    def flush():
        nonlocal start,replacement
        if start is not None:out.append((start,i,replacement));start=None;replacement=[]
    while i<n or j<m:
        if i<n and j<m and base[i]==variant[j]:flush();i+=1;j+=1
        else:
            if start is None:start=i
            if i<n and (j==m or dp[i+1][j]>=dp[i][j+1]):i+=1
            else:replacement.append(variant[j]);j+=1
    flush();return out

def overlap(a,b):
    s,e,_=a;t,u,_=b
    if s==e and t==u:return s==t
    if s==e:return t<s<u
    if t==u:return s<t<e
    return max(s,t)<min(e,u)

def materialize(base,start,end,edits):
    result=[];pos=start
    for s,e,repl in sorted(edits,key=lambda x:(x[0],x[1])):
        result.extend(base[pos:s]);result.extend(repl);pos=e
    result.extend(base[pos:end]);return result

def analyze(base,left,right):
    for text in (base,left,right):need(type(text) is str and len(text.encode('utf-8'))<=1048576,'expected UTF-8 text <=1 MiB')
    base,left,right=[x.splitlines(keepends=True) for x in (base,left,right)]
    need(max(map(len,(base,left,right)))<=500,'each file limited to 500 Python splitlines lines')
    edits=[(side,h) for side,version in [('left',left),('right',right)] for h in hunks(base,version)]
    remaining=set(range(len(edits)));groups=[]
    while remaining:
        seed=min(remaining);remaining.remove(seed);group={seed};pending=[seed]
        while pending:
            i=pending.pop()
            for j in sorted(remaining.copy()):
                if edits[i][0]!=edits[j][0] and overlap(edits[i][1],edits[j][1]):
                    remaining.remove(j);group.add(j);pending.append(j)
        groups.append(group)
    regions=[];merged=[];pos=0;conflicts=0
    for group in sorted(groups,key=lambda g:min((edits[i][1][0],edits[i][1][1]) for i in g)):
        start=min(edits[i][1][0] for i in group);end=max(edits[i][1][1] for i in group)
        versions={side:materialize(base,start,end,[edits[i][1] for i in group if edits[i][0]==side]) for side in ['left','right']}
        sides={edits[i][0] for i in group}
        conflict=len(sides)==2 and versions['left']!=versions['right']
        chosen=versions['left'] if 'left' in sides else versions['right']
        regions.append({'base_range':[start,end],'base':''.join(base[start:end]),'left':''.join(versions['left']),'right':''.join(versions['right']),'conflict':conflict})
        conflicts+=conflict;merged.extend(base[pos:start]);merged.extend(chosen);pos=end
    merged.extend(base[pos:])
    return {'clean':not conflicts,'conflict_count':conflicts,'regions':regions,'merged_text':None if conflicts else ''.join(merged),
            'coordinates':'zero-based half-open base line ranges; boundary insertions are independent'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['base','left','right']:p.add_argument(name)
    a=p.parse_args()
    try:
        def read(path):
            with pathlib.Path(path).open('rb') as f:raw=f.read(1048577)
            need(len(raw)<=1048576,'file exceeds 1 MiB');return raw.decode('utf-8')
        result=analyze(read(a.base),read(a.left),read(a.right));print(json.dumps(result,indent=2));return int(not result['clean'])
    except (OSError,ValueError) as e:print(str(e),file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
