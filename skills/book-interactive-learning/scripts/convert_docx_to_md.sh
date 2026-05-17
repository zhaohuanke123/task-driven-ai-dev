#!/bin/bash

# Word 文档转 Markdown
# 用途：很多课程素材是 Word 文件，AI 读不了，批量转换

set -e

if [ $# -lt 1 ]; then
    echo "用法: $0 <input.docx> [output.md]"
    echo "示例: $0 document.docx"
    echo "示例: $0 document.docx output.md"
    exit 1
fi

INPUT="$1"
OUTPUT="${2:-${INPUT%.docx}.md}"

# 检查输入文件
if [ ! -f "$INPUT" ]; then
    echo "错误: 文件不存在: $INPUT"
    exit 1
fi

# 检查 pandoc 是否安装
if ! command -v pandoc &> /dev/null; then
    echo "错误: 需要安装 pandoc"
    echo "安装: sudo apt install pandoc"
    exit 1
fi

# 转换
echo "转换中: $INPUT -> $OUTPUT"
pandoc "$INPUT" -o "$OUTPUT" --extract-media=./media

echo "完成！"
echo "输出文件: $OUTPUT"
if [ -d "./media" ]; then
    echo "图片目录: ./media/"
fi
