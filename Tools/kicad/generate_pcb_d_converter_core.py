from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import argparse
import uuid

parser = argparse.ArgumentParser(description='Generate PCB-D KiCad symbol library and converter-core schematic deterministically.')
parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parents[2] / 'Hardware' / 'KiCad')
args = parser.parse_args()
OUT = args.output_dir
OUT.mkdir(parents=True, exist_ok=True)
NS = uuid.UUID('1cfb640a-2819-4f68-a76f-c45a4cb50d66')

def uid(name: str) -> str:
    return str(uuid.uuid5(NS, name))

def fx(v: float) -> str:
    s = f'{v:.4f}'.rstrip('0').rstrip('.')
    return '0' if s == '-0' else s

def effects(size=1.0, hide=False, justify=None):
    parts = [f'(effects (font (size {fx(size)} {fx(size)}))']
    if justify:
        parts.append(f' (justify {justify})')
    if hide:
        parts.append(' (hide yes)')
    parts.append(')')
    return ''.join(parts)

@dataclass
class Pin:
    num: str
    name: str
    etype: str
    side: str = 'left'
    y: float = 0.0
    style: str = 'line'
    net: str = ''

# Exact PCB-D configuration-specific electrical typing.
pin_rows = [
('1','SS2','passive','SS_COMMON'),('2','COMP2','passive','COMP_COMMON'),('3','FB2','input','AGND'),
('4','CS2','input','CS2_FILTERED'),('5','VOUT2','input','5V_SYS_BUS'),('6','VCCX','power_in','5V_SYS_BUS'),
('7','PG2','open_collector','NC_PG2_TESTPAD'),('8','HOL2','output','GH2_OFF'),('9','HO2','output','GH2_ON'),
('10','SW2','passive','PHASE2_SW'),('11','HB2','passive','HB2_BOOT'),('12','LOL2','output','GL2_OFF'),
('13','LO2','output','GL2_ON'),('14','PGND2','power_in','POWER_GND'),('15','VCC','power_out','VCC_BIAS'),
('16','VCC','passive','VCC_BIAS'),('17','PGND1','power_in','POWER_GND'),('18','LO1','output','GL1_ON'),
('19','LOL1','output','GL1_OFF'),('20','HB1','passive','HB1_BOOT'),('21','SW1','passive','PHASE1_SW'),
('22','HO1','output','GH1_ON'),('23','HOL1','output','GH1_OFF'),('24','PG1','open_collector','P5_PGOOD_OD'),
('25','VIN','power_in','PACK_BUS_P5_IN'),('26','VOUT1','input','5V_SYS_BUS'),('27','CS1','input','CS1_FILTERED'),
('28','FB1','input','AGND'),('29','COMP1','output','COMP_COMMON'),('30','SS1','input','SS_COMMON'),
('31','EN1','input','EN_RUN'),('32','RES','output','RES_TIMER'),('33','DEMB','input','VDDA_BIAS'),
('34','MODE','input','VDDA_BIAS'),('35','AGND','power_in','AGND'),('36','VDDA','power_out','VDDA_BIAS'),
('37','RT','input','RT_SET'),('38','DITH','input','VDDA_BIAS'),('39','SYNCOUT','output','SYNCOUT_TESTPAD'),
('40','EN2','input','EN_RUN'),('EP','EXPOSED_PAD','passive','AGND'),
]

pins: list[Pin] = []
for i,(num,name,etype,net) in enumerate(pin_rows[:-1]):
    if i < 20:
        y = -24.13 + i*2.54
        side='left'
    else:
        y = -24.13 + (i-20)*2.54
        side='right'
    pins.append(Pin(num,name,etype,side,y,'line',net))
pins.append(Pin('EP','EXPOSED_PAD','passive','bottom',0,'line','AGND'))


def prop(key, val, idx, x, y, angle=0, hide=False):
    return f'''\t\t(property "{key}" "{val}"\n\t\t\t(at {fx(x)} {fx(y)} {angle})\n\t\t\t{effects(1.0, hide)}\n\t\t)'''

def pin_def(pin: Pin):
    if pin.side == 'left':
        x, y, ang = -15.24, pin.y, 0
    elif pin.side == 'right':
        x, y, ang = 15.24, pin.y, 180
    else:
        x, y, ang = 0, 27.94, 270
    return f'''\t\t\t(pin {pin.etype} {pin.style}\n\t\t\t\t(at {fx(x)} {fx(y)} {ang})\n\t\t\t\t(length 2.54)\n\t\t\t\t(name "{pin.name}" {effects(0.9)})\n\t\t\t\t(number "{pin.num}" {effects(0.9)})\n\t\t\t)'''

def controller_symbol(lib_id='plataVM:LM5143A_Q1_RHA40'):
    props = '\n'.join([
        prop('Reference','U',0,0,-29.21),
        prop('Value','LM5143A_Q1_RHA40',1,0,-26.67),
        prop('Footprint','',2,0,0,hide=True),
        prop('Datasheet','https://www.ti.com/lit/ds/symlink/lm5143a-q1.pdf',3,0,0,hide=True),
        prop('Description','LM5143A-Q1 PCB-D configured exact RHA-40 symbol; no footprint freeze',4,0,0,hide=True),
    ])
    pintext='\n'.join(pin_def(p) for p in pins)
    return f'''\t(symbol "{lib_id}"\n\t\t(pin_names (offset 0.762))\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n{props}\n\t\t(symbol "LM5143A_Q1_RHA40_0_1"\n\t\t\t(rectangle\n\t\t\t\t(start -12.7 -25.4)\n\t\t\t\t(end 12.7 25.4)\n\t\t\t\t(stroke (width 0.254) (type default))\n\t\t\t\t(fill (type background))\n\t\t\t)\n\t\t\t(text "LM5143A-Q1" (at 0 -2.54 0) {effects(1.27)})\n\t\t\t(text "RHA-40 / PCB-D" (at 0 0 0) {effects(1.0)})\n\t\t\t(text "PIN MAP VERIFIED" (at 0 2.54 0) {effects(0.9)})\n\t\t)\n\t\t(symbol "LM5143A_Q1_RHA40_1_1"\n{pintext}\n\t\t)\n\t)'''

def two_pin_symbol(name, ref, graphic='box', in_bom='yes', on_board='yes', pin_types=('passive','passive')):
    if graphic == 'res':
        shape='''\t\t\t(rectangle (start -2.54 -1.016) (end 2.54 1.016) (stroke (width 0.254) (type default)) (fill (type none)))'''
    elif graphic == 'cap':
        shape='''\t\t\t(polyline (pts (xy -0.762 -2.032) (xy -0.762 2.032)) (stroke (width 0.254) (type default)) (fill (type none)))\n\t\t\t(polyline (pts (xy 0.762 -2.032) (xy 0.762 2.032)) (stroke (width 0.254) (type default)) (fill (type none)))'''
    elif graphic == 'diode':
        shape='''\t\t\t(polyline (pts (xy -1.27 -1.778) (xy -1.27 1.778) (xy 1.27 0) (xy -1.27 -1.778)) (stroke (width 0.254) (type default)) (fill (type none)))\n\t\t\t(polyline (pts (xy 1.27 -1.778) (xy 1.27 1.778)) (stroke (width 0.254) (type default)) (fill (type none)))'''
    elif graphic == 'inductor':
        shape='''\t\t\t(rectangle (start -2.54 -1.27) (end 2.54 1.27) (stroke (width 0.254) (type default)) (fill (type none)))\n\t\t\t(text "L" (at 0 0 0) (effects (font (size 1 1))))'''
    else:
        shape='''\t\t\t(rectangle (start -2.54 -1.27) (end 2.54 1.27) (stroke (width 0.254) (type default)) (fill (type none)))'''
    props='\n'.join([
        prop('Reference',ref,0,0,-2.54), prop('Value',name.split(':')[-1],1,0,2.54),
        prop('Footprint','',2,0,0,hide=True), prop('Datasheet','~',3,0,0,hide=True)
    ])
    base=name.split(':')[-1]
    return f'''\t(symbol "{name}"\n\t\t(pin_names (offset 0))\n\t\t(exclude_from_sim no)\n\t\t(in_bom {in_bom})\n\t\t(on_board {on_board})\n{props}\n\t\t(symbol "{base}_0_1"\n{shape}\n\t\t)\n\t\t(symbol "{base}_1_1"\n\t\t\t(pin {pin_types[0]} line (at -5.08 0 0) (length 2.54) (name "1" {effects(0.8)}) (number "1" {effects(0.8)}))\n\t\t\t(pin {pin_types[1]} line (at 5.08 0 180) (length 2.54) (name "2" {effects(0.8)}) (number "2" {effects(0.8)}))\n\t\t)\n\t)'''

def nmos_symbol():
    props='\n'.join([prop('Reference','Q',0,0,-4.064),prop('Value','NMOS_POWER',1,0,4.064),prop('Footprint','',2,0,0,hide=True),prop('Datasheet','~',3,0,0,hide=True)])
    return f'''\t(symbol "plataVM:NMOS_POWER"\n\t\t(pin_names (offset 0.5))\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n{props}\n\t\t(symbol "NMOS_POWER_0_1"\n\t\t\t(rectangle (start -2.54 -2.54) (end 2.54 2.54) (stroke (width 0.254) (type default)) (fill (type none)))\n\t\t\t(text "NMOS" (at 0 0 0) {effects(0.8)})\n\t\t)\n\t\t(symbol "NMOS_POWER_1_1"\n\t\t\t(pin passive line (at -5.08 0 0) (length 2.54) (name "G" {effects(0.8)}) (number "1" {effects(0.8)}))\n\t\t\t(pin passive line (at 5.08 -1.27 180) (length 2.54) (name "D" {effects(0.8)}) (number "2" {effects(0.8)}))\n\t\t\t(pin passive line (at 5.08 1.27 180) (length 2.54) (name "S" {effects(0.8)}) (number "3" {effects(0.8)}))\n\t\t)\n\t)'''

def one_pin_symbol(name, ref, etype='passive', on_board='yes', in_bom='no'):
    base=name.split(':')[-1]
    props='\n'.join([prop('Reference',ref,0,0,-2.54,hide=True),prop('Value',base,1,0,2.54),prop('Footprint','',2,0,0,hide=True),prop('Datasheet','~',3,0,0,hide=True)])
    return f'''\t(symbol "{name}"\n\t\t(pin_names hide)\n\t\t(exclude_from_sim no)\n\t\t(in_bom {in_bom})\n\t\t(on_board {on_board})\n{props}\n\t\t(symbol "{base}_0_1"\n\t\t\t(polyline (pts (xy -1.27 0) (xy 1.27 0)) (stroke (width 0.254) (type default)) (fill (type none)))\n\t\t)\n\t\t(symbol "{base}_1_1"\n\t\t\t(pin {etype} line (at 0 2.54 270) (length 2.54) (name "1" {effects(0.8)}) (number "1" {effects(0.8)}))\n\t\t)\n\t)'''


def box_symbol(name, ref, pin_specs, width=15.24, height=12.7, in_bom='yes', on_board='yes'):
    """Create a deterministic multi-pin placeholder block.

    pin_specs entries are: (number, name, electrical_type, side, offset).
    For left/right pins, offset is Y. For top/bottom pins, offset is X.
    """
    base=name.split(':')[-1]
    props='\\n'.join([
        prop('Reference',ref,0,0,-height/2-2.54),
        prop('Value',base,1,0,height/2+2.54),
        prop('Footprint','',2,0,0,hide=True),
        prop('Datasheet','~',3,0,0,hide=True),
        prop('Description','CALC_TBD placeholder; no production part/footprint freeze',4,0,0,hide=True),
    ])
    pin_lines=[]
    for num,pname,etype,side,offset in pin_specs:
        if side=='left':
            x,y,ang=-width/2-2.54,offset,0
        elif side=='right':
            x,y,ang=width/2+2.54,offset,180
        elif side=='top':
            x,y,ang=offset,-height/2-2.54,90
        elif side=='bottom':
            x,y,ang=offset,height/2+2.54,270
        else:
            raise ValueError(side)
        pin_lines.append(
            f'''\\t\\t\\t(pin {etype} line (at {fx(x)} {fx(y)} {ang}) (length 2.54) (name "{pname}" {effects(0.8)}) (number "{num}" {effects(0.8)}))'''
        )
    return f'''\\t(symbol "{name}"
\\t\\t(pin_names (offset 0.6))
\\t\\t(exclude_from_sim no)
\\t\\t(in_bom {in_bom})
\\t\\t(on_board {on_board})
{props}
\\t\\t(symbol "{base}_0_1"
\\t\\t\\t(rectangle (start {fx(-width/2)} {fx(-height/2)}) (end {fx(width/2)} {fx(height/2)}) (stroke (width 0.254) (type default)) (fill (type background)))
\\t\\t\\t(text "CALC_TBD" (at 0 0 0) {effects(0.9)})
\\t\\t)
\\t\\t(symbol "{base}_1_1"
{chr(10).join(pin_lines)}
\\t\\t)
\\t)'''

uvlo_symbol = box_symbol('plataVM:UVLO_SUPERVISOR_TBD','U',[
    ('1','VIN_SENSE','power_in','left',-2.54),
    ('2','GND','power_in','left',2.54),
    ('3','UVLO_OK','output','right',0),
], width=15.24, height=10.16)
enable_symbol = box_symbol('plataVM:HW_ENABLE_GATE_TBD','U',[
    ('1','5V_SYS_EN','input','left',-6.35),
    ('2','UVLO_OK','input','left',-3.81),
    ('3','SAFE_OFF','input','left',-1.27),
    ('4','HARD_OFF','input','left',1.27),
    ('5','PACK_BIAS','power_in','left',3.81),
    ('6','GND','power_in','left',6.35),
    ('7','EN_RUN','output','right',0),
], width=20.32, height=17.78)
fault_symbol = box_symbol('plataVM:FAULT_EXPORT_TBD','U',[
    ('1','PGOOD_OD','input','left',-3.81),
    ('2','UVLO_OK','input','left',-1.27),
    ('3','EN_RUN','input','left',1.27),
    ('4','GND','power_in','left',3.81),
    ('5','FAULT_N','open_collector','right',0),
], width=17.78, height=12.7)
isense_symbol = box_symbol('plataVM:ISENSE_EXPORT_TBD','U',[
    ('1','SHUNT_HI','input','left',-1.27),
    ('2','SHUNT_LO','input','left',1.27),
    ('3','ISENSE','output','right',0),
], width=15.24, height=7.62)
isum_symbol = box_symbol('plataVM:ISENSE_SUM_TBD','U',[
    ('1','PHASE1','input','left',-1.27),
    ('2','PHASE2','input','left',1.27),
    ('3','TOTAL','output','right',0),
], width=15.24, height=7.62)

lib_defs = [
    controller_symbol(),
    two_pin_symbol('plataVM:R','R','res'),
    two_pin_symbol('plataVM:C','C','cap'),
    two_pin_symbol('plataVM:L','L','inductor'),
    two_pin_symbol('plataVM:D','D','diode'),
    two_pin_symbol('plataVM:NET_TIE_TBD','NT','box','no','no'),
    nmos_symbol(),
    one_pin_symbol('plataVM:PWR_FLAG','#FLG','power_out','no','no'),
    one_pin_symbol('plataVM:TESTPOINT','TP','passive','yes','yes'),
    uvlo_symbol, enable_symbol, fault_symbol, isense_symbol, isum_symbol,
]


# External symbol library uses entry names without nickname.
external = '\n'.join(s.replace('"plataVM:','"') for s in lib_defs)
sym_text = f'''(kicad_symbol_lib\n\t(version 20241209)\n\t(generator "plataVM_symbol_gate")\n{external}\n)\n'''
(OUT/'plataVM_symbols.kicad_sym').write_text(sym_text, encoding='utf-8')

# Schematic generator helpers.
root_uuid = uid('schematic-root')
objects=[]

def property_instance(k,v,x,y,hide=False):
    return f'''\t\t(property "{k}" "{v}"\n\t\t\t(at {fx(x)} {fx(y)} 0)\n\t\t\t{effects(1.0, hide)}\n\t\t)'''

def sym_instance(lib, ref, value, x, y, pin_nums, rot=0, in_bom='yes', on_board='yes', dnp='no'):
    suid=uid(f'sym:{ref}')
    p_lines=[]
    for num in pin_nums:
        p_lines.append(f'''\t\t(pin "{num}"\n\t\t\t(uuid "{uid(f'pin:{ref}:{num}')}")\n\t\t)''')
    props='\n'.join([
        property_instance('Reference',ref,x,y-4.0), property_instance('Value',value,x,y+4.0),
        property_instance('Footprint','',x,y,True), property_instance('Datasheet','~',x,y,True),
        property_instance('Description','PROTOTYPE / NO FOOTPRINT FREEZE',x,y,True),
    ])
    return f'''\t(symbol\n\t\t(lib_id "{lib}")\n\t\t(at {fx(x)} {fx(y)} {rot})\n\t\t(unit 1)\n\t\t(exclude_from_sim no)\n\t\t(in_bom {in_bom})\n\t\t(on_board {on_board})\n\t\t(dnp {dnp})\n\t\t(uuid "{suid}")\n{props}\n{chr(10).join(p_lines)}\n\t\t(instances\n\t\t\t(project "plataVM"\n\t\t\t\t(path "/{suid}"\n\t\t\t\t\t(reference "{ref}")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)'''

def label(name,x,y,justify='left'):
    return f'''\t(label "{name}"\n\t\t(at {fx(x)} {fx(y)} 0)\n\t\t{effects(0.9, justify=justify)}\n\t\t(uuid "{uid(f'label:{name}:{x}:{y}')}")\n\t)'''

def wire(x1,y1,x2,y2,name):
    return f'''\t(wire\n\t\t(pts (xy {fx(x1)} {fx(y1)}) (xy {fx(x2)} {fx(y2)}))\n\t\t(stroke (width 0) (type default))\n\t\t(uuid "{uid('wire:'+name)}")\n\t)'''

def add_two(ref, lib, value, x,y, net1,net2, rot=0):
    objects.append(sym_instance(lib,ref,value,x,y,['1','2'],rot))
    if rot in (0,180):
        # We only use rot=0 here.
        objects.extend([wire(x-5.08,y,x-7.62,y,f'{ref}:1'),label(net1,x-7.62,y,'right'),wire(x+5.08,y,x+7.62,y,f'{ref}:2'),label(net2,x+7.62,y,'left')])
    else:
        raise NotImplementedError

def add_nmos(ref,x,y,gate,drain,source):
    objects.append(sym_instance('plataVM:NMOS_POWER',ref,'BUK9Y6R0-60E,115',x,y,['1','2','3']))
    objects.extend([
        wire(x-5.08,y,x-7.62,y,f'{ref}:G'),label(gate,x-7.62,y,'right'),
        wire(x+5.08,y-1.27,x+7.62,y-1.27,f'{ref}:D'),label(drain,x+7.62,y-1.27,'left'),
        wire(x+5.08,y+1.27,x+7.62,y+1.27,f'{ref}:S'),label(source,x+7.62,y+1.27,'left'),
    ])

def add_flag(ref,x,y,net):
    objects.append(sym_instance('plataVM:PWR_FLAG',ref,'PWR_FLAG',x,y,['1'],in_bom='no',on_board='no'))
    objects.extend([wire(x,y+2.54,x,y+5.08,f'{ref}:1'),label(net,x,y+5.08,'left')])

def add_tp(ref,x,y,net):
    objects.append(sym_instance('plataVM:TESTPOINT',ref,'TESTPOINT',x,y,['1']))
    objects.extend([wire(x,y+2.54,x,y+5.08,f'{ref}:1'),label(net,x,y+5.08,'left')])

def add_box(ref, lib, value, x, y, pin_connections, width, height, in_bom='yes', on_board='yes'):
    """Instantiate a box symbol and connect every pin to an explicit named net."""
    objects.append(
        sym_instance(
            lib, ref, value, x, y, [p[0] for p in pin_connections],
            in_bom=in_bom, on_board=on_board,
        )
    )
    for num,side,offset,net in pin_connections:
        if side=='left':
            px,py=x-width/2-2.54,y+offset; ox=px-5.08
            objects.extend([wire(px,py,ox,py,f'{ref}:{num}'), label(net,ox,py,'right')])
        elif side=='right':
            px,py=x+width/2+2.54,y+offset; ox=px+5.08
            objects.extend([wire(px,py,ox,py,f'{ref}:{num}'), label(net,ox,py,'left')])
        elif side=='top':
            px,py=x+offset,y-height/2-2.54; oy=py-5.08
            objects.extend([wire(px,py,px,oy,f'{ref}:{num}'), label(net,px,oy,'left')])
        elif side=='bottom':
            px,py=x+offset,y+height/2+2.54; oy=py+5.08
            objects.extend([wire(px,py,px,oy,f'{ref}:{num}'), label(net,px,oy,'left')])
        else:
            raise ValueError(side)

# Controller instance and every pin connection.
ux,uy=150.0,95.0
objects.append(sym_instance('plataVM:LM5143A_Q1_RHA40','U_DCDC','LM5143QRHARQ1',ux,uy,[p.num for p in pins]))
for p in pins:
    if p.side=='left':
        px,py=ux-15.24,uy+p.y; ox=px-5.08
        objects.extend([wire(px,py,ox,py,f'U:{p.num}'), label(p.net,ox,py,'right')])
    elif p.side=='right':
        px,py=ux+15.24,uy+p.y; ox=px+5.08
        objects.extend([wire(px,py,ox,py,f'U:{p.num}'), label(p.net,ox,py,'left')])
    else:
        px,py=ux,uy+27.94; oy=py+5.08
        objects.extend([wire(px,py,px,oy,f'U:{p.num}'), label(p.net,px,oy,'left')])

# Phase 1 and 2 power stages.
add_nmos('Q_HS1',35,55,'Q_HS1_GATE','PACK_BUS_P5_IN','PHASE1_SW')
add_nmos('Q_LS1',35,70,'Q_LS1_GATE','PHASE1_SW','POWER_GND')
add_two('L1','plataVM:L','XAL1010-332MED 3.3uH',62,60,'PHASE1_SW','PHASE1_L_OUT')
add_two('RSH1','plataVM:R','WSK25125L000FEA 5mR 1%',88,60,'PHASE1_L_OUT','5V_SYS_BUS')
add_nmos('Q_HS2',35,125,'Q_HS2_GATE','PACK_BUS_P5_IN','PHASE2_SW')
add_nmos('Q_LS2',35,140,'Q_LS2_GATE','PHASE2_SW','POWER_GND')
add_two('L2','plataVM:L','XAL1010-332MED 3.3uH',62,130,'PHASE2_SW','PHASE2_L_OUT')
add_two('RSH2','plataVM:R','WSK25125L000FEA 5mR 1%',88,130,'PHASE2_L_OUT','5V_SYS_BUS')

# Split gate resistors: independent turn-on and turn-off paths.
gate_defs=[
('R_GH1_ON','GH1_ON','Q_HS1_GATE'),('R_GH1_OFF','GH1_OFF','Q_HS1_GATE'),('R_GL1_ON','GL1_ON','Q_LS1_GATE'),('R_GL1_OFF','GL1_OFF','Q_LS1_GATE'),
('R_GH2_ON','GH2_ON','Q_HS2_GATE'),('R_GH2_OFF','GH2_OFF','Q_HS2_GATE'),('R_GL2_ON','GL2_ON','Q_LS2_GATE'),('R_GL2_OFF','GL2_OFF','Q_LS2_GATE')]
for i,(ref,n1,n2) in enumerate(gate_defs):
    row=i%4; col=i//4
    add_two(ref,'plataVM:R','CALC_TBD',220+col*42,45+row*12,n1,n2)

# Bootstrap networks.
add_two('D_BOOT1','plataVM:D','CALC_TBD',220,98,'VCC_BIAS','HB1_BOOT')
add_two('C_BOOT1','plataVM:C','CALC_TBD',250,98,'HB1_BOOT','PHASE1_SW')
add_two('D_BOOT2','plataVM:D','CALC_TBD',220,112,'VCC_BIAS','HB2_BOOT')
add_two('C_BOOT2','plataVM:C','CALC_TBD',250,112,'HB2_BOOT','PHASE2_SW')

# Differential high-frequency current-sense filters.
add_two('R_CS1','plataVM:R','CALC_TBD',220,132,'PHASE1_L_OUT','CS1_FILTERED')
add_two('C_CS1','plataVM:C','CALC_TBD',250,132,'CS1_FILTERED','5V_SYS_BUS')
add_two('R_CS2','plataVM:R','CALC_TBD',220,146,'PHASE2_L_OUT','CS2_FILTERED')
add_two('C_CS2','plataVM:C','CALC_TBD',250,146,'CS2_FILTERED','5V_SYS_BUS')

# Timing and compensation.
add_two('R_RT','plataVM:R','54.9k 1%',220,172,'RT_SET','AGND')
add_two('C_SS','plataVM:C','510nF',250,172,'SS_COMMON','AGND')
add_two('C_RES','plataVM:C','470nF PROTOTYPE_START',280,172,'RES_TIMER','AGND')
add_two('R_COMP','plataVM:R','24.9k 1%',220,188,'COMP_COMMON','COMP_RC_NODE')
add_two('C_COMP','plataVM:C','3.3nF',250,188,'COMP_RC_NODE','AGND')
add_two('C_HF','plataVM:C','220pF',280,188,'COMP_COMMON','AGND')

# Decoupling/capacitor aggregate placeholders.
add_two('C_VCC','plataVM:C','CALC_TBD',220,205,'VCC_BIAS','POWER_GND')
add_two('C_VDDA','plataVM:C','CALC_TBD',250,205,'VDDA_BIAS','AGND')
add_two('C_VCCX','plataVM:C','CALC_TBD',280,205,'5V_SYS_BUS','POWER_GND')
add_two('CIN_EQ','plataVM:C','Ceff>=100uF @16V',220,221,'PACK_BUS_P5_IN','POWER_GND')
add_two('COUT_EQ','plataVM:C','2x330uF + X7R TUNING',265,221,'5V_SYS_BUS','POWER_GND')

# Test points and power flags.
add_tp('TP_PG2',305,55,'NC_PG2_TESTPAD')
add_tp('TP_SYNC',320,55,'SYNCOUT_TESTPAD')
for i,net in enumerate(['PACK_BUS_P5_IN','5V_SYS_BUS','POWER_GND','AGND']):
    add_flag(f'#FLG{i+1:02d}',305+i*15,90,net)

# Fail-safe control and diagnostic boundaries. Exact parts and values remain CALC_TBD.
add_box('U_UVLO','plataVM:UVLO_SUPERVISOR_TBD','CALC_TBD 8.9V_RISE 8.35V_FALL',45,185,[
    ('1','left',-2.54,'PACK_BUS_P5_IN'),
    ('2','left',2.54,'AGND'),
    ('3','right',0,'UVLO_OK'),
],15.24,10.16)
add_box('U_EN_GATE','plataVM:HW_ENABLE_GATE_TBD','CALC_TBD FAIL_SAFE_HW',87,185,[
    ('1','left',-6.35,'5V_SYS_EN'),
    ('2','left',-3.81,'UVLO_OK'),
    ('3','left',-1.27,'P5_GROUP_SAFE_OFF'),
    ('4','left',1.27,'P5_GROUP_HARD_OFF'),
    ('5','left',3.81,'PACK_BUS_P5_IN'),
    ('6','left',6.35,'AGND'),
    ('7','right',0,'EN_RUN'),
],20.32,17.78)
add_box('U_FAULT','plataVM:FAULT_EXPORT_TBD','CALC_TBD FAULT_AGGREGATE',125,185,[
    ('1','left',-3.81,'P5_PGOOD_OD'),
    ('2','left',-1.27,'UVLO_OK'),
    ('3','left',1.27,'EN_RUN'),
    ('4','left',3.81,'AGND'),
    ('5','right',0,'P5_DC_DC_FAULT_N'),
],17.78,12.7)
add_two('R_PG1_PULLUP','plataVM:R','CALC_TBD',160,185,'5V_SYS_BUS','P5_PGOOD_OD')

add_box('U_ISENSE1','plataVM:ISENSE_EXPORT_TBD','CALC_TBD PHASE1_MONITOR',45,215,[
    ('1','left',-1.27,'PHASE1_L_OUT'),
    ('2','left',1.27,'5V_SYS_BUS'),
    ('3','right',0,'P5_PHASE1_ISENSE'),
],15.24,7.62)
add_box('U_ISENSE2','plataVM:ISENSE_EXPORT_TBD','CALC_TBD PHASE2_MONITOR',87,215,[
    ('1','left',-1.27,'PHASE2_L_OUT'),
    ('2','left',1.27,'5V_SYS_BUS'),
    ('3','right',0,'P5_PHASE2_ISENSE'),
],15.24,7.62)
add_box('U_ISUM','plataVM:ISENSE_SUM_TBD','CALC_TBD TOTAL_MONITOR',125,215,[
    ('1','left',-1.27,'P5_PHASE1_ISENSE'),
    ('2','left',1.27,'P5_PHASE2_ISENSE'),
    ('3','right',0,'5V_SYS_TOTAL_ISENSE'),
],15.24,7.62)

# Intentional AGND/PGND star boundary. Copper, EP vias and final net-tie footprint remain a layout Gate.
add_two('NT_AGND_PGND','plataVM:NET_TIE_TBD','AGND_PGND_STAR_LAYOUT_TBD',180,215,'AGND','POWER_GND')

# External sheet interfaces retained.
hlabels=[
('PACK_BUS_P5_IN','input',25,245),('POWER_GND','passive',25,252),('5V_SYS_EN','input',25,259),
('P5_GROUP_SAFE_OFF','input',25,266),('P5_GROUP_HARD_OFF','input',25,273),
('5V_SYS_BUS','output',310,245),('5V_SYS_VSENSE','output',310,252),('5V_SYS_TOTAL_ISENSE','output',310,259),
('P5_DC_DC_FAULT_N','output',310,266),('P5_PHASE1_ISENSE','output',310,273),('P5_PHASE2_ISENSE','output',310,280)]
for name,shape,x,y in hlabels:
    objects.append(f'''\t(hierarchical_label "{name}"\n\t\t(shape {shape})\n\t\t(at {fx(x)} {fx(y)} 0)\n\t\t{effects(1.0, justify='left')}\n\t\t(uuid "{uid('hlabel:'+name)}")\n\t)''')
# Tie every hierarchical interface to its internal named net. This avoids floating sheet pins.
for name,shape,x,y in hlabels:
    if x < 100:
        objects.extend([wire(x,y,x+7.62,y,f'h:{name}'),label(name,x+7.62,y,'left')])
    else:
        internal = '5V_SYS_BUS' if name == '5V_SYS_VSENSE' else name
        objects.extend([wire(x,y,x-7.62,y,f'h:{name}'),label(internal,x-7.62,y,'right')])

notes=[
('PCB-D 5-V CONVERTER CORE — SYMBOL INSTANTIATION GATE',12,12,1.5),
('LM5143A-Q1 RHA-40 exact pin map instantiated. No production footprint/BOM/copper/layout freeze.',12,18,1.0),
('Eight independent HO/HOL and LO/LOL gate-resistor positions are intentional; all values remain CALC_TBD.',12,23,1.0),
('Direct SAFE/HARD_OFF hardware gate, UVLO, fault/current-monitor blocks and AGND-PGND star are explicit CALC_TBD boundaries.',12,28,1.0),
('Native KiCad ERC is performed by CI/owner KiCad 10.0.5. Bench Bode/OCP/load-step/thermal Gates remain open.',12,33,1.0),
]
for text,x,y,sz in notes:
    objects.append(f'''\t(text "{text}"\n\t\t(exclude_from_sim no)\n\t\t(at {fx(x)} {fx(y)} 0)\n\t\t{effects(sz, justify='left')}\n\t\t(uuid "{uid('text:'+text)}")\n\t)''')

sch_text=f'''(kicad_sch\n\t(version 20260306)\n\t(generator "plataVM_symbol_gate")\n\t(generator_version "1.0")\n\t(uuid "{root_uuid}")\n\t(paper "A3")\n\t(title_block\n\t\t(title "41_5V_DC_DC - PCB-D converter core exact-symbol Gate V1.9")\n\t\t(date "2026-07-23")\n\t\t(rev "B3-SYMBOL")\n\t\t(company "Gonoboben/plataVM")\n\t\t(comment 1 "Exact LM5143A-Q1 RHA-40 symbol instantiated; native ERC target")\n\t\t(comment 2 "No production BOM, footprints, copper, layout or thermal freeze")\n\t)\n\t(lib_symbols\n{chr(10).join(lib_defs)}\n\t)\n{chr(10).join(objects)}\n\t(sheet_instances\n\t\t(path "/"\n\t\t\t(page "1")\n\t\t)\n\t)\n\t(embedded_fonts no)\n)\n'''
(OUT/'41_5V_DC_DC.kicad_sch').write_text(sch_text, encoding='utf-8')

# Basic deterministic structural checks.
def balance(text):
    depth=0; q=False; esc=False
    for ch in text:
        if q:
            if esc: esc=False
            elif ch=='\\': esc=True
            elif ch=='"': q=False
        else:
            if ch=='"': q=True
            elif ch=='(': depth+=1
            elif ch==')':
                depth-=1
                if depth<0: return False
    return depth==0 and not q

for p in OUT.iterdir():
    t=p.read_text(encoding='utf-8')
    assert balance(t), p
    print(p.name, len(t), 'bytes', 'balanced')
print('symbol pins', len(pins), 'physical+EP')
print('schematic symbols', sch_text.count('\n\t(symbol\n'))
