import os
from docx import Document
from datetime import datetime

source_dir = r"I:\我的记录\记录=大学期间-2022年工作前--文档\2021年末到2022年初的思维的文字记录"
target_dir = r"D:\个人记录\obsidian-file\wjmber\《记录》\《2024记录》\回忆记录\2021-2022思维记录_导入"

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

def convert_docx_to_md(docx_path, md_path):
    try:
        doc = Document(docx_path)
        md_content = []
        
        # Add YAML frontmatter
        md_content.append("---")
        md_content.append(f'original_source: "{docx_path}"')
        md_content.append(f"converted_at: {datetime.now().strftime('%Y-%m-%d')}")
        md_content.append("tags: [回忆, 2021-2022, 大学期间]")
        md_content.append("---\n")
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                md_content.append("")
                continue
                
            # Handle basic heading styles
            if para.style.name.startswith('Heading'):
                level = para.style.name.split()[-1]
                if level.isdigit():
                    md_content.append(f"{'#' * int(level)} {text}")
                else:
                    md_content.append(f"# {text}")
            else:
                md_content.append(text)
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))
        return True
    except Exception as e:
        print(f"Error converting {docx_path}: {e}")
        return False

files = [f for f in os.listdir(source_dir) if f.endswith('.docx') or f.endswith('.doc')]

converted_count = 0
for file in files:
    if file.startswith('~$'): # Skip temp files
        continue
    source_path = os.path.join(source_dir, file)
    md_filename = os.path.splitext(file)[0] + ".md"
    target_path = os.path.join(target_dir, md_filename)
    
    if convert_docx_to_md(source_path, target_path):
        print(f"Converted: {file} -> {md_filename}")
        converted_count += 1

print(f"\nSuccessfully converted {converted_count} files.")
