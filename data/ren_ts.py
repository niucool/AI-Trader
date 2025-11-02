import os
import re
import shutil

def rename_timestamp_directories(root_dir='.'):
    """
    递归遍历目录，将形如 '2025-10-01 15:00:00' 的目录重命名为 '2025-10-01_150000'
    
    Args:
        root_dir: 要遍历的根目录，默认为当前目录
    """
    # 匹配形如 '2025-10-01 15:00:00' 的目录名模式
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}):(\d{2})$')
    
    renamed_count = 0
    error_count = 0
    
    print(f"开始遍历目录: {os.path.abspath(root_dir)}")
    print("正在查找时间戳格式的目录...")
    
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for dir_name in dirs:
            match = pattern.match(dir_name)
            if match:
                # 提取日期和时间部分
                date_part = match.group(1)  # 2025-10-01
                hour = match.group(2)       # 15
                minute = match.group(3)     # 00
                second = match.group(4)     # 00
                
                # 构建新目录名：2025-10-01_150000
                new_dir_name = f"{date_part}_{hour}{minute}{second}"
                
                old_path = os.path.join(root, dir_name)
                new_path = os.path.join(root, new_dir_name)
                
                try:
                    # 检查目标路径是否已存在
                    if os.path.exists(new_path):
                        print(f"警告: 目标路径已存在，跳过: {new_path}")
                        error_count += 1
                        continue
                    
                    # 重命名目录
                    shutil.move(old_path, new_path)
                    print(f"重命名: {old_path} -> {new_path}")
                    renamed_count += 1
                    
                except Exception as e:
                    print(f"错误: 无法重命名 {old_path} -> {new_path}: {e}")
                    error_count += 1
    
    print(f"\n操作完成!")
    print(f"成功重命名: {renamed_count} 个目录")
    print(f"错误/跳过: {error_count} 个目录")

def preview_changes(root_dir='.'):
    """
    预览将要进行的更改，不实际执行重命名
    """
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}):(\d{2})$')
    
    print(f"预览模式 - 将要重命名的目录:")
    print("-" * 60)
    
    count = 0
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            match = pattern.match(dir_name)
            if match:
                date_part = match.group(1)
                hour = match.group(2)
                minute = match.group(3)
                second = match.group(4)
                new_dir_name = f"{date_part}_{hour}{minute}{second}"
                
                old_path = os.path.join(root, dir_name)
                new_path = os.path.join(root, new_dir_name)
                
                print(f"{old_path}")
                print(f"  -> {new_path}")
                count += 1
    
    print("-" * 60)
    print(f"总共找到 {count} 个需要重命名的目录")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='重命名时间戳格式的目录')
    parser.add_argument('--preview', action='store_true', 
                       help='预览模式，不实际执行重命名')
    parser.add_argument('--directory', default='.', 
                       help='要处理的目录路径 (默认: 当前目录)')
    
    args = parser.parse_args()
    
    if args.preview:
        preview_changes(args.directory)
        print("\n使用以下命令执行重命名:")
        print(f"python {os.path.basename(__file__)} --directory \"{args.directory}\"")
    else:
        print("警告: 此操作将实际重命名目录!")
        print("建议先使用 --preview 参数预览更改")
        response = input("确定要继续吗? (y/N): ")
        if response.lower() in ['y', 'yes']:
            rename_timestamp_directories(args.directory)
        else:
            print("操作已取消")

