// 工具函数库

window.Helpers = {
    
    // 防抖函数
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func(...args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func(...args);
        };
    },
    
    // 节流函数
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    // 格式化数字
    formatNumber: function(num) {
        if (num === null || num === undefined) return '0';
        return new Intl.NumberFormat('zh-CN').format(num);
    },
    
    // 格式化百分比
    formatPercentage: function(num, decimals = 1) {
        if (num === null || num === undefined) return '0%';
        return num.toFixed(decimals) + '%';
    },
    
    // 格式化日期
    formatDate: function(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return '';
        return date.toLocaleDateString('zh-CN');
    },
    
    // 格式化日期时间
    formatDateTime: function(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return '';
        return date.toLocaleString('zh-CN');
    },
    
    // 格式化相对时间
    formatRelativeTime: function(dateString) {
        if (!dateString) return '';
        
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return '';
        
        const now = new Date();
        const diffMs = now - date;
        const diffSeconds = Math.floor(diffMs / 1000);
        const diffMinutes = Math.floor(diffSeconds / 60);
        const diffHours = Math.floor(diffMinutes / 60);
        const diffDays = Math.floor(diffHours / 24);
        
        if (diffSeconds < 60) {
            return '刚刚';
        } else if (diffMinutes < 60) {
            return `${diffMinutes}分钟前`;
        } else if (diffHours < 24) {
            return `${diffHours}小时前`;
        } else if (diffDays === 1) {
            return '昨天';
        } else if (diffDays < 7) {
            return `${diffDays}天前`;
        } else {
            return this.formatDate(dateString);
        }
    },
    
    // 格式化时长（秒转换为分:秒）
    formatDuration: function(seconds) {
        if (!seconds || seconds < 0) return '00:00';
        
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },
    
    // 转义HTML
    escapeHtml: function(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    },
    
    // 生成UUID
    generateUUID: function() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    },
    
    // 深拷贝对象
    deepClone: function(obj) {
        if (obj === null || typeof obj !== 'object') return obj;
        if (obj instanceof Date) return new Date(obj.getTime());
        if (obj instanceof Array) return obj.map(item => this.deepClone(item));
        if (typeof obj === 'object') {
            const clonedObj = {};
            for (const key in obj) {
                if (obj.hasOwnProperty(key)) {
                    clonedObj[key] = this.deepClone(obj[key]);
                }
            }
            return clonedObj;
        }
    },
    
    // 获取查询参数
    getUrlParams: function() {
        const params = {};
        const searchParams = new URLSearchParams(window.location.search);
        
        for (const [key, value] of searchParams) {
            params[key] = value;
        }
        
        return params;
    },
    
    // 设置查询参数
    setUrlParams: function(params) {
        const url = new URL(window.location);
        
        Object.keys(params).forEach(key => {
            if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
                url.searchParams.set(key, params[key]);
            } else {
                url.searchParams.delete(key);
            }
        });
        
        window.history.replaceState(null, '', url);
    },
    
    // 滚动到元素
    scrollToElement: function(element, offset = 0, duration = 300) {
        const targetElement = typeof element === 'string' ? document.querySelector(element) : element;
        
        if (!targetElement) return;
        
        const targetPosition = targetElement.offsetTop - offset;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        let startTime = null;
        
        function animation(currentTime) {
            if (startTime === null) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const run = ease(timeElapsed, startPosition, distance, duration);
            window.scrollTo(0, run);
            if (timeElapsed < duration) requestAnimationFrame(animation);
        }
        
        function ease(t, b, c, d) {
            t /= d / 2;
            if (t < 1) return c / 2 * t * t + b;
            t--;
            return -c / 2 * (t * (t - 2) - 1) + b;
        }
        
        requestAnimationFrame(animation);
    },
    
    // 本地存储封装
    storage: {
        set: function(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
                return true;
            } catch (e) {
                console.error('本地存储设置失败:', e);
                return false;
            }
        },
        
        get: function(key, defaultValue = null) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : defaultValue;
            } catch (e) {
                console.error('本地存储读取失败:', e);
                return defaultValue;
            }
        },
        
        remove: function(key) {
            try {
                localStorage.removeItem(key);
                return true;
            } catch (e) {
                console.error('本地存储删除失败:', e);
                return false;
            }
        },
        
        clear: function() {
            try {
                localStorage.clear();
                return true;
            } catch (e) {
                console.error('本地存储清除失败:', e);
                return false;
            }
        }
    },
    
    // 验证函数
    validate: {
        // 验证邮箱
        email: function(email) {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return re.test(email);
        },
        
        // 验证手机号
        phone: function(phone) {
            const re = /^1[3-9]\d{9}$/;
            return re.test(phone);
        },
        
        // 验证用户名（2-20个字符，可以是中文、英文、数字）
        username: function(username) {
            const re = /^[\u4e00-\u9fa5a-zA-Z0-9]{2,20}$/;
            return re.test(username);
        },
        
        // 验证年级（3-6）
        grade: function(grade) {
            const num = parseInt(grade);
            return !isNaN(num) && num >= 3 && num <= 6;
        },
        
        // 验证单元（正整数）
        unit: function(unit) {
            const num = parseInt(unit);
            return !isNaN(num) && num > 0;
        },
        
        // 验证掌握程度（1-5）
        masteryLevel: function(level) {
            const num = parseInt(level);
            return !isNaN(num) && num >= 1 && num <= 5;
        }
    },
    
    // 加载状态管理
    loading: {
        show: function(element, text = '加载中...') {
            const target = typeof element === 'string' ? document.querySelector(element) : element;
            if (!target) return;
            
            target.classList.add('loading');
            
            // 创建加载指示器
            const loadingElement = document.createElement('div');
            loadingElement.className = 'loading-indicator';
            loadingElement.innerHTML = `
                <div class="loading-spinner"></div>
                <div class="loading-text">${text}</div>
            `;
            
            target.appendChild(loadingElement);
        },
        
        hide: function(element) {
            const target = typeof element === 'string' ? document.querySelector(element) : element;
            if (!target) return;
            
            target.classList.remove('loading');
            
            const loadingElement = target.querySelector('.loading-indicator');
            if (loadingElement) {
                loadingElement.remove();
            }
        }
    }
};