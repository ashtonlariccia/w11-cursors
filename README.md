## Offwhite Cursor Pack

Minimal cursors in two variants:

| Variant | Look |
|---|---|
| **Minimal Offwhite** | off-white fill, charcoal outline |
| **Minimal Offwhite Dark** | charcoal fill, off-white outline |

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

`Minimal Offwhite` is the source. After changing any of its cursors, regenerate the dark scheme and both Linux themes:

```sh
pip install pillow
python tools/build.py
```
