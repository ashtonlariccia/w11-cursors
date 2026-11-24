"""Read/write Windows .cur/.ani and write Xcursor files (pure Python + Pillow)."""
import io, struct
from PIL import Image


# ---------- Windows .cur ----------

def _dib_to_image(data):
    hdr = struct.unpack('<IiiHHIIiiII', data[:40])
    size, w, h2, _, bpp = hdr[:5]
    if bpp != 32:
        raise ValueError(f'unsupported bpp {bpp}')
    h = h2 // 2
    px = data[size:size + w * h * 4]
    img = Image.frombytes('RGBA', (w, h), px, 'raw', 'BGRA')
    return img.transpose(Image.FLIP_TOP_BOTTOM)


def _image_to_dib(img):
    w, h = img.size
    px = img.transpose(Image.FLIP_TOP_BOTTOM).tobytes('raw', 'BGRA')
    row = ((w + 31) // 32) * 4
    mask = b'\x00' * (row * h)  # alpha carries transparency
    hdr = struct.pack('<IiiHHIIiiII', 40, w, h * 2, 1, 32, 0, len(px) + len(mask), 0, 0, 0, 0)
    return hdr + px + mask


def read_cur(data):
    """Return list of (image, hotx, hoty) for each size."""
    _, typ, n = struct.unpack('<HHH', data[:6])
    out = []
    for i in range(n):
        w, h, _, _, hx, hy, ln, off = struct.unpack('<BBBBHHII', data[6 + 16 * i:22 + 16 * i])
        blob = data[off:off + ln]
        img = Image.open(io.BytesIO(blob)).convert('RGBA') if blob[:4] == b'\x89PNG' else _dib_to_image(blob)
        out.append((img, hx, hy))
    return out


def write_cur(frames):
    n = len(frames)
    head = struct.pack('<HHH', 0, 2, n)
    blobs, entries, off = [], b'', 6 + 16 * n
    for img, hx, hy in frames:
        b = _image_to_dib(img)
        w, h = img.size
        entries += struct.pack('<BBBBHHII', w % 256, h % 256, 0, 0, hx, hy, len(b), off)
        blobs.append(b)
        off += len(b)
    return head + entries + b''.join(blobs)


# ---------- Windows .ani ----------

def _chunks(data, start, end):
    p = start
    while p + 8 <= end:
        cid = data[p:p + 4]
        sz = struct.unpack('<I', data[p + 4:p + 8])[0]
        yield cid, p + 8, sz
        p += 8 + sz + (sz & 1)


def read_ani(data):
    """Return dict(frames=[cur-frames], steps=[(frame_index, jiffies)], name=str)."""
    assert data[:4] == b'RIFF' and data[8:12] == b'ACON'
    frames, anih, rate, seq, name = [], None, None, None, ''
    for cid, p, sz in _chunks(data, 12, len(data)):
        body = data[p:p + sz]
        if cid == b'anih':
            anih = struct.unpack('<9I', body[:36])
        elif cid == b'rate':
            rate = list(struct.unpack(f'<{sz // 4}I', body))
        elif cid == b'seq ':
            seq = list(struct.unpack(f'<{sz // 4}I', body))
        elif cid == b'LIST' and body[:4] == b'fram':
            for c2, p2, s2 in _chunks(data, p + 4, p + sz):
                if c2 == b'icon':
                    frames.append(read_cur(data[p2:p2 + s2]))
        elif cid == b'LIST' and body[:4] == b'INFO':
            for c2, p2, s2 in _chunks(data, p + 4, p + sz):
                if c2 == b'INAM':
                    name = data[p2:p2 + s2].rstrip(b'\x00').decode('latin-1')
    nsteps, jif = anih[2], anih[7]
    seq = seq or list(range(nsteps))
    rate = rate or [jif] * nsteps
    return dict(frames=frames, steps=list(zip(seq, rate)), name=name)


def _chunk(cid, body):
    return cid + struct.pack('<I', len(body)) + body + (b'\x00' if len(body) & 1 else b'')


def write_ani(ani):
    frames, steps = ani['frames'], ani['steps']
    seq = [s for s, _ in steps]
    rate = [r for _, r in steps]
    simple = seq == list(range(len(frames)))
    uniform = len(set(rate)) == 1
    flags = 1 | (0 if simple else 2)
    anih = struct.pack('<9I', 36, len(frames), len(steps), 0, 0, 0, 0, rate[0], flags)
    body = b''
    if ani.get('name'):
        nm = ani['name'].encode('latin-1') + b'\x00'
        body += _chunk(b'LIST', b'INFO' + _chunk(b'INAM', nm))
    body += _chunk(b'anih', anih)
    if not uniform:
        body += _chunk(b'rate', struct.pack(f'<{len(rate)}I', *rate))
    if not simple:
        body += _chunk(b'seq ', struct.pack(f'<{len(seq)}I', *seq))
    body += _chunk(b'LIST', b'fram' + b''.join(_chunk(b'icon', write_cur(f)) for f in frames))
    return b'RIFF' + struct.pack('<I', len(body) + 4) + b'ACON' + body


# ---------- Xcursor ----------

def write_xcursor(images):
    """images: list of (img RGBA, hotx, hoty, delay_ms). Grouped by nominal size = width."""
    n = len(images)
    out_hdr = struct.pack('<4sIII', b'Xcur', 16, 0x10000, n)
    toc, blobs, off = b'', b'', 16 + 12 * n
    for img, hx, hy, delay in images:
        w, h = img.size
        # Xcursor wants premultiplied ARGB, little-endian uint32 -> bytes BGRA
        pre = img.convert('RGBa').tobytes('raw', 'BGRa')
        chunk = struct.pack('<IIIIIIIII', 36, 0xFFFD0002, w, 1, w, h, hx, hy, delay) + pre
        toc += struct.pack('<III', 0xFFFD0002, w, off)
        blobs += chunk
        off += len(chunk)
    return out_hdr + toc + blobs
