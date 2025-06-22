import json
import requests
import os
import sys
from datetime import datetime

HTTP_OK = list(range(200, 300))

def today_in_history(lang="zh-CN"):
    """获取今日历史事件（原main.py的功能）"""
    now = datetime.now()
    month = "%02d" % now.month
    day = "%02d" % now.day

    url = f"https://baike.baidu.com/cms/home/eventsOnHistory/{month}.json"
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/\
537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    headers = {
        "host": "baike.baidu.com",
        "referer": "https://www.baidu.com",
        "User-Agent": agent,
        "Accept-Language": lang,
        "Accept": "text/html",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows"
    }

    response = requests.get(url=url, headers=headers)

    if response.status_code not in HTTP_OK:
        raise KeyError(f"远程服务器返回错误:{response.status_code}")

    meta = json.loads(response.content.decode("utf-8"))
    return meta[f"{month}"][f"{month}{day}"]

def process_event(event):
    """处理单个事件数据"""
    # 从标题中移除HTML标签
    title = event['title'].split('>')[-1].split('<')[0] if '<' in event['title'] else event['title']
    
    # 翻译事件类型
    type_map = {"birth": "出生", "death": "逝世", "event": "事件"}
    event_type = type_map.get(event['type'], event['type'])
    
    return f"""
<local:MyCard Title="事件：【{title}】时间：【{event['year']}年】类型【{event_type}】" Margin="0,0,0,15" CanSwap="True" IsSwaped="True">
    <StackPanel Margin="25,40,23,15">
        <local:MyListItem Margin="30,2,-5,8"
                    Logo="https://main.cn-nb1.rains3.com/baidu.jpg" 
                    Title="历史详情" 
                    Info="打开百度百科"
                    EventType="打开网页" 
                    EventData="{event['link']}" 
                    Type="Clickable" />
    </StackPanel>
</local:MyCard>"""

def process_files():
    """处理文件生成"""
    try:
        print("正在获取今日历史事件...")
        events = today_in_history()
        
        if not events or len(events) == 0:
            raise ValueError("未获取到历史事件数据")
        
        # 读取模板文件
        if not os.path.exists('temp.xaml'):
            raise FileNotFoundError("temp.xaml文件不存在")
        
        with open('temp.xaml', 'r', encoding='utf-8') as f:
            temp_content = f.read().strip()
        
        # 生成新内容（最多5个事件）
        new_content = "\n".join([process_event(event) for event in events[:5]])
        
        # 合并内容
        final_content = f"{temp_content}\n{new_content}"
        
        # 写入输出文件
        with open('Custom.xaml', 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print(f"✓ 成功生成Custom.xaml，添加了{min(len(events), 5)}个事件")
        return True
    
    except Exception as e:
        print(f"处理失败: {str(e)}")
        return False

if __name__ == '__main__':
    print("\n" + "="*50)
    print(f"开始生成Custom.xaml - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    success = process_files()
    
    print("\n" + "="*50)
    print("任务完成!" if success else "任务失败!")
    print("="*50)
    
    sys.exit(0 if success else 1)
