#!/usr/bin/env python3
"""
lib_dsa — reusable DSA lecture render engine (PIL + ffmpeg), native 1080p.

Design: authors write scenes in a 1280x720 LOGICAL coordinate space (easy to
reason about); the engine scales every draw by S=1.5 onto a native 1920x1080
canvas, so output is crisp 1080p with no per-scene retuning. Linux fonts
(DejaVu + Humor Sans handwriting). Reused by every per-question video; only the
scene functions + narration change per lesson.

Primitives: canvas/header/footer/rrect/ctext, array_cells (+pointers),
counter, code_panel, trace_table, and the "pen" set (hand write-on, wobble
underline, circle highlight). Add linked_list/tree/grid/heap/dp_table here as
new patterns need them — one place, all videos benefit.
"""
import math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ---- resolution: logical 720p space -> native 1080p ----
LOGW, LOGH = 1280, 720
S = 1.5
W, H = int(LOGW * S), int(LOGH * S)   # 1920 x 1080
FPS = 15
def sc(v): return int(round(v * S))

# ---- theme ----
PAPER=(250,250,245); INK=(30,41,59); INDIGO=(67,56,202); AMBER=(180,83,9)
GREEN=(4,120,87); RED=(220,38,38); CARD=(255,255,255); BORDER=(203,213,225)
MUTED=(100,116,139); IDEBG=(30,32,44); IDEFG=(220,223,235)

FD="/usr/share/fonts/truetype/dejavu/"
FH="/usr/share/fonts/truetype/humor-sans/Humor-Sans.ttf"
_fc={}
def font(sz, bold=False, mono=False):
    key=(sz,bold,mono)
    if key not in _fc:
        if mono: f="DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"
        else: f="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        _fc[key]=ImageFont.truetype(FD+f, sc(sz))
    return _fc[key]
def hfont(sz):
    key=("H",sz)
    if key not in _fc: _fc[key]=ImageFont.truetype(FH, sc(sz))
    return _fc[key]

# ---- timing ----
def ease(x): return 3*x*x-2*x*x*x
def clamp(x,a=0.0,b=1.0): return max(a,min(b,x))
def frac(t,start,dur):
    if dur<=0: return 1.0 if t>=start else 0.0
    return ease(clamp((t-start)/dur))

# ---- base canvas ----
def canvas():
    im=Image.new("RGB",(W,H),PAPER); return im, ImageDraw.Draw(im)
def ctext(d,cx,y,s,f,fill,anchor="mm"):
    d.text((sc(cx),sc(y)),s,font=f,fill=fill,anchor=anchor)
def header(d,title,rev=1.0,lesson=None):
    ctext(d,LOGW/2,52,title,font(34,bold=True),INDIGO)
    w=sc(360*rev); d.line([(W//2-w,sc(80)),(W//2+w,sc(80))],fill=INDIGO,width=sc(3))
    if lesson: ctext(d,LOGW/2,96,lesson,font(16),MUTED)
def footer(d,tag="Google DSA · L08"):
    d.rectangle([0,H-sc(6),W,H],fill=INDIGO)
    ctext(d,LOGW-150,LOGH-26,tag,font(15),MUTED,anchor="rm")
def rrect(d,box,r,fill,outline=None,width=1):
    b=[sc(box[0]),sc(box[1]),sc(box[2]),sc(box[3])]
    d.rounded_rectangle(b,radius=sc(r),fill=fill,outline=outline,width=sc(width) if outline else 1)
def line(d,pts,fill,width=1,joint=None):
    d.line([(sc(x),sc(y)) for x,y in pts],fill=fill,width=sc(width),joint=joint)
def poly(d,pts,fill):
    d.polygon([(sc(x),sc(y)) for x,y in pts],fill=fill)
def ellipse(d,box,fill=None,outline=None,width=1):
    b=[sc(box[0]),sc(box[1]),sc(box[2]),sc(box[3])]
    d.ellipse(b,fill=fill,outline=outline,width=sc(width) if outline else 1)

# ---- array of cells with pointers ----
def cell_box(cx,y,n,k,cell=92):
    x0=cx-(n*cell)//2; return [x0+k*cell+6,y,x0+(k+1)*cell-6,y+cell]
def array_cells(d,vals,cx,y,cell=92,hi=None,lptr=None,rptr=None,iptr=None,jptr=None,
                dim=None,found=None):
    n=len(vals); x0=cx-(n*cell)//2
    for k,v in enumerate(vals):
        bx=[x0+k*cell+6,y,x0+(k+1)*cell-6,y+cell]
        col=CARD; oc=BORDER; tc=INK
        if dim and k in dim: col=(238,240,244); tc=MUTED
        if hi and k in hi: col=(219,234,254); oc=INDIGO
        if found and k in found: col=(209,250,229); oc=GREEN
        rrect(d,bx,10,col,oc,3)
        ctext(d,(bx[0]+bx[2])/2,(bx[1]+bx[3])/2,str(v),font(40,bold=True),tc)
        ctext(d,(bx[0]+bx[2])/2,y+cell+16,str(k),font(18),MUTED)
    def arrow(k,label,color,below=True):
        ax=x0+k*cell+cell//2
        if below:
            ay=y+cell+40
            line(d,[(ax,ay+34),(ax,ay+8)],color,5); poly(d,[(ax-9,ay+16),(ax+9,ay+16),(ax,ay+4)],color)
            ctext(d,ax,ay+52,label,font(22,bold=True),color)
        else:
            ay=y-14
            line(d,[(ax,ay-34),(ax,ay-8)],color,5); poly(d,[(ax-9,ay-16),(ax+9,ay-16),(ax,ay-4)],color)
            ctext(d,ax,ay-52,label,font(22,bold=True),color)
    if lptr is not None: arrow(lptr,"left",INDIGO,True)
    if rptr is not None: arrow(rptr,"right",AMBER,True)
    if iptr is not None: arrow(iptr,"i",INDIGO,False)
    if jptr is not None: arrow(jptr,"j",AMBER,False)

def counter(d,label,val,color=RED,x=980,y=150):
    rrect(d,[x,y,x+250,y+90],12,CARD,BORDER,2)
    ctext(d,x+125,y+26,label,font(20),MUTED)
    ctext(d,x+125,y+60,str(val),font(40,bold=True),color)

# ---- dark code panel with live typing ----
def code_panel(d,lines,box,typed_upto=None,hi=None,filename="solution.py"):
    x0,y0,x1,y1=box; rrect(d,box,12,IDEBG)
    d.rectangle([sc(x0),sc(y0),sc(x1),sc(y0+34)],fill=(44,47,63))
    for cx,col in [(x0+18,(230,90,90)),(x0+40,(230,180,80)),(x0+62,(120,200,120))]:
        ellipse(d,[cx-7,y0+10,cx+7,y0+24],fill=col)
    ctext(d,x0+150,y0+17,filename,font(16),(160,165,185),anchor="lm")
    fm=font(26,mono=True); lh=38; ty=y0+54; shown=0
    for i,ln in enumerate(lines):
        yy=ty+i*lh
        if hi and i in hi: d.rectangle([sc(x0+8),sc(yy-4),sc(x1-8),sc(yy+lh-8)],fill=(60,64,86))
        ctext(d,x0+30,yy+10,str(i+1),font(18,mono=True),(110,116,140),anchor="lm")
        text=ln
        if typed_upto is not None:
            if shown+len(ln)<=typed_upto: shown+=len(ln)+1
            else:
                take=max(0,typed_upto-shown); text=ln[:take]; shown=typed_upto+1
                if take<len(ln):
                    d.text((sc(x0+66),sc(yy+10)),text,font=fm,fill=IDEFG,anchor="lm")
                    tw=d.textlength(text,font=fm)
                    d.rectangle([sc(x0+66)+tw+2,sc(yy-2),sc(x0+66)+tw+sc(12),sc(yy+lh-12)],fill=(180,200,255))
                    break
        col=(120,170,120) if ln.strip().startswith("#") else IDEFG
        d.text((sc(x0+66),sc(yy+10)),text,font=fm,fill=col,anchor="lm")

# ---- pen primitives ----
def hand(im,xy,text,size=30,color=AMBER,reveal=1.0,anchor="lm"):
    if reveal<=0: return
    f=hfont(size); tmp=ImageDraw.Draw(im)
    bb=tmp.textbbox((0,0),text,font=f); tw=bb[2]-bb[0]; th=bb[3]-bb[1]
    x=sc(xy[0]); y=sc(xy[1])
    if anchor in ("mm","mb","mt"): x=int(x-tw/2)
    if anchor in ("rm","rb","rt"): x=int(x-tw)
    layer=Image.new("RGBA",(tw+8,th+bb[1]+8),(0,0,0,0))
    ImageDraw.Draw(layer).text((-bb[0]+2,2),text,font=f,fill=color+(255,))
    cut=max(1,int((tw+4)*clamp(reveal))); crop=layer.crop((0,0,cut,layer.height))
    py=int(y-th/2-bb[1]); im.paste(crop,(x,py-2),crop)
    if 0.03<reveal<0.985:
        ImageDraw.Draw(im).ellipse([x+cut-6,y-6,x+cut+6,y+6],fill=color)
def wobble_underline(d,x1,x2,y,color=AMBER,reveal=1.0,amp=3.0,width=4):
    if reveal<=0: return
    xend=x1+(x2-x1)*clamp(reveal); pts=[]; x=x1
    while x<=xend: pts.append((x,y+math.sin((x-x1)/16.0)*amp)); x+=6
    if len(pts)>=2: line(d,pts,color,width,joint="curve")
def circle_marker(d,box,color=AMBER,reveal=1.0,width=4,pad=14):
    if reveal<=0: return
    x0,y0,x1,y1=box; cx=(x0+x1)/2; cy=(y0+y1)/2
    rx=(x1-x0)/2+pad; ry=(y1-y0)/2+pad; N=64; n=int(N*clamp(reveal)); start=-0.6; pts=[]
    for i in range(n+1):
        a=start+(i/N)*(2*math.pi*1.10); jit=1+0.035*math.sin(a*5+1)
        pts.append((cx+math.cos(a)*rx*jit, cy+math.sin(a)*ry*jit))
    if len(pts)>=2: line(d,pts,color,width,joint="curve")

def linked_list(d, vals, cx, y, node=104, gap=54, slow=None, fast=None, ptr=None,
                cycle_to=None, hi=None, dim=None):
    """A singly-linked-list node chain: rounded nodes + arrows.
    slow/fast/ptr = index to mark with a labeled arrow above.
    cycle_to = index the last node loops back to (draws a curved back-edge).
    hi/dim = sets of indices to highlight / dim."""
    n=len(vals); span=n*node+(n-1)*gap; x0=cx-span//2
    centers=[]
    for k,v in enumerate(vals):
        bx0=x0+k*(node+gap); bx=[bx0,y,bx0+node,y+node]; centers.append((bx0+node//2,y+node//2))
        col=CARD; oc=BORDER; tc=INK
        if dim and k in dim: col=(238,240,244); tc=MUTED
        if hi and k in hi: col=(219,234,254); oc=INDIGO
        rrect(d,bx,14,col,oc,3)
        ctext(d,bx0+node//2,y+node//2,str(v),font(34,bold=True),tc)
        if k<n-1:  # forward arrow to next
            ax0=bx0+node+6; ax1=bx0+node+gap-6; ay=y+node//2
            line(d,[(ax0,ay),(ax1,ay)],MUTED,4); poly(d,[(ax1-10,ay-7),(ax1-10,ay+7),(ax1,ay)],MUTED)
    # null tail or cycle back-edge
    lastx=x0+(n-1)*(node+gap)+node
    if cycle_to is None:
        ay=y+node//2; line(d,[(lastx+6,ay),(lastx+40,ay)],MUTED,4)
        ctext(d,lastx+58,ay,"∅",font(30,bold=True),MUTED)
    else:
        tx=centers[cycle_to][0]; ty=y+node
        line(d,[(lastx-node//2,y+node),(lastx-node//2,y+node+42),(tx,y+node+42),(tx,y+node+6)],AMBER,4)
        poly(d,[(tx-7,y+node+14),(tx+7,y+node+14),(tx,y+node+4)],AMBER)
    def mark(k,label,color,slot=0):
        cx0=centers[k][0]; ay=y-18-slot*46
        line(d,[(cx0,ay-30),(cx0,ay-6)],color,5); poly(d,[(cx0-9,ay-16),(cx0+9,ay-16),(cx0,ay-4)],color)
        ctext(d,cx0,ay-46,label,font(20,bold=True),color)
    if slow is not None: mark(slow,"slow",INDIGO,0)
    if fast is not None: mark(fast,"fast",AMBER,1 if slow==fast else 0)
    if ptr is not None: mark(ptr,"curr",GREEN,0)
    return centers

def grid(d, matrix, cx, top_y, cell=88, color_map=None, hi=None, dim=None,
         show_text=True, gap=6, labels=None):
    """Draw a 2D grid (matrix = list of rows). color_map = {value: fill color}
    for cell backgrounds; hi/dim = sets of (r,c) to outline-highlight / dim.
    labels = {(r,c): text} overrides the displayed text. Returns {(r,c):(x,y)}."""
    rows=len(matrix); cols=len(matrix[0]) if rows else 0
    tw=cols*cell; x0=cx-tw//2; pos={}
    for r in range(rows):
        for c in range(cols):
            v=matrix[r][c]
            bx=[x0+c*cell+gap//2, top_y+r*cell+gap//2, x0+(c+1)*cell-gap//2, top_y+(r+1)*cell-gap//2]
            fill=CARD; oc=BORDER; tc=INK
            if color_map and v in color_map: fill=color_map[v]
            if dim and (r,c) in dim: fill=(238,240,244); tc=MUTED
            if hi and (r,c) in hi: oc=INDIGO
            rrect(d,bx,8,fill,oc,3 if (hi and (r,c) in hi) else 2)
            cxy=((bx[0]+bx[2])//2,(bx[1]+bx[3])//2); pos[(r,c)]=cxy
            if show_text:
                txt=labels[(r,c)] if (labels and (r,c) in labels) else str(v)
                ctext(d,cxy[0],cxy[1],txt,font(30,bold=True),tc)
    return pos

def binary_tree(d, level_order, cx, top_y, vgap=118, node_r=38, span=None,
                hi=None, dim=None, edge_hi=None, node_color=None):
    """Draw a binary tree from a level-order list (None = absent node).
    Children of index i are 2i+1 and 2i+2. hi/dim = sets of indices to
    highlight / dim. edge_hi = set of child indices whose edge is drawn amber.
    node_color = dict index->color for the fill outline. Returns {i:(x,y)}.
    Uses heap indexing; positions each node by its slot within its depth."""
    if not level_order: return {}
    depth=0
    while (1<<(depth+1))-1 < len(level_order): depth+=1
    maxslots=1<<depth
    if span is None: span=min(1080, maxslots*150)
    pos={}
    for i,v in enumerate(level_order):
        if v is None: continue
        dep=0
        while (1<<(dep+1))-1 <= i: dep+=1
        slot=i-((1<<dep)-1); slots=1<<dep
        x=cx - span/2 + (slot+0.5)*(span/slots)
        y=top_y + dep*vgap
        pos[i]=(x,y)
    # edges first
    for i,v in enumerate(level_order):
        if v is None or i not in pos: continue
        for c in (2*i+1, 2*i+2):
            if c<len(level_order) and level_order[c] is not None and c in pos:
                col=AMBER if (edge_hi and c in edge_hi) else MUTED
                w=5 if (edge_hi and c in edge_hi) else 3
                line(d,[pos[i],pos[c]],col,w)
    # nodes on top
    for i,(x,y) in pos.items():
        col=CARD; oc=BORDER; tc=INK
        if dim and i in dim: col=(238,240,244); tc=MUTED
        if hi and i in hi: col=(219,234,254); oc=INDIGO
        if node_color and i in node_color: oc=node_color[i]
        ellipse(d,[x-node_r,y-node_r,x+node_r,y+node_r],fill=col,outline=oc,width=3)
        ctext(d,x,y,str(level_order[i]),font(30,bold=True),tc)
    return pos

def stack_column(d, items, x, base_y, w=150, cell=62, label="stack",
                 top_hi=None, color=INDIGO, popping=None):
    """A vertical stack growing UPWARD from base_y. items[0] = bottom.
    top_hi = highlight the top tile (True) or a color. popping = index drawn
    fading/offset to the side (mid-pop). Draws a base line + label. Returns
    list of tile center (x,y)."""
    # base line
    line(d,[(x-8,base_y+4),(x+w+8,base_y+4)],MUTED,4)
    ctext(d,x+w//2,base_y+30,label,font(18,bold=True),MUTED)
    centers=[]
    for i,v in enumerate(items):
        ty=base_y-(i+1)*cell+4; by=base_y-i*cell-2
        bx=[x+8,ty,x+w-8,by]; is_top=(i==len(items)-1)
        col=CARD; oc=BORDER; tc=INK
        if is_top and top_hi:
            oc=color if top_hi is True else top_hi; col=(219,234,254) if top_hi is True else CARD
        rrect(d,bx,10,col,oc,3)
        ctext(d,x+w//2,(ty+by)//2,str(v),font(30,bold=True),tc)
        centers.append((x+w//2,(ty+by)//2))
    if not items: ctext(d,x+w//2,base_y-30,"(empty)",font(20),MUTED)
    if popping is not None:
        v=popping; bx=[x+w+30,base_y-cell+4,x+w+30+w-16,base_y-2]
        rrect(d,bx,10,(254,226,226),RED,3); ctext(d,(bx[0]+bx[2])//2,(bx[1]+bx[3])//2,str(v),font(30,bold=True),RED)
        ctext(d,(bx[0]+bx[2])//2,base_y+26,"pop",font(18,bold=True),RED)
    return centers

def window_band(im, cx, y, n, lo, hi, cell=92, color=INDIGO, label="window",
                above=True, alpha=46, reveal=1.0):
    """Translucent highlighted band over array cells lo..hi = the sliding window.
    Draw AFTER array_cells so the tint sits on top (numbers stay visible).
    lo/hi are cell indices (inclusive). Pass im (needs alpha compositing)."""
    if reveal<=0 or hi<lo: return
    x0=cx-(n*cell)//2
    bx0=x0+lo*cell+2; bx1=x0+(hi+1)*cell-2; by0=y-8; by1=y+cell+8
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    od.rounded_rectangle([sc(bx0),sc(by0),sc(bx1),sc(by1)],radius=sc(12),
        fill=color+(int(alpha*clamp(reveal)),), outline=color+(255,), width=sc(4))
    im.paste(ov,(0,0),ov)
    if label:
        ly=(by0-26) if above else (by1+22)
        ctext(ImageDraw.Draw(im),(bx0+bx1)/2,ly,label,font(20,bold=True),color)

# ---- audio (espeak placeholder; swap voices for ElevenLabs) ----
def gen_audio(sections, audio_dir, teacher="en-us+m3", learner="en-us+f4"):
    audio_dir=Path(audio_dir); audio_dir.mkdir(parents=True,exist_ok=True)
    for name,voice,text in sections:
        v=teacher if voice=="T" else learner
        spd="158" if voice=="T" else "170"; pit="42" if voice=="T" else "68"
        subprocess.run(["espeak-ng","-v",v,"-s",spd,"-p",pit,"-w",str(audio_dir/f"{name}.wav"),text],check=True)
def dur(name,audio_dir):
    out=subprocess.run(["ffprobe","-v","quiet","-show_entries","format=duration","-of","csv=p=0",
        str(Path(audio_dir)/f"{name}.wav")],capture_output=True,text=True).stdout.strip()
    return float(out)

# ---- render + assemble ----
def render(sections, scenes, out_path, audio_dir, work_dir, tag):
    audio_dir=Path(audio_dir); work_dir=Path(work_dir); work_dir.mkdir(parents=True,exist_ok=True)
    timeline=[(n,scenes[n],dur(n,audio_dir)) for n,_,_ in sections]
    total=sum(d for _,_,d in timeline)
    vid=work_dir/"video.mp4"
    ff=subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}",
        "-r",str(FPS),"-i","-","-an","-c:v","libx264","-pix_fmt","yuv420p","-crf","20",str(vid)],
        stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    for name,fn,d in timeline:
        nf=max(1,int(round(d*FPS)))
        for k in range(nf): ff.stdin.write(fn(k/FPS,d,tag).tobytes())
        print(f"   rendered {name} ({nf}f)")
    ff.stdin.close(); ff.wait()
    lst=work_dir/"audio.txt"; lst.write_text("".join(f"file '{audio_dir/(n+'.wav')}'\n" for n,_,_ in sections))
    aud=work_dir/"audio.wav"
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(lst),"-ar","44100","-ac","2",str(aud)],
        check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg","-y","-i",str(vid),"-i",str(aud),"-c:v","copy","-c:a","aac","-b:a","160k",
        "-shortest",str(out_path)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    print(f"DONE → {out_path}  ({Path(out_path).stat().st_size//1024} KB, ~{total:.0f}s, {W}x{H})")
