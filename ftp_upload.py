import ftplib
import os
import sys
from datetime import datetime

def upload_to_ftp():
    try:
        # 获取环境变量
        FTP_HOST = os.getenv('FTP_HOST', 'cn-nb1.rains3.com')
        FTP_PORT = int(os.getenv('FTP_PORT', 8021))
        FTP_USER = os.getenv('FTP_USER', 'oDvjrdGc8bSdN5sf')
        FTP_PASS = os.getenv('FTP_PASS')
        LOCAL_FILE = "Custom.xaml"
        
        if not FTP_PASS:
            print("错误: FTP密码未设置")
            return False

        # 检查本地文件是否存在
        if not os.path.isfile(LOCAL_FILE):
            print(f"错误: 未找到文件 {LOCAL_FILE}")
            return False
            
        # 添加时间戳日志
        print(f"开始上传任务: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"服务器: {FTP_HOST}:{FTP_PORT}")
        print(f"用户名: {FTP_USER}")
        
        # 连接FTP服务器
        print("正在连接FTP服务器...")
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)
        print("✓ 登录成功")
        
        # 设置二进制模式
        ftp.voidcmd("TYPE I")
        
        # 上传文件
        print(f"上传文件: {LOCAL_FILE}...")
        with open(LOCAL_FILE, 'rb') as f:
            ftp.storbinary(f"STOR {LOCAL_FILE}", f)
        
        # 验证文件大小
        local_size = os.path.getsize(LOCAL_FILE)
        remote_size = ftp.size(LOCAL_FILE)
        
        if local_size == remote_size:
            print(f"✓ 上传成功! 文件大小: {local_size} 字节")
        else:
            print(f"⚠ 警告: 文件大小不一致 (本地: {local_size}, 远程: {remote_size})")
        
        # 关闭连接
        ftp.quit()
        return True
        
    except Exception as e:
        print(f"上传失败: {str(e)}")
        return False

if __name__ == "__main__":
    result = upload_to_ftp()
    sys.exit(0 if result else 1)
