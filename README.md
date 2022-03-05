# dingtalk-for-fedora

English | [中文](README_zh.md)

## Description

This repository provides spec file which can help you to repack the official dingtalk deb package to rpm package.

If you don't want to build it by yourself, you can download the binary rpm built by github action from [this page](https://github.com/zhullyb/dingtalk-for-fedora/actions/workflows/rpmbuild.yml), simply click the **latest workflow run** with ✅ labeled and download the **Artifacts** with your github account logged-in.

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

## Q&A

Q: Why no release was created ?

A: I don't have the right to redistribute the software, so I shouldn't create a release on some extent.

Q: I saw that the file name downloaded from github action is labeled with "fc35", can I install the package to fedora 34 or some other version ?

A: You can install it to other fedora version, but I can't guarantee whether the software can be runned corrently, so you make the decision.