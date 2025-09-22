import csv
import json
from io import StringIO
from app.services.word_service import WordService
from app.models.word import Word
from app import db

class DataImportService:
    """数据导入服务类"""
    
    @staticmethod
    def import_from_csv(csv_content, encoding='utf-8'):
        """从CSV内容导入词库数据"""
        try:
            # 读取CSV数据
            csv_reader = csv.DictReader(StringIO(csv_content))
            
            imported_words = []
            errors = []
            
            for row_num, row in enumerate(csv_reader, start=2):  # 从第2行开始（第1行是标题）
                try:
                    word_data = DataImportService._validate_word_data(row)
                    
                    # 检查单词是否已存在
                    existing_word = Word.query.filter_by(
                        word=word_data['word'],
                        grade=word_data['grade'],
                        unit=word_data['unit']
                    ).first()
                    
                    if existing_word:
                        # 更新现有单词
                        updated_word = WordService.update_word(existing_word.id, word_data)
                        if updated_word:
                            imported_words.append(updated_word)
                    else:
                        # 创建新单词
                        new_word = WordService.create_word(word_data)
                        imported_words.append(new_word)
                        
                except Exception as e:
                    errors.append(f"第{row_num}行: {str(e)}")
            
            return {
                'success': True,
                'imported_count': len(imported_words),
                'errors': errors,
                'words': [w.to_dict() for w in imported_words]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"CSV解析错误: {str(e)}",
                'imported_count': 0,
                'errors': [],
                'words': []
            }
    
    @staticmethod
    def import_from_json(json_content):
        """从JSON内容导入词库数据"""
        try:
            # 解析JSON数据
            if isinstance(json_content, str):
                data = json.loads(json_content)
            else:
                data = json_content
            
            if not isinstance(data, list):
                return {
                    'success': False,
                    'error': 'JSON数据必须是数组格式',
                    'imported_count': 0,
                    'errors': [],
                    'words': []
                }
            
            imported_words = []
            errors = []
            
            for index, word_data in enumerate(data):
                try:
                    validated_data = DataImportService._validate_word_data(word_data)
                    
                    # 检查单词是否已存在
                    existing_word = Word.query.filter_by(
                        word=validated_data['word'],
                        grade=validated_data['grade'],
                        unit=validated_data['unit']
                    ).first()
                    
                    if existing_word:
                        # 更新现有单词
                        updated_word = WordService.update_word(existing_word.id, validated_data)
                        if updated_word:
                            imported_words.append(updated_word)
                    else:
                        # 创建新单词
                        new_word = WordService.create_word(validated_data)
                        imported_words.append(new_word)
                        
                except Exception as e:
                    errors.append(f"索引{index}: {str(e)}")
            
            return {
                'success': True,
                'imported_count': len(imported_words),
                'errors': errors,
                'words': [w.to_dict() for w in imported_words]
            }
            
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f"JSON解析错误: {str(e)}",
                'imported_count': 0,
                'errors': [],
                'words': []
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"导入错误: {str(e)}",
                'imported_count': 0,
                'errors': [],
                'words': []
            }
    
    @staticmethod
    def _validate_word_data(data):
        """验证和清洗单词数据"""
        # 必需字段
        required_fields = ['word', 'chinese_meaning', 'grade', 'unit']
        
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"缺少必需字段: {field}")
        
        # 验证数据类型和格式
        word = str(data['word']).strip()
        if not word:
            raise ValueError("单词不能为空")
        
        chinese_meaning = str(data['chinese_meaning']).strip()
        if not chinese_meaning:
            raise ValueError("中文含义不能为空")
        
        try:
            grade = int(data['grade'])
            if grade < 3 or grade > 6:
                raise ValueError("年级必须在3-6之间")
        except (ValueError, TypeError):
            raise ValueError("年级必须是有效的数字")
        
        try:
            unit = int(data['unit'])
            if unit < 1:
                raise ValueError("单元必须是正整数")
        except (ValueError, TypeError):
            raise ValueError("单元必须是有效的数字")
        
        # 可选字段
        phonetic = str(data.get('phonetic', '')).strip()
        phonics_breakdown = str(data.get('phonics_breakdown', '')).strip()
        memory_method = str(data.get('memory_method', '')).strip()
        book_version = str(data.get('book_version', 'PEP')).strip()
        audio_url = str(data.get('audio_url', '')).strip()
        
        return {
            'word': word,
            'chinese_meaning': chinese_meaning,
            'phonetic': phonetic,
            'phonics_breakdown': phonics_breakdown,
            'memory_method': memory_method,
            'grade': grade,
            'unit': unit,
            'book_version': book_version,
            'audio_url': audio_url
        }
    
    @staticmethod
    def export_to_csv(grade=None, unit=None):
        """导出词库数据为CSV格式"""
        words = WordService.get_words_by_criteria(grade=grade, unit=unit)
        
        if not words:
            return None, "没有数据可导出"
        
        # 生成CSV内容
        output = StringIO()
        fieldnames = [
            'word', 'chinese_meaning', 'phonetic', 'phonics_breakdown',
            'memory_method', 'grade', 'unit', 'book_version', 'audio_url'
        ]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for word in words:
            writer.writerow({
                'word': word.word,
                'chinese_meaning': word.chinese_meaning,
                'phonetic': word.phonetic or '',
                'phonics_breakdown': word.phonics_breakdown or '',
                'memory_method': word.memory_method or '',
                'grade': word.grade,
                'unit': word.unit,
                'book_version': word.book_version,
                'audio_url': word.audio_url or ''
            })
        
        csv_content = output.getvalue()
        output.close()
        
        return csv_content, None
    
    @staticmethod
    def export_to_json(grade=None, unit=None):
        """导出词库数据为JSON格式"""
        words = WordService.get_words_by_criteria(grade=grade, unit=unit)
        
        if not words:
            return None, "没有数据可导出"
        
        words_data = [word.to_dict() for word in words]
        
        try:
            json_content = json.dumps(words_data, ensure_ascii=False, indent=2)
            return json_content, None
        except Exception as e:
            return None, f"JSON导出错误: {str(e)}"
    
    @staticmethod
    def get_import_template():
        """获取导入模板"""
        template_data = [
            {
                'word': 'apple',
                'chinese_meaning': '苹果',
                'phonetic': '/ˈæpl/',
                'phonics_breakdown': 'a-pp-le',
                'memory_method': '红红的苹果（apple）挂在树上',
                'grade': 3,
                'unit': 1,
                'book_version': 'PEP',
                'audio_url': ''
            },
            {
                'word': 'banana',
                'chinese_meaning': '香蕉',
                'phonetic': '/bəˈnɑːnə/',
                'phonics_breakdown': 'ba-na-na',
                'memory_method': '弯弯的香蕉（banana）像月亮',
                'grade': 3,
                'unit': 1,
                'book_version': 'PEP',
                'audio_url': ''
            }
        ]
        
        return template_data
    
    @staticmethod
    def validate_import_file(file_content, file_type):
        """验证导入文件格式"""
        if file_type.lower() == 'csv':
            try:
                csv_reader = csv.DictReader(StringIO(file_content))
                first_row = next(csv_reader, None)
                
                if not first_row:
                    return False, "CSV文件为空"
                
                required_columns = ['word', 'chinese_meaning', 'grade', 'unit']
                missing_columns = [col for col in required_columns if col not in first_row]
                
                if missing_columns:
                    return False, f"缺少必需列: {', '.join(missing_columns)}"
                
                return True, "CSV格式验证通过"
                
            except Exception as e:
                return False, f"CSV格式错误: {str(e)}"
        
        elif file_type.lower() == 'json':
            try:
                data = json.loads(file_content)
                
                if not isinstance(data, list):
                    return False, "JSON数据必须是数组格式"
                
                if not data:
                    return False, "JSON数据为空"
                
                # 检查第一个对象的必需字段
                first_item = data[0]
                required_fields = ['word', 'chinese_meaning', 'grade', 'unit']
                missing_fields = [field for field in required_fields if field not in first_item]
                
                if missing_fields:
                    return False, f"缺少必需字段: {', '.join(missing_fields)}"
                
                return True, "JSON格式验证通过"
                
            except json.JSONDecodeError as e:
                return False, f"JSON格式错误: {str(e)}"
            except Exception as e:
                return False, f"文件验证错误: {str(e)}"
        
        else:
            return False, "不支持的文件类型"