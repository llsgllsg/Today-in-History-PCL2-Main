import requests
import os
from datetime import datetime

API_URL = "https://api.leafone.cn/api/lishi"
XAML_FILE = "Custom.xaml"


def fetch_api_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求 API 时出错: {e}")
        return None


def generate_xaml_entries(data):
    entries = []
    for item in data["data"]["list"][:5]:
        title = item["title"]
        time = item["time"]
        event_type = item["type"]
        desc = item["desc"]
        entry = f'<local:MyCard Title="事件：【{title}】时间：【{time}】类型【{event_type}】" Margin="0,0,0,15" CanSwap="True" IsSwaped="True">\n'
        entry += f'    <StackPanel Margin="25,40,23,15">\n'
        entry += f'        <TextBlock TextWrapping="Wrap" Margin="0,0,0,4"\n'
        entry += f'                    Text="{desc}" />\n'
        entry += f'    </StackPanel>\n'
        entry += f'</local:MyCard>'
        entries.append(entry)
    return entries


def update_xaml_file(entries):
    if os.path.exists(XAML_FILE):
        with open(XAML_FILE, "r", encoding="utf-8") as file:
            content = file.read()
    else:
        content = ""
    new_content = "\n".join(entries)
    # 将新内容添加到原内容之后
    content = content + "\n" + new_content if content else new_content
    with open(XAML_FILE, "w", encoding="utf-8") as file:
        file.write(content)


if __name__ == "__main__":
    api_data = fetch_api_data()
    if api_data:
        xaml_entries = generate_xaml_entries(api_data)
        update_xaml_file(xaml_entries)
        print("XAML 文件已成功更新。")
    
