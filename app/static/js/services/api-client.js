// API客户端 - 处理所有HTTP请求

window.ApiClient = {
    baseUrl: '/api',
    
    // 通用请求方法
    request: async function(url, options = {}) {
        const fullUrl = url.startsWith('http') ? url : this.baseUrl + url;
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        };
        
        const finalOptions = { ...defaultOptions, ...options };
        
        // 显示加载状态（如果配置了目标元素）
        if (options.loadingTarget) {
            showLoading(options.loadingTarget, options.loadingOptions);
        }
        
        try {
            const response = await fetch(fullUrl, finalOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const contentType = response.headers.get('content-type');
            let result;
            
            if (contentType && contentType.includes('application/json')) {
                result = await response.json();
            } else {
                result = await response.text();
            }
            
            // 隐藏加载状态
            if (options.loadingTarget) {
                hideLoading(options.loadingTarget);
            }
            
            // 显示成功反馈（如果配置了）
            if (options.successMessage && result.success) {
                showNotification(options.successMessage, 'success');
            }
            
            return result;
            
        } catch (error) {
            console.error('API请求失败:', error);
            
            // 隐藏加载状态
            if (options.loadingTarget) {
                hideLoading(options.loadingTarget);
            }
            
            // 显示错误反馈
            if (options.showErrorNotification !== false) {
                const errorMessage = options.errorMessage || '请求失败，请稍后重试';
                showNotification(errorMessage, 'error');
            }
            
            throw error;
        }
    },
    
    // GET请求
    get: function(url, params = {}) {
        const searchParams = new URLSearchParams(params);
        const fullUrl = searchParams.toString() ? `${url}?${searchParams}` : url;
        
        return this.request(fullUrl, {
            method: 'GET'
        });
    },
    
    // POST请求
    post: function(url, data = {}) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    // PUT请求
    put: function(url, data = {}) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    // DELETE请求
    delete: function(url) {
        return this.request(url, {
            method: 'DELETE'
        });
    },
    
    // 词库相关API
    words: {
        // 获取单词列表
        getList: function(params = {}) {
            return ApiClient.get('/words', params);
        },
        
        // 获取单词详情
        getById: function(wordId) {
            return ApiClient.get(`/words/${wordId}`);
        },
        
        // 获取随机单词
        getRandom: function(params = {}) {
            return ApiClient.get('/words/random', params);
        },
        
        // 搜索单词
        search: function(keyword, grade = null) {
            const params = { keyword };
            if (grade) params.grade = grade;
            return ApiClient.get('/words', params);
        },
        
        // 获取年级列表
        getGrades: function() {
            return ApiClient.get('/words/grades');
        },
        
        // 获取单元列表
        getUnits: function(grade) {
            return ApiClient.get(`/words/units/${grade}`);
        },
        
        // 获取统计信息
        getStatistics: function() {
            return ApiClient.get('/words/statistics');
        },
        
        // 创建单词
        create: function(wordData) {
            return ApiClient.post('/words', wordData);
        },
        
        // 更新单词
        update: function(wordId, wordData) {
            return ApiClient.put(`/words/${wordId}`, wordData);
        },
        
        // 删除单词
        delete: function(wordId) {
            return ApiClient.delete(`/words/${wordId}`);
        },
        
        // 导入单词
        import: function(importData) {
            return ApiClient.post('/words/import', importData);
        },
        
        // 导出单词
        export: function(params = {}) {
            return ApiClient.get('/words/export', params);
        },
        
        // 获取导入模板
        getTemplate: function() {
            return ApiClient.get('/words/template');
        }
    },
    
    // 学习相关API
    study: {
        // 开始学习会话
        startSession: function(userId, grade, unit = null) {
            return ApiClient.post('/study/start', {
                user_id: userId,
                grade: grade,
                unit: unit
            });
        },
        
        // 记录学习进度
        recordProgress: function(userId, wordId, masteryLevel) {
            return ApiClient.post('/study/progress', {
                user_id: userId,
                word_id: wordId,
                mastery_level: masteryLevel
            });
        },
        
        // 获取学习进度
        getProgress: function(userId, grade = null, unit = null) {
            const params = {};
            if (grade) params.grade = grade;
            if (unit) params.unit = unit;
            return ApiClient.get(`/study/progress/${userId}`, params);
        },
        
        // 获取推荐单词
        getRecommended: function(userId, count = 10) {
            return ApiClient.get(`/study/recommended/${userId}`, { count });
        },
        
        // 获取学习统计
        getStatistics: function(userId, days = 7) {
            return ApiClient.get(`/study/statistics/${userId}`, { days });
        },
        
        // 获取掌握程度分布
        getMasteryDistribution: function(userId) {
            return ApiClient.get(`/study/mastery/${userId}`);
        }
    },
    
    // 测验相关API
    test: {
        // 生成测验
        generate: function(userId, testType, grade = null, unit = null, questionCount = 10) {
            return ApiClient.post('/test/generate', {
                user_id: userId,
                test_type: testType,
                grade: grade,
                unit: unit,
                question_count: questionCount
            });
        },
        
        // 提交答案
        submitAnswer: function(testId, questionId, answer) {
            return ApiClient.post('/test/answer', {
                test_id: testId,
                question_id: questionId,
                answer: answer
            });
        },
        
        // 完成测验
        finish: function(testId) {
            return ApiClient.post('/test/finish', {
                test_id: testId
            });
        },
        
        // 获取测验结果
        getResult: function(testId) {
            return ApiClient.get(`/test/result/${testId}`);
        },
        
        // 获取测验历史
        getHistory: function(userId, limit = 10) {
            return ApiClient.get(`/test/history/${userId}`, { limit });
        },
        
        // 获取测验统计
        getStatistics: function(userId) {
            return ApiClient.get(`/test/statistics/${userId}`);
        },
        
        // 重新测验错题
        retryWrongWords: function(userId, originalTestId) {
            return ApiClient.post('/test/retry', {
                user_id: userId,
                original_test_id: originalTestId
            });
        }
    },
    
    // 用户相关API
    users: {
        // 获取用户列表
        getList: function() {
            return ApiClient.get('/users');
        },
        
        // 创建用户
        create: function(username, grade) {
            return ApiClient.post('/users', {
                username: username,
                grade: grade
            });
        },
        
        // 获取用户信息
        getById: function(userId) {
            return ApiClient.get(`/users/${userId}`);
        },
        
        // 更新用户信息
        update: function(userId, userData) {
            return ApiClient.put(`/users/${userId}`, userData);
        },
        
        // 删除用户
        delete: function(userId) {
            return ApiClient.delete(`/users/${userId}`);
        },
        
        // 获取用户仪表板数据
        getDashboard: function(userId) {
            return ApiClient.get(`/users/${userId}/dashboard`);
        }
    }
};