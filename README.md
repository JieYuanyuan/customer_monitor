# customer_monitor
# 免费客户情报监控 - 快速开始

5分钟搭建，完全免费！

---

## 🚀 最快方案：GitHub Actions + RSS（5分钟）

### 步骤1：Fork仓库

1. 创建一个新的GitHub仓库
2. 上传以下文件：
   - `monitor_free.py`
   - `.github/workflows/monitor.yml`

### 步骤2：配置企微Webhook

1. 在企微群中添加机器人
2. 复制Webhook地址
3. 在GitHub仓库设置中添加Secret：
   - 名称：`WECHAT_WEBHOOK`
   - 值：你的Webhook地址

### 步骤3：等待推送

每天9点自动执行，免费推送到企微！

---

## 📱 本地运行方案

### 安装依赖

```bash
pip install feedparser requests
```

### 配置环境变量

```bash
export WECHAT_WEBHOOK="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
```

### 运行

```bash
python monitor_free.py
```

---

## 📊 效果展示

推送效果：

```markdown
## 📰 客户新闻日报 - 2026年04月16日

💡 共监控到 3 条客户相关新闻

---

### 🏦 中国银行

**中国银行推出新一代核心系统**
> 基于云原生架构，采用DevOps研发模式...
> 📎 [36氪](https://36kr.com/...)

### 🏦 四川银行

**四川银行数字化转型加速**
> 计划投资5000万建设金融科技平台...
> 📎 [雷锋网](https://leiphone.com/...)

---
📎 数据来源：RSS新闻监控 | 💰 完全免费
```

---

## 💡 进阶：添加更多数据源

编辑 `monitor_free.py`，添加RSS源：

```python
self.rss_sources = {
    "36氪": "https://rsshub.app/36kr/news",
    "雷锋网": "https://rsshub.app/leiphone",
    "华尔街见闻": "https://rsshub.app/wallstreetcn/news/global",
    # 添加更多...
    "你的RSS": "https://rsshub.app/xxx",
}
```

---

## 🎁 更多免费数据源

| 类型 | 来源 | 网址 |
|------|------|------|
| 科技新闻 | RSSHub | https://rsshub.app/ |
| 财经新闻 | 华尔街见闻 | https://rsshub.app/wallstreetcn |
| 招投标 | 中国政府采购网 | http://www.ccgp.gov.cn/ |
| 工商信息 | 企查查免费版 | https://www.qichacha.com/ |

---

**完全免费，立即开始！** 🎉
