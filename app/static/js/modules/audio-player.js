// 音频播放器组件

window.AudioPlayer = {
    // 当前播放的音频对象
    currentAudio: null,
    
    // 播放音频
    play: function(audioUrl, options = {}) {
        if (!audioUrl) {
            console.warn('音频URL为空');
            return Promise.reject('音频URL为空');
        }
        
        return new Promise((resolve, reject) => {
            try {
                // 停止当前播放的音频
                this.stop();
                
                // 创建新的音频对象
                this.currentAudio = new Audio(audioUrl);
                
                // 设置音频属性
                this.currentAudio.volume = options.volume || 1.0;
                this.currentAudio.playbackRate = options.speed || 1.0;
                
                // 监听事件
                this.currentAudio.onloadstart = () => {
                    if (options.onLoadStart) options.onLoadStart();
                };
                
                this.currentAudio.oncanplay = () => {
                    if (options.onCanPlay) options.onCanPlay();
                };
                
                this.currentAudio.onplay = () => {
                    if (options.onPlay) options.onPlay();
                };
                
                this.currentAudio.onpause = () => {
                    if (options.onPause) options.onPause();
                };
                
                this.currentAudio.onended = () => {
                    if (options.onEnded) options.onEnded();
                    this.currentAudio = null;
                    resolve();
                };
                
                this.currentAudio.onerror = (error) => {
                    console.error('音频播放失败:', error);
                    if (options.onError) options.onError(error);
                    this.currentAudio = null;
                    reject(error);
                };
                
                // 开始播放
                this.currentAudio.play().catch(error => {
                    console.error('音频播放失败:', error);
                    this.currentAudio = null;
                    reject(error);
                });
                
            } catch (error) {
                console.error('创建音频对象失败:', error);
                reject(error);
            }
        });
    },
    
    // 停止播放
    stop: function() {
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
            this.currentAudio = null;
        }
    },
    
    // 暂停播放
    pause: function() {
        if (this.currentAudio && !this.currentAudio.paused) {
            this.currentAudio.pause();
        }
    },
    
    // 继续播放
    resume: function() {
        if (this.currentAudio && this.currentAudio.paused) {
            return this.currentAudio.play();
        }
    },
    
    // 获取播放状态
    isPlaying: function() {
        return this.currentAudio && !this.currentAudio.paused;
    },
    
    // 设置音量
    setVolume: function(volume) {
        if (this.currentAudio) {
            this.currentAudio.volume = Math.max(0, Math.min(1, volume));
        }
    },
    
    // 设置播放速度
    setSpeed: function(speed) {
        if (this.currentAudio) {
            this.currentAudio.playbackRate = Math.max(0.25, Math.min(4, speed));
        }
    },
    
    // 获取播放进度
    getProgress: function() {
        if (this.currentAudio) {
            return {
                currentTime: this.currentAudio.currentTime,
                duration: this.currentAudio.duration,
                progress: this.currentAudio.duration ? 
                    this.currentAudio.currentTime / this.currentAudio.duration : 0
            };
        }
        return null;
    }
};

// 单词音频播放器
window.WordAudioPlayer = {
    // 播放单词音频
    playWord: function(word, buttonElement) {
        // 显示加载状态
        if (buttonElement) {
            this.setButtonState(buttonElement, 'loading');
        }
        
        // 如果单词有音频URL，直接播放
        if (word.audio_url) {
            return this.playAudio(word.audio_url, buttonElement);
        }
        
        // 如果没有音频，先生成音频
        return this.generateAndPlayAudio(word, buttonElement);
    },
    
    // 播放音频
    playAudio: function(audioUrl, buttonElement) {
        return AudioPlayer.play(audioUrl, {
            onPlay: () => {
                if (buttonElement) {
                    this.setButtonState(buttonElement, 'playing');
                }
            },
            onEnded: () => {
                if (buttonElement) {
                    this.setButtonState(buttonElement, 'ready');
                }
            },
            onError: (error) => {
                if (buttonElement) {
                    this.setButtonState(buttonElement, 'error');
                }
                WordApp.showAlert('音频播放失败', 'error');
            }
        });
    },
    
    // 生成并播放音频
    generateAndPlayAudio: function(word, buttonElement) {
        return ApiClient.post(`/words/${word.id}/audio`)
            .then(response => {
                if (response.success) {
                    // 更新单词的音频URL
                    word.audio_url = response.data.audio_url;
                    
                    // 播放生成的音频
                    return this.playAudio(response.data.audio_url, buttonElement);
                } else {
                    throw new Error(response.error);
                }
            })
            .catch(error => {
                console.error('生成音频失败:', error);
                if (buttonElement) {
                    this.setButtonState(buttonElement, 'error');
                }
                WordApp.showAlert('音频生成失败', 'error');
            });
    },
    
    // 设置按钮状态
    setButtonState: function(button, state) {
        const states = {
            loading: { text: '⏳', disabled: true, title: '加载中...' },
            playing: { text: '🔊', disabled: true, title: '播放中...' },
            ready: { text: '🔊', disabled: false, title: '点击播放' },
            error: { text: '❌', disabled: false, title: '播放失败，点击重试' }
        };
        
        const stateConfig = states[state];
        if (stateConfig) {
            button.textContent = stateConfig.text;
            button.disabled = stateConfig.disabled;
            button.title = stateConfig.title;
            button.className = `btn-icon play-audio ${state}`;
        }
    },
    
    // 批量生成音频
    batchGenerateAudio: function(grade, unit, forceRegenerate = false) {
        const data = { grade, unit, force_regenerate: forceRegenerate };
        
        return ApiClient.post('/words/audio/batch', data)
            .then(response => {
                if (response.success) {
                    const results = response.data;
                    let message = `音频生成完成：成功 ${results.success_count} 个`;
                    
                    if (results.error_count > 0) {
                        message += `，失败 ${results.error_count} 个`;
                    }
                    
                    WordApp.showAlert(message, 'success');
                    return results;
                } else {
                    throw new Error(response.error);
                }
            })
            .catch(error => {
                console.error('批量生成音频失败:', error);
                WordApp.showAlert('批量生成音频失败', 'error');
                throw error;
            });
    },
    
    // 验证音频文件
    validateAudioFiles: function() {
        return ApiClient.get('/words/audio/validate')
            .then(response => {
                if (response.success) {
                    const results = response.data;
                    let message = `音频验证完成：有效 ${results.valid_count} 个`;
                    
                    if (results.invalid_count > 0) {
                        message += `，无效 ${results.invalid_count} 个`;
                    }
                    
                    WordApp.showAlert(message, 'info');
                    return results;
                } else {
                    throw new Error(response.error);
                }
            })
            .catch(error => {
                console.error('音频验证失败:', error);
                WordApp.showAlert('音频验证失败', 'error');
                throw error;
            });
    }
};

// 初始化音频播放器
document.addEventListener('DOMContentLoaded', function() {
    // 为所有播放按钮添加事件监听器
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('play-audio')) {
            e.preventDefault();
            
            const button = e.target;
            const wordId = button.dataset.wordId;
            const audioUrl = button.dataset.audio;
            
            if (audioUrl) {
                // 直接播放音频
                WordAudioPlayer.playAudio(audioUrl, button);
            } else if (wordId) {
                // 生成并播放音频
                const word = { id: wordId };
                WordAudioPlayer.generateAndPlayAudio(word, button);
            }
        }
    });
    
    // 页面卸载时停止音频播放
    window.addEventListener('beforeunload', function() {
        AudioPlayer.stop();
    });
});