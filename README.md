# dingtalk-for-fedora

English | [中文](README_zh.md)

## Description

This repository provides the spec file which can help you to repack the official dingtalk deb package to rpm package.

If you don't want to build it yourself, you can download the binary rpm built by GitHub Actions from [this page](https://github.com/zhullyb/dingtalk-for-fedora/actions/workflows/rpmbuild.yml), simply click the **latest workflow run** with ✅ labeled and download the **Artifacts** with your github account logged-in.

## Build

Copy `dingtalk-bin.spec` to SPECS dir and other things to SOURCES dir.

### rpmbuild

If you are using rpmbuild, simply run:

```bash
sudo dnf builddep SPECS/dingtalk-bin.spec
spectool -gR SPECS/dingtalk-bin.spec
rpmbuild -ba SPECS/dingtalk-bin.spec
```

### mock

If you want to build it with mock, you will need to generate a source rpm first and use `mock --rebuild`

```bash
cd SRPMS
spectool -gR ../SPECS/dingtalk-bin.spec
rpmbuild -bs ../SPECS/dingtalk-bin.spec
mock --rebuild dingtalk-bin*.src.rpm 
```

## Usage
This part documents common problems encountered while using this package.

### Elevator.sh is not working?
DO NOT use the `Elevator.sh` provided by the package, which is deprecated. Rather, use the `/usr/bin/dingtalk` executable created by the
package or the desktop file it created.

### Cannot Download files?
This is reported by KDE users at the moment. If you cannot download any files, please untick the "Use System File Manager Dialog" in your 
preferences. (Avator -> Settings -> Downloads)


## FAQ

Q: Why no release was created?

A: I don't have the right to redistribute the software, so I shouldn't create a release on some extent.

Q: I saw that the file downloaded from GitHub Actions is labeled with "fc37", can I install the package to fedora 36 or some other version ?

A: Installation and running on other Fedora versions have not been tested but it should work (no guarantees). Use at your own expense.
