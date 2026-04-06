import tkinter as tk,random,math,pickle,json
from enum import IntEnum,IntFlag,auto
R=random
SW,SH=80,24

class AS(IntEnum):MENU=0;PLAYING=1;GAME_OVER=2;VICTORY=3;DIR=4;SELECT=5;INV=6
class RO(IntEnum):CORPSE=1;TRAP=2;ITEM=3;ACTOR=4
class TT(IntEnum):VOID=0;FL=1;WH=2;WV=3;COR=4;DOOR=5;SD=6;SU=7;TRAP=8;SEC=9
class IC(IntEnum):GOLD=0;POT=1;SCR=2;FOOD=3;WPN=4;ARM=5;WAND=6;RING=7;AMU=8
class IS(IntEnum):CURSED=-1;N=0;BLESSED=1;VORPAL=2
class ES(IntFlag):NONE=0;BLIND=auto();CONF=auto();HALL=auto();HELD=auto();SLEEP=auto();INVIS=auto();HASTE=auto();SLOW=auto();TERR=auto();SEEINV=auto();LEVI=auto()

COL={"BLACK":"#000000","DARK_BROWN":"#4a3c31","FOREST_GREEN":"#228b22","GOLD":"#ffd700","WHITE":"#eeeeee","GRAY":"#777777","RED":"#ff3333","GREEN":"#33ff33","YELLOW":"#ffff33","BLUE":"#3333ff","CYAN":"#33ffff","ORANGE":"#ffaa33","PURPLE":"#ff33ff","LIGHT_BLUE":"#8888ff","MAGENTA":"#ff00ff","SILVER":"#C0C0C0","BRONZE":"#CD7F32"}
TC={TT.VOID:' ',TT.FL:'.',TT.WH:'-',TT.WV:'|',TT.COR:'#',TT.DOOR:'+',TT.SEC:'#',TT.SD:'>',TT.SU:'<',TT.TRAP:'^'}
TLC={TT.VOID:"BLACK",TT.FL:"DARK_BROWN",TT.WH:"FOREST_GREEN",TT.WV:"FOREST_GREEN",TT.COR:"GRAY",TT.DOOR:"GOLD",TT.SEC:"FOREST_GREEN",TT.SD:"WHITE",TT.SU:"WHITE",TT.TRAP:"MAGENTA"}

# Bestiary: char name lv ac hd dmg xp flags color
_BD="A Aquator 5 2 5d8 0d0 20 Rust,Mean BLUE|B Bat 1 3 1d8 1d2 1 Fly,Erratic ORANGE|C Centaur 4 4 4d8 1d6/1d6 15 - GREEN|D Dragon 10 -1 10d8 1d8/1d8/3d10 5000 FireBreath,Mean RED|E Emu 1 7 1d8 1d2 2 Mean WHITE|F Flytrap 8 3 8d8 0d0 80 Hold,Mean GREEN|G Griffin 13 2 13d8 4d3/3d5 2000 Fly,Regen,Mean YELLOW|H Hobgoblin 1 5 1d8 1d8 3 Mean GREEN|I IceMonster 2 9 2d8 0d0 5 Freeze CYAN|J Jabberwock 15 6 15d8 2d12/2d4 3000 Mean RED|K Kestrel 1 7 1d8 1d4 1 Mean YELLOW|L Leprechaun 3 8 3d8 1d1 10 StealGold GREEN|M Medusa 8 2 8d8 3d4/3d4 200 Gaze,Mean PURPLE|N Nymph 3 9 3d8 0d0 37 StealItem BLUE|O Orc 4 6 1d8 1d8 5 Greed,Mean GREEN|P Phantom 7 3 3d8 1d2 120 Invis GRAY|Q Quagga 3 3 3d8 1d2/1d2 15 Mean ORANGE|R Rattlesnake 3 3 2d8 1d6 9 DrainStr,Mean YELLOW|S Snake 1 5 1d8 1d3 2 Mean GREEN|T Troll 6 4 6d8 1d8/1d8/2d6 120 Regen,Mean GREEN|U Urvile 15 -2 7d8 1d3/1d3/4d6 190 Mean BLACK|V Vampire 8 1 8d8 1d10 350 DrainHP,Regen,Mean RED|W Wraith 5 4 5d8 1d6 55 DrainLevel GRAY|X Xeroc 7 7 7d8 3d4 100 Mimic RED|Y Yeti 4 6 4d8 1d6/1d6 50 - WHITE|Z Zombie 2 8 2d8 1d8 6 Mean GRAY"
BES={p[0]:p for p in ([s.split() for s in _BD.split('|')])}

WPN={"Mace":"2d4","Long Sword":"3d4","Dagger":"1d6","Spear":"2d3","Two-Handed Sword":"4d4","Bow":"1d1"}
ARM={"Leather Armor":8,"Studded Leather":7,"Ring Mail":6,"Scale Mail":5,"Splint Mail":4,"Banded Mail":4,"Chain Mail":4,"Plate Mail":3}
TRAPS=["Trapdoor","Bear Trap","Sleeping Gas Trap","Arrow Trap","Teleport Trap","Rust Trap"]
PN=["Healing","Extra Healing","Strength","Raise Level","Haste","Poison","Blindness","Confusion","See Invisible","Restore Strength","Levitation","Hallucination","Monster Detection","Magic Detection"]
PC=["Red","Blue","Green","Yellow","Purple","Pink","White","Black","Orange","Clear","Plaid","Amber","Turquoise","Vermilion"]
SN=["Identify","Magic Mapping","Sleep","Enchant Weapon","Enchant Armor","Remove Curse","Teleportation","Scare Monster","Aggravate Monster","Create Monster","Hold Monster","Food Detection","Gold Detection","Light","Genocide","Blank Paper","Vorpalize Weapon"]
ST=["ZELGO MER","JUYED AWK YACC","NR 9","XIXAXA XOXAXA","PRANTL","READ ME","VEJO","HACKEM MUCHE","ELBIB YLOH","FOO BAR","KERNIGHAN","RITCHIE","THOMPSON","BSD","V7","USR","HAL"]
WN=["Magic Missile","Polymorph","Cancellation","Teleport","Fire","Cold","Slow Monster","Haste Monster","Light","Drain Life","Lightning","Invisibility"]
WM=["Steel","Bronze","Gold","Silver","Copper","Nickel","Cobalt","Iron","Ebony","Zinc","Tin","Bone"]
RN=["Protection","Add Strength","Searching","Stealth","Slow Digestion","Sustain Strength","Regeneration","Add Damage","Maintain Armor","Teleportation","Adornment","Aggravate Monster"]
RS=["Agate","Onyx","Sapphire","Ruby","Diamond","Emerald","Topaz","Amethyst","Granite","Opal","Kryptonite","Quartz"]
XPT=[0,10,20,40,80,160,320,640,1280,2560,5120,10000,20000,40000,80000,160000,320000]
ML,AL,PS=26,26,23
HG={"MAX":2000,"WARN":150,"WEAK":0,"FAINT":-10,"STARVE":-20}

def roll(d):
 if not d or d=='0d0':return 0
 p=d.split('/')[0].split('+');m=int(p[1])if len(p)>1 else 0;d=p[0].split('d')
 return sum(R.randint(1,int(d[1]))for _ in range(int(d[0])))+m if len(d)>1 else m

def smod(s):return(3,3)if s>=19 else(2,2)if s>=18 else(1,2)if s==17 else(0,1)if s==16 else(-1,0)if s<8 else(0,0)

class Fighter:
 def __init__(s,hp,ac,st,dmg,lv=1):
  s.max_hp=s.hp=hp;s.base_ac=ac;s.strength=s.max_strength=st;s.damage=dmg;s.level=lv;s.xp=0;s.flags=[];s.paralyzed_turns=0;s.status=ES.NONE

class Item:
 def __init__(s,cat,name,val=0,dmg="",ac=0,eff=None,ch=0):
  s.category=cat;s.real_name=name;s.value=val;s.identified=False;s.equipped=False;s.damage=dmg;s.ac=ac;s.effect=eff;s.charges=ch;s.unknown_name=name;s.status=IS.N;s.bonus=0

class Entity:
 def __init__(s,x,y,ch,col,nm,bl=True,ro=RO.ACTOR):
  s.x=x;s.y=y;s.char=ch;s.color=col;s.name=nm;s.blocks=bl;s.render_order=ro;s.fighter=None;s.item=None;s.inventory=[]

class Rect:
 def __init__(s,x,y,w,h):
  s.x1=x;s.y1=y;s.x2=x+w;s.y2=y+h;s.w=w;s.h=h;s.is_dark=R.random()<0.3;s.is_lit=not s.is_dark
 def center(s):return(s.x1+s.w//2,s.y1+s.h//2)

class DungeonMap:
 def __init__(s,w,h):
  s.width,s.height=w,h;s.tiles=[[TT.VOID]*h for _ in range(w)];s.visible=[[False]*h for _ in range(w)];s.explored=[[False]*h for _ in range(w)];s.rooms=[];s.traps={}

 def is_blocked(s,x,y):
  return not(0<=x<s.width and 0<=y<s.height)or s.tiles[x][y]in(TT.WH,TT.WV,TT.VOID,TT.SEC)

 def generate(s,lv,ents):
  s.tiles=[[TT.VOID]*s.height for _ in range(s.width)];s.visible=[[False]*s.height for _ in range(s.width)];s.explored=[[False]*s.height for _ in range(s.width)];s.rooms=[];s.traps={}
  if lv>12 and R.random()<0.3:return s.gen_maze(lv,ents)
  cw,ch=s.width//3,s.height//3;rooms=[]
  for sy in range(3):
   for sx in range(3):
    w,h=R.randint(5,cw-2),R.randint(4,ch-2);x=(sx*cw)+R.randint(1,cw-w-1);y=(sy*ch)+R.randint(1,ch-h-1);nr=Rect(x,y,w,h);rooms.append(nr);s.rooms.append(nr)
    for rx in range(nr.x1+1,nr.x2):
     for ry in range(nr.y1+1,nr.y2):s.tiles[rx][ry]=TT.FL
    for rx in range(nr.x1,nr.x2+1):s.tiles[rx][nr.y1]=s.tiles[rx][nr.y2]=TT.WH
    for ry in range(nr.y1,nr.y2+1):s.tiles[nr.x1][ry]=s.tiles[nr.x2][ry]=TT.WV
    if R.random()<0.1:tx,ty=R.randint(nr.x1+1,nr.x2-1),R.randint(nr.y1+1,nr.y2-1);s.traps[(tx,ty)]=R.choice(TRAPS)
  R.shuffle(rooms)
  for i in range(len(rooms)-1):
   x1,y1=rooms[i].center();x2,y2=rooms[i+1].center()
   if R.random()<0.5:s._dh(x1,x2,y1);s._dv(y1,y2,x2)
   else:s._dv(y1,y2,x1);s._dh(x1,x2,y2)
  sp=rooms[0].center();s._stairs(lv,rooms[-1].center(),ents);return sp

 def gen_maze(s,lv,ents):
  for x in range(1,s.width-1):
   for y in range(1,s.height-1):s.tiles[x][y]=TT.WH
  st=[];sx,sy=R.randint(1,(s.width-2)//2)*2+1,R.randint(1,(s.height-2)//2)*2+1;s.tiles[sx][sy]=TT.COR;st.append((sx,sy))
  while st:
   cx,cy=st[-1];nb=[(cx+dx,cy+dy,dx,dy)for dx,dy in[(0,-2),(0,2),(-2,0),(2,0)]if 0<cx+dx<s.width-1 and 0<cy+dy<s.height-1 and s.tiles[cx+dx][cy+dy]==TT.WH]
   if nb:nx,ny,dx,dy=R.choice(nb);s.tiles[cx+dx//2][cy+dy//2]=TT.COR;s.tiles[nx][ny]=TT.COR;st.append((nx,ny))
   else:st.pop()
  os=[(x,y)for x in range(s.width)for y in range(s.height)if s.tiles[x][y]==TT.COR];R.shuffle(os);sp,ep=os.pop(),os.pop();s._stairs(lv,ep,ents);return sp

 def _stairs(s,lv,pos,ents):
  fx,fy=pos
  if lv==AL:am=Entity(fx,fy,',','YELLOW','Amulet of Yendor',False,RO.ITEM);am.item=Item(IC.AMU,'Amulet of Yendor');ents.append(am)
  else:
   s.tiles[fx][fy]=TT.SD
   if lv>1:
    for r in s.rooms:
     ux,uy=R.randint(r.x1+1,r.x2-1),R.randint(r.y1+1,r.y2-1)
     if(ux,uy)!=(fx,fy):s.tiles[ux][uy]=TT.SU;break

 def _dh(s,x1,x2,y):
  for x in range(min(x1,x2),max(x1,x2)+1):
   if s.tiles[x][y]in(TT.VOID,TT.WV):s.tiles[x][y]=TT.COR
   elif s.tiles[x][y]==TT.WH:s.tiles[x][y]=TT.SEC if R.random()<0.2 else TT.DOOR

 def _dv(s,y1,y2,x):
  for y in range(min(y1,y2),max(y1,y2)+1):
   if s.tiles[x][y]in(TT.VOID,TT.WH):s.tiles[x][y]=TT.COR
   elif s.tiles[x][y]==TT.WV:s.tiles[x][y]=TT.SEC if R.random()<0.2 else TT.DOOR

 def fov(s,px,py,blind=False):
  s.visible=[[False]*s.height for _ in range(s.width)]
  if blind:s.visible[px][py]=True;return
  for r in s.rooms:
   if r.x1<=px<r.x2 and r.y1<=py<r.y2:
    if r.is_lit:
     for x in range(r.x1,r.x2+1):
      for y in range(r.y1,r.y2+1):s.visible[x][y]=s.explored[x][y]=True
    else:
     for dx in range(-1,2):
      for dy in range(-1,2):
       nx,ny=px+dx,py+dy
       if r.x1<=nx<=r.x2 and r.y1<=ny<=r.y2:s.visible[nx][ny]=s.explored[nx][ny]=True
    return
  for dx in range(-1,2):
   for dy in range(-1,2):
    nx,ny=px+dx,py+dy
    if 0<=nx<s.width and 0<=ny<s.height:s.visible[nx][ny]=s.explored[nx][ny]=True

class CombatSystem:
 def __init__(s,eng):s.e=eng

 def resolve(s,att,def_):
  for ds in att.fighter.damage.split('/'):
   s._hit(att,def_,ds)
   if def_.fighter.hp<=0:break
  if def_.fighter.hp<=0:s._death(att,def_)

 def _hit(s,att,def_,ds):
  e=s.e;L=e.log;sv=e.eff_str(att);hb,db=smod(sv);hb+=att.fighter.level;is_v=False
  if att==e.player:
   w=next((i for i in att.inventory if i.category==IC.WPN and i.equipped),None)
   if w:hb+=w.bonus;db+=w.bonus;is_v=w.status==IS.VORPAL
   if e.hunger<=HG['WEAK']:hb-=2;db-=2
  tac=def_.fighter.base_ac
  if def_==e.player:
   a=next((i for i in def_.inventory if i.category==IC.ARM and i.equipped),None)
   if a:tac=a.ac-a.bonus
   for r in[i for i in def_.inventory if i.category==IC.RING and i.equipped and i.real_name=="Protection"]:tac-=1
  tn=20-tac;d20=R.randint(1,20);th=d20+hb
  if th>=tn:
   if is_v and d20==20:def_.fighter.hp=0;L("Vorpal blade severs the head!");return
   w=next((i for i in att.inventory if i.category==IC.WPN and i.equipped),None)if att==e.player else None
   td=max(1,roll(w.damage if w else ds)+db)
   for r in[i for i in att.inventory if i.category==IC.RING and i.equipped and i.real_name=="Add Damage"]if att==e.player else[]:td+=1
   def_.fighter.hp-=td;L(f"{att.name} hits {def_.name}.")
   if att!=e.player and att.fighter.flags:s._mflags(att,def_)
  else:L(f"{att.name} misses.")

 def throw(s,idx,dx,dy):
  e=s.e;L=e.log;it=e.player.inventory.pop(idx);dmg=it.damage if it.category==IC.WPN else "1d2"
  bow=next((i for i in e.player.inventory if i.category==IC.WPN and i.real_name=="Bow" and i.equipped),None)
  if bow and it.real_name=="Arrow":dmg="2d3"
  hb=(1 if it.real_name in["Dagger","Spear"]else 0)+it.bonus+(bow.bonus if bow and it.real_name=="Arrow"else 0)
  db=it.bonus+(bow.bonus if bow and it.real_name=="Arrow"else 0)
  cx,cy=e.player.x,e.player.y;hit=False
  for _ in range(8):
   cx+=dx;cy+=dy
   if e.map.is_blocked(cx,cy):break
   tgt=next((en for en in e.entities if en.x==cx and en.y==cy and en.fighter),None)
   if tgt and tgt!=e.player:
    _,sdm=smod(e.eff_str(e.player));tn=20-tgt.fighter.base_ac;d20=R.randint(1,20)
    if d20+e.player.fighter.level+hb>=tn:
     dv=roll(dmg)+sdm+db;tgt.fighter.hp-=max(1,dv);L(f"{it.real_name} hits {tgt.name}.")
     if tgt.fighter.hp<=0:e.entities.remove(tgt);e.player.fighter.xp+=tgt.fighter.xp;L(f"{tgt.name} dies.");s._lvlup(e.player)
    else:L(f"{it.real_name} misses.")
    hit=True;break
  if not hit:
   ch_map={IC.WPN:')',IC.POT:'!',IC.SCR:'?',IC.FOOD:':',IC.ARM:']',IC.WAND:'/',IC.RING:'=',IC.AMU:',',IC.GOLD:'*'}
   d=Entity(cx-dx,cy-dy,ch_map.get(it.category,'?'),"WHITE",it.real_name,False,RO.ITEM);d.item=it;e.entities.append(d);L(f"{it.real_name} falls.")

 def _mflags(s,att,def_):
  e=s.e;L=e.log;fl=att.fighter.flags
  if "Rust" in fl:
   a=next((i for i in def_.inventory if i.category==IC.ARM and i.equipped),None)
   if a and "Leather" not in a.real_name and not any(r.real_name=="Maintain Armor" and r.equipped for r in def_.inventory):
    if a.ac<10 and R.random()<0.5:a.ac+=1;L("Your armor weakens!")
  if "DrainStr" in fl and not any(i.real_name=="Sustain Strength" and i.equipped for i in def_.inventory):def_.fighter.strength=max(3,def_.fighter.strength-1);L("You feel weaker.")
  if "DrainHP" in fl:def_.fighter.max_hp-=1;def_.fighter.hp=min(def_.fighter.hp,def_.fighter.max_hp);L("Life force drains!")
  if "DrainLevel" in fl and def_.fighter.level>1:def_.fighter.level-=1;def_.fighter.max_hp=max(1,def_.fighter.max_hp-roll("1d10"));def_.fighter.hp=min(def_.fighter.hp,def_.fighter.max_hp);def_.fighter.xp=XPT[def_.fighter.level-1];L("Experience drains!")
  if "Freeze" in fl:def_.fighter.paralyzed_turns+=R.randint(4,10);L("You are frozen!")
  if "Hold" in fl:def_.fighter.paralyzed_turns+=2;L("You are held!")
  if "StealGold" in fl and e.gold_purse>0:e.gold_purse=0;L("Purse feels lighter!");s._tp(att)
  if "StealItem" in fl and def_.inventory:
   c=[i for i in def_.inventory if not i.equipped]or def_.inventory
   if c:st=R.choice(c);def_.inventory.remove(st);L(f"She stole {st.real_name}!");s._tp(att)

 def _tp(s,e):
  if e in s.e.entities:s.e.entities.remove(e)
  s.e.log(f"{e.name} vanishes!")

 def _death(s,att,def_):
  e=s.e
  if def_==e.player:e.state=AS.GAME_OVER;e.log("You have died.")
  else:
   if def_ in e.entities:e.entities.remove(def_)
   att.fighter.xp+=def_.fighter.xp;e.log(f"Defeated {def_.name}.");s._lvlup(att)

 def _lvlup(s,ent):
  while ent.fighter.level<len(XPT) and ent.fighter.xp>=XPT[ent.fighter.level]:
   ent.fighter.level+=1;hg=roll("1d10");ent.fighter.max_hp+=hg;ent.fighter.hp=ent.fighter.max_hp
   if ent == s.e.player: s.e.log(f"Welcome to level {ent.fighter.level}.")

class MagicSystem:
 def __init__(s,eng):s.e=eng

 def use(s,idx):
  e=s.e;it=e.player.inventory[idx];e.known_types.add(it.real_name)
  if it.category==IC.SCR and it.real_name=="Identify":e.state=AS.SELECT;e.pending_scroll_idx=idx;e.log("Identify what? (a-z)");return
  if it.category in[IC.POT,IC.SCR,IC.FOOD]:e.player.inventory.pop(idx)
  if it.category==IC.POT:s._quaff(it)
  elif it.category==IC.SCR:s._read(it)
  elif it.category==IC.FOOD:s._eat(it)
  elif it.category==IC.WPN:s._wield(it)
  elif it.category==IC.ARM:s._wear(it)
  elif it.category==IC.RING:s._ring(it)

 def identify(s,tidx):
  e=s.e;sidx=e.pending_scroll_idx;e.player.inventory.pop(sidx)
  if tidx>sidx:tidx-=1
  if 0<=tidx<len(e.player.inventory):ti=e.player.inventory[tidx];ti.identified=True;e.log(f"It is a {ti.real_name}.")
  e.state=AS.PLAYING;e.pending_scroll_idx=None

 def _quaff(s,it):
  e=s.e;L=e.log;pf=e.player.fighter;n=it.real_name
  if n=="Healing":pf.hp=min(pf.max_hp,pf.hp+roll(f"{pf.level}d4"));L("You feel better.")
  elif n=="Extra Healing":pf.hp=min(pf.max_hp,pf.hp+roll(f"{pf.level*2}d4"));L("You feel much better.")
  elif n=="Strength":pf.strength+=1;pf.max_strength+=1;L("You feel stronger.")
  elif n=="Restore Strength":pf.strength=pf.max_strength;L("You feel great.")
  elif n=="Raise Level":pf.level+=1;pf.max_hp+=roll("1d10");pf.hp=pf.max_hp;L(f"Level {pf.level}!")
  elif n=="Haste":pf.status|=ES.HASTE;L("You move faster.")
  elif n=="Poison":pf.strength=max(3,pf.strength-R.randint(1,3));L("You feel sick.")
  elif n=="Blindness":pf.status|=ES.BLIND;L("Darkness surrounds you.")
  elif n=="Hallucination":pf.status|=ES.HALL;L("Oh wow! Cosmic!")
  elif n=="Confusion":pf.status|=ES.CONF;L("What's going on?")
  elif n=="See Invisible":pf.status|=ES.SEEINV;L("Your eyes tingle.")
  elif n=="Levitation":pf.status|=ES.LEVI;L("You float up.")
  elif n=="Monster Detection":[e.map.visible.__setitem__((en.x,en.y),True)for en in e.entities if en.fighter and en!=e.player];L("You sense monsters.")
  elif n=="Magic Detection":[e.map.visible.__setitem__((en.x,en.y),True)for en in e.entities if en.item and en.item.category in[IC.POT,IC.SCR,IC.RING,IC.WAND]];L("You sense magic.")

 def _read(s,it):
  e=s.e;L=e.log;n=it.real_name;p=e.player
  if n=="Magic Mapping":[e.map.explored[x].__setitem__(y,True)for x in range(e.map.width)for y in range(e.map.height)];L("Map etched in mind.")
  elif n=="Teleportation":p.x,p.y=e.rnd_floor();L("You are teleported.")
  elif n=="Enchant Weapon":
   w=next((i for i in p.inventory if i.equipped and i.category==IC.WPN),None)
   if w:w.bonus+=1;w.status=IS.BLESSED;L("Weapon glows blue.")
   else:L("Hands tingle.")
  elif n=="Enchant Armor":
   a=next((i for i in p.inventory if i.equipped and i.category==IC.ARM),None)
   if a:a.bonus+=1;a.status=IS.BLESSED;L("Armor glows silver.")
   else:L("Skin tingles.")
  elif n=="Vorpalize Weapon":
   w=next((i for i in p.inventory if i.equipped and i.category==IC.WPN),None)
   if w:w.bonus+=1;w.status=IS.VORPAL;L("Weapon flashes!")
   else:L("Hands twitch.")
  elif n=="Remove Curse":[setattr(i,'status',IS.N)for i in p.inventory if i.status==IS.CURSED];L("Burden lifts.")
  elif n=="Sleep":L("You fall asleep.");p.fighter.paralyzed_turns+=R.randint(2,5)
  elif n=="Aggravate Monster":L("High pitched hum.");[setattr(en.fighter,'status',en.fighter.status&~ES.SLEEP)for en in e.entities if en.fighter and en!=p]
  elif n=="Scare Monster":L("Maniacal laughter.");[setattr(en.fighter,'status',en.fighter.status|ES.TERR)for en in e.entities if en.fighter and en!=p and math.hypot(en.x-p.x,en.y-p.y)<2]
  elif n=="Create Monster":c=[k for k,v in BES.items()if int(v[2])<=e.level+2]or['B'];e.spawn(R.choice(c),True);L("New presence.")
  elif n=="Hold Monster":L("Stillness falls.");[setattr(en.fighter,'paralyzed_turns',en.fighter.paralyzed_turns+R.randint(2,5))for en in e.entities if en.fighter and en!=p and math.hypot(en.x-p.x,en.y-p.y)<3]
  elif n=="Food Detection":L("You smell food."if any(en.item and en.item.category==IC.FOOD for en in e.entities)else"Nothing.")
  elif n=="Gold Detection":L("You sense gold."if any(en.item and en.item.category==IC.GOLD for en in e.entities)else"Nothing.")
  elif n=="Light":
   for r in e.map.rooms:
    if r.x1<=p.x<r.x2 and r.y1<=p.y<r.y2:r.is_lit=True;r.is_dark=False;L("Room is lit.");return
   L("Corridor glows.")
  elif n=="Genocide":
   tgt=next((en for en in e.entities if en.fighter and en!=p and math.hypot(en.x-p.x,en.y-p.y)<2),None)
   if tgt:[e.entities.remove(en)for en in list(e.entities)if en.char==tgt.char and en.fighter and en!=p];L(f"Wiped out {tgt.name}s.")
   else:L("Nothing happens.")
  elif n=="Blank Paper":L("Scroll is blank.")

 def _eat(s,it):s.e.hunger=min(s.e.hunger+800,2000);s.e.log("Tastes good."if it.real_name!="Slime Mold"else"Yummy slime mold!")

 def _wield(s,it):
  L=s.e.log
  if it.equipped:
   if it.status==IS.CURSED:L("Can't let go!");return
   it.equipped=False;L(f"Unwielded {it.real_name}.")
  else:[setattr(i,'equipped',False)for i in s.e.player.inventory if i.category==IC.WPN];it.equipped=True;L(f"Wielding {it.real_name}.")

 def _wear(s,it):
  L=s.e.log
  if it.equipped:
   if it.status==IS.CURSED:L("Can't remove!");return
   it.equipped=False;L(f"Removed {it.real_name}.")
  else:[setattr(i,'equipped',False)for i in s.e.player.inventory if i.category==IC.ARM];it.equipped=True;L(f"Wearing {it.real_name}.")

 def _ring(s,it):
  L=s.e.log
  if it.equipped:
   if it.status==IS.CURSED:L("Can't remove!");return
   it.equipped=False;L(f"Removed {it.real_name}.")
  else:
   if sum(1 for i in s.e.player.inventory if i.category==IC.RING and i.equipped)>=2:L("Two rings max.");return
   it.equipped=True;L(f"Wearing {it.real_name}.")

 def zap(s,it,dx,dy):
  e=s.e;L=e.log;it.charges-=1;n=it.real_name;e.known_types.add(n)
  if n=="Light":
   for r in e.map.rooms:
    if r.x1<=e.player.x<r.x2 and r.y1<=e.player.y<r.y2:r.is_lit=True;r.is_dark=False;L("Room is lit.");return
   L("Corridor glows.");return
  cx,cy=e.player.x,e.player.y
  for _ in range(8):
   cx+=dx;cy+=dy
   if e.map.is_blocked(cx,cy):L("Bolt hits wall.");break
   tgt=next((en for en in e.entities if en.x==cx and en.y==cy and en.fighter),None)
   if tgt and tgt!=e.player:s._wand(tgt,n);return

 def _wand(s,tgt,n):
  e=s.e;L=e.log
  if n=="Magic Missile":tgt.fighter.hp-=roll("1d4");L(f"Missile hits {tgt.name}.")
  elif n=="Fire":tgt.fighter.hp-=roll("3d6")if"Fire"not in tgt.fighter.flags else 0;L(f"Flame burns {tgt.name}.")
  elif n=="Cold":tgt.fighter.hp-=roll("3d6")if"Freeze"not in tgt.fighter.flags else 0;L(f"Ice freezes {tgt.name}.")
  elif n=="Lightning":tgt.fighter.hp-=roll("6d6");L(f"Lightning strikes {tgt.name}.")
  elif n=="Polymorph":tgt.char=R.choice(list(BES.keys()));L(f"{tgt.name} changes shape!")
  elif n=="Teleport":tgt.x,tgt.y=e.rnd_floor();L(f"{tgt.name} vanishes!")
  elif n=="Cancellation":tgt.fighter.flags=[];L(f"{tgt.name} cancelled.")
  elif n=="Drain Life":dr=tgt.fighter.hp//2;tgt.fighter.hp-=dr;e.player.fighter.hp=min(e.player.fighter.max_hp,e.player.fighter.hp+(dr//2));L(f"Drain {tgt.name}.")
  elif n=="Slow Monster":tgt.fighter.status|=ES.SLOW;L(f"{tgt.name} slows.")
  elif n=="Haste Monster":tgt.fighter.status|=ES.HASTE;L(f"{tgt.name} speeds up.")
  elif n=="Invisibility":tgt.fighter.status|=ES.INVIS;tgt.fighter.flags.append("Invis");L(f"{tgt.name} invisible!")
  if tgt.fighter.hp<=0:e.entities.remove(tgt);e.player.fighter.xp+=tgt.fighter.xp;L(f"{tgt.name} killed.");e.combat_system._lvlup(e.player)

class AISystem:
 def __init__(s,eng):s.e=eng

 def tick(s):
  e=s.e;p=e.player;L=e.log
  hs=any(i.real_name=="Stealth"and i.equipped for i in p.inventory);ha=any(i.real_name=="Aggravate Monster"and i.equipped for i in p.inventory)
  ar=3 if hs else 6;ar=999 if ha else ar
  os=any(en.x==p.x and en.y==p.y and en.item and en.item.category==IC.SCR and en.item.real_name=="Scare Monster"for en in e.entities)
  for en in list(e.entities):
   if en==p or not en.fighter:continue
   f=en.fighter
   if"Regen"in f.flags and f.hp<f.max_hp:f.hp+=1
   if ha:f.status&=~ES.SLEEP
   if f.paralyzed_turns>0:f.paralyzed_turns-=1;continue
   if f.status&(ES.SLEEP|ES.HELD|ES.CONF):
    if R.random()<0.2: f.status &= ~(ES.SLEEP|ES.HELD|ES.CONF)
    continue
   if"Mimic"in f.flags:
    d=math.hypot(en.x-p.x,en.y-p.y)
    if not(d<1.5 or f.hp<f.max_hp):continue
   if f.status&ES.TERR:continue
   if"Greed"in f.flags:
    gld=s._gold(en)
    if gld:s._mv(en,gld.x,gld.y);continue
   d=math.hypot(en.x-p.x,en.y-p.y)
   if"Gaze"in f.flags and d<6 and e.map.visible[en.x][en.y]:
    if R.random()<0.2:p.fighter.status|=ES.CONF;L("Medusa's gaze confuses you!")
   if"FireBreath"in f.flags and d<6 and e.map.visible[en.x][en.y]:
    if R.random()<0.3:L("Dragon breathes fire!");p.fighter.hp-=roll("3d6")
    if p.fighter.hp<=0:e.state=AS.GAME_OVER;return
   if d<ar or"Mean"in f.flags:
    # Strictly orthogonal attack rule
    if abs(en.x - p.x) + abs(en.y - p.y) == 1:
     if not os:e.combat_system.resolve(en,p)
     if e.state==AS.GAME_OVER:return
    else:s._mv(en,p.x,p.y)
   elif"Erratic"in f.flags and R.random()<0.5:
    dx,dy=R.choice([(0,1),(0,-1),(1,0),(-1,0)])
    nx,ny=en.x+dx,en.y+dy
    if not e.map.is_blocked(nx,ny) and not any(o.x==nx and o.y==ny and o.blocks for o in e.entities):en.x,en.y=nx,ny

 def _gold(s,m):
  mg=None;md=10
  for en in s.e.entities:
   if en.item and en.item.category==IC.GOLD:
    d=math.hypot(m.x-en.x,m.y-en.y)
    if d<md and s.e.map.visible[en.x][en.y]:md=d;mg=en
  return mg

 def _mv(s,en,tx,ty):
  dx,dy=tx-en.x,ty-en.y
  if dx==0 and dy==0:return
  px, py = (1 if dx>0 else -1 if dx<0 else 0, 0)
  sx, sy = (0, 1 if dy>0 else -1 if dy<0 else 0)
  if abs(dy) > abs(dx): px, py, sx, sy = sx, sy, px, py

  for mx, my in [(px, py), (sx, sy)]:
   if mx==0 and my==0: continue
   nx, ny = en.x + mx, en.y + my
   if not s.e.map.is_blocked(nx,ny) and not any(o.x==nx and o.y==ny and o.blocks for o in s.e.entities):
    en.x, en.y = nx, ny
    return

class Renderer:
 def __init__(s,root):
  s.root=root;root.title("Micro Rogue");s.scale=1;s.gi=False
  s._setup();s.shadow=[[None]*SH for _ in range(SW)]

 def _setup(s):
  w,h=SW*6,SH*10;s.root.geometry(f"{w}x{h}");s.root.configure(bg=COL["BLACK"])
  if hasattr(s,'canvas'):s.canvas.destroy()
  s.canvas=tk.Canvas(s.root,width=w,height=h,bg=COL["BLACK"],highlightthickness=0);s.canvas.pack();s.gi=False

 def _grid(s):
  if s.gi:return
  s.canvas.delete("all");fnt=("Courier New",10,"bold");cw,ch=6,10
  s.tiles=[[s.canvas.create_text(x*cw+3,y*ch+5,text=" ",fill=COL["BLACK"],font=fnt,anchor="center")for y in range(SH)]for x in range(SW)];s.gi=True

 def _txt(s,g,cx,y,txt,col):
  off=len(txt)//2
  for i,c in enumerate(txt):
   tx=cx-off+i
   if 0<=tx<SW:g[tx][y]=(c,col)

 def _flush(s,vg):
  for x in range(SW):
   for y in range(SH):
    if vg[x][y]!=s.shadow[x][y]:c,col=vg[x][y];s.canvas.itemconfigure(s.tiles[x][y],text=c,fill=COL.get(col,col));s.shadow[x][y]=vg[x][y]

 def menu(s):
  s._grid();g=[[(" ","BLACK")for _ in range(SH)]for _ in range(SW)]
  s._txt(g,SW//2,8,"MICRO ROGUE","GOLD");s._txt(g,SW//2,10,"Rogue 1980 Reference","GREEN");s._txt(g,SW//2,14,"[ENTER] Start  [ESC] Quit","WHITE");s._flush(g)

 def game(s,eng):
  s._grid();vg=[[(" ","BLACK")for _ in range(SH)]for _ in range(SW)];hl=bool(eng.player.fighter.status&ES.HALL)
  for x in range(SW):
   for y in range(SH):
    if eng.map.visible[x][y]:
     if hl and R.random()<0.3:vg[x][y]=(R.choice(['#','.','*','|','+']),R.choice(list(COL.keys())))
     else:tt=eng.map.tiles[x][y];vg[x][y]=(TC.get(tt if tt!=TT.SEC else TT.WH,' '),TLC.get(tt if tt!=TT.SEC else TT.WH,"WHITE"))
    elif eng.map.explored[x][y]:tt=eng.map.tiles[x][y];vg[x][y]=(TC.get(tt if tt!=TT.SEC else TT.WH,' '),"GRAY")
  for ent in sorted(eng.entities,key=lambda e:e.render_order):
   if eng.map.visible[ent.x][ent.y]:
    if eng.player.fighter.status&ES.BLIND and ent!=eng.player:continue
    if ent.fighter and"Invis"in ent.fighter.flags and ent!=eng.player and not(eng.player.fighter.status&ES.SEEINV):continue
    c,col=ent.char,ent.color
    if hl and ent!=eng.player:c,col=chr(R.randint(65,90)),R.choice(list(COL.keys()))
    if ent.fighter and"Mimic"in ent.fighter.flags and not(ent.fighter.status&~ES.NONE):c,col='?',"LIGHT_BLUE"
    vg[ent.x][ent.y]=(c,col)
  msg=eng.current_msg or(eng.msg_queue[0]if eng.msg_queue else"")
  msg=(msg[:SW-10]+"...")if len(msg)>SW else msg
  msg+=" --More--"if len(eng.msg_queue)>1 else""
  if eng.state==AS.DIR:msg="Direction?"
  for i,c in enumerate(msg):
   if i<SW:vg[i][0]=(c,"WHITE")
  hs="Hungry"if eng.hunger<150 else""
  if eng.hunger<=0:hs="Weak"
  if eng.hunger<=-10:hs="Faint"
  pf=eng.player.fighter
  if pf.status&ES.BLIND:hs+=" Blind"
  if pf.status&ES.CONF:hs+=" Conf"
  if pf.status&ES.HALL:hs+=" Hallu"
  if pf.status&ES.LEVI:hs+=" Float"
  ac=pf.base_ac;a=next((i for i in eng.player.inventory if i.category==IC.ARM and i.equipped),None)
  if a:ac=a.ac-a.bonus
  for r in[i for i in eng.player.inventory if i.category==IC.RING and i.equipped and i.real_name=="Protection"]:ac-=1
  st=f"Lv:{pf.level} Au:{eng.gold_purse} Hp:{pf.hp}({pf.max_hp}) Str:{pf.strength}({pf.max_strength}) Ac:{ac} Xp:{pf.xp} Dl:{eng.level} {hs}"
  for i,c in enumerate(st):
   if i<SW:vg[i][SH-1]=(c,"WHITE")
  s._flush(vg)

 def inv(s,items,kt=set()):
  s._grid();g=[[(" ","BLACK")for _ in range(SH)]for _ in range(SW)];cx=SW//2;s._txt(g,cx,2,"INVENTORY","GOLD")
  for i,it in enumerate(items[:26]):
   let=chr(ord('a')+i);st=""
   kn = it.real_name in kt
   dn=it.real_name if (it.identified or kn) else it.unknown_name
   if it.equipped:st=" (equipped)"
   elif it.category==IC.WAND:st=f" [{it.charges}]"
   sfx=(" (Cursed)"if it.status==IS.CURSED else" (Blessed)"if it.status==IS.BLESSED else" (Vorpal)"if it.status==IS.VORPAL else"")if (it.identified or kn) else""
   s._txt(g,cx,4+i,f"{let}) {dn}{sfx}{st}","WHITE")
  s._flush(g)

 def end(s,eng):
  s._grid();g=[[(" ","BLACK")for _ in range(SH)]for _ in range(SW)];cx,cy=SW//2,SH//2
  if eng.state==AS.VICTORY:s._txt(g,cx,cy-4,"*** VICTORY ***","GOLD");s._txt(g,cx,cy-2,"You escaped the dungeon!","GREEN")
  else:s._txt(g,cx,cy-4,"*** YOU DIED ***","RED");s._txt(g,cx,cy-2,"Better luck next time.","GRAY")
  sc,gp=eng.final_score();s._txt(g,cx,cy,f"Score: {sc}  Gold: {gp}","YELLOW");s._txt(g,cx,cy+2,"[ENTER] New Game","WHITE");s._flush(g)

class GameEngine:
 def __init__(s):
  s.level=1;s.entities=[];s.msg_queue=[];s.player=None;s.map=None;s.state=AS.PLAYING
  s.hunger=2000;s.turns=0;s.has_amulet=False;s.gold_purse=0;s.current_msg=""
  s.pending_action=None;s.pending_scroll_idx=None;s.known_types=set()
  s.combat_system=CombatSystem(s);s.magic_system=MagicSystem(s);s.ai_system=AISystem(s)
  s._ids();s.new_level()

 def _ids(s):
  def mid(n,d):d=list(d);R.shuffle(d);return{n[i]:d[i%len(d)]for i in range(len(n))}
  s.potion_ids=mid(PN,PC);s.scroll_ids=mid(SN,ST);s.wand_ids=mid(WN,WM);s.ring_ids=mid(RN,RS)

 def log(s,t):s.msg_queue.append(t)

 def new_level(s):
  if s.player:s.entities=[s.player]
  else:
   s.player=Entity(0,0,'@',"WHITE","Player",True);s.player.fighter=Fighter(12,10,16,"1d4")
   m=Item(IC.WPN,"Mace",dmg="2d4");m.identified=True;m.equipped=True;s.player.inventory.append(m)
   s.player.inventory.append(Item(IC.FOOD,"Food ration"));s.entities=[s.player]
  s.map=DungeonMap(SW,SH);sx,sy=s.map.generate(s.level,s.entities);s.player.x,s.player.y=sx,sy;s.spawn_objs();s.fov();s.log(f"Level {s.level}")

 def spawn_objs(s):
  c=[k for k,v in BES.items()if int(v[2])<=s.level]or['B']
  for _ in range(s.level+3):s.spawn(R.choice(c))
  wt=[40,18,18,10,8,8,6,4];tp=[IC.GOLD,IC.POT,IC.SCR,IC.FOOD,IC.WPN,IC.ARM,IC.WAND,IC.RING]
  for _ in range(R.randint(4,8)):
   cat=R.choices(tp,weights=wt,k=1)[0];x,y=s.rnd_floor()
   r=R.random();st=IS.CURSED if r<0.1 else IS.BLESSED if r>0.9 else IS.N
   bn=R.randint(1,3)if st==IS.BLESSED else R.randint(-3,-1)if st==IS.CURSED else 0
   if cat==IC.GOLD:v=(roll("2d6")+2)*s.level;gld=Entity(x,y,'*',"GOLD","Gold",False,RO.ITEM);gld.item=Item(cat,"Gold",val=v);s.entities.append(gld)
   elif cat==IC.POT:knd=R.choice(list(s.potion_ids.keys()));unk=f"{s.potion_ids[knd]} Potion";ent=Entity(x,y,'!',"CYAN",unk,False,RO.ITEM);ent.item=Item(cat,knd,eff=knd);ent.item.unknown_name=unk;s.entities.append(ent)
   elif cat==IC.SCR:knd=R.choice(list(s.scroll_ids.keys()));unk=f"Scroll '{s.scroll_ids[knd]}'";ent=Entity(x,y,'?',"LIGHT_BLUE",unk,False,RO.ITEM);ent.item=Item(cat,knd,eff=knd);ent.item.unknown_name=unk;s.entities.append(ent)
   elif cat==IC.FOOD:fnm="Food ration"if R.random()>=0.05 else"Slime Mold";ent=Entity(x,y,':',"ORANGE",fnm,False,RO.ITEM);ent.item=Item(cat,fnm);s.entities.append(ent)
   elif cat==IC.WPN:knd=R.choice(list(WPN.keys()));ent=Entity(x,y,')',"BLUE",knd,False,RO.ITEM);ent.item=Item(cat,knd,dmg=WPN[knd]);ent.item.status=st;ent.item.bonus=bn;s.entities.append(ent)
   elif cat==IC.ARM:knd=R.choice(list(ARM.keys()));ent=Entity(x,y,']',"GRAY",knd,False,RO.ITEM);ent.item=Item(cat,knd,ac=ARM[knd]);ent.item.status=st;ent.item.bonus=bn;s.entities.append(ent)
   elif cat==IC.WAND:knd=R.choice(list(s.wand_ids.keys()));unk=f"{s.wand_ids[knd]} Wand";ent=Entity(x,y,'/',"SILVER",unk,False,RO.ITEM);ent.item=Item(cat,knd,eff=knd,ch=R.randint(3,10));ent.item.unknown_name=unk;s.entities.append(ent)
   elif cat==IC.RING:knd=R.choice(list(s.ring_ids.keys()));unk=f"{s.ring_ids[knd]} Ring";ent=Entity(x,y,'=',"BRONZE",unk,False,RO.ITEM);ent.item=Item(cat,knd,eff=knd);ent.item.unknown_name=unk;ent.item.status=st;ent.item.bonus=bn;s.entities.append(ent)

 def spawn(s,key,np=False):
  md=BES[key];x,y=0,0
  if np:
   fd=False
   for dx in range(-1,2):
    for dy in range(-1,2):
     nx,ny=s.player.x+dx,s.player.y+dy
     if not s.map.is_blocked(nx,ny)and not any(e.x==nx and e.y==ny for e in s.entities):x,y=nx,ny;fd=True;break
    if fd:break
   if not fd:return
  else:x,y=s.rnd_floor()
  m=Entity(x,y,md[0],md[8],md[1].replace('_',' '),True,RO.ACTOR)
  m.fighter=Fighter(roll(md[4]),int(md[3]),10,md[5],int(md[2]));m.fighter.xp=int(md[6]);m.fighter.flags=md[7].split(',')if md[7]!='-'else[];s.entities.append(m);return m

 def rnd_floor(s):
  while True:
   r=R.choice(s.map.rooms);x,y=R.randint(r.x1+1,r.x2-1),R.randint(r.y1+1,r.y2-1)
   if not any(e.x==x and e.y==y for e in s.entities):return x,y

 def eff_str(s,e):
  sv=e.fighter.strength
  if e==s.player:
   for r in[i for i in e.inventory if i.category==IC.RING and i.equipped and i.real_name=="Add Strength"]:sv+=1
  return sv

 def fov(s):s.map.fov(s.player.x,s.player.y,bool(s.player.fighter.status&ES.BLIND))

 def handle(s,act):
  if s.state!=AS.PLAYING:return
  if act=="PICKUP":s.pickup();return
  if act=="SEARCH":s.search();s.tick();return
  if act=="WAIT":s.tick();return
  if act=="DROP":
   inv=[i for i in s.player.inventory if not i.equipped]
   if inv:
    it=inv[0];s.player.inventory.remove(it)
    ch_map={IC.WPN:')',IC.POT:'!',IC.SCR:'?',IC.FOOD:':',IC.ARM:']',IC.WAND:'/',IC.RING:'=',IC.AMU:',',IC.GOLD:'*'}
    d=Entity(s.player.x,s.player.y,ch_map.get(it.category,']'),"GRAY",it.real_name,False,RO.ITEM);d.item=it;s.entities.append(d);s.log(f"Dropped {it.real_name}.")
   else:s.log("Nothing to drop.")
   return
  dx,dy=0,0
  if act=='N':dy=-1
  elif act=='S':dy=1
  elif act=='W':dx=-1
  elif act=='E':dx=1
  if s.player.fighter.status&ES.CONF:
   if R.random()<0.4:dx,dy=R.choice([(0,1),(0,-1),(1,0),(-1,0)]);s.log("You stagger...")
  nx,ny=s.player.x+dx,s.player.y+dy
  if dx!=0 or dy!=0:
   if s.player.fighter.paralyzed_turns>0:s.player.fighter.paralyzed_turns-=1;s.log("Frozen!");s.tick();return
   tgt=next((e for e in s.entities if e.x==nx and e.y==ny and e.blocks),None)
   if tgt and tgt.fighter:s.combat_system.resolve(s.player,tgt)
   elif not s.map.is_blocked(nx,ny):
    s.player.x,s.player.y=nx,ny
    if(nx,ny)in s.map.traps:
     if not(s.player.fighter.status&ES.LEVI):
      tt=s.map.traps.pop((nx,ny));s.log(f"Trap: {tt}!")
      if tt=="Trapdoor":s.level+=1;s.new_level();return
      elif tt=="Arrow Trap":s.player.fighter.hp-=roll("1d6")
      elif tt=="Rust Trap":
       a=next((i for i in s.player.inventory if i.equipped and i.category==IC.ARM),None)
       if a and"Leather"not in a.real_name and not any(r.real_name=="Maintain Armor"and r.equipped for r in s.player.inventory)and R.random()<0.5:a.ac+=1;s.log("Armor weakens!")
      elif tt=="Teleport Trap":s.player.x,s.player.y=s.rnd_floor();s.log("Whoosh!")
      elif tt=="Sleeping Gas Trap":s.player.fighter.paralyzed_turns+=5;s.log("You fall asleep.")
      elif tt=="Bear Trap":s.player.fighter.paralyzed_turns+=3;s.log("You are caught!")
     else:s.log("Float over trap.")
    ih=[e for e in s.entities if e.x==nx and e.y==ny and e.item]
    if ih:
     tp=ih[0]
     nm=tp.item.real_name if tp.item.category in(IC.WPN,IC.ARM,IC.FOOD)or tp.item.identified or tp.item.real_name in s.known_types else tp.item.unknown_name
     s.log(f"You see {nm}.")
    tl=s.map.tiles[nx][ny]
    if tl==TT.SU:
     if s.level>1:s.level-=1;s.new_level();s.log("Spiral up.")
     elif s.has_amulet:s.state=AS.VICTORY;s.log("You escape! Victory!")
     else:s.log("Need the Amulet!")
    elif tl==TT.SD:s.level+=1;s.new_level();s.log("Descend.")
  if s.state==AS.PLAYING:s.tick()

 def pickup(s):
  ih=[e for e in s.entities if e.x==s.player.x and e.y==s.player.y and e.item]
  if not ih:s.log("Nothing here.");return
  tgt=ih[0]
  if tgt.item.category==IC.GOLD:s.gold_purse+=tgt.item.value;s.log(f"{tgt.item.value} gold.");s.entities.remove(tgt);return
  if tgt.item.category==IC.AMU:s.has_amulet=True;s.log("Got the Amulet!");s.entities.remove(tgt);return
  if len(s.player.inventory)>=PS:s.log("Pack full.");return
  s.player.inventory.append(tgt.item);s.entities.remove(tgt)
  nm=tgt.item.real_name if tgt.item.identified or tgt.item.real_name in s.known_types else tgt.item.unknown_name
  s.log(f"Picked up {nm}.")

 def search(s):
  ch=0.50 if any(i.real_name=="Searching"and i.equipped for i in s.player.inventory)else 0.16
  fd=False
  if R.random()<ch:
   for dx in range(-1,2):
    for dy in range(-1,2):
     nx,ny=s.player.x+dx,s.player.y+dy
     if 0<=nx<s.map.width and 0<=ny<s.map.height:
      if s.map.tiles[nx][ny]==TT.SEC:s.map.tiles[nx][ny]=TT.DOOR;fd=True
      if(nx,ny)in s.map.traps:s.log(f"Found {s.map.traps[(nx,ny)]}!");fd=True
  s.log("Found something!"if fd else"Nothing found.")

 def final_score(s):
  sc=s.gold_purse+(int(s.gold_purse*0.1)if s.has_amulet else 0)+(s.gold_purse if s.state==AS.VICTORY else 0)
  return sc,s.gold_purse

 def tick(s):
  if s.state!=AS.PLAYING:return
  s.turns+=1;s.ai_system.tick()
  if s.state!=AS.PLAYING:return
  rw=sum(1 for i in s.player.inventory if i.category==IC.RING and i.equipped);hc=1+rw
  if any(i.real_name=="Slow Digestion"and i.equipped for i in s.player.inventory):hc=max(1,hc//2)
  s.hunger-=hc

  # Status Recovery logic so you aren't blind/confused forever
  if R.random() < 0.05: s.player.fighter.status &= ~(ES.BLIND | ES.CONF | ES.HALL)

  if any(i.real_name=="Teleportation"and i.equipped for i in s.player.inventory):
   if R.random()<0.02:s.player.x,s.player.y=s.rnd_floor();s.log("Ring teleports you!")
  if s.hunger==HG['WARN']:s.log("Getting hungry.")
  if s.hunger==HG['WEAK']:s.log("You feel weak.")
  if HG['STARVE']<s.hunger<=HG['FAINT']:
   if R.random()<0.1:s.log("Faint from hunger.");s.player.fighter.paralyzed_turns+=R.randint(2,5)
  if s.hunger<=HG['STARVE']:s.state=AS.GAME_OVER;s.log("Starved to death.");return
  rr=max(1,21-(s.player.fighter.level*2))
  if any(i.real_name=="Regeneration"and i.equipped for i in s.player.inventory):rr=max(1,rr//2)
  if s.turns%rr==0 and s.hunger>0:s.player.fighter.hp=min(s.player.fighter.max_hp,s.player.fighter.hp+1)
  s.fov()

class RogueApp:
 def __init__(s):
  s.root=tk.Tk();s.rnd=Renderer(s.root);s.state=AS.MENU;s.inv_mode=None
  try:
   with open("rogue.dat","rb")as f:s.engine=pickle.load(f)
   s.state=AS.PLAYING;s.engine.log("Game Loaded.");s.rnd.game(s.engine)
  except:s.rnd.menu()
  s.root.bind("<KeyPress>",s.handle);s.root.mainloop()

 def start(s):s.engine=GameEngine();s.state=AS.PLAYING;s.rnd.game(s.engine)

 def _save_score(s):
  try:
   sc,gp=s.engine.final_score();hs=[]
   try:
    with open("highscores.json")as f:hs=json.load(f)
   except:pass
   hs.append({"score":sc,"gold":gp,"level":s.engine.level});hs.sort(key=lambda x:-x["score"]);hs=hs[:10]
   with open("highscores.json","w")as f:json.dump(hs,f)
  except:pass

 def handle(s,ev):
  k=ev.keysym.upper();c=ev.char
  if s.state in(AS.GAME_OVER,AS.VICTORY):
   if k=="RETURN":s._save_score();s.state=AS.MENU;s.rnd.menu()
   elif k=="ESCAPE":s.root.destroy()
   return
  if s.state==AS.MENU:
   if k=="RETURN":s.start()
   elif k=="ESCAPE":s.root.destroy()
  elif s.state==AS.PLAYING:
   if s.engine.state in(AS.GAME_OVER,AS.VICTORY):s.state=s.engine.state;s.rnd.end(s.engine);return
   if len(s.engine.msg_queue)>1:
    if k=="SPACE":s.engine.msg_queue.pop(0);s.rnd.game(s.engine)
    return
   act=None
   if k in["UP","K","W"]:act="N"
   elif k in["DOWN","J","S"]:act="S"
   elif k in["LEFT","H","A"]:act="W"
   elif k in["RIGHT","L","D"]:act="E"
   elif k in["PERIOD","SPACE"]:act="WAIT"
   elif k=="COMMA":act="PICKUP"
   elif c=="s":act="SEARCH"
   elif c=="d":act="DROP"
   elif c=="S":
    try:
     with open("rogue.dat","wb")as f:pickle.dump(s.engine,f)
     s.engine.log("Saved.");s.root.destroy();import sys;sys.exit()
    except:s.engine.log("Save Failed!")
   elif k=="I":s.state=AS.INV;s.inv_mode=None;s.rnd.inv(s.engine.player.inventory,s.engine.known_types);return
   elif c=="z":s.state=AS.INV;s.inv_mode="ZAP";s.rnd.inv([i for i in s.engine.player.inventory if i.category==IC.WAND],s.engine.known_types);return
   elif c=="t":s.state=AS.INV;s.inv_mode="THROW";s.rnd.inv(s.engine.player.inventory,s.engine.known_types);return
   if act:s.engine.handle(act)
   if s.engine.state in(AS.GAME_OVER,AS.VICTORY):s.state=s.engine.state;s.rnd.end(s.engine);return
   s.rnd.game(s.engine)
  elif s.state==AS.SELECT:
   if k=="ESCAPE":s.state=AS.PLAYING;s.engine.state=AS.PLAYING;s.engine.pending_scroll_idx=None;s.rnd.game(s.engine);return
   if len(c)==1 and'a'<=c<='z':s.engine.magic_system.identify(ord(c)-ord('a'));s.state=AS.PLAYING;s.rnd.game(s.engine)
  elif s.state==AS.INV:
   if k=="ESCAPE":s.state=AS.PLAYING;s.inv_mode=None;s.rnd.game(s.engine)
   elif len(c)==1 and'a'<=c<='z':
    idx=ord(c)-ord('a');inv=s.engine.player.inventory
    if s.inv_mode=="ZAP":
     wnd=[i for i in inv if i.category==IC.WAND]
     if 0<=idx<len(wnd):rid=inv.index(wnd[idx]);s.engine.pending_action=("ZAP",rid);s.state=AS.DIR;s.rnd.game(s.engine)
     return
    elif s.inv_mode=="THROW":
     if 0<=idx<len(inv):s.engine.pending_action=("THROW",idx);s.state=AS.DIR;s.rnd.game(s.engine)
     return
    if 0<=idx<len(inv):s.engine.use(idx);s.state=AS.PLAYING if s.engine.state!=AS.SELECT else AS.SELECT;s.rnd.game(s.engine)
  elif s.state==AS.DIR:
   dx,dy={"UP":(0,-1),"DOWN":(0,1),"LEFT":(-1,0),"RIGHT":(1,0),"K":(0,-1),"J":(0,1),"H":(-1,0),"L":(1,0)}.get(k,(0,0))
   if dx or dy:
    act,idx=s.engine.pending_action
    if act=="ZAP":s.engine.magic_system.zap(s.engine.player.inventory[idx],dx,dy)
    elif act=="THROW":s.engine.combat_system.throw(idx,dx,dy)
    s.engine.pending_action=None;s.engine.tick();s.state=AS.PLAYING;s.rnd.game(s.engine)
   elif k=="ESCAPE":s.state=AS.PLAYING;s.engine.pending_action=None;s.rnd.game(s.engine)

if __name__=="__main__":RogueApp()