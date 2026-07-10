# dingtalk-for-fedora

English | [中文](README_zh.md)

## Description

This repository provides the spec file and a helper script that repack the official dingtalk deb package into an rpm package.

If you don't want to build it yourself, you can download the binary rpm built by GitHub Actions from [this page](https://github.com/zhullyb/dingtalk-for-fedora/actions/workflows/rpmbuild.yml), simply click the **latest workflow run** with ✅ labeled and download the **Artifacts** with your github account logged-in.

## Build

> Tested: version `8.1.0.6021101` builds and runs on Fedora 44.

### build.sh (recommended, no sudo)

Put an official `com.alibabainc.dingtalk_<version>_amd64.deb` next to `build.sh` and run:

```bash
./build.sh                 # use the newest deb in this directory
./build.sh 8.1.0.6021101   # use the deb matching this version
./build.sh path/to/xxx.deb # use a specific deb file
```

The script uses `./build` as a private rpm topdir, so it never touches `~/rpmbuild` and needs no root. On success the resulting `.rpm`/`.src.rpm` are copied next to the script.

Build dependencies (install once, needs privileges):

```bash
sudo dnf install rpm-build dpkg execstack
```

Install the result (needs privileges):

```bash
sudo dnf install ./dingtalk-bin-*.x86_64.rpm
```

### rpmbuild (manual)

Copy `dingtalk-bin.spec` to your SPECS dir and the other files to SOURCES, then:

```bash
sudo dnf builddep dingtalk-bin.spec
spectool -gR dingtalk-bin.spec
# version defaults to the value in the spec; override it explicitly if needed:
rpmbuild -ba --define "dt_version 8.1.0.6021101" dingtalk-bin.spec
```

### What the spec does to make it run on recent Fedora

- Uses the system `cairo` (`Requires: cairo`) instead of shipping the old bundled `libcairo.so.2`.
- Clears the executable-stack (`RWE GNU_STACK`) flag on the bundled `.so` files with `execstack -c`. Without this, recent kernels/glibc loaders abort with `cannot enable executable stack as shared object requires`.
- Removes libraries that break Chinese input / url opening, as before.

### mock

If you want to build it with mock, generate a source rpm first and use `mock --rebuild`:

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
