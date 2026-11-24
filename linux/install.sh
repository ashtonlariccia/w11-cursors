#!/bin/sh
# Install the Minimal Offwhite Xcursor themes and create their alias symlinks.
#   ./install.sh            -> ~/.local/share/icons   (current user)
#   sudo ./install.sh /usr/share/icons                (system-wide / packaging)
set -eu
here=$(cd "$(dirname "$0")" && pwd)
dest=${1:-${XDG_DATA_HOME:-$HOME/.local/share}/icons}

for theme in Minimal-Offwhite Minimal-Offwhite-Dark; do
    out="$dest/$theme"
    rm -rf "$out"
    mkdir -p "$out/cursors"
    cp "$here/$theme/index.theme" "$out/"
    cp "$here/$theme/cursors/"* "$out/cursors/"
    grep -v '^#' "$here/$theme/aliases" | while read -r alias target; do
        [ -n "$alias" ] && ln -sf "$target" "$out/cursors/$alias"
    done
    echo "Installed $theme -> $out"
done

cat <<EOF

Select a theme with your DE's settings, or set it directly:
  XCURSOR_THEME=Minimal-Offwhite-Dark XCURSOR_SIZE=24        (env, X11 + most Wayland compositors)
  gsettings set org.gnome.desktop.interface cursor-theme Minimal-Offwhite-Dark
Sizes included: 24, 36, 48.
EOF
