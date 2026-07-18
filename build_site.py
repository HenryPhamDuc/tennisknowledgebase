"""
Build Tennis KB from Downloads/new-documents source
Copies content to docs/en/{foundation,advanced,elite}/{basics,deep-dives}/
              and docs/vi/{foundation,advanced,elite}/{basics,deep-dives}/
"""
import os
import shutil
import re
from pathlib import Path

SRC = r"C:\Users\Henry\Downloads\Tenniskb\new-documents"
DST_ROOT = r"C:\Users\Henry\Documents\Github\tenniskb\docs"

# Tier classification keywords
FOUNDATION_EN = ['grip', 'forehand', 'backhand', 'footwork', 'continental', 'eastern', 'western', 'slice', 'lob', 'overhead', 'volley', 'serve', 'service', 'groundstroke']
ADVANCED_EN = ['advanced', 'tactic', 'pattern', 'mental', 'pressure', 'decision', 'myelination', 'proprioception', 'fascia', 'reflex', 'embodied', 'fracture', 'doubles']
ELITE_EN = ['manifesto', 'constraint', 'x-factor', 'vestibular', 'hrv', 'choking', 'amygdala', 'dream', 'self-coaching', 'kinh', 'mushin', 'tensegrity', 'hidden speed', 'trường lực', 'trương lực']

FOUNDATION_VI = ['tay cầm', 'forehand', 'backhand', 'di chuyển', 'footwork', 'cắt', 'bổng', 'smash', 'vợt', 'giao bóng', 'cú đánh']
ADVANCED_VI = ['nâng cao', 'chiến thuật', 'mẫu hình', 'tâm lý', 'áp lực', 'quyết định', 'myelination', 'proprioception', 'fascia', 'phản xạ', 'đôi']
ELITE_VI = ['tuyên ngôn', 'ràng buộc', 'yếu tố x', 'tiền đình', 'hrv', 'nghẹt thở', 'amygdala', 'giấc mơ', 'tự huấn luyện', 'kinh', 'mushin', 'căng bằng', 'tốc độ ẩn', 'trường lực']

AI_SLOP_EN = [
    'Key Takeaways', 'In conclusion', "Let's dive", 'As we can see', "It's important to note",
    'In summary', 'To summarize', 'In short', 'Bottom line', 'Takeaway', 'Main point',
    'The main idea', 'The point is', 'What this means is', 'This shows that', 'This demonstrates',
    'This illustrates', 'This highlights', 'This emphasizes', 'This underscores',
    'Game-changer', 'Next level', 'Elevate your game', 'Level up', 'Step up your game',
    'Take it to the next level', 'See you on the court', 'engineer', 'kỹ sư',
    'Sources:', 'Nguồn:', '🎾', '🏆', '💪', '🔥', '🇬🇧', '🇻🇳', '⚡', '🎉', '👍', '👏',
    '🙌', '✨', '💡', '📋', '🎯', '🔑', '⭐', '❌', '✅', '📌', '📊', '📈', '📉', '🎪', '🎨', '🎸'
]

AI_SLOP_VI = [
    'Kết luận', 'Tóm lại', 'Quan trọng là', 'Điều này cho thấy', 'Điều này minh họa',
    'Điểm mấu chốt', 'Bài học chính', 'Những điểm chính', 'Tạm kết', 'Lời kết',
    'Hẹn gặp trên sân', '🎾', '🏆', '💪', '🔥', '🇬🇧', '🇻🇳', '⚡', '🎉', '👍', '👏',
    '🙌', '✨', '💡', '📋', '🎯', '🔑', '⭐', '❌', '✅', '📌', '📊', '📈', '📉', '🎪', '🎨', '🎸'
]

def classify_tier_en(folder_name, filename):
    """Classify EN file into tier"""
    combined = f"{folder_name} {filename}".lower()
    if any(k in combined for k in ELITE_EN):
        return 'elite'
    if any(k in combined for k in ADVANCED_EN):
        return 'advanced'
    return 'foundation'

def classify_tier_vi(folder_name, filename):
    """Classify VI file into tier"""
    combined = f"{folder_name} {filename}".lower()
    if any(k in combined for k in ELITE_VI):
        return 'elite'
    if any(k in combined for k in ADVANCED_VI):
        return 'advanced'
    return 'foundation'

def determine_section(folder_name, filename):
    """Determine if basics or deep-dives"""
    combined = f"{folder_name} {filename}".lower()
    deep_dive_keywords = ['deep dive', 'deep-dive', 'deep_dive', 'manifesto', 'constraint', 'x-factor', 
                          'embodied', 'proprioception', 'fascia', 'myelination', 'tensegrity', 'trương lực']
    if any(k in combined for k in deep_dive_keywords):
        return 'deep-dives'
    return 'basics'

def remove_ai_slop(content, is_vi=False):
    """Remove AI slop patterns from content"""
    patterns = AI_SLOP_VI if is_vi else AI_SLOP_EN
    for pattern in patterns:
        # Remove as whole words/phrases
        content = re.sub(re.escape(pattern), '', content, flags=re.IGNORECASE)
    # Clean up multiple spaces/lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'  +', ' ', content)
    return content.strip()

def copy_file(src, dst, lang='en'):
    """Copy file and remove AI slop"""
    try:
        with open(src, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove AI slop
        content = remove_ai_slop(content, is_vi=(lang=='vi'))
        
        # Write to destination
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"ERROR copying {src}: {e}")
        return False

# Walk source and copy files
en_count = 0
vi_count = 0
errors = []

print("Processing files...")
print("=" * 80)

for root, dirs, files in os.walk(SRC):
    rel_path = os.path.relpath(root, SRC).replace('\\', '/')
    
    # Determine language
    lang = None
    parts = rel_path.lower().split('/')
    if 'vietnamese' in parts or ('vi' in parts and 'en' not in parts):
        lang = 'vi'
    elif 'en' in parts:
        lang = 'en'
    else:
        # Check folder structure
        if 'vi/' in rel_path.lower() or '/vi' in rel_path.lower():
            lang = 'vi'
        elif 'en/' in rel_path.lower() or '/en' in rel_path.lower():
            lang = 'en'
    
    if not lang or not files:
        continue
    
    for f in files:
        if not f.endswith('.md'):
            continue
        
        src_file = os.path.join(root, f)
        
        # Determine tier and section
        if lang == 'en':
            tier = classify_tier_en(rel_path, f)
        else:
            tier = classify_tier_vi(rel_path, f)
        
        section = determine_section(rel_path, f)
        
        # Create destination path
        dst_dir = os.path.join(DST_ROOT, lang, tier, section, f.replace('.md', '').replace('/', '-'))
        dst_file = os.path.join(dst_dir, 'index.md')
        
        # Copy and process
        if copy_file(src_file, dst_file, lang):
            if lang == 'en':
                en_count += 1
            else:
                vi_count += 1

print(f"\nCopy complete!")
print(f"  EN files: {en_count}")
print(f"  VI files: {vi_count}")
print(f"  Total: {en_count + vi_count}")
if errors:
    print(f"\nErrors: {len(errors)}")
    for e in errors[:10]:
        print(f"  - {e}")