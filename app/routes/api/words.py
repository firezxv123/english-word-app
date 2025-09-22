from flask import request, jsonify
from app.routes.api import api
from app.services.word_service import WordService
from app.services.data_import import DataImportService
from app.utils.error_handler import ErrorHandler, ValidationError, NotFoundError, Validator
from app.utils.param_helpers import safe_get_int_param

@api.route('/words', methods=['GET'])
@ErrorHandler.handle_api_error
def get_words():
    """获取单词列表"""
    grade = safe_get_int_param(request.args, 'grade')
    unit = safe_get_int_param(request.args, 'unit')
    limit = safe_get_int_param(request.args, 'limit')
    offset = safe_get_int_param(request.args, 'offset')
    keyword = request.args.get('keyword')
    
    # 验证参数
    if grade is not None:
        Validator.validate_grade(grade)
    if unit is not None:
        Validator.validate_unit(unit)
    
    if keyword:
        # 搜索单词
        words = WordService.search_words(keyword, grade)
    else:
        # 获取单词列表
        words = WordService.get_words_by_criteria(grade, unit, limit, offset)
    
    return jsonify({
        'success': True,
        'data': [word.to_dict() for word in words],
        'count': len(words)
    })

@api.route('/words/<int:word_id>', methods=['GET'])
@ErrorHandler.handle_api_error
def get_word(word_id):
    """获取单词详情"""
    word = WordService.get_word_by_id(word_id)
    
    if not word:
        raise NotFoundError('单词不存在')
    
    return jsonify({
        'success': True,
        'data': word.to_dict()
    })

@api.route('/words/random', methods=['GET'])
def get_random_words():
    """获取随机单词"""
    try:
        grade = safe_get_int_param(request.args, 'grade')
        unit = safe_get_int_param(request.args, 'unit')
        count = safe_get_int_param(request.args, 'count', 10)
        
        words = WordService.get_random_words(grade, unit, count)
        
        return jsonify({
            'success': True,
            'data': [word.to_dict() for word in words],
            'count': len(words)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/words/statistics', methods=['GET'])
@ErrorHandler.handle_api_error
def get_word_statistics():
    """获取词库统计信息"""
    # 使用缓存的统计信息
    from app.services.cache_service import WordCacheService
    stats = WordCacheService.get_word_statistics()
    
    return jsonify({
        'success': True,
        'data': stats
    })

@api.route('/words/grades', methods=['GET'])
@ErrorHandler.handle_api_error
def get_grades():
    """获取所有年级"""
    # 使用缓存的年级列表
    from app.services.cache_service import WordCacheService
    grades = WordCacheService.get_all_grades()
    
    return jsonify({
        'success': True,
        'data': grades
    })

@api.route('/words/units/<int:grade>', methods=['GET'])
@ErrorHandler.handle_api_error
def get_units(grade):
    """获取指定年级的所有单元"""
    # 验证年级
    Validator.validate_grade(grade)
    
    # 使用缓存的单元列表
    from app.services.cache_service import WordCacheService
    units = WordCacheService.get_grade_units(grade)
    
    return jsonify({
        'success': True,
        'data': units
    })

@api.route('/words/<int:word_id>/audio', methods=['POST'])
def generate_word_audio(word_id):
    """为单词生成音频"""
    try:
        audio_url, error = WordService.generate_word_audio(word_id)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': {
                'audio_url': audio_url
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/words/audio/batch', methods=['POST'])
def batch_generate_audio():
    """批量生成音频"""
    try:
        data = request.get_json() or {}
        
        grade = safe_get_int_param(request.args, 'grade')
        unit = safe_get_int_param(request.args, 'unit')
        force_regenerate = data.get('force_regenerate', False)
        
        results = WordService.batch_generate_audio(grade, unit, force_regenerate)
        
        return jsonify({
            'success': True,
            'data': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/words/audio/validate', methods=['GET'])
def validate_audio_files():
    """验证音频文件"""
    try:
        results = WordService.validate_audio_files()
        
        return jsonify({
            'success': True,
            'data': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/words/without-audio', methods=['GET'])
def get_words_without_audio():
    """获取没有音频的单词"""
    try:
        grade = safe_get_int_param(request.args, 'grade')
        unit = safe_get_int_param(request.args, 'unit')
        
        words = WordService.get_words_without_audio(grade, unit)
        
        return jsonify({
            'success': True,
            'data': [word.to_dict() for word in words],
            'count': len(words)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
@api.route('/words', methods=['POST'])
@ErrorHandler.handle_api_error
def create_word():
    """创建新单词"""
    data = request.get_json()
    
    if not data:
        raise ValidationError('请提供单词数据')
    
    # 验证数据
    Validator.validate_word_data(data)
    
    # 记录操作日志
    ErrorHandler.log_system_event('word_create', f'创建单词: {data.get("word")}')
    
    word = WordService.create_word(data)
    
    return jsonify({
        'success': True,
        'data': word.to_dict()
    }), 201

@api.route('/words/<int:word_id>', methods=['PUT'])
def update_word(word_id):
    """更新单词信息"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '请提供更新数据'
            }), 400
        
        word = WordService.update_word(word_id, data)
        
        if not word:
            return jsonify({
                'success': False,
                'error': '单词不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'data': word.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/words/<int:word_id>', methods=['DELETE'])
def delete_word(word_id):
    """删除单词"""
    try:
        success = WordService.delete_word(word_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': '单词不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'message': '单词删除成功'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/words/import', methods=['POST'])
def import_words():
    """导入单词数据"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '请提供导入数据'
            }), 400
        
        import_type = data.get('type', 'json').lower()
        content = data.get('content', '')
        
        if import_type == 'csv':
            result = DataImportService.import_from_csv(content)
        elif import_type == 'json':
            result = DataImportService.import_from_json(content)
        else:
            return jsonify({
                'success': False,
                'error': '不支持的导入类型'
            }), 400
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/words/export', methods=['GET'])
def export_words():
    """导出单词数据"""
    try:
        export_type = request.args.get('type', 'json').lower()
        grade = safe_get_int_param(request.args, 'grade')
        unit = safe_get_int_param(request.args, 'unit')
        
        if export_type == 'csv':
            content, error = DataImportService.export_to_csv(grade, unit)
        elif export_type == 'json':
            content, error = DataImportService.export_to_json(grade, unit)
        else:
            return jsonify({
                'success': False,
                'error': '不支持的导出类型'
            }), 400
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': content,
            'type': export_type
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/words/template', methods=['GET'])
def get_import_template():
    """获取导入模板"""
    try:
        template = DataImportService.get_import_template()
        
        return jsonify({
            'success': True,
            'data': template
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500