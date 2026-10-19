# 零成本自建 Cloudflare 节点：新手完整教程（v3，2026-10）

> 这篇写给从没搭过节点的人。我们自己从零搭过两次，踩过的坑都写在里面，另外还整合了几个社区教程里最有用的部分，每一步都注明了出处。
>
> **文中所有域名、密码、UUID、IP 都是占位符**（`<你的域名>`、`192.0.2.x` 这类），照抄连不上，要换成你自己的。
>
> 主要来源：
> - 节点程序：[cmliu/edgetunnel](https://github.com/cmliu/edgetunnel)（GPL-2.0）
> - Skill 原作：[free-dam-man/cf-global-edge-node-skill](https://github.com/free-dam-man/cf-global-edge-node-skill)
> - 社区教程：[yonggekkk/Cloudflare-vless-trojan](https://github.com/yonggekkk/Cloudflare-vless-trojan)（端口、proxyip、IP 查询）、[XIU2/CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest)（本地测速）、[BPB-Worker-Panel 文档](https://github.com/bia-pain-bache/BPB-Worker-Panel)（分片、常见问题）

## 目录

1. [先看懂：它是怎么工作的](#1-先看懂它是怎么工作的)
2. [准备清单](#2-准备清单)
3. [选路线](#3-选路线)
4. [注册 Cloudflare，领免费域名](#4-注册-cloudflare领免费域名)
5. [下载程序并核对指纹](#5-下载程序并核对指纹)
6. [部署（网页版 / 命令行版）](#6-部署)
7. [KV 和变量](#7-kv-和变量)
8. [绑定域名](#8-绑定域名)
9. [面板和优选 IP](#9-面板和优选-ip)
10. [proxyip 是什么](#10-proxyip-是什么为什么-x-和-chatgpt-需要它)
11. [订阅、二维码、导入客户端](#11-订阅二维码导入客户端)
12. [测试和换掉坏节点](#12-测试和换掉坏节点)
13. [日常维护](#13-日常维护)
14. [安全和隐私](#14-安全和隐私老实说)
15. [常见问题](#15-常见问题)
16. [另一条路：你有 VPS 的话](#16-另一条路你有-vps-的话)
17. [让 AI 帮你做](#17-让-ai-帮你做)

---

## 1. 先看懂：它是怎么工作的

```text
你的手机/电脑 ──► 优选 IP（Cloudflare 的入口） ──► 你的 Worker/Pages 程序 ──► 目标网站
                                                         │
                                                         └─► 目标网站也在 CF 后面（X、ChatGPT 等）
                                                              → 改走 proxyip 中转（见第 10 节）
```

- **花多少钱**：0 元。Cloudflare（下面简称 CF）账号免费，域名用免费域名，不用信用卡，也不用买 VPS。
- **够不够用**：免费版每天 10 万次请求，UTC 零点（北京时间早上 8 点）重置。一个人刷 X、看 YouTube 用不完。
- **出口是什么**：普通网站看到的是 CF 的 IP，套了 CF 的网站看到的是 proxyip 的 IP。**都不是家宽**。
- **适合**：自己或家里人日常刷推、看视频、用 AI。
- **不适合**：分享给别人或者做机场（CF 条款不允许，最容易封号）；要家宽 IP 的；要 100% 稳定的（建议另外留一条备用线路）。

整体流程：注册 CF → 领免费域名 → 部署程序 → 绑域名 → 选优选 IP → 拿订阅 → 小火箭 / Clash Verge 导入。熟练的话半小时以内。

## 2. 准备清单

| 东西 | 说明 |
|---|---|
| 主流邮箱 | Outlook、Gmail 都行。**别用临时邮箱**，DNSHE 会直接拒绝 |
| 手机验证器 App | Microsoft / Google Authenticator 都行。DNSHE 领域名前必须绑两步验证 |
| 电脑 | Win10 就行，用来下载、上传文件和测速 |
| 客户端 | iPhone：Shadowrocket（小火箭，要外区 Apple ID 购买）；Windows：Clash Verge Rev 或 v2rayN |
| 面板密码 | 至少 12 位，别和其他地方的密码重复 |

## 3. 选路线

| 路线 | 适合谁 | 要等多久 | 说明 |
|---|---|---|---|
| **B. Pages + CNAME 子域名**（推荐） | 用 DNSHE 这类免费域名，能自己改 DNS | 几分钟 | 不用把整个域名迁到 CF。我们第二次搭就走的这条。根域名不能用，只能用子域名 |
| **A. Workers + 自定义域** | 域名已经托管在 CF 上（状态是 Active） | 几分钟 | CF 自动建 DNS 和证书 |
| C. 先把域名 NS 迁到 CF，再走 A | 域名在别家，又不能加 CNAME | 几分钟到几小时 | 最慢，A、B 都不行再用 |
| ~~只用 workers.dev / pages.dev~~ | 不推荐 | — | 大陆网络下常见**节点全部超时**：面板打得开，节点却连不上，换优选 IP 也没用 |

> 两种部署方式的区别来自 [edgetunnel README](https://github.com/cmliu/edgetunnel)：作者也把"Pages 上传"标成最推荐。

## 4. 注册 Cloudflare，领免费域名

**Cloudflare**：打开 dash.cloudflare.com，用主流邮箱注册并验证，顺手开两步验证。

**免费域名**（选一个就行；规则经常变，以官网当时显示的为准）：

| 平台 | 后缀举例 | 期限 / 门槛 | 我们的情况 |
|---|---|---|---|
| [DNSHE](https://my.dnshe.com/clientarea.php?language=chinese&autolang=1) | us.ci、ccwu.cc 等 | 有 1 年期也有 10 年期，1 年期的到期前 180 天内可免费续 | **实测用过**：拿到 1 年期 `us.ci`；必须先绑 TOTP 两步验证；临时邮箱被拒 |
| DigitalPlat | dpdns.org、qzz.io | 要 GitHub 验证，一年一续 | 社区反馈，未实测 |
| eu.org | eu.org | 人工审核，几天到几周 | 社区反馈，未实测 |

DNSHE 步骤：
1. 用主流邮箱注册，邮箱会收到验证码。
2. **先绑两步验证**：用验证器 App 扫页面上的二维码，输入 6 位数。这一项**千万别删**，删了可能登不回去。
3. 搜一个名字，**看清期限**再注册。能选 10 年就选 10 年；只有 1 年期的，给自己定个提醒，大约 5 个月后去续。
4. 一个账号能领的不多，一次只注册一个。

## 5. 下载程序并核对指纹

节点程序就是一个 `_worker.js` 文件（约 5 MB）。**只从原作者仓库下载**：网上有很多"魔改版""加强版"，有的被改过代码，会偷你的 UUID。

我们固定用这个版本（commit `66f1c51c`，2026-10-19 核对过，跟作者最新 main 分支的文件一模一样）：

```text
https://raw.githubusercontent.com/cmliu/edgetunnel/66f1c51c4ecee058b959104cb0517e073cdb1213/_worker.js
```

**Win10 上核对指纹**（在下载文件夹里打开 PowerShell）：

```powershell
curl.exe -L -o _worker.js https://raw.githubusercontent.com/cmliu/edgetunnel/66f1c51c4ecee058b959104cb0517e073cdb1213/_worker.js
Get-FileHash .\_worker.js -Algorithm SHA256
# 必须是 1E84D11AF0544654BF56A06FA833E77184A57193288A9FFCCF62C031A9FB7D65
```

Mac / Linux 用 `sha256sum _worker.js`。**对不上就别用。**

## 6. 部署

### 6.1 先起一个不起眼的名字

项目名和 KV 名别带 `proxy`、`vpn`、`vless`、`tunnel`、`node` 这类字眼，起个 `notes-blog`、`my-diary` 就行。有人第一次用很像代理的名字，项目刚建就被风控，换个普通名字重建就过了。[BPB 的常见问题](https://github.com/bia-pain-bache/BPB-Worker-Panel/blob/main/docs/en/docs/faq.md)里也提到：报 1101 多半是账号被标记了，项目名别带面板的名字。

### 6.2 网页版：Pages 上传（推荐，配合路线 B）

1. 新建一个文件夹，比如 `dist`，只放 `_worker.js` 一个文件，然后打包成 zip。（edgetunnel 原教程是直接上传整个 `main.zip`，效果一样，但那样拿到的是最新版，不是我们核对过指纹的固定版。）
2. CF 后台 → Workers 和 Pages → 创建 → Pages → **上传资产**，填项目名，上传 zip，部署。
3. 拖进去没反应、卡了 10 分钟以上：别跟网页较劲，改用下面 6.4 的命令行上传。
4. 部署完记下**实际分到的** `xxx.pages.dev`。名字被别人占了，CF 会自动加后缀（比如 `notes-blog-abc.pages.dev`）。没加后缀的那个地址可能是别人的项目。

### 6.3 网页版：Workers（配合路线 A）

来自 [edgetunnel README](https://github.com/cmliu/edgetunnel)：
1. Workers 和 Pages → 创建 → Worker，起名，先部署默认代码。
2. 编辑代码 → 全选删掉 → 粘贴 `_worker.js` 的全部内容 → 部署。文件有 5 MB，**一定要粘贴完整**，少一截就会报 1101。

### 6.4 命令行版：wrangler（会用终端的）

wrangler 4 要配 Node 22。下面这几行把我们踩过的坑都提前绕开了：

```bash
mkdir -p notes-blog/dist notes-blog/node_modules && cd notes-blog   # 空的 node_modules 必须建，不然报 /node_modules 权限错误
cp ../_worker.js dist/
export WRANGLER_SEND_METRICS=false WRANGLER_CACHE_DIR="$PWD/.wrangler/cache"
npx wrangler login
npx wrangler kv namespace create notes-blog-kv          # 记下输出的 id，填进 wrangler.toml
npx wrangler pages project create notes-blog --production-branch main
npx wrangler pages project list                         # 看实际分到的 xxx.pages.dev
npx wrangler pages deploy --project-name notes-blog --branch main --no-bundle --commit-dirty=true
```

`wrangler.toml` 模板在 `templates/wrangler.pages.toml.example`（Pages 用）和 `templates/wrangler.toml.example`（Workers 用）。**密码和 UUID 不要写进这个文件**，到网页后台按"加密"类型添加。

## 7. KV 和变量

1. 存储和数据库 → KV → 创建一个命名空间（名字也起普通点）。
2. 回到项目 → 设置 → **绑定** → 添加 KV 命名空间，**变量名必须是大写的 `KV`**。
3. 设置 → **变量和机密**，按下表填：

| 变量 | 填什么 | 类型 |
|---|---|---|
| `ADMIN` | 面板密码（≥12 位） | 加密 / Secret |
| `UUID` | 新生成一个 UUID v4（PowerShell 里运行 `[guid]::NewGuid()`） | 加密 / Secret |
| `KEY` | 可选，快捷订阅路径用 | 加密 / Secret |
| `HOST` | 第 8 步绑好的子域名，比如 `blog.<你的域名>` | 普通变量 |
| `PROXYIP`、`BEST_SUB`、`GO2SOCKS5`、`PATH`、`URL` | **先都别填** | — |

4. 改完设置一定要**重新部署一次**才生效（Pages：部署 → 创建新部署，重新传一次 zip）。

> 为什么要固定 `UUID`：edgetunnel 不填 UUID 时会用 `ADMIN` + `KEY` 算一个出来，以后改密码，所有节点和订阅会一起失效（见 [edgetunnel README](https://github.com/cmliu/edgetunnel) 的「高级实用技巧」）。
>
> `URL` 是首页伪装，不填时打开域名首页就是一个普通的 nginx 页面，已经够了。别填别人的网站。

## 8. 绑定域名

**路线 B（Pages + CNAME）**
1. Pages 项目 → 自定义域 → 设置自定义域，填一个**子域名**，比如 `blog.<你的域名>`，选"我的 DNS 提供商"。
2. 回 DNSHE → DNS 管理 → 添加 **CNAME**：主机名 `blog`，目标填第 6 步**实际分到的** `xxx.pages.dev`。已经有同名记录就换个子域名，别覆盖。
3. 几分钟后 Pages 显示"有效"并签好证书。把变量 `HOST` 改成这个子域名，再部署一次。

**路线 A（Workers + CF 上的域名）**：Worker → 设置 → 域和路由 → 添加 → 自定义域，填 `blog.<你的域名>`，CF 会自动建记录和证书（按钮名以当前后台为准）。

以后节点、订阅都用这个子域名，**不要再用 pages.dev / workers.dev**。

## 9. 面板和优选 IP

打开 `https://blog.<你的域名>/login`，输入 `ADMIN` 密码进面板。

### 9.1 为什么要换优选 IP

默认是"随机 IP"模式，每次刷新订阅都随机出 16 个 CF 的 IP，能用但不稳，地区也不固定。在面板的优选订阅设置里**把"随机IP"关掉**，然后编辑 `ADD.txt`。保存就生效，不用重新部署。

### 9.2 ADD.txt 怎么写

一行一个，`#` 后面是节点名。下面的写法都是我们对着 edgetunnel 源码核对过的：

```text
192.0.2.10:8443#JP-1
[2001:db8::10]:443#JP-v6
cdn.example.com:2053#SG-1
https://example.com/my-ip-list.txt
```

| 写法 | 意思 |
|---|---|
| `IP:端口#名字` | 最常用。不写端口默认 443 |
| `[IPv6]:端口#名字` | IPv6 地址要加方括号 |
| `域名:端口#名字` | 优选域名也行 |
| `https://...` 整行 | 一个远程 IP 列表（社区优选 API），程序会自己去拉 |

格式写错的行会被**悄悄跳过**，不会报错，只是少一个节点。行尾别加注释。

端口规则（[CF 官方端口表](https://developers.cloudflare.com/fundamentals/reference/network-ports/)，[yonggekkk 教程](https://github.com/yonggekkk/Cloudflare-vless-trojan)也有整理）：

| 类型 | 端口 | 能不能用在我们这套 |
|---|---|---|
| HTTPS（443 系） | 443、2053、2083、2087、2096、8443 | **能**。我们绑了自己域名，节点都走 TLS |
| HTTP（80 系） | 80、8080、8880、2052、2082、2086、2095 | 不能（这些不加密，只适合不绑域名的 Workers 玩法） |

CF 官方 IP 用上面任意一个 443 系端口都行；第三方反代 IP 只能用它自己开的那个端口。

### 9.3 IP 从哪里来

**方法一：用 CloudflareSpeedTest 在你自己电脑上测（最准）**

服务器上测得快，不代表你家宽带连得快，所以最好在你自己的网络上测。工具是 [XIU2/CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest)（下面简称 CFST），以下用法摘自它的 README：

1. 到 [Releases](https://github.com/XIU2/CloudflareSpeedTest/releases) 下载 Windows 版（`cfst_windows_amd64.zip`），解压到比如 `D:\cfst`。
2. **先退出 Clash Verge / 关掉代理**。CFST 作者特别提醒：测出来延迟只有零点几毫秒，说明走了代理，结果不能用。
3. 在 `D:\cfst` 文件夹地址栏输入 `powershell` 回车，运行：

```powershell
# 只要日本/新加坡/台湾/美国的机房，按延迟排序，不测下载速度（新手先用这个）
.\cfst.exe -httping -cfcolo NRT,KIX,SIN,TPE,LAX,SJC,SEA -tl 250 -dd -n 100
```

   - `-httping -cfcolo ...`：只留指定机房的 IP（机场三字码：NRT/KIX 日本，SIN 新加坡，TPE 台湾，LAX/SJC/SEA 美国），`-cfcolo` 只有 HTTPing 模式才能用；
   - `-tl 250`：只要平均延迟 250ms 以内的；
   - `-dd`：不测下载速度（默认的下载测速地址不保证能用）；
   - `-n 100`：降低并发。作者提醒 HTTPing 本质上算扫描，并发太高可能被运营商或 CF 临时限制。
   - 想顺便测下载速度：去掉 `-dd`，加 `-dn 10`。
   - 你家有 IPv6 的话（可以用 test-ipv6.com 测）：加 `-f ipv6.txt` 测 IPv6 入口。注意手机切到没 IPv6 的网络就连不上，所以 IPv4、IPv6 各放几个。
4. 结果在 `result.csv`（用 Excel 打开中文会乱码，正常，用记事本看）。挑前几个，按 `IP:443#地区-序号` 写进 ADD.txt。
5. 每次测的结果都不一样（CFST 每个 /24 段随机挑一个 IP），这是正常的。隔几周测一次就行。

> CF 官方 IP 进到哪个机房，是你的运营商决定的，常见的情况是落到美国西海岸。所以想要日本、新加坡出口，常常得靠第三方反代 IP（方法二）。

**方法二：第三方反代 IP（我们实际在用）**
- 好用的大多在非 443 端口：**2053 / 2083 / 2087 / 8443**。
- 这些是别人的机器，能看到你的连接信息，随时可能消失。
- **列表上写的地区不能全信**：我们遇到过标着"台湾"、实际从美国出去的。节点名写**实测出来的地区**。

**方法三：社区优选列表**：把列表地址作为 `https://...` 一行写进 ADD.txt，最省事，但列表随时会变、会失效，适合先跑通，之后换成自己测过的 IP。

### 9.4 选哪些地区

- 要用 ChatGPT、Claude、Gemini，**别选香港**，这些 AI 不对香港开放。
- 延迟低又能用 AI：**台湾、日本、新加坡**，再加**美国**当保底。
- 台湾能用的入口很少，很多像是别人家里的设备，过几天就没了。少放几个，多留备用。
- 最多放 10 个；另外每个地区留 3~5 个备用，先别写进去。

## 10. proxyip 是什么？为什么 X 和 ChatGPT 需要它

- CF 规定 Worker **不能直接连 CF 自己的 IP**（[官方文档](https://developers.cloudflare.com/workers/runtime-apis/tcp-sockets/)：Outbound TCP sockets to Cloudflare IP ranges are blocked）。
- X、ChatGPT 和很多网站本身就套着 CF。所以访问它们时，程序要先把流量交给一台"中转机"，由它去连。这台中转机就是 **proxyip**。
- 所以会出现一种典型现象：**YouTube 正常，X / ChatGPT 打不开**，十有八九是 proxyip 的问题，不是节点坏了。
- 也就是说，ChatGPT 看到的地区，是 **proxyip 的地区**，不是你选的入口的地区。

**怎么办**：
1. **首次搭建别填 `PROXYIP`**。edgetunnel 不填时会按你连到的机房自动选一个，失败还会自动兜底（源码已核对）。
2. 真遇到 X / ChatGPT 打不开：先换一个其他地区的节点试。还不行，再在变量 `PROXYIP` 填一个可用的（格式 `域名:端口` 或 `IP:端口`，edgetunnel README 的例子是 `proxyip.cmliussss.net:443`）。**注意：一填上自动兜底就关了**，这一个挂了，所有套 CF 的网站都会打不开，所以填之前先确认它能用。
3. [BPB 的常见问题](https://github.com/bia-pain-bache/BPB-Worker-Panel/blob/main/docs/en/docs/faq.md)也提醒：只填一个 proxyip，用一阵子可能就失效了。不需要固定 IP 的话，用默认的就好。

**怎么查**（来自 [yonggekkk 教程](https://github.com/yonggekkk/Cloudflare-vless-trojan)）：开着节点，
- 打开 `https://www.whatismyip.com`：显示 CF 的 IP，这是普通网站看到的出口；
- 打开 `https://ip.sb`：显示 proxyip 的 IP，这是套了 CF 的网站（X、ChatGPT）看到的出口。
- 想直接看 ChatGPT 认为你在哪：打开 `https://chatgpt.com/cdn-cgi/trace`，看 `loc=` 后面的地区代码。（这一招是我们按原理推的，不是哪个教程写的，仅供参考。）

## 11. 订阅、二维码、导入客户端

### 11.1 订阅链接

面板里可以直接复制，长这样：

```text
https://blog.<你的域名>/sub?token=<一串32位字符>
```

令牌是 `MD5MD5(域名 + UUID)` 算出来的，想核对可以用 `templates/sub_token.py`。**改了域名或 UUID，令牌就变了**，旧链接和旧二维码都会失效。

### 11.2 二维码

```bash
pip install "qrcode[pil]"
SUB_URL="https://blog.<你的域名>/sub?token=<令牌>" python3 templates/make_sub_qr.py --output my-sub.png
```

**别用在线二维码网站**：订阅链接就是钥匙，谁拿到谁就能用你的节点。

### 11.3 iPhone · Shadowrocket（小火箭）

1. 首页右上角扫一扫，扫二维码。正常会提示"添加订阅"，不是只加一个节点。
2. 二维码就在这台手机上的话，改成复制链接：右上角 `+` → 类型选 Subscribe → 粘贴 → 完成 → 下拉刷新。
3. **关掉 UDP 转发**。这套只走 TCP；[BPB 常见问题](https://github.com/bia-pain-bache/BPB-Worker-Panel/blob/main/docs/en/docs/faq.md)也说了，CF 处理不好 UDP，Telegram 语音这类东西本来就用不了。
4. 点"连通性测试"，看哪几个超时。

### 11.4 Windows 10 · Clash Verge Rev

1. 订阅 → 粘贴订阅链接 → 导入 → 选中这个订阅。
2. 代理里选一个节点 → 打开**系统代理**。有的软件不走系统代理，就开 TUN 模式。
3. 导入失败、小火箭却正常：多半是订阅转换服务（SUBAPI）暂时挂了，过一会儿再试。
4. 介意转换服务能看到你的域名，可以改用 **v2rayN**：它直接读原始订阅，不经过转换服务。

### 11.5 进阶：域名被墙时试试分片

如果某天节点突然全部超时，换 IP 也没用，可能是你的域名在 TLS 握手阶段被阻断了。
- 先试最简单的：换一个新子域名，重新绑定，改 `HOST`，重新出订阅。
- 或者在客户端开 **TLS 分片（Fragment）**。BPB 的文档解释过原理：分片把握手拆开，让中间设备认不出域名；[yonggekkk 教程](https://github.com/yonggekkk/Cloudflare-vless-trojan)也说，开分片能让被 TLS 阻断的域名重新用起来。edgetunnel 面板里有个"TLS分片"选项，可以选 Shadowrocket 版，订阅里的节点就会自动带上分片参数（源码已核对）。
- 没被阻断时**别开分片**：会变慢，配错还会卡住。

## 12. 测试和换掉坏节点

我们服务器端测通的 9 个节点，手机上一测，有 3 个超时。这很正常：你的运营商跟测试机走的不是同一条线路。

1. 小火箭里做一次连通性测试，截图记下哪几个超时。
2. 去面板 `ADD.txt`，把超时的换成备用的，保存。
3. 手机上刷新订阅，再测一次。
4. 再按第 10 节查一下出口：普通网站看 whatismyip，AI 网站看 ip.sb 或 chatgpt.com/cdn-cgi/trace。

## 13. 日常维护

| 事情 | 多久一次 | 怎么做 |
|---|---|---|
| 续域名 | 看期限 | DNSHE 1 年期的，到期前 180 天内免费续，记在日历里 |
| 换掉坏节点 | 发现超时就换 | 只改 ADD.txt，不用重新部署 |
| 重新测速 | 几周一次 | 第 9.3 节的 CFST 命令跑一遍 |
| 看额度 | 偶尔 | 项目 → 指标，看每天请求数（上限 10 万） |
| 升级程序 | 不着急 | 见下面 |

**升级 edgetunnel**：能用就别急着升级。真要升级：
1. 先看作者仓库的 [CHANGELOG](https://github.com/cmliu/edgetunnel/blob/main/CHANGELOG) 改了什么；
2. 从原作者仓库下载新的 `_worker.js`，**自己算一遍 SHA-256 记下来**（以后核对就用这个新值）；
3. 留着旧文件，新版有问题可以马上传回去；
4. 重新部署后检查：面板能登录、订阅能拿到、手机能连。KV 里的设置和 ADD.txt 不会丢。

## 14. 安全和隐私（老实说）

1. **封号风险**：CF 条款不允许把 Workers / Pages 当代理服务用。CFST 作者也在 README 里专门提醒：CF CDN 已明文禁止代理用法，风险自担。自己用、量小，算是自担风险；分享、做机场、转卖，最容易被封。所以只自己用，再留一条备用线路。
2. **面板界面是远程加载的**：edgetunnel 的登录页和管理页从作者的网站（edt-pages.github.io）加载，理论上那边的代码能看到你的配置。这是程序本身的设计，不代表作者会做什么，但**面板少登**：配好就别常进，日常只用订阅。
3. **Clash 订阅要经过转换服务（SUBAPI）**：转换服务能看到你的域名和入口 IP，看不到 UUID。介意的话改用 v2rayN 或小火箭这类能直接读原始订阅的客户端，或者自己搭一个转换服务。
4. **别把节点交给公共工具**：公共的"优选订阅生成器"作者自己都提醒，别把私人节点放进去，不然所有人都能拿到（见 [WorkerVless2sub](https://github.com/cmliu/WorkerVless2sub)）。
5. **中转 IP 是别人的机器**：能看到你的连接信息，可能随时消失。日常上网可以，敏感的事别只靠它。
6. **出口不是家宽**：别拿共享出口去登你最重要的账号。
7. **只认原作者仓库**，下载后一定核对 SHA-256。
8. **订阅链接、二维码、面板密码、UUID 都是钥匙**：别发到群里、截图里、文章里。

## 15. 常见问题

| 现象 | 原因 | 怎么办 |
|---|---|---|
| 面板能打开，节点全部超时 | 用了 `workers.dev` / `pages.dev` 当节点地址 | 绑自己的子域名，改 `HOST`，重新出订阅 |
| 用的自己域名，也突然全部超时 | 域名可能被阻断了 | 换个新子域名，或在客户端开分片（11.5） |
| YouTube 正常，X / ChatGPT 打不开 | proxyip 问题 | 第 10 节 |
| ChatGPT 提示地区不支持 | 出口在香港，或 proxyip 在不支持的地区 | 换台、日、新、美的节点；用 chatgpt.com/cdn-cgi/trace 看 `loc=` |
| 报错 1101 | 代码没粘贴完整；或者账号、项目被风控 | 重新传核对过的文件；换个普通名字新建项目 |
| 报错 1027 | 当天 10 万次额度用完了 | 北京时间早上 8 点重置；查查哪个设备在疯狂刷新 |
| `/admin` 总是跳回登录页 | 密码不对，或改完变量没重新部署 | 重设 `ADMIN`，重新部署 |
| 每次刷新节点都变 | "随机IP"没关 | 第 9.1 节 |
| 部分节点超时 | 你的线路连不上那几个入口 | 换成备用 IP，刷新订阅 |
| 浏览器打开订阅是一堆明文 | 正常：浏览器拿到明文版，客户端拿到 base64 版 | 不用管 |
| Clash 导入失败，小火箭正常 | 订阅转换服务暂时挂了 | 稍后再试，或改用 v2rayN |
| 改了域名或 UUID，订阅失效 | 令牌跟着变了 | 重新复制订阅链接、重新出二维码 |
| Telegram 语音、部分游戏不通 | 这套不支持 UDP | 正常现象，这类需求用 VPS（第 16 节） |
| CFST 测出来延迟零点几毫秒 | 测速时代理还开着 | 关掉 Clash Verge 再测 |
| CFST 结果是 0 个 IP | 指定地区没有可用 IP，或测速地址不通 | 去掉 `-cfcolo` 试试；加 `-debug` 看原因 |
| DNSHE 邮箱被拒 / 不让领域名 | 用了临时邮箱 / 没绑两步验证 | 换 Outlook、Gmail；先绑 TOTP |
| wrangler 报 `/node_modules` 权限错误 | 项目里没有 node_modules | 建一个空的 `node_modules` 文件夹，用 Node 22 |
| 项目刚建就被风控 | 名字太像代理 | 换个普通名字重建 |

## 16. 另一条路：你有 VPS 的话

CF 节点是"免费、够用"，VPS 节点是"自己的、更稳、支持 UDP"。如果你有一台 VPS（包括只有 IPv6 的免费小鸡）：

- **一键脚本**：[yonggekkk/sing-box-yg](https://github.com/yonggekkk/sing-box-yg)（一键装 VLESS-Reality、Hysteria2、TUIC 等五种协议，支持纯 IPv6，回车三次装好），或 [233boy/sing-box](https://github.com/233boy/sing-box)（默认就是 VLESS-REALITY，[安装文档](https://233boy.com/sing-box/sing-box-script/)）。
- **协议优先 VLESS-Reality**：不用域名、不用证书。有人反馈 Hysteria2（走 UDP）在国内连不上、换 Reality 就通了，这跟运营商对 UDP 的限制有关，不一定人人一样。
- **只有 IPv6 的 VPS**：你的手机或电脑也得有 IPv6 才能直连（先去 test-ipv6.com 测）。
- **合并成一个订阅**：edgetunnel 的 ADD.txt 支持直接放完整的 `vless://...` 节点链接（源码已核对），可以把 VPS 节点也塞进同一个订阅，客户端里一起管理。
- yonggekkk 还介绍了用纯 IPv6 VPS 自建 proxyip 的玩法，进阶再看。

## 17. 让 AI 帮你做

把本仓库（`SKILL.md` + `templates/`）交给支持 Skill 的 AI 助理，说"帮我搭一个 CF 节点"。它会先发一张说明卡，然后从"第 1/6 步"问到"第 6/6 步"。部署、绑域名、测 IP、出二维码都是它来做，你只需要：

1. 登录或注册账号，遇到验证码、两步验证自己输入；**密码别发在聊天里**；
2. 确认要注册的域名；
3. 选地区；
4. 扫码验收，把超时的节点截图发给它换掉。

---

*最后核对：2026-10-19。CF 免费额度、免费域名规则、edgetunnel 版本、各后台按钮名都可能变化，动手前以官网和仓库为准。*
