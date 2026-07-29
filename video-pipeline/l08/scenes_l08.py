#!/usr/bin/env python3
"""L08 — Two Pointers: Pair with Target Sum. Scenes on the shared lib_dsa engine
(native 1080p). Placeholder espeak voices; swap to ElevenLabs by changing
lib_dsa.gen_audio's voice ids. Run:  python3 scenes_l08.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # find lib_dsa
import lib_dsa as L
from lib_dsa import (canvas, header, footer, rrect, ctext, array_cells, counter,
    code_panel, hand, wobble_underline, circle_marker, cell_box, font, frac,
    PAPER, INK, INDIGO, AMBER, GREEN, RED, CARD, BORDER, MUTED)

ROOT=Path(__file__).resolve().parent
W,H = L.LOGW, L.LOGH          # logical 1280x720 space (engine scales to 1080p)
CY=390; TAG="Google DSA · L08"
VALS=[1,3,4,6,8,11]; TARGET=10

SECTIONS=[
 ("s01","T","A problem so simple it feels like a warm up. Given a sorted list of numbers, find the two that add up to a target. You write two loops, try every pair. It passes the tiny example. You submit... Time Limit Exceeded."),
 ("s02","T","Here is the whole problem in one line. Find the two numbers that add up to the target, and return their positions. The list is sorted. Hold on to that word. It is the whole game."),
 ("s03","T","Let us do what the brain does first. Pin i on the first number, one. Now j checks everyone after it. One plus three, one plus four, one plus six, and so on. Then i moves, and j scans again. For a big list that is n times n. On a hundred thousand numbers, ten billion operations. That is your timeout."),
 ("s04","L","But wait. The numbers are just in some order. What is there to even use?"),
 ("s04b","T","That is the instinct to break. We ignored a gift. The list is sorted. Let sorted tell us which way to look, instead of checking everything."),
 ("s05","T","Here is the move. One finger on the smallest number, one on the largest. One plus eleven is twelve. Too big. To shrink the sum, move the right finger in. One plus eight is nine. Too small. Move the left finger up. Three plus eight, eleven, too big, right in. Three plus six, nine, too small, left up. Four plus six... ten. Found it. Five steps, not dozens."),
 ("s06","T","The whole pattern in one line. Sum too big, move the right pointer in. Too small, move the left in. Equal, you are done. That is two pointers."),
 ("s07","T","Let us write it. Two pointers, one at each end. Loop while they have not met. Add them. If it hits the target, return the indices. If the sum is too small, move left up. Too big, move right down."),
 ("s08","T","Trace it. One plus eleven, twelve, right moves in. One plus eight, nine, left moves up. Three plus eight, eleven, right in. Three plus six, nine, left up. Four plus six, ten. Return two and three."),
 ("s09","L","Could I just use a hash map instead? Store what I have seen, look up the complement?"),
 ("s09b","T","For an unsorted list, yes. But that costs order n extra space. Here the list is sorted, so two pointers gets the same order n time at constant space. When it is sorted, pointers win."),
 ("s10","T","Three things to keep. Sorted is the trigger. Too big, right in; too small, left up. And it is order n time, constant space. When you see sorted and find a pair, your hands should reach for both ends. Next up, three sum."),
]

def bg(title,rev=1.0):
    im,d=canvas(); header(d,title,rev); footer(d,TAG); return im,d

def s01(t,D,tag):
    im,d=bg("Pair with Target Sum",frac(t,0,D*0.4))
    ctext(d,W/2,150,"Sorted list — find two numbers that add to the target.",font(30),INK)
    array_cells(d,VALS,W//2,CY-40)
    ctext(d,W/2,CY+150,f"target = {TARGET}",font(34,bold=True),INDIGO)
    if t>D*0.55:
        rrect(d,[W//2-260,560,W//2+260,640],12,(254,226,226),RED,3)
        ctext(d,W/2,600,"Time Limit Exceeded",font(34,bold=True),RED)
    return im

def s02(t,D,tag):
    im,d=bg("The Problem")
    ctext(d,W/2,150,"Find two numbers that sum to the target — return positions.",font(28),INK)
    array_cells(d,VALS,W//2,CY-40)
    ctext(d,W/2,CY+150,f"target = {TARGET}",font(34,bold=True),INDIGO)
    circle_marker(d,[W//2-290,CY-52,W//2+290,CY+44],AMBER,frac(t,D*0.30,D*0.30),width=5,pad=10)
    hand(im,(W/2,635),"already sorted — use it!",34,AMBER,frac(t,D*0.62,D*0.30),anchor="mm")
    return im

def s03(t,D,tag):
    im,d=bg("Brute Force — every pair")
    steps=[(0,1),(0,2),(0,3),(0,4),(0,5),(1,2),(1,3),(1,4),(2,3)]
    f=frac(t,D*0.15,D*0.68); idx=min(len(steps)-1,int(f*len(steps)))
    i,j=steps[idx]
    array_cells(d,VALS,W//2,CY-20,iptr=i,jptr=j)
    counter(d,"comparisons", idx+1 if t<D*0.8 else "≈ 10,000,000,000", RED, x=980,y=150)
    ctext(d,W/2,635,"two nested loops  →  O(n²)",font(30,bold=True),RED)
    return im

def s04(t,D,tag):
    im,d=bg("Wait…")
    array_cells(d,VALS,W//2,CY-20,iptr=0,jptr=3,dim=set(range(6)))
    rrect(d,[W//2-430,150,W//2+430,240],14,(255,247,237),AMBER,2)
    ctext(d,W/2,195,'LEARNER:  "The numbers are in some order — what is there to use?"',font(24),AMBER)
    return im

def s04b(t,D,tag):
    im,d=bg("Use the sort")
    array_cells(d,VALS,W//2,CY-20)
    ctext(d,W/2,150,"Let SORTED tell us which way to look.",font(30,bold=True),GREEN)
    return im

def s05(t,D,tag):
    im,d=bg("The Two-Pointer Squeeze")
    seq=[(0,5,">"),(0,4,"<"),(1,4,">"),(1,3,"<"),(2,3,"=")]
    f=frac(t,D*0.12,D*0.68); idx=min(len(seq)-1,int(f*len(seq)))
    l,r,v=seq[idx]; s=VALS[l]+VALS[r]; found=(v=="=")
    array_cells(d,VALS,W//2,CY-20,lptr=l,rptr=r,found={l,r} if found else None)
    col={">":RED,"<":AMBER,"=":GREEN}[v]
    txt=f"{VALS[l]} + {VALS[r]} = {s}   " + {">":"too big → move right in",
        "<":"too small → move left in","=":f"= target ✓  return [{l}, {r}]"}[v]
    ctext(d,W/2,150,txt,font(30,bold=True),col)
    counter(d,"comparisons",idx+1,GREEN,x=980,y=560)
    note={">":"too big!","<":"too small!","=":"found it!"}[v]
    step_dur=D*0.68/len(seq); step_start=D*0.12+idx*step_dur
    nr=max(0.0,min(1.0,(t-step_start)/max(0.15,step_dur*0.5)))
    hand(im,(120,CY+30),note,42,col,nr,anchor="lm")
    if found:
        bl=cell_box(W//2,CY-20,len(VALS),l); br=cell_box(W//2,CY-20,len(VALS),r)
        circle_marker(d,[bl[0]-2,bl[1],br[2]+2,br[3]],AMBER,frac(t,D*0.84,D*0.14),width=5,pad=15)
    return im

def s06(t,D,tag):
    im,d=bg("The Key Move")
    rrect(d,[W//2-470,300,W//2+470,420],16,(238,242,255),INDIGO,3)
    ctext(d,W/2,345,"Too big → right in.   Too small → left in.",font(32,bold=True),INDIGO)
    ctext(d,W/2,392,"Equal → done.",font(32,bold=True),INDIGO)
    ctext(d,W/2,520,"That's two pointers.",font(28),INK)
    wobble_underline(d,W//2-250,W//2+250,560,AMBER,frac(t,D*0.5,D*0.4),width=5)
    hand(im,(W/2,255),"memorize this one line!",28,AMBER,frac(t,D*0.7,D*0.3),anchor="mm")
    return im

CODE=["def pair_sum(arr, target):","    left, right = 0, len(arr) - 1",
"    while left < right:","        s = arr[left] + arr[right]","        if s == target:",
"            return [left, right]","        if s < target:","            left += 1",
"        else:","            right -= 1","    return [-1, -1]"]
def s07(t,D,tag):
    im,d=bg("Code It")
    total=sum(len(l)+1 for l in CODE); up=int(frac(t,D*0.10,D*0.82)*total)
    code_panel(d,CODE,[W//2-470,120,W//2+470,660],typed_upto=up,filename="pair_sum.py")
    return im

def s08(t,D,tag):
    im,d=bg("Trace the Code")
    rows=[("0 (1)","5 (11)","12","> 10 → right--"),("0 (1)","4 (8)","9","< 10 → left++"),
          ("1 (3)","4 (8)","11","> 10 → right--"),("1 (3)","3 (6)","9","< 10 → left++"),
          ("2 (4)","3 (6)","10","== → return [2,3] ✓")]
    x0,y0=W//2-500,150; cw=[150,150,90,360]; rh=74; heads=["left","right","sum","action"]
    cx=x0
    for k,hh in enumerate(heads):
        rrect(d,[cx,y0,cx+cw[k],y0+56],8,(238,242,255),INDIGO,2)
        ctext(d,cx+cw[k]//2,y0+28,hh,font(24,bold=True),INDIGO); cx+=cw[k]
    nshow=min(len(rows),1+int(frac(t,D*0.12,D*0.80)*len(rows)))
    for ri in range(nshow):
        yy=y0+56+ri*rh; cx=x0; last=(ri==4)
        for k,val in enumerate(rows[ri]):
            rrect(d,[cx,yy,cx+cw[k],yy+rh],8,(226,247,236) if last else CARD,BORDER,1)
            ctext(d,cx+cw[k]//2,yy+rh//2,val,font(22,bold=last),GREEN if last else INK); cx+=cw[k]
    return im

def s09(t,D,tag):
    im,d=bg("What about a hash map?")
    rrect(d,[W//2-440,180,W//2+440,270],14,(255,247,237),AMBER,2)
    ctext(d,W/2,225,'LEARNER:  "Why not a hash map — store seen, look up complement?"',font(23),AMBER)
    return im

def s09b(t,D,tag):
    im,d=bg("Sorted → pointers win")
    rows=[("Hash map (unsorted)","O(n) time","O(n) space",RED),
          ("Two pointers (sorted)","O(n) time","O(1) space",GREEN)]
    for ri,(a,b,c,col) in enumerate(rows):
        yy=220+ri*120; rrect(d,[W//2-460,yy,W//2+460,yy+96],14,CARD,col,3)
        ctext(d,W//2-250,yy+48,a,font(28,bold=True),col)
        ctext(d,W//2+90,yy+48,b,font(26),INK)
        ctext(d,W//2+320,yy+48,c,font(26,bold=True),col)
    return im

def s10(t,D,tag):
    im,d=bg("Lock It In")
    pts=["1.  \"Sorted\" is the trigger.","2.  Too big → right in;  too small → left up.",
         "3.  O(n) time, O(1) space — beats the hash map."]
    for i,p in enumerate(pts):
        if t>0.3+i*0.6: ctext(d,W//2-430,210+i*70,p,font(30),INK,anchor="lm")
    if t>D*0.55:
        rrect(d,[W//2-470,470,W//2+470,560],16,(238,242,255),INDIGO,3)
        ctext(d,W/2,515,"See sorted + find a pair → reach for both ends.",font(28,bold=True),INDIGO)
        wobble_underline(d,W//2-300,W//2+300,548,AMBER,frac(t,D*0.68,D*0.3),width=4)
    if t>D*0.8: hand(im,(W/2,632),"Next: 3Sum →",34,AMBER,frac(t,D*0.82,D*0.18),anchor="mm")
    return im

SCENES={"s01":s01,"s02":s02,"s03":s03,"s04":s04,"s04b":s04b,"s05":s05,
        "s06":s06,"s07":s07,"s08":s08,"s09":s09,"s09b":s09b,"s10":s10}

if __name__=="__main__":
    ad=ROOT/"audio"
    if not all((ad/f"{n}.wav").exists() for n,_,_ in SECTIONS):
        print("1) audio…"); L.gen_audio(SECTIONS, ad)
    else: print("1) audio… (reusing)")
    L.render(SECTIONS, SCENES, ROOT/"GOOG_L08.mp4", ad, ROOT/"work", TAG)
