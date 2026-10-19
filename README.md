# CF 全球边缘节点 Skill（v3）

> 一个能让 AI 一步步带新手搭好**个人 Cloudflare 节点**的 Skill，外加一篇照着就能做的中文教程。
> v3 把三样东西合成了一版：free-dam-man 的原版 Skill、我们两次实战部署的笔记、几个社区知名教程里最有用的部分。

- **新手看这个** → [docs/tutorial-zh.md](docs/tutorial-zh.md)：从注册到扫码，一共 17 节，含本地测速、proxyip 原理、排障表、日常维护
- **AI 看这个** → [SKILL.md](SKILL.md)：门禁、向导（第1/6步～第6/6步）、钉版校验、部署、优选 IP、验证、交付清单
- **发推用** → [docs/x-thread-zh.md](docs/x-thread-zh.md)

## 它做出来的是什么

- 入口：Cloudflare 全球边缘（优选 IP，写在 KV 的 `ADD.txt` 里）
- 核心：钉版的 [cmliu/edgetunnel](https://github.com/cmliu/edgetunnel) `_worker.js`（commit `66f1c51c`，SHA-256 见 SKILL.md 第 2 节；2026-10-19 核对仍与上游 main 一致）
- 出口：普通网站看到的是 Cloudflare 的 IP，套了 CF 的网站（X、ChatGPT）看到的是 proxyip 的 IP。**不是家宽，也不是 VPS**
- 交付：管理面板地址、订阅链接、订阅二维码、至少一个已经连通的客户端

## v3 新增了什么

| 内容 | 来源 |
|---|---|
| 教程重写成 17 节：选路线、免费域名对比、网页版和命令行版部署、变量表、绑域名、ADD.txt 全部写法、地区建议、维护、VPS 备选 | 原版 + 实战笔记 + 下面各家 |
| **在自己的 Win10 上用 CloudflareSpeedTest 测优选 IP**（先关代理、指定机房、降并发） | [XIU2/CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest) |
| **proxyip 讲清楚**：为什么 YouTube 能开、X/ChatGPT 打不开；whatismyip 和 ip.sb 分别看哪个出口 | [CF 官方文档](https://developers.cloudflare.com/workers/runtime-apis/tcp-sockets/)、[yonggekkk](https://github.com/yonggekkk/Cloudflare-vless-trojan)、edgetunnel 源码 |
| CF 端口表（443 系 / 80 系），哪些端口能用 | CF 官方文档、yonggekkk |
| 域名被阻断时的办法：换子域名，或客户端开 TLS 分片 | [BPB-Worker-Panel 文档](https://github.com/bia-pain-bache/BPB-Worker-Panel)、yonggekkk、edgetunnel 源码 |
| ADD.txt 支持的写法：IPv6、域名、远程列表、直接放 `vless://` 节点（可以把 VPS 节点并进同一个订阅） | edgetunnel 源码（已逐行核对） |
| 新的排障条目：proxyip、AI 提示地区不支持、域名被阻断、UDP 不通、测速结果异常 | 各家 + 实战 |
| 日常维护和安全升级的步骤（续域名、换节点、升级时重新钉版） | 实战 |
| 有 VPS 时的备选：sing-box-yg / 233boy，优先 VLESS-Reality | [yonggekkk/sing-box-yg](https://github.com/yonggekkk/sing-box-yg)、[233boy/sing-box](https://github.com/233boy/sing-box) |
| 隐私提醒：公共订阅生成器别放私人节点；介意转换服务的话改用 v2rayN | [cmliu/WorkerVless2sub](https://github.com/cmliu/WorkerVless2sub)、edgetunnel 源码 |

SKILL.md 保留了原版的整体结构（门禁、W1–W7 向导、第X/6步编号、地区确认循环、钉版校验、交付清单），新知识按需并进对应章节，第 16 节有"哪条来自哪里"的索引。完整变更见 [CHANGELOG](CHANGELOG.md)。

## 向导开场预览

装好 Skill 的 AI 会先发这一张卡，然后从第1/6步问到第6/6步（选地区）：

```text
先花30秒看完, 然后我们一步一步来:
一共6步, 每步我只问一句, 你回一句就行, 部署的活我来做, 不用你动手。
必需: 一个免费的 Cloudflare 账号。没有的话先用邮箱注册, 有的话登录就行。
不必需: 域名。有绑在 Cloudflare 上的域名优先用它当正式地址; 没有就先用 workers.dev 免费地址, 但大陆网络下它常见整批节点超时, 能部署不等于手机一定能连, 到时绑域名重发订阅再测。
你要准备: 能注册或登录的邮箱, 想一个面板密码, 选一个想要的国家或地区, 最后用手机客户端扫码。
全程你只做四件事: 1) 注册或登录, 2) 回数字或贴回我需要的值, 3) 选国家或地区, 4) 最后扫码验收。
预计耗时: 通常几分钟到十几分钟, 这是估计, 主要取决于注册、登录验证和你的回复速度, 不保证固定时间。
说明: 我只能尽量把入口偏向你选的国家或地区, 不能承诺任意国家的IP, 最后以实测出口为准, 你点头才算定。
```

## 怎么用

把整个文件夹交给支持 Skill 的 AI 助理，让它先读 `SKILL.md` 第 0 节门禁。缺 Cloudflare 登录方式、项目名、域名决定、ADMIN 密码、UUID 决定里的任何一项，它都必须停下来问你，不能自己假设。你只需要登录、过验证码、确认域名、选地区、最后扫码。

## 文件清单

| 文件 | 作用 |
|---|---|
| `SKILL.md` | Skill 本体 |
| `docs/tutorial-zh.md` | 新手中文教程（v3） |
| `docs/x-thread-zh.md` | 推文串精简版 |
| `templates/wrangler.toml.example` | Workers 命令行部署模板（密钥不进此文件） |
| `templates/wrangler.pages.toml.example` | 路线 B：Pages 直传钉版文件的模板 |
| `templates/env.example` | 变量清单（与 SKILL.md 第 3.2 节一致） |
| `templates/ADD.txt.example` | 优选 IP 格式示例（占位符） |
| `templates/make_sub_qr.py` | 订阅二维码生成 + 解码校验 |
| `templates/sub_token.py` | 按源码公式 `MD5MD5(host+uuid)` 核对订阅令牌 |
| `templates/probe_e2e.py` | 优选入口 TLS 探活 + xray 端到端出口核验 |
| `CHANGELOG.md` | 版本记录 |

## 费用实话（以 Cloudflare 官方文档为准）

Workers 免费版每天 100,000 次请求，超了报 1027，UTC 零点（北京时间 8 点）重置；KV 免费版每天 100,000 次读、1,000 次写。一个人自用一般够。说"无限免费"的，让他拿官方文档出来。

## 安全红线

- `ADMIN`、`UUID`、`KEY`、订阅链接、二维码、API Token 都是钥匙。本仓库全是占位符。
- `_worker.js` 只从原作者仓库的钉版地址下载，核对 SHA-256，对不上就停。网上的复制版可能被改过代码偷 UUID。
- 只自己用。Cloudflare 条款不允许拿 Workers/Pages 当通用代理（CloudflareSpeedTest 作者也在 README 里明确提醒），分享、做机场、转卖最容易封号。留一条非 CF 的备用线路。
- 面板界面从 edt-pages.github.io 远程加载，Clash 订阅要经过 SUBAPI 转换：面板少登，介意就用 v2rayN / 小火箭直接读原始订阅。

## 致谢与来源

- **Skill 原作**：[free-dam-man/cf-global-edge-node-skill](https://github.com/free-dam-man/cf-global-edge-node-skill)（v2，2026-10-17）。SKILL.md 的结构、向导流程、门禁和模板都出自原作，后续版本在此基础上补充修正。
- **节点程序**：[cmliu/edgetunnel](https://github.com/cmliu/edgetunnel)（GPL-2.0）。本仓库不收录 `_worker.js`，只给钉版下载地址和 SHA-256。
- **社区教程**：[yonggekkk/Cloudflare-vless-trojan](https://github.com/yonggekkk/Cloudflare-vless-trojan)、[yonggekkk/sing-box-yg](https://github.com/yonggekkk/sing-box-yg)、[XIU2/CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest)、[bia-pain-bache/BPB-Worker-Panel](https://github.com/bia-pain-bache/BPB-Worker-Panel)、[cmliu/WorkerVless2sub](https://github.com/cmliu/WorkerVless2sub)、[233boy/sing-box](https://github.com/233boy/sing-box)。本仓库只引用、转述它们的做法并附链接，不复制它们的代码或数据文件。
- 社区优选 IP 列表等第三方数据只在运行时引用，不收录进本仓库。

## 许可证 / License

本仓库的文档、Skill 和脚本以 [MIT](LICENSE) 许可发布。节点程序 `_worker.js` 来自 [cmliu/edgetunnel](https://github.com/cmliu/edgetunnel)（GPL-2.0），本仓库不打包它，请从原作者仓库下载并遵守其许可。
