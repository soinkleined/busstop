declare -a PKG_LIST=("git" "xserver-xorg" "x11-xserver-utils" "xinit" "openbox" "chromium-browser" "unclutter")
sudo apt update
sudo apt full-upgrade
for PKG in "${PKG_LIST[@]}"; do
    PKG_INFO=$(dpkg -s  "${PKG}" 2>/dev/null)
    PKG_NAME=$(echo "$PKG_INFO" | grep "^Package:" | cut -f2- -d:)
    PKG_VERSION=$(echo "$PKG_INFO" | grep "^Version:" | cut -f2- -d:)
    PKG_STATUS=$(echo "$PKG_INFO" | grep "^Status:" | cut -f2- -d:)
    echo "$PKG_NAME"
    echo "$PKG_VERSION"
    echo "$PKG_STATUS"
done
