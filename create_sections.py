"""Create index.md landing pages for all section folders"""
import os

DOCS = r"C:\Users\Henry\Documents\Github\tenniskb\docs"

templates = {
    ('en', 'foundation', 'basics'): ('Foundation Basics', 'Core techniques and quick-reference guides for tennis fundamentals.', 'foundational'),
    ('en', 'foundation', 'deep-dives'): ('Foundation Deep Dives', 'Detailed technique analysis and neural control explanations.', 'foundational'),
    ('en', 'advanced', 'basics'): ('Advanced Basics', 'Tactical concepts and pattern recognition fundamentals.', 'advanced'),
    ('en', 'advanced', 'deep-dives'): ('Advanced Deep Dives', 'Mental game, embodied cognition, and the science behind feel.', 'advanced'),
    ('en', 'elite', 'basics'): ('Elite Basics', 'Core concepts of constraint-led learning and embodied tennis.', 'elite-level'),
    ('en', 'elite', 'deep-dives'): ('Elite Deep Dives', 'Manifesto, philosophy, and the full constraint-led framework.', 'elite-level'),
    ('vi', 'foundation', 'basics'): ('Cơ Bản Nền Tảng', 'Kỹ thuật cốt lõi và hướng dẫn tham khảo nhanh cho các nguyên tắc quần vợt.', 'nền tảng'),
    ('vi', 'foundation', 'deep-dives'): ('Chuyên Sâu Nền Tảng', 'Phân tích kỹ thuật chi tiết và giải thích điều khiển thần kinh.', 'nền tảng'),
    ('vi', 'advanced', 'basics'): ('Cơ Bản Nâng Cao', 'Khái niệm chiến thuật và nguyên tắc nhận diện mẫu hình.', 'nâng cao'),
    ('vi', 'advanced', 'deep-dives'): ('Chuyên Sâu Nâng Cao', 'Tâm lý thi đấu, nhận thức thể hiện, và khoa học đằng sau cảm giác.', 'nâng cao'),
    ('vi', 'elite', 'basics'): ('Cơ Bản Cao Cấp', 'Khái niệm cốt lõi của học tập theo ràng buộc và quần vợt thể hiện.', 'cao cấp'),
    ('vi', 'elite', 'deep-dives'): ('Chuyên Sâu Cao Cấp', 'Tuyên ngôn, triết lý, và khung ràng buộc đầy đủ.', 'cao cấp'),
}

count = 0
for (lang, tier, section), (title, desc, tier_adj) in templates.items():
    folder = os.path.join(DOCS, lang, tier, section)
    if not os.path.exists(folder):
        continue
    
    # Get list of subfolders
    subfolders = sorted([d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))])
    
    # Build content list
    if lang == 'en':
        intro = f"This section contains {tier_adj} tennis content focused on {section.replace('-', ' ')}."
        link_text = "Back to"
        back_tier = f"../index.html"
        back_lang = f"../../index.html" if lang == 'en' else f"../../../en/index.html"
        back_home = f"../../index.html"
    else:
        intro = f"Phần này chứa nội dung quần vợt {tier_adj} tập trung vào {section.replace('-', ' ')}."
        link_text = "Quay Lại"
        back_tier = f"../index.html"
        back_lang = f"../../index.html" if lang == 'vi' else f"../../../vi/index.html"
        back_home = f"../../../index.html"
    
    content = f"""---
title: {title}
description: {desc}
---

# {title}

{intro}

## Topics in This Section

<ul>
"""
    
    for sf in subfolders[:30]:  # Limit to 30
        clean_name = sf.replace('-', ' ').replace('_', ' ').title()
        content += f'<li><a href="{sf}/index.html">{clean_name}</a></li>\n'
    
    if len(subfolders) > 30:
        content += f'<li><em>... and {len(subfolders) - 30} more topics</em></li>\n'
    
    content += f"""</ul>

[{link_text} {tier.title()}](../index.html) | [{link_text} {'English' if lang == 'en' else 'Vietnamese'} Home]({back_lang}) | [Home]({back_home})
"""
    
    with open(os.path.join(folder, 'index.md'), 'w', encoding='utf-8') as f:
        f.write(content)
    count += 1
    print(f"Created {lang}/{tier}/{section}/index.md ({len(subfolders)} topics)")

print(f"\nTotal: {count} index pages created")