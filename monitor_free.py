"""
客户情报监控系统 - 完全免费版
无需天眼查API，使用RSS+免费数据源
"""
import os
import json
import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict


class FreeCustomerMonitor:
    """
    完全免费的客户监控方案
    """
    
    def __init__(self):
        # 企业微信Webhook（从环境变量读取）
        self.wechat_webhook = os.getenv("WECHAT_WEBHOOK", "")
        
        # 监控的客户
        self.companies = [
            {"name": "中国银行", "keywords": ["中国银行", "中行", "Bank of China"]},
            {"name": "人保集团", "keywords": ["人保集团", "中国人保", "PICC Group"]},
            {"name": "人保财险", "keywords": ["人保财险", "中国财险", "PICC"]},
            {"name": "国联民生", "keywords": ["国联民生", "国联证券"]},
            {"name": "浙江农商", "keywords": ["浙江农商", "浙江农信", "浙江农村商业"]},
            {"name": "中信国际", "keywords": ["中信国际", "信银国际", "中信银行国际"]},
            {"name": "四川银行", "keywords": ["四川银行", "Sichuan Bank"]},
            {"name": "中盾安信", "keywords": ["中盾安信"]},
        ]
        
        # RSS数据源
        self.rss_sources = {
            "36氪": "https://rsshub.app/36kr/news",
            "雷锋网": "https://rsshub.app/leiphone",
            "华尔街见闻": "https://rsshub.app/wallstreetcn/news/global",
        }
    
    def fetch_rss_news(self) -> List[Dict]:
        """
        从RSS源获取新闻
        """
        results = []
        
        for source_name, url in self.rss_sources.items():
            try:
                print(f"正在获取 {source_name}...")
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:30]:  # 最近30条
                    title = entry.get("title", "")
                    summary = entry.get("summary", "")
                    
                    # 检查是否包含客户关键词
                    for company in self.companies:
                        for keyword in company["keywords"]:
                            if keyword in title or keyword in summary:
                                results.append({
                                    "company": company["name"],
                                    "title": title,
                                    "summary": summary[:150] + "..." if len(summary) > 150 else summary,
                                    "source": source_name,
                                    "url": entry.get("link", ""),
                                    "time": entry.get("published", ""),
                                })
                                break  # 匹配到一个关键词就跳出
                
                # 避免请求过快
                import time
                time.sleep(1)
                
            except Exception as e:
                print(f"获取 {source_name} 失败: {e}")
        
        return results
    
    def send_wechat(self, title: str, content: str) -> bool:
        """
        推送到企业微信
        """
        if not self.wechat_webhook:
            print("⚠️ 未配置企业微信Webhook，跳过推送")
            print(f"消息内容:\n{title}\n{content}")
            return False
        
        try:
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "content": f"## {title}\n\n{content}"
                }
            }
            response = requests.post(self.wechat_webhook, json=data, timeout=10)
            result = response.json()
            
            if result.get("errcode") == 0:
                print("✅ 推送成功")
                return True
            else:
                print(f"❌ 推送失败: {result.get('errmsg')}")
                return False
                
        except Exception as e:
            print(f"❌ 推送异常: {e}")
            return False
    
    def generate_report(self, news_list: List[Dict]) -> str:
        """
        生成报告
        """
        if not news_list:
            return "今日暂无客户相关新闻"
        
        # 按公司分组
        company_news = {}
        for news in news_list:
            company = news["company"]
            if company not in company_news:
                company_news[company] = []
            company_news[company].append(news)
        
        # 生成Markdown
        content = f"""💡 共监控到 **{len(news_list)}** 条客户相关新闻

---

"""
        
        for company, news_items in company_news.items():
            content += f"### 🏦 {company}\n\n"
            for news in news_items[:3]:  # 每家公司最多3条
                content += f"**{news['title']}**\n"
                content += f"> {news['summary']}\n"
                content += f"> 📎 [{news['source']}]({news['url']})\n\n"
        
        content += """
---
📎 数据来源：RSS新闻监控
"""
        return content
    
    def run(self):
        """
        执行监控
        """
        today = datetime.now().strftime("%Y年%m月%d日")
        print(f"\n{'='*60}")
        print(f"客户情报监控- {today}")
        print(f"{'='*60}\n")
        
        # 获取新闻
        print("正在获取新闻...")
        news = self.fetch_rss_news()
        print(f"✅ 找到 {len(news)} 条相关新闻\n")
        
        # 生成报告
        report = self.generate_report(news)
        
        # 推送
        self.send_wechat(f"📰 客户新闻日报 - {today}", report)
        
        # 保存到本地（可选）
        self.save_to_file(news)
        
        print(f"\n{'='*60}")
        print("监控完成")
        print(f"{'='*60}\n")
    
    def save_to_file(self, news_list: List[Dict]):
        """
        保存到本地文件
        """
        today = datetime.now().strftime("%Y%m%d")
        filename = f"news_{today}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        
        print(f"💾 已保存到 {filename}")


def main():
    """
    主函数
    """
    monitor = FreeCustomerMonitor()
    monitor.run()


if __name__ == "__main__":
    main()
