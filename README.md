## Offwhite Cursor Pack

Minimal cursors in two variants: **Minimal Offwhite** (off-white fill, charcoal outline) and **Minimal Offwhite Dark** (charcoal fill, off-white outline).

| Cursor | Minimal Offwhite | Minimal Offwhite Dark | Windows file | Linux name |
|---|:-:|:-:|---|---|
| Normal select | <img src="previews/pointer-light.png" alt="Normal select, light"> | <img src="previews/pointer-dark.png" alt="Normal select, dark"> | `pointer.cur` | `default` |
| Help select | <img src="previews/help-light.png" alt="Help select, light"> | <img src="previews/help-dark.png" alt="Help select, dark"> | `help.cur` | `help` |
| Working in background | <img src="previews/working-light.gif" alt="Working in background, light"> | <img src="previews/working-dark.gif" alt="Working in background, dark"> | `working.ani` | `progress` |
| Busy | <img src="previews/busy-light.gif" alt="Busy, light"> | <img src="previews/busy-dark.gif" alt="Busy, dark"> | `busy.ani` | `wait` |
| Precision select | <img src="previews/precision-light.png" alt="Precision select, light"> | <img src="previews/precision-dark.png" alt="Precision select, dark"> | `precision.cur` | `crosshair` |
| Text select | <img src="previews/text-light.png" alt="Text select, light"> | <img src="previews/text-dark.png" alt="Text select, dark"> | `text.cur` | `text` |
| Handwriting | <img src="previews/handwriting-light.png" alt="Handwriting, light"> | <img src="previews/handwriting-dark.png" alt="Handwriting, dark"> | `handwriting.cur` | `pencil` |
| Unavailable | <img src="previews/unavailable-light.png" alt="Unavailable, light"> | <img src="previews/unavailable-dark.png" alt="Unavailable, dark"> | `unavailable.cur` | `not-allowed` |
| Vertical resize | <img src="previews/vert-light.png" alt="Vertical resize, light"> | <img src="previews/vert-dark.png" alt="Vertical resize, dark"> | `vert.cur` | `ns-resize` |
| Horizontal resize | <img src="previews/horz-light.png" alt="Horizontal resize, light"> | <img src="previews/horz-dark.png" alt="Horizontal resize, dark"> | `horz.cur` | `ew-resize` |
| Diagonal resize 1 | <img src="previews/dgn1-light.png" alt="Diagonal resize 1, light"> | <img src="previews/dgn1-dark.png" alt="Diagonal resize 1, dark"> | `dgn1.cur` | `nwse-resize` |
| Diagonal resize 2 | <img src="previews/dgn2-light.png" alt="Diagonal resize 2, light"> | <img src="previews/dgn2-dark.png" alt="Diagonal resize 2, dark"> | `dgn2.cur` | `nesw-resize` |
| Move | <img src="previews/move-light.png" alt="Move, light"> | <img src="previews/move-dark.png" alt="Move, dark"> | `move.cur` | `move` |
| Alternate select | <img src="previews/alternate-light.png" alt="Alternate select, light"> | <img src="previews/alternate-dark.png" alt="Alternate select, dark"> | `alternate.cur` | `up-arrow` |
| Link select | <img src="previews/link-light.png" alt="Link select, light"> | <img src="previews/link-dark.png" alt="Link select, dark"> | `link.cur` | `pointer` |
| Location select | <img src="previews/pin-light.png" alt="Location select, light"> | <img src="previews/pin-dark.png" alt="Location select, dark"> | `pin.cur` | `pin` |
| Person select | <img src="previews/person-light.png" alt="Person select, light"> | <img src="previews/person-dark.png" alt="Person select, dark"> | `person.cur` | `person` |

### Windows 11

Either right-click `install.inf` > **Install** and pick the scheme in Mouse Properties > Pointers, or run
the folder's `apply.ps1` to install and apply it in one step (no admin needed):

```powershell
powershell -ExecutionPolicy Bypass -File ".\Minimal Offwhite Dark\apply.ps1"
```

### Linux (X11 and Wayland)

`linux/` holds both variants as Xcursor themes (`Minimal-Offwhite`, `Minimal-Offwhite-Dark`) in sizes 24, 36 and 48,
with the standard CSS/freedesktop names plus legacy X11 and hash aliases.

```sh
cd linux
./install.sh                        # current user: ~/.local/share/icons
sudo ./install.sh /usr/share/icons  # system-wide, or point it at a package staging dir
```

Then select it in your settings, or set `XCURSOR_THEME=Minimal-Offwhite-Dark` and `XCURSOR_SIZE=24`.
The extra `pin` and `person` cursors have no standard Linux name; they ship as `pin` and `person` for your own use.

### Rebuilding

`Minimal Offwhite` is the source. After changing any of its cursors, regenerate the dark scheme, both Linux themes and the preview images above:

```sh
pip install pillow
python tools/build.py
```
