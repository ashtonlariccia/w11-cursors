"""Generate the dark Windows scheme and both Linux Xcursor themes from 'Minimal Offwhite'.

Usage (from repo root):  python tools/build.py
Requires: Python 3.8+, Pillow (pip install pillow)
"""
import os, re, shutil, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from curlib import read_cur, write_cur, read_ani, write_ani, write_xcursor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'Minimal Offwhite')
DARK_NAME = 'Minimal Offwhite Dark'
DARK = os.path.join(ROOT, DARK_NAME)
LINUX = os.path.join(ROOT, 'linux')

# The two palette anchors of the light theme: off-white fill and charcoal outline.
FILL = (242, 240, 235)
LINE = (41, 43, 50)

# ---------- dark recolor ----------

def _lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

_LF, _LL = _lum(FILL), _lum(LINE)
_LUT = {}

def _swap(r, g, b, a):
    if a == 0:
        return (0, 0, 0, 0)
    key = (r, g, b, a)
    if key not in _LUT:
        # Position between outline (0) and fill (1), then mirror it: fill -> charcoal, outline -> off-white.
        t = (_lum((r, g, b)) - _LL) / (_LF - _LL)
        u = 1 - max(-0.2, min(1.2, t))
        new = [max(0, min(255, LINE[i] + (FILL[i] - LINE[i]) * u)) for i in range(3)]
        # Faint, near-transparent pixels are the drop shadow: keep them dark.
        s = max(0.0, min(1.0, (a - 20) / 40))
        _LUT[key] = tuple(int(round((r, g, b)[i] * (1 - s) + new[i] * s)) for i in range(3)) + (a,)
    return _LUT[key]

def darken(img):
    out = Image.new('RGBA', img.size)
    out.putdata([_swap(*p) for p in img.get_flattened_data()])
    return out

def darken_frames(frames):
    return [(darken(im), hx, hy) for im, hx, hy in frames]

# ---------- Windows dark scheme ----------

def build_windows_dark():
    os.makedirs(DARK, exist_ok=True)
    for f in sorted(os.listdir(SRC)):
        src, dst = os.path.join(SRC, f), os.path.join(DARK, f)
        if f.endswith('.cur'):
            with open(dst, 'wb') as o:
                o.write(write_cur(darken_frames(read_cur(open(src, 'rb').read()))))
        elif f.endswith('.ani'):
            ani = read_ani(open(src, 'rb').read())
            ani['frames'] = [darken_frames(fr) for fr in ani['frames']]
            ani['name'] = ani['name'].replace('Minimal Offwhite', DARK_NAME)
            with open(dst, 'wb') as o:
                o.write(write_ani(ani))
        elif f == 'install.inf':
            txt = open(src, encoding='utf-8', newline='').read()
            txt = re.sub(r'(CUR_DIR\s*=\s*"Cursors\\)[^"]*"', lambda m: m.group(1) + DARK_NAME + '"', txt)
            txt = re.sub(r'(SCHEME_NAME\s*=\s*)"[^"]*"', lambda m: m.group(1) + '"' + DARK_NAME + '"', txt)
            open(dst, 'w', encoding='utf-8', newline='').write(txt)
        elif f == 'apply.ps1':  # uses its own folder name as the scheme name
            shutil.copyfile(src, dst)

# ---------- Linux Xcursor themes ----------

# Windows file -> Xcursor names. The first name is the real file; the rest become symlinks.
# Covers CSS/freedesktop names, legacy X11 core names and the hash names Qt/GTK/Firefox probe.
NAMES = {
    'pointer.cur': ['default', 'left_ptr', 'arrow', 'top_left_arrow', 'left-arrow', 'context-menu',
                    'copy', 'alias', 'dnd-move', 'dnd-copy', 'dnd-link', 'dnd-ask', 'grab', 'grabbing',
                    'openhand', 'closedhand', 'fcf21c00b30f7e3f83fe0dfd12e71cff',
                    '6407b0e94181790501fd1e167b474872', '1081e37283d90000800003c07f3ef6bf',
                    '640fb0e74195791501fd1ed57b41487f', '3085a0e285430894940527032f8b26df',
                    'a2a266d0498c3104214a47bd64ab0fc8', 'b66166c04f8c3109214a4fbd64a50fc8'],
    'help.cur': ['help', 'question_arrow', 'whats_this', 'left_ptr_help',
                 '5c6cd98b3f3ebcb1f9c7f1c204630408', 'd9ce0ab605698f320427677b458ad60b'],
    'working.ani': ['progress', 'left_ptr_watch', 'half-busy', '3ecb610c1bf2410f44200f48c40d3599',
                    '00000000000000020006000e7e9ffc3f', '08e8e1c95fe2fc01f976f1e063a24ccd'],
    'busy.ani': ['wait', 'watch', 'clock'],
    'precision.cur': ['crosshair', 'cross', 'tcross', 'cross_reverse', 'diamond_cross', 'cell', 'plus'],
    'text.cur': ['text', 'xterm', 'ibeam', 'vertical-text'],
    'handwriting.cur': ['pencil', 'draft', 'color-picker'],
    'unavailable.cur': ['not-allowed', 'no-drop', 'dnd-no-drop', 'crossed_circle', 'forbidden', 'circle',
                        '03b6e0fcb3499374a867c041f52298f0'],
    'vert.cur': ['ns-resize', 'n-resize', 's-resize', 'row-resize', 'size_ver', 'sb_v_double_arrow',
                 'v_double_arrow', 'double_arrow', 'top_side', 'bottom_side', 'split_v',
                 '00008160000006810000408080010102', '2870a09082c103050810ffdffffe0204'],
    'horz.cur': ['ew-resize', 'e-resize', 'w-resize', 'col-resize', 'size_hor', 'sb_h_double_arrow',
                 'h_double_arrow', 'left_side', 'right_side', 'split_h',
                 '028006030e0e7ebffc7f7070c0600140', '14fef782d02440884392942c11205230'],
    'dgn1.cur': ['nwse-resize', 'nw-resize', 'se-resize', 'size_fdiag', 'bd_double_arrow',
                 'top_left_corner', 'bottom_right_corner', 'c7088f0f3e6c8088236ef8e1e3e70000'],
    'dgn2.cur': ['nesw-resize', 'ne-resize', 'sw-resize', 'size_bdiag', 'fd_double_arrow',
                 'top_right_corner', 'bottom_left_corner', 'fcf1c3c7cd4491d801f1e1c78f100000'],
    'move.cur': ['move', 'all-scroll', 'fleur', 'size_all', 'all-resize',
                 '4498f0e0c1937ffe01fd06f973665830', '9081237383d90e509aa00f00170e968f'],
    'alternate.cur': ['up-arrow', 'center_ptr', 'sb_up_arrow'],
    'link.cur': ['pointer', 'hand', 'hand1', 'hand2', 'pointing_hand',
                 'e29285e634086352946a0e7090d73106', '9d800788f1b08800ae810202380a0822'],
    'pin.cur': ['pin'],
    'person.cur': ['person'],
}

# Windows canvas size -> Xcursor nominal size. The art only fills ~55% of the Windows canvas,
# so cropping to 75% gives Linux-proportioned cursors (24 is the usual default size).
SIZE_MAP = {32: 24, 48: 36, 64: 48}
JIFFY_MS = 1000 / 60

def _x_images(frames, delay=0):
    out = []
    for im, hx, hy in frames:
        n = SIZE_MAP[im.size[0]]
        out.append((im.crop((0, 0, n, n)), hx, hy, delay))
    return out

def build_linux(src_dir, theme, comment):
    tdir = os.path.join(LINUX, theme)
    cdir = os.path.join(tdir, 'cursors')
    shutil.rmtree(tdir, ignore_errors=True)
    os.makedirs(cdir)
    for f, names in NAMES.items():
        data = open(os.path.join(src_dir, f), 'rb').read()
        if f.endswith('.cur'):
            imgs = _x_images(read_cur(data))
        else:
            ani = read_ani(data)
            per_size = {}
            for idx, jif in ani['steps']:
                for img in _x_images(ani['frames'][idx], max(1, round(jif * JIFFY_MS))):
                    per_size.setdefault(img[0].size[0], []).append(img)
            imgs = [i for s in sorted(per_size) for i in per_size[s]]
        with open(os.path.join(cdir, names[0]), 'wb') as o:
            o.write(write_xcursor(imgs))
    with open(os.path.join(tdir, 'index.theme'), 'w', newline='\n') as o:
        o.write(f'[Icon Theme]\nName={theme}\nComment={comment}\nInherits=Adwaita\n')
    with open(os.path.join(tdir, 'aliases'), 'w', newline='\n') as o:
        o.write('# <alias> <target>  (install.sh turns these into symlinks)\n')
        for names in NAMES.values():
            for a in names[1:]:
                o.write(f'{a} {names[0]}\n')


def main():
    print('Building Windows dark scheme...')
    build_windows_dark()
    print('Building Linux themes...')
    build_linux(SRC, 'Minimal-Offwhite', 'Minimal off-white cursors')
    build_linux(DARK, 'Minimal-Offwhite-Dark', 'Minimal dark cursors with off-white outline')
    print('Done.')

if __name__ == '__main__':
    main()
