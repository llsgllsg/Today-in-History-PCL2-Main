import requests
import json
import os
import sys
from datetime import datetime

# 从 Todayinhistory 仓库中引入 today_in_history 函数
def today_in_history(lang="zh-CN"):
    now = datetime.now()
    month = "%02d" % now.month
    day = "%02d" % now.day

    url = f"https://baike.baidu.com/cms/home/eventsOnHistory/{month}.json"
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
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
    HTTP_OK = list(range(200, 300))
    if response.status_code not in HTTP_OK:
        raise KeyError(f"{'远程服务器返回错误' if lang == 'zh-CN' else 'Remote server returned an error'}:{response.status_code}")

    meta = json.loads(response.content.decode("utf-8"))
    return meta[f"{month}"][f"{month}{day}"]

def get_today_events():
    """从API获取今日历史事件"""
    try:
        return today_in_history()
    except Exception as e:
        print(f"获取API数据失败: {str(e)}")
        return None

def translate_event_type(event_type):
    """翻译事件类型"""
    type_map = {
        "birth": "出生",
        "death": "逝世",
        "event": "事件"
    }
    return type_map.get(event_type, event_type)

def generate_xaml_content(api_data):
    """生成要追加的XAML内容"""
    xaml_entries = []
    for event in api_data[:5]:  # 只取前5个事件
        event_type = translate_event_type(event['type'])
        xaml_entry = f"""
<local:MyCard Title="事件：【{event['title']}】时间：【{event['year']}年】类型【{event_type}】" Margin="0,0,0,15" CanSwap="True" IsSwaped="True">
    <StackPanel Margin="25,40,23,15">
        <local:MyListItem Margin="30,2,-5,8"
                    Logo="https://main.cn-nb1.rains3.com/baidu.jpg" Title="历史详情" Info="打开百度百科"
                    EventType="打开网页" EventData="{event['link']}" Type="Clickable" />
    </StackPanel>
</local:MyCard>"""
        xaml_entries.append(xaml_entry)
    return "\n".join(xaml_entries)

def process_files():
    """处理文件生成"""
    try:
        # 1. 从API获取数据
        print("正在从API获取今日历史事件...")
        api_data = get_today_events()
        if not api_data:
            raise ValueError("获取API数据失败或数据格式不正确")
        
        # 2. 读取temp.xaml内容
        if not os.path.exists('temp.xaml'):
            raise FileNotFoundError("temp.xaml文件不存在")
        
        with open('temp.xaml', 'r', encoding='utf-8') as f:
            temp_content = f.read().strip()  # 去除首尾空白
        
        # 3. 生成要追加的内容
        new_content = generate_xaml_content(api_data)
        
        # 4. 直接追加新内容（不再处理结束标签）
        final_content = f"{temp_content}\n{new_content}"
        
        # 5. 写入Custom.xaml
        with open('Custom.xaml', 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print("✓ Custom.xaml生成成功")
        return True
    
    except Exception as e:
        print(f"处理文件失败: {str(e)}")
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
