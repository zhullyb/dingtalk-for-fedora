%global __brp_check_rpaths %{nil}
%global debug_package %{nil}
%define _build_id_links none
%undefine __arch_install_post
AutoReqProv: no

# Version can be overridden from the command line, e.g.
#   rpmbuild -ba --define "dt_version 8.1.0.6021101" dingtalk-bin.spec
# Default keeps the last known-good version for a plain `rpmbuild` run.
%{!?dt_version: %global dt_version 8.1.0.6021101}

Name:           dingtalk-bin
Version:        %{dt_version}
Release:        1%{?dist}
Summary:        钉钉

License:        Custom
URL:            https://gov.dingtalk.com
Source0:        https://dtapp-pub.dingtalk.com/dingtalk-desktop/xc_dingtalk_update/linux_deb/Release/com.alibabainc.dingtalk_%{version}_amd64.deb
Source1:        https://tms.dingtalk.com/markets/dingtalk/service-terms-zh
Source2:        dingtalk-bin.desktop
Source3:        dingtalk.svg
Source4:        dingtalk-launcher.sh
Source6:        xdg-open
Source7:        dingtalk-gray-hook.cpp
BuildRequires:  dpkg
BuildRequires:  execstack
BuildRequires:  gcc-c++
Requires:       libGLU.so.1
Requires:       libxcrypt-compat
# Use the system cairo instead of the bundled patch library.
Requires:       cairo

%description
钉钉

%prep
%setup -T -c %{name}-%{version}
dpkg -X %{S:0} .
%define BUILD_DIR %{_builddir}/%{name}-%{version}

%build
cp %{S:1} ./LICENSE
g++ -shared -fPIC -O2 -D_GNU_SOURCE -Wl,-z,defs %{S:7} -o dingtalk-gray-hook.so -ldl

%install
# Main program
install -d %{buildroot}/opt/dingtalk-bin
mv %{BUILD_DIR}/opt/apps/com.alibabainc.dingtalk/files/* %{buildroot}/opt/dingtalk-bin/

# Desktop file
install -Dm644 %{S:2} -t %{buildroot}%{_datarootdir}/applications/

# Icons
install -Dm644 %{S:3} -t %{buildroot}%{_datarootdir}/icons/hicolor/scalable/apps/

# Launcher
install -d %{buildroot}%{_bindir}
install -Dm755 %{S:4} %{buildroot}%{_bindir}/dingtalk

# Patch
# use system cairo: do NOT install the bundled libcairo.so.2
# fix chinese input in workbench
rm -rf %{buildroot}/opt/dingtalk-bin/*Release*/{libm.so.6,Resources/{i18n/tool/*.exe,qss/mac,web_content/NativeWebContent_*.zip},libstdc*}
# fix chinese input in workbench
rm -rf %{buildroot}/opt/dingtalk-bin/*Release*/libgtk-x11-2.0.so.*
# fix open url
install -Dm755 %{S:6} -t %{buildroot}/opt/dingtalk-bin/*Release*
# keep plain-text newlines on paste (see dingtalk-gray-hook.cpp)
install -Dm755 dingtalk-gray-hook.so -t %{buildroot}/opt/dingtalk-bin/*Release*

# remove unused lib
rm -rf %{buildroot}/opt/dingtalk-bin/*Release*/{libcurl.so.4,libz*}

# fix "cannot enable executable stack" on newer kernels/glibc loader:
# clear the executable-stack (RWE GNU_STACK) flag on all bundled shared objects.
for f in $(find %{buildroot}/opt/dingtalk-bin/*Release* -type f \( -name '*.so' -o -name '*.so.*' \)); do
    if head -c4 "$f" | grep -q ELF; then execstack -c "$f" 2>/dev/null || :; fi
done

%files
%license LICENSE
%{_bindir}/dingtalk
%{_datarootdir}/applications/*
%{_datarootdir}/icons/hicolor/scalable/apps/*
/opt/dingtalk-bin/

%changelog
* Fri Aug 14 2026 local build - 8.1.0.6021101-1
- preserve newlines when pasting plain text (disable markdown paste gray switch)

* Fri Jul 10 2026 local build - 8.1.0.6021101-1
- parameterize version via --define "dt_version ..."
- use system cairo (drop bundled libcairo.so.2 patch)
- clear executable stack flag on bundled .so (fix load failure on newer kernel)

* Tue Jan 17 2023 zhullyb <zhullyb@outlook.com> - 1.6.0.230113-2
- fix open url

* Tue Jan 17 2023 zhullyb <zhullyb@outlook.com> - 1.6.0.230113-1
- new version
- remove unused lib
- depend libGLU.so.1 and libxcrypt-compat
- use x11 if dingtalk do not support wayland

* Mon May 23 2022 zhullyb <zhullyb@outlook.com> - 1.4.0.20425-2
- Build for Fedora36
