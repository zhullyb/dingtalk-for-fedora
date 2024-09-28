%global __brp_check_rpaths %{nil}
%global debug_package %{nil}
%define _build_id_links none
%undefine __arch_install_post
AutoReqProv: no

Name:           dingtalk-bin
Version:        7.6.0.40718
Release:        2%{?dist}
Summary:        钉钉

License:        Custom
URL:            https://gov.dingtalk.com
Source0:        https://dtapp-pub.dingtalk.com/dingtalk-desktop/xc_dingtalk_update/linux_deb/Release/com.alibabainc.dingtalk_%{version}_amd64.deb
Source1:        https://tms.dingtalk.com/markets/dingtalk/service-terms-zh
Source2:        dingtalk-bin.desktop
Source3:        dingtalk.svg
Source4:        dingtalk-launcher.sh
Source5:        libcairo.so.2
Source6:        xdg-open
BuildRequires:  dpkg
Requires:       libGLU.so.1
Requires:       libxcrypt-compat

%description
钉钉

%prep
%setup -T -c %{name}-%{version}
dpkg -X %{S:0} .
%define BUILD_DIR %{_builddir}/%{name}-%{version}

%build
cp %{S:1} ./LICENSE

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
# fix cairo
install -Dm644 %{S:5} %{buildroot}/opt/dingtalk-bin/*Release*
# fix chinese input in workbench
rm -rf %{buildroot}/opt/dingtalk-bin/*Release*/{libm.so.6,Resources/{i18n/tool/*.exe,qss/mac,web_content/NativeWebContent_*.zip},libstdc*}
# fix chinese input in workbench
rm -rf %{buildroot}/opt/dingtalk-bin/*Release*/libgtk-x11-2.0.so.*
# fix open url
install -Dm755 %{S:6} -t %{buildroot}/opt/dingtalk-bin/*Release*

# remove unused lib
rm -rf %{buildroot}/opt/dingtalk-bin/*Release*/{libcurl.so.4,libz*}

%files
%license LICENSE
%{_bindir}/dingtalk
%{_datarootdir}/applications/*
%{_datarootdir}/icons/hicolor/scalable/apps/*
/opt/dingtalk-bin/

%changelog
* Tue Jan 17 2023 zhullyb <zhullyb@outlook.com> - 1.6.0.230113-2
- fix open url

* Tue Jan 17 2023 zhullyb <zhullyb@outlook.com> - 1.6.0.230113-1
- new version
- remove unused lib
- depend libGLU.so.1 and libxcrypt-compat
- use x11 if dingtalk do not support wayland

* Tue Jan 17 2023 zhullyb <zhullyb@outlook.com> - 1.4.0.20829-1
- new version

* Mon May 23 2022 zhullyb <zhullyb@outlook.com> - 1.4.0.20425-2
- Build for Fedora36

* Sat Apr 30 2022 zhullyb <zhullyb@outlook.com> - 1.4.0.20425-1
- new version

* Fri Apr 15 2022 zhullyb <zhullyb@outlook.com> - 1.4.0.20413-1
- new version

* Sat Apr 09 2022 zhullyb <zhullyb@outlook.com> - 1.4.0.20408-1
- new version

* Thu Mar 24 2022 zhullyb <zhullyb@outlook.com> - 1.4.0.42-1
- new version

* Sat Mar 19 2022 zhullyb <zhullyb@outlook.com> - 1.4.0.37-1
- new version

* Thu Feb 24 2022 zhullyb <zhullyb@outlook.com> - 1.3.0.20214-2
- Disable debuginfo package generation.

* Sun Feb 20 2022 zhullyb <zhullyb@outlook.com> - 1.3.0.20214-1
- Update to 1.3.0.20214

* Mon Feb 14 2022 zhullyb <zhullyb@outlook.com> - 1.3.0.12502-1
- First build.
