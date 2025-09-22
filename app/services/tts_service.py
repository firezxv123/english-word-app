#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import hashlib
from gtts import gTTS
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class TTSService:
    """文本转语音服务"""
    
    @staticmethod
    def generate_audio(text, lang='en'):
        """生成音频文件
        
        Args:
            text (str): 要转换的文本
            lang (str): 语言代码，默认为英语
        
        Returns:
            tuple: (音频文件URL, 错误信息)
        """
        try:
            if not text or not text.strip():
                return None, "文本不能为空"
            
            # 生成文件名（基于文本内容的哈希值）
            text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
            filename = f"{text_hash}_{lang}.mp3"
            
            audio_folder = current_app.config.get('AUDIO_FOLDER', 'app/static/audio')
            file_path = os.path.join(audio_folder, filename)
            
            # 检查文件是否已存在
            if os.path.exists(file_path):
                audio_url = f"/static/audio/{filename}"
                return audio_url, None
            
            # 确保音频目录存在
            os.makedirs(audio_folder, exist_ok=True)
            
            # 生成音频文件
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(file_path)
            
            # 返回音频URL
            audio_url = f"/static/audio/{filename}"
            logger.info(f"成功生成音频文件: {filename}")
            
            return audio_url, None
            
        except Exception as e:
            error_msg = f"音频生成失败: {str(e)}"
            logger.error(error_msg)
            return None, error_msg
    
    @staticmethod
    def generate_word_audio(word):
        """为单词生成音频文件
        
        Args:
            word (Word): 单词对象
        
        Returns:
            tuple: (音频文件URL, 错误信息)
        """
        if not word or not word.word:
            return None, "无效的单词对象"
        
        return TTSService.generate_audio(word.word, 'en')
    
    @staticmethod
    def batch_generate_audio(words):
        """批量生成音频文件
        
        Args:
            words (list): 单词对象列表
        
        Returns:
            dict: 生成结果统计
        """
        results = {
            'success_count': 0,
            'error_count': 0,
            'errors': []
        }
        
        for word in words:
            try:
                audio_url, error = TTSService.generate_word_audio(word)
                
                if error:
                    results['error_count'] += 1
                    results['errors'].append(f"单词 '{word.word}': {error}")
                else:
                    # 更新单词的音频URL
                    if audio_url and not word.audio_url:
                        word.audio_url = audio_url
                        results['success_count'] += 1
                
            except Exception as e:
                results['error_count'] += 1
                results['errors'].append(f"单词 '{word.word}': {str(e)}")
        
        return results
    
    @staticmethod
    def delete_audio_file(audio_url):
        """删除音频文件
        
        Args:
            audio_url (str): 音频文件URL
        
        Returns:
            bool: 删除是否成功
        """
        try:
            if not audio_url:
                return True
            
            # 从URL获取文件名
            filename = os.path.basename(audio_url)
            audio_folder = current_app.config.get('AUDIO_FOLDER', 'app/static/audio')
            file_path = os.path.join(audio_folder, filename)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"成功删除音频文件: {filename}")
            
            return True
            
        except Exception as e:
            logger.error(f"删除音频文件失败: {str(e)}")
            return False
    
    @staticmethod
    def get_audio_info(audio_url):
        """获取音频文件信息
        
        Args:
            audio_url (str): 音频文件URL
        
        Returns:
            dict: 音频文件信息
        """
        try:
            if not audio_url:
                return None
            
            filename = os.path.basename(audio_url)
            audio_folder = current_app.config.get('AUDIO_FOLDER', 'app/static/audio')
            file_path = os.path.join(audio_folder, filename)
            
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            
            return {
                'filename': filename,
                'size': stat.st_size,
                'created_time': stat.st_ctime,
                'url': audio_url
            }
            
        except Exception as e:
            logger.error(f"获取音频信息失败: {str(e)}")
            return None