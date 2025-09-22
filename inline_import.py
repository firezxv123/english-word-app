import sqlite3
import json
import os

# 创建内联词汇数据
grade3_part1 = [
    {"word": "pen", "chinese_meaning": "钢笔", "grade": 3, "unit": 1},
    {"word": "pencil", "chinese_meaning": "铅笔", "grade": 3, "unit": 1},
    {"word": "pencil-case", "chinese_meaning": "铅笔盒", "grade": 3, "unit": 1},
    {"word": "ruler", "chinese_meaning": "尺子", "grade": 3, "unit": 1},
    {"word": "eraser", "chinese_meaning": "橡皮", "grade": 3, "unit": 1},
    {"word": "crayon", "chinese_meaning": "蜡笔", "grade": 3, "unit": 1},
    {"word": "sharpener", "chinese_meaning": "卷笔刀", "grade": 3, "unit": 1}
]

grade5_words = [
    {"word": "young", "chinese_meaning": "年轻的", "grade": 5, "unit": 1},
    {"word": "funny", "chinese_meaning": "滑稽可笑的", "grade": 5, "unit": 1},
    {"word": "tall", "chinese_meaning": "高的", "grade": 5, "unit": 1},
    {"word": "strong", "chinese_meaning": "强壮的", "grade": 5, "unit": 1},
    {"word": "kind", "chinese_meaning": "和蔼的", "grade": 5, "unit": 1},
    {"word": "old", "chinese_meaning": "年老的", "grade": 5, "unit": 1},
    {"word": "short", "chinese_meaning": "矮的", "grade": 5, "unit": 1},
    {"word": "thin", "chinese_meaning": "瘦的", "grade": 5, "unit": 1},
    {"word": "Mr", "chinese_meaning": "先生", "grade": 5, "unit": 1},
    {"word": "like", "chinese_meaning": "像", "grade": 5, "unit": 1}
]

grade6_words = [
    {"word": "by", "chinese_meaning": "经，乘", "grade": 6, "unit": 1},
    {"word": "foot", "chinese_meaning": "脚", "grade": 6, "unit": 1},
    {"word": "train", "chinese_meaning": "火车", "grade": 6, "unit": 1},
    {"word": "how", "chinese_meaning": "怎样", "grade": 6, "unit": 1},
    {"word": "go to school", "chinese_meaning": "上学", "grade": 6, "unit": 1},
    {"word": "traffic", "chinese_meaning": "交通", "grade": 6, "unit": 1},
    {"word": "traffic light", "chinese_meaning": "交通灯", "grade": 6, "unit": 1},
    {"word": "stop", "chinese_meaning": "停", "grade": 6, "unit": 1},
    {"word": "wait", "chinese_meaning": "等待", "grade": 6, "unit": 1}
]

# 数据库路径
db_path = 'd:/qodercode/data-dev.sqlite'

try:
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("开始导入词汇到数据库...")
    
    # 合并所有词汇数据
    all_words = grade3_part1 + grade5_words + grade6_words
    
    imported_count = 0
    
    for word_data in all_words:
        word = word_data['word']
        chinese_meaning = word_data['chinese_meaning']
        grade = word_data['grade']
        unit = word_data['unit']
        
        # 检查是否已存在
        cursor.execute(
            "SELECT id FROM word WHERE word = ? AND grade = ? AND unit = ?",
            (word, grade, unit)
        )
        
        if not cursor.fetchone():
            # 插入新词汇
            cursor.execute(
                "INSERT INTO word (word, chinese_meaning, grade, unit) VALUES (?, ?, ?, ?)",
                (word, chinese_meaning, grade, unit)
            )
            imported_count += 1
            print(f"添加: {word} -> {chinese_meaning} ({grade}年级第{unit}单元)")
    
    # 提交事务
    conn.commit()
    print(f"成功导入 {imported_count} 个新词汇")
    
    # 统计结果
    print("\n词库统计:")
    cursor.execute("SELECT COUNT(*) FROM word")
    total = cursor.fetchone()[0]
    print(f"总词汇数: {total}")
    
    for grade in [3, 4, 5, 6]:
        cursor.execute("SELECT COUNT(*) FROM word WHERE grade = ?", (grade,))
        count = cursor.fetchone()[0]
        print(f"{grade}年级: {count}个词汇")
    
    conn.close()
    print("数据库操作完成")
    
except Exception as e:
    print(f"导入过程中出错: {e}")
    if conn:
        conn.close()