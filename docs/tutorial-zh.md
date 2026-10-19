# 零成本自建 Cloudflare 节点:普通人也能照着做的教程(2026-10 实测版)

> 这篇是给完全没搭过节点的人写的。我们自己从零搭了一遍,把踩过的坑都写进来了。文中所有域名、密码、UUID、IP 都是占位符,照抄不能用,要换成你自己的。
>
> 节点程序用的是 [cmliu/edgetunnel](https://github.com/cmliu/edgetunnel)(GPL-2.0),AI 自动部署用的 Skill 改编自 [free-dam-man/cf-global-edge-node-skill](https://github.com/free-dam-man/cf-global-edge-node-skill)。

## 先说清楚:这是什么、适不适合你

- **是什么**:在 Cloudflare(下面简称 CF)的免费服务上放一个小程序,你的手机或电脑先连到 CF 的全球节点,再从 CF 出去上网。
- **花多少钱**:0 元。CF 账号免费,域名用 DNSHE 的免费域名,不用信用卡,也不用买 VPS。
- **够不够用**:免费版每天 10 万次请求。一个人日常刷 X、看 YouTube,根本用不完。
- **适合谁**:自己一个人或一家人日常用,刷推、看视频、用 AI。
- **不适合**:
  - 分享给别人或者做机场。CF 条款不允许把它当代理服务,分享出去最容易被封号。
  - 要"家宽 IP"的。这套的出口是 CF 机房的 IP,不是家宽。
  - 要求 100% 稳定的。建议另外留一条备用线路。

整体流程:注册 CF → 领免费域名 → 部署程序 → 绑域名 → 选优选 IP → 拿订阅 → 小火箭 / Clash Verge 扫码导入。熟练的话半小时以内。

---

## 第 0 步:准备好这些东西

| 东西 | 说明 |
|---|---|
| 一个主流邮箱 | Outlook、Gmail 都行。**别用临时邮箱**,DNSHE 会直接拒绝 |
| 手机验证器 App | Microsoft Authenticator、Google Authenticator 都可以。DNSHE 领域名前必须先绑两步验证 |
| 一台电脑 | 用来上传文件、改设置 |
| 客户端 | iPhone 用 Shadowrocket(小火箭,要外区 Apple ID 购买);Windows 用 Clash Verge |
| 一个面板密码 | 至少 12 位,不要和别的地方重复 |

> 懒得自己动手?把本仓库交给支持 Skill 的 AI 助理,它会一步一步问你,你只需要登录、过验证码、确认域名,最后扫码。见文末。

---

## 第 1 步:注册 Cloudflare 账号

打开 dash.cloudflare.com,用邮箱注册并验证。建议顺手开启两步验证。

## 第 2 步:领一个免费域名(DNSHE)

**为什么一定要域名?** CF 会免费给你一个 `xxx.workers.dev` 或 `xxx.pages.dev` 地址,但在大陆网络下,拿它当节点地址经常**全部超时**:面板在浏览器里打得开,节点却连不上,换优选 IP 也救不了。绑一个自己的域名就好了。

1. 打开 [DNSHE](https://my.dnshe.com/clientarea.php?language=chinese&autolang=1),用**主流邮箱**注册。邮箱会收到验证码。
2. **先绑两步验证(TOTP)**:页面会显示一个二维码,用验证器 App 扫码,再输入 App 上的 6 位数。不绑这个领不了域名。验证器里的这一项**千万别删**,删了可能就登不回去了。
3. 搜一个想要的名字,我们这次用的是 `us.ci` 后缀,也就是 `<你的名字>.us.ci`。
4. 看清期限再注册。我们拿到的是 **1 年期**,**到期前 180 天内可以免费续期**,以页面当时的规则为准。记得给自己定个提醒,注册后大约 5 个月去续。
5. 一个账号能领的免费域名不多,一次只注册一个,别批量注册。

## 第 3 步:下载节点程序,并核对"指纹"

节点程序是一个叫 `_worker.js` 的文件。**只从原作者仓库下载**:网上有很多复制版,有的可能被改过代码,会偷你的 UUID。

我们用的是固定版本(commit `66f1c51c`)。在电脑上运行:

```bash
curl -L -o _worker.js https://raw.githubusercontent.com/cmliu/edgetunnel/66f1c51c4ecee058b959104cb0517e073cdb1213/_worker.js
sha256sum _worker.js
# 必须是 1e84d11af0544654bf56a06fa833e77184a57193288a9ffccf62c031a9fb7d65
```

Windows 下可以用 `certutil -hashfile _worker.js SHA256` 查看。**对不上就别用。**

## 第 4 步:在 Cloudflare Pages 上部署

### 4.1 起一个不起眼的名字

项目名别带 `proxy`、`vpn`、`vless`、`tunnel`、`node` 这类字眼,起个 `notes-blog`、`my-diary` 之类的就行。有人第一次用很像代理的名字,项目刚建就被风控;换个普通名字重建就过了。这是个案经验,不是官方规则,但改个名又不费事。

### 4.2 网页操作(适合大多数人)

1. 新建一个文件夹,比如 `dist`,把 `_worker.js` 放进去。
2. CF 后台 → Workers & Pages → 创建 → Pages → **上传资产(Direct Upload)**,填项目名,把 `dist` 文件夹(或者打包好的 zip)拖进去,点部署。
3. 新建 KV:存储和数据库 → KV → 创建,名字同样起得普通一点。
4. 回到 Pages 项目 → 设置:
   - **绑定**:添加 KV 命名空间,变量名必须是大写的 `KV`。
   - **变量和机密**:添加 `ADMIN`(面板密码)、`UUID`(在电脑上运行 `uuidgen` 生成,或者用在线 UUID v4 生成器生成)。这两个都选**加密 / Secret** 类型。再加一个普通变量 `HOST`,先空着,第 5 步再填。`PROXYIP`、`BEST_SUB` 这些先**不要填**。
5. 改完设置要**重新部署一次**才生效。

### 4.3 命令行操作(会用终端的)

用 wrangler 4,要配 Node 22。下面是我们踩过的坑,提前设好:

```bash
mkdir -p notes-blog/dist notes-blog/node_modules && cd notes-blog   # 空的 node_modules 必须建,不然会报 /node_modules 权限错误
cp ../_worker.js dist/
export WRANGLER_SEND_METRICS=false WRANGLER_CACHE_DIR="$PWD/.wrangler/cache"
npx wrangler login
npx wrangler kv namespace create notes-blog-kv
npx wrangler pages project create notes-blog --production-branch main
npx wrangler pages project list        # 记下实际分到的 xxx.pages.dev,名字被占时会自动加后缀
npx wrangler pages deploy --project-name notes-blog --branch main --no-bundle --commit-dirty=true
```

`wrangler.toml` 的模板见 `templates/wrangler.pages.toml.example`。密码和 UUID **不要写进这个文件**,到网页后台按"加密"类型添加。

## 第 5 步:绑定你的域名(关键一步)

1. Pages 项目 → 自定义域 → 设置自定义域,填一个**子域名**,比如 `blog.<你的域名>`。根域名不行。选"我的 DNS 提供商"。
2. 回到 DNSHE → DNS 管理 → 添加一条 **CNAME** 记录:主机名填 `blog`,目标填第 4 步**实际分到的** `xxx.pages.dev`。如果已经有同名记录,换个子域名,别覆盖。
3. 等几分钟,Pages 里显示"有效 / Active",证书签好就行。不用把整个域名迁到 CF,所以很快。
4. 把变量 `HOST` 改成 `blog.<你的域名>`,再重新部署一次。

以后节点地址、订阅地址全都用这个域名,**不要再用 pages.dev**。

## 第 6 步:登录面板,换成优选 IP

1. 打开 `https://blog.<你的域名>/login`,输入 `ADMIN` 密码。
2. 默认是"随机 IP"模式,每次刷新订阅节点都会变。在面板的优选订阅设置里**把"随机IP"关掉**,再编辑 `ADD.txt`,一行一个节点:

```text
<入口IP>:8443#JP-1
<入口IP>:2053#SG-1
<入口IP>:2087#US-1
```

**优选 IP 怎么挑(我们的经验):**
- 好用的大多是第三方反代 IP,端口用 CF 的非 443 端口:**2053 / 2083 / 2087 / 8443**。
- 要用 ChatGPT、Claude、Gemini 的话,**别选香港**,这些 AI 不对香港开放。延迟低、又能用 AI 的组合是**台湾、日本、新加坡**,再加美国当保底。
- 台湾能用的入口很少,很多像是别人家里的设备,过几天就没了。台湾少放几个,多留备用。
- 标签写**实测出来的地区**,别信列表上写的。我们就遇到过标着"台湾"、实际从美国出去的入口。
- Win10 上可以用 [XIU2/CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest) 测测你家宽带连哪些 IP 快。小批量测就行。
- 最多放 10 个,另外留 3~5 个备用,先不写进去。

保存后不用重新部署,刷新订阅就生效。

> 会用命令行的,可以用 `templates/probe_e2e.py` 配合 xray 真跑一遍,看每个入口实际从哪个地区出去。注意:你电脑上测得快,不代表手机运营商连得上。

## 第 7 步:拿订阅链接,生成二维码

订阅链接长这样(面板里能直接复制):

```text
https://blog.<你的域名>/sub?token=<一串32位字符>
```

令牌是程序算出来的,公式是 `MD5MD5(域名 + UUID)`。想核对的话可以用 `templates/sub_token.py`。

生成二维码:

```bash
pip install "qrcode[pil]"
SUB_URL="https://blog.<你的域名>/sub?token=<令牌>" python3 templates/make_sub_qr.py --output my-sub.png
```

**别用在线二维码网站**:订阅链接就是你的钥匙,谁拿到谁就能用你的节点。

## 第 8 步:导入客户端

**iPhone · Shadowrocket(小火箭)**
1. 首页右上角扫一扫,扫二维码。正常会提示"添加订阅",而不是只添加一个节点。
2. 二维码就在同一台手机上的话,改成复制链接:点右上角 `+` → 类型选 Subscribe → 粘贴 → 完成 → 下拉刷新。
3. 关掉 UDP 转发,这套主要走 TCP,开着反而像是节点坏了。
4. 点"连通性测试",看哪几个节点超时。

**Windows 10 · Clash Verge**
1. 订阅(Profiles)→ 粘贴订阅链接 → 导入 → 选中这个订阅。
2. 代理(Proxies)里选一个节点 → 打开**系统代理**。有的软件不走系统代理,就开 TUN 模式。
3. 导入失败但小火箭正常:多半是订阅转换服务暂时挂了,过一会儿再试。

## 第 9 步:测一遍,把超时的换掉

我们服务器端测通的 9 个节点,用户手机一测,有 3 个超时。这很正常:你的运营商跟测试机走的不是同一条线路。

做法很简单:截图看哪几个超时,去面板 `ADD.txt` 里把它们换成备用的,保存,手机上刷新订阅,再测一次。

打开 `https://www.cloudflare.com/cdn-cgi/trace`,`loc=` 后面就是你实际出口的地区。

---

## 坑位汇总(我们都踩过)

| 现象 | 原因 / 解决 |
|---|---|
| 面板能打开,节点全部超时 | 用了 `workers.dev` / `pages.dev` 当地址。去绑自己的域名 |
| DNSHE 注册时邮箱被拒 | 临时邮箱不行,换 Outlook、Gmail |
| DNSHE 不让领域名 | 先绑 TOTP 两步验证 |
| 项目刚建就被风控 | 换个普通名字重建,别再用带"代理"意思的名字 |
| wrangler 报 `/node_modules` 权限错误 | 在项目目录里建一个空的 `node_modules` 文件夹,用 Node 22 |
| 每次刷新节点都变 | "随机IP"没关 |
| 部分节点超时 | 换成备用 IP,换完刷新订阅 |
| 浏览器打开订阅是一堆明文 | 正常,浏览器拿到的是明文版,客户端拿到的是 base64 版 |
| Clash 导入失败、小火箭正常 | 订阅转换服务挂了,稍后再试 |
| 改了域名或 UUID 后订阅失效 | 令牌跟着变了,要重新出订阅链接和二维码 |

## 风险,老实说

1. **封号风险**:CF 条款不允许把 Workers / Pages 当代理服务。自己用量小是在"自担风险";分享、做机场、转卖最容易被封。所以只自己用,另外留一条备用线路。
2. **出口不是家宽**:网站看到的是 CF 或中转的 IP。有的网站对这类 IP 有限制,也别拿共享出口去登你最重要的账号。
3. **面板界面是远程加载的**:edgetunnel 的登录页和管理页是从作者的网站(edt-pages.github.io)加载的,理论上那边的代码能看到你的配置。这是程序本身的设计,不代表作者会怎样,但**面板少登**:配好就别常进,日常只用订阅。
4. **Clash 订阅要经过转换服务(SUBAPI)**:转换服务能看到你的域名和入口 IP,看不到 UUID。介意的话,自己搭一个转换服务,或者只用小火箭这种能直接读 base64 订阅的客户端。
5. **中转 IP 是别人的机器**:能看到你的连接信息,可能随时消失。日常上网可以,敏感的事别只靠它。
6. **只认原作者仓库**:搜出来的"魔改版""加强版"很多,有的会偷 UUID。下载后一定要核对 SHA-256。
7. **订阅链接、二维码、面板密码、UUID 都是钥匙**:不要发到群里、截图里、文章里。

## 让 AI 帮你做

把本仓库(`SKILL.md` + `templates/`)交给支持 Skill 的 AI 助理,对它说"帮我搭一个 CF 节点"。它会先发一张说明卡,然后按"第 1/6 步"到"第 6/6 步"一步一步问你。部署、绑域名、测 IP、出二维码都是它来做,你只需要:

1. 登录或注册账号,遇到验证码、两步验证自己输入;**密码别发在聊天里**。
2. 确认要注册的域名。
3. 选地区。
4. 扫码验收,把超时的节点截图发给它换掉。

---

*最后核对:2026-10-19。CF 免费额度、DNSHE 规则、edgetunnel 版本都可能变化,动手前以官网和仓库为准。*
