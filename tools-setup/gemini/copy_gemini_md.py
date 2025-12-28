import shutil
from pathlib import Path

# The name of the file to be copied
file_name = "GEMINI.md"

# The directory where this script is located, using pathlib
script_directory = Path(__file__).parent

# The full path to the source file
source_path = script_directory / file_name

# The user's home directory, using pathlib
home_directory = Path.home()

# The destination directory, using pathlib
destination_directory = home_directory / ".gemini"

# The full path to the destination file
destination_path = destination_directory / file_name

# Ensure the destination directory exists, using pathlib.
# This is more concise than the original os.path.exists and os.makedirs.
destination_directory.mkdir(parents=True, exist_ok=True)
print(f"确保目录存在：{destination_directory}")

# Copy the file
if source_path.exists():
    shutil.copy2(source_path, destination_path)
    print(f"成功将 {source_path} 复制到 {destination_path}")
else:
    print(f"错误：源文件 {source_path} 不存在。")
