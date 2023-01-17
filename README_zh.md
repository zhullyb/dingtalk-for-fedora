# dingtalk-for-fedora

[English](README.md) | 中文

## 描述

这个仓库提供了可以帮助你把官方的钉钉deb包打成rpm包的spec文件。

如果你不想自己构建rpm包，你可以登陆 github 帐号，在[这个页面](https://github.com/zhullyb/dingtalk-for-fedora/actions/workflows/rpmbuild.yml)点击最近的一次被✅标记的 action， 下载里面的 Artifacts。

## Build

将 `dingtalk-bin.spec`复制到 SPECS 文件夹，其他的文件扔到 SOURCES 文件夹。

### rpmbuild

如果你想用 rpmbuild 进行构建，只需要执行

```bash
sudo dnf builddep SPECS/dingtalk-bin.spec
spectool -gR SPECS/dingtalk-bin.spec
rpmbuild -ba SPECS/dingtalk-bin.spec
```

### mock

如果你想用 mock 执行构建，你需要先用 rpmbuild 来生成 srpm，并对其使用 `mock --rebuild`

```bash
cd SRPMS
spectool -gR ../SPECS/dingtalk-bin.spec
rpmbuild -bs ../SPECS/dingtalk-bin.spec
mock --rebuild dingtalk-bin*.src.rpm 
```

## 常见问题

### 无法使用 Elevator.sh?
**Elevator.sh** 已被弃用，请直接运行 `/usr/bin/dingtalk`。

### 无法下载任何文件?
目前只有 KDE 用户报告这个问题。请在个人设置（头像 -> 设置 -> 下载） 中去掉“使用系统文件对话框”的选项。

## Q&A

Q: 为什么不发个 release ？

A: 我无权分发重新打包的钉钉的rpm包，所以从某种程度上来说，我不应该发 release。

Q: 我注意到从 github action 下载的 Artifacts 文件名中有 "fc37" 的标识，我可以在 fedora 36 或者别的版本上安装它嘛？

A: 可以，但我不能保证它可以被正常运行，所以到底要不要安装的决定权在你手里。
