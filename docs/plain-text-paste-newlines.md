# 聊天输入框粘贴纯文本时换行丢失

**记录日期：** 2026-08-14  
**钉钉版本：** `8.1.0.6021101`（`8.1.0-Release.6021101`）  
**打包产物：** `dingtalk-bin-8.1.0.6021101-1.fc44`  
**验证环境：** Fedora 44；安装前缀 `~/.local/opt/dingtalk-bin`

## 现象

向聊天输入框粘贴含换行的纯文本后，换行符被丢弃，多行内容合并为单行。

粘贴 Markdown 后本地可见排版、对端仅见无格式文本的情况，系对端客户端版本过低所致，与下述补丁无关。

## 根因

原生富文本输入框（`InputRichTextEdit`）在下列灰度配置下，将剪贴板文本按 Markdown 解析并插入：

- `im/enable_native_input_paste_markdown_1013 = true`
- `im/rollback_paste_match_plain_text_markdown = false`

日志关键字：`InsertFromMimeData, insert markdown`。

CommonMark 将单独的 `\n` 视为软换行，渲染时折叠为空格；硬换行需空行（`\n\n`）或行末连续两个空格。故纯文本中的单换行无法保留。

日志路径：`~/.config/DingTalk/log/dingtalk_*.log`。摘录：

```text
[InputRichTextEdit] InsertFromMimeData, insert markdown, cid=...
[gray_tracker] module:im key:enable_native_input_paste_markdown_1013 value:1
[gray_tracker] module:im key:rollback_paste_match_plain_text_markdown value:0
```

## 处理

以 `LD_PRELOAD` 拦截 `gaea::config::ConfigService::GetGraySwitch` 及 `GetGraySwitchWithOrgId`。当 `module` 为 `im` 时覆盖如下开关：

| 开关 | 取值 | 说明 |
|------|------|------|
| `enable_native_input_paste_markdown` | false | 停用原 Markdown 粘贴逻辑 |
| `enable_native_input_paste_markdown_1013` | false | 停用 1013 路径的 Markdown 粘贴 |
| `enable_native_input_paste_markdown_linux` | false | 停用 Linux 侧 Markdown 粘贴 |
| `rollback_paste_match_plain_text_markdown` | true | 启用官方回滚：纯文本不按 Markdown 匹配 |

此后纯文本由 `HandleInsertTextFromMimeData` 插入，换行得以保留。

实现与安装位置：

- 源码：[`dingtalk-gray-hook.cpp`](../dingtalk-gray-hook.cpp)
- 启动脚本：[`dingtalk-launcher.sh`](../dingtalk-launcher.sh)；若目录中存在 `dingtalk-gray-hook.so`，则设置 `LD_PRELOAD`
- RPM：`dingtalk-bin.spec` 于 `%build` 编译该库，安装至 `/opt/dingtalk-bin/*Release*/`

用户目录安装时，动态库路径为：

```text
~/.local/opt/dingtalk-bin/8.1.0-Release.6021101/dingtalk-gray-hook.so
```

`LD_PRELOAD` 由 `~/.local/libexec/dingtalk` 设置。须结束钉钉进程后重新启动，预加载方可生效。验证方法：粘贴含换行的纯文本，确认行结构保持不变。
