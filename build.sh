#!/usr/bin/env bash
#
# Build the dingtalk RPM from an official .deb, without sudo, into ./build.
#
# Usage:
#   ./build.sh                       # use the newest com.alibabainc.dingtalk_*.deb in this dir
#   ./build.sh 8.1.0.6021101         # use the .deb matching this version
#   ./build.sh path/to/xxx.deb       # use a specific .deb file
#
# Notes:
#   - Requires: rpmbuild, dpkg, execstack (dnf install rpm-build dpkg execstack).
#     Installing build deps needs privileges; the build itself does not.
#   - Output RPM/SRPM are copied next to this script when the build succeeds.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$here"

spec="dingtalk-bin.spec"
topdir="$here/build"

die() { echo "error: $*" >&2; exit 1; }

# --- resolve the .deb to build from ------------------------------------------
deb=""
version="${1:-}"

if [[ -n "$version" && -f "$version" ]]; then
    # argument is an explicit path to a .deb
    deb="$version"
    version=""
elif [[ -n "$version" ]]; then
    # argument is a version string
    deb="com.alibabainc.dingtalk_${version}_amd64.deb"
    [[ -f "$deb" ]] || die "deb for version '$version' not found: $deb"
else
    # no argument: pick the newest deb by mtime
    deb="$(ls -1t com.alibabainc.dingtalk_*_amd64.deb 2>/dev/null | head -n1 || true)"
    [[ -n "$deb" ]] || die "no com.alibabainc.dingtalk_*_amd64.deb found in $here"
fi

# derive version from the deb filename when not given explicitly
if [[ -z "$version" ]]; then
    base="$(basename "$deb")"
    version="${base#com.alibabainc.dingtalk_}"
    version="${version%_amd64.deb}"
fi
[[ -n "$version" ]] || die "could not determine version from '$deb'"

echo ">> deb     : $deb"
echo ">> version : $version"
echo ">> topdir  : $topdir"

# --- tool checks -------------------------------------------------------------
for t in rpmbuild dpkg execstack; do
    command -v "$t" >/dev/null 2>&1 || die "missing tool '$t' (try: sudo dnf install rpm-build dpkg execstack)"
done

# --- stage sources -----------------------------------------------------------
mkdir -p "$topdir"/{SOURCES,SPECS,BUILD,BUILDROOT,RPMS,SRPMS}

cp -f "$deb" "$topdir/SOURCES/com.alibabainc.dingtalk_${version}_amd64.deb"
for s in dingtalk-bin.desktop dingtalk.svg dingtalk-launcher.sh xdg-open; do
    [[ -f "$s" ]] || die "missing source file: $s"
    cp -f "$s" "$topdir/SOURCES/"
done

# service-terms-zh becomes the LICENSE; download once if not present locally.
if [[ -f service-terms-zh ]]; then
    cp -f service-terms-zh "$topdir/SOURCES/service-terms-zh"
else
    echo ">> service-terms-zh not found locally, fetching..."
    curl -fsSL "https://tms.dingtalk.com/markets/dingtalk/service-terms-zh" \
        -o "$topdir/SOURCES/service-terms-zh" \
        || die "failed to fetch service-terms-zh; place it next to this script and retry"
fi

cp -f "$spec" "$topdir/SPECS/dingtalk-bin.spec"

# --- build -------------------------------------------------------------------
# Fast payload compression: zstd level 2 + multithread. rpm defaults to
# zstd level 19 which is ~20x slower on a ~400MB payload.
rpmbuild -ba \
    --define "_topdir $topdir" \
    --define "dt_version $version" \
    --define "_binary_payload w2T0.zstdio" \
    "$topdir/SPECS/dingtalk-bin.spec"

# --- collect artifacts -------------------------------------------------------
shopt -s nullglob
rpms=("$topdir"/RPMS/*/*.rpm "$topdir"/SRPMS/*.rpm)
[[ ${#rpms[@]} -gt 0 ]] || die "build finished but no rpm was produced"

echo ">> artifacts:"
for r in "${rpms[@]}"; do
    cp -f "$r" "$here/"
    echo "   $(basename "$r")  ($(du -h "$r" | cut -f1))"
done
echo ">> copied to: $here"
