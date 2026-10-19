# X 推文串版（8 条）

> 每条控制在约 140 个汉字以内（X 上中文按 2 字符计，大致不超过 280 字符）。

**1/8**
0 元、不用信用卡、不用 VPS，在 Cloudflare 上搭了个自己的节点，刷推、看 YouTube 很稳。免费版每天 10 万次请求，一个人用不完。我把原版教程、我们两次实测踩的坑、几个知名社区教程的精华合成了一篇新手教程 🧵

**2/8**
原料三样：
① Cloudflare 免费账号
② 免费域名（我们用 DNSHE 的 us.ci，1 年期，到期前 180 天内免费续）
③ cmliu/edgetunnel 的 _worker.js，只从原作者仓库下，并核对 SHA-256。网上的魔改版有偷 UUID 的

**3/8**
最关键：别用 workers.dev / pages.dev 当节点地址，大陆网络下经常全部超时。用 Pages 上传部署，在域名后台加一条子域名 CNAME 指过去，几分钟生效，不用把整个域名迁到 CF。项目名起个 notes-blog 这种普通名字

**4/8**
优选 IP 最好在自己电脑上测：Win10 下载 XIU2 的 CloudflareSpeedTest，先关掉代理再跑
cfst.exe -httping -cfcolo NRT,SIN,TPE,LAX -dd -n 100
只留日本、新加坡、台湾、美国机房的 IP，按延迟排好，挑前几个写进 ADD.txt

**5/8**
第三方反代入口多在 2053 / 2083 / 2087 / 8443 端口，好用但会突然消失，每个地区留几个备用。要用 AI 就别选香港，台、日、新加坡加美国最合适。服务器测通的 9 个节点，手机上有 3 个超时，换成备用就好

**6/8**
YouTube 能开、X 和 ChatGPT 打不开？多半不是节点坏了，是 proxyip 的事：CF 不让 Worker 直连 CF 自家的 IP，而 X、ChatGPT 都套着 CF，得靠 proxyip 中转。首次搭建别填 PROXYIP，程序会自动选、还会自动兜底

**7/8**
老实说风险：
· CF 条款不让拿它当代理。自己用是自担风险，分享或做机场最容易被封
· 出口是 CF 的 IP，不是家宽
· 面板界面是远程加载的，少登录
· Clash 订阅要过第三方转换，介意就用 v2rayN

**8/8**
iPhone 用小火箭扫码，Win10 用 Clash Verge 或 v2rayN。整套也做成了 AI Skill，交给 AI 后你只要登录、确认域名、选地区、扫码。
教程和 Skill：https://github.com/yunc20/cf-global-edge-node-skill
感谢 free-dam-man、cmliu、yonggekkk、XIU2
