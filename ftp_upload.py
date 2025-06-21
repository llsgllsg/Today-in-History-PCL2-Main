from ftplib import FTP
import os
import sys
from datetime import datetime

def upload_to_ftp():
    try:
        # 配置信息
        ftp_server = 'cn-nb1.rains3.com'
        ftp_port = 8021
        ftp_user = 'oDvjrdGc8bSdN5sf'
        ftp_pass = os.getenv('FTP_PASSWORD')
        remote_dir = '/main/'  # 远程目标目录
        filename = 'Custom.xaml'  # 要上传的文件名
        
        # 检查密码是否设置
        if not ftp_pass:
            print("错误: FTP密码未设置")
            return False
            
        # 检查文件是否存在
        if not os.path.isfile(filename):
            print(f"错误: 当前目录下未找到文件 {filename}")
            print(f"当前目录内容: {os.listdir()}")
            return False
            
        # 打印开始信息
        print("\n" + "="*50)
        print(f"FTP文件上传任务启动: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        print(f"服务器: {ftp_server}:{ftp_port}")
        print(f"用户名: {ftp_user}")
        print(f"目标目录: {remote_dir}")
        print(f"本地文件: {filename} ({os.path.getsize(filename)} 字节)")
        
        # 连接到FTP服务器
        print("\n[1/4] 正在连接FTP服务器...")
        ftp = FTP()
        ftp.connect(ftp_server, ftp_port)
        ftp.login(user=ftp_user, passwd=ftp_pass)
        print("✓ 登录成功")
        
        # 切换到远程目录（如果不存在则创建）
        print("\n[2/4] 准备远程目录...")
        try:
            ftp.cwd(remote_dir)
            print(f"✓ 已切换到目录: {remote_dir}")
        except Exception as e:
            print(f"目录不存在，尝试创建: {remote_dir}")
            ftp.mkd(remote_dir)
            ftp.cwd(remote_dir)
            print(f"✓ 已创建并切换到目录: {remote_dir}")
        
        # 上传文件
        print("\n[3/4] 开始上传文件...")
        with open(filename, 'rb') as file:
            ftp.storbinary(f'STOR {filename}', file)
        print(f"✓ 文件上传成功: {remote_dir}{filename}")
        
        # 验证上传
        print("\n[4/4] 验证上传结果...")
        local_size = os.path.getsize(filename)
        try:
            remote_size = ftp.size(filename)
            if local_size == remote_size:
                print(f"✓ 验证成功! 文件大小匹配: {local_size} 字节")
            else:
                print(f"⚠ 警告: 文件大小不一致 (本地: {local_size}, 远程: {remote_size})")
        except Exception as e:
            print(f"⚠ 无法验证远程文件大小: {str(e)}")
        
        # 关闭连接
        ftp.quit()
        print("\n" + "="*50)
        print("✓ 上传任务完成! FTP连接已关闭")
        print("="*50)
        return True
        
    except Exception as e:
        print("\n" + "="*50)
        print(f"上传失败: {str(e)}")
        print("="*50)
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    result = upload_to_ftp()
    sys.exit(0 if result else 1)
