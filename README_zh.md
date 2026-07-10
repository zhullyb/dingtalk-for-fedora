# dingtalk-for-fedora

[English](README.md) | 中文

## 描述

这个仓库提供了可以帮助你把官方的钉钉 deb 包打成 rpm 包的 spec 文件和构建脚本。

如果你不想自己构建 rpm 包，你可以登陆 github 帐号，在[这个页面](https://github.com/zhullyb/dingtalk-for-fedora/actions/workflows/rpmbuild.yml)点击最近的一次被✅标记的 action，下载里面的 Artifacts。

## 构建

> 已验证：`8.1.0.6021101` 可在 Fedora 44 上构建成功并正常运行。

### build.sh（推荐，无需 sudo）

把官方的 `com.alibabainc.dingtalk_<版本>_amd64.deb` 放到 `build.sh` 同级目录，然后执行：

```bash
./build.sh                 # 使用目录下最新的 deb
./build.sh 8.1.0.6021101   # 使用指定版本对应的 deb
./build.sh path/to/xxx.deb # 使用指定的 deb 文件
```

脚本用 `./build` 作为私有的 rpm topdir，不会污染 `~/rpmbuild`，也不需要 root。构建成功后，生成的 `.rpm`/`.src.rpm` 会被复制到脚本同级目录。

构建依赖（只需安装一次，需要权限）：

```bash
sudo dnf install rpm-build dpkg execstack
```

安装构建产物（需要权限）：

```bash
sudo dnf install ./dingtalk-bin-*.x86_64.rpm
```

### rpmbuild（手动）

将 `dingtalk-bin.spec` 复制到 SPECS 文件夹，其他文件放到 SOURCES 文件夹，然后执行：

```bash
sudo dnf builddep dingtalk-bin.spec
spectool -gR dingtalk-bin.spec
# 版本默认取 spec 里的值，需要时可显式覆盖：
rpmbuild -ba --define "dt_version 8.1.0.6021101" dingtalk-bin.spec
```

### spec 为在较新 Fedora 上运行做的处理

- 使用系统 `cairo`（`Requires: cairo`），不再打包旧的 `libcairo.so.2`。
- 用 `execstack -c` 清除随包 `.so` 上的可执行栈（`RWE GNU_STACK`）标志。否则较新的内核/glibc 加载器会报 `cannot enable executable stack as shared object requires` 而无法启动。
- 和以前一样，移除会破坏中文输入 / 打开链接的库。

### mock

如果你想用 mock 执行构建，你需要先用 rpmbuild 生成 srpm，并对其使用 `mock --rebuild`：

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
目前只有 KDE 用户报告这个问题。请在个人设置（头像 -> 设置 -> 下载）中去掉“使用系统文件对话框”的选项。

## Q&A

Q: 为什么不发个 release ？

A: 我无权分发重新打包的钉钉的 rpm 包，所以从某种程度上来说，我不应该发 release。

Q: 我注意到从 github action 下载的 Artifacts 文件名中有 "fc37" 的标识，我可以在 fedora 36 或者别的版本上安装它嘛？

A: 可以，但我不能保证它可以被正常运行，所以到底要不要安装的决定权在你手里。
