#!/bin/bash
set -e
APPIMAGE="metUnow-x86_64.AppImage"
APPDIR="metUnow.AppDir"

# 실행 중인 인스턴스 종료
if pgrep -f "$APPIMAGE" > /dev/null; then
    echo "기존 인스턴스 종료 중..."
    pkill -f "$APPIMAGE"
    sleep 2
fi

# 버전 기록
BUILD_TIME=$(date '+%Y-%m-%d %H:%M')
echo "BUILD_TIME = \"$BUILD_TIME\"" > version.py
echo "버전: $BUILD_TIME"

# PyInstaller 빌드
echo "PyInstaller 빌드 중..."
.venv/bin/pyinstaller metUnow.spec --noconfirm

# AppDir 갱신
rm -rf "$APPDIR/metUnow"
cp -r dist/metUnow "$APPDIR/"

# AppImage 빌드
echo "AppImage 패키징 중..."
ARCH=x86_64 ~/.local/bin/appimagetool "$APPDIR" "$APPIMAGE"

# 자동시작 등록
cat > ~/.config/autostart/metUnow.desktop << EOF
[Desktop Entry]
Type=Application
Name=metUnow
Exec=$(pwd)/$APPIMAGE
Icon=$(pwd)/metUnow.png
X-GNOME-Autostart-enabled=true
Terminal=false
EOF

# 앱 런처 등록
cat > ~/.local/share/applications/metUnow.desktop << EOF
[Desktop Entry]
Type=Application
Name=metUnow
Exec=$(pwd)/$APPIMAGE
Icon=$(pwd)/metUnow.png
Categories=Network;
Terminal=false
EOF

echo "빌드 완료: $(pwd)/$APPIMAGE"
