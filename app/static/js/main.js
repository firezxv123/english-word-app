// 主JavaScript文件 - 应用入口和全局功能

// 应用全局对象
window.WordApp = {
    version: '1.0.0',
    apiBaseUrl: '/api',
    currentUser: null,
    
    // 初始化应用
    init: function() {
        console.log('小学英语单词复习应用 v' + this.version + ' 初始化中...');
        
        // 初始化全局事件监听
        this.initGlobalEvents();
        
        // 初始化用户信息
        this.initUserInfo();
        
        // 初始化页面特定功能
        this.initPageFeatures();
        
        console.log('应用初始化完成');
    },
    
    // 初始化全局事件
    initGlobalEvents: function() {
        // 导航菜单切换
        const navToggle = document.getElementById('navToggle');
        const navMenu = document.getElementById('navMenu');
        
        if (navToggle && navMenu) {
            navToggle.addEventListener('click', function() {
                navMenu.classList.toggle('active');
                navToggle.classList.toggle('active');
            });
            
            // 点击菜单项时关闭移动端菜单
            navMenu.addEventListener('click', function(e) {
                if (e.target.classList.contains('nav-link')) {
                    navMenu.classList.remove('active');
                    navToggle.classList.remove('active');
                }
            });
        }
        
        // 自动隐藏Flash消息
        this.initFlashMessages();
        
        // 窗口大小变化时的处理
        window.addEventListener('resize', this.handleResize.bind(this));
    },
    
    // 初始化Flash消息
    initFlashMessages: function() {
        const alerts = document.querySelectorAll('.alert');
        
        alerts.forEach(function(alert) {
            // 添加关闭按钮事件
            const closeBtn = alert.querySelector('.alert-close');
            if (closeBtn) {
                closeBtn.addEventListener('click', function() {
                    WordApp.closeAlert(alert);
                });
            }
            
            // 自动隐藏
            setTimeout(function() {
                if (alert.parentNode) {
                    WordApp.closeAlert(alert);
                }
            }, 5000);
        });
    },
    
    // 关闭提醒消息
    closeAlert: function(alert) {
        alert.style.opacity = '0';
        alert.style.transform = 'translateX(100%)';
        setTimeout(function() {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 300);
    },
    
    // 显示新的提醒消息
    showAlert: function(message, type = 'info') {
        const alertsContainer = document.querySelector('.flash-messages') || this.createAlertsContainer();
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.innerHTML = `
            <span>${message}</span>
            <button type="button" class="alert-close">×</button>
        `;
        
        alertsContainer.appendChild(alert);
        
        // 添加事件监听
        const closeBtn = alert.querySelector('.alert-close');
        closeBtn.addEventListener('click', function() {
            WordApp.closeAlert(alert);
        });
        
        // 自动隐藏
        setTimeout(function() {
            if (alert.parentNode) {
                WordApp.closeAlert(alert);
            }
        }, 5000);
        
        return alert;
    },
    
    // 创建提醒消息容器
    createAlertsContainer: function() {
        const container = document.createElement('div');
        container.className = 'flash-messages';
        document.body.appendChild(container);
        return container;
    },
    
    // 初始化用户信息
    initUserInfo: function() {
        // 从URL参数或本地存储获取当前用户信息
        const urlParams = new URLSearchParams(window.location.search);
        const userId = urlParams.get('user_id');
        
        if (userId) {
            this.loadUserInfo(userId);
        } else {
            // 尝试从本地存储获取
            const savedUserId = localStorage.getItem('wordapp_user_id');
            if (savedUserId) {
                this.loadUserInfo(savedUserId);
            }
        }
    },
    
    // 加载用户信息
    loadUserInfo: function(userId) {
        ApiClient.get(`/users/${userId}`)
            .then(response => {
                if (response.success) {
                    this.currentUser = response.data;
                    localStorage.setItem('wordapp_user_id', userId);
                    this.updateUserDisplay();
                }
            })
            .catch(error => {
                console.error('加载用户信息失败:', error);
            });
    },
    
    // 更新用户显示
    updateUserDisplay: function() {
        if (!this.currentUser) return;
        
        // 更新导航栏用户信息
        const userInfo = document.querySelector('.user-info');
        if (userInfo) {
            userInfo.textContent = `👤 ${this.currentUser.username} (${this.currentUser.grade}年级)`;
        }
        
        // 触发用户信息更新事件
        document.dispatchEvent(new CustomEvent('userInfoUpdated', {
            detail: { user: this.currentUser }
        }));
    },
    
    // 初始化页面特定功能
    initPageFeatures: function() {
        const body = document.body;
        
        // 根据页面类型初始化不同功能
        if (body.classList.contains('page-index')) {
            this.initIndexPage();
        } else if (body.classList.contains('page-study')) {
            this.initStudyPage();
        } else if (body.classList.contains('page-test')) {
            this.initTestPage();
        }
    },
    
    // 初始化首页
    initIndexPage: function() {
        console.log('初始化首页功能');
        
        // 加载用户统计数据
        if (this.currentUser) {
            this.loadUserStats(this.currentUser.id);
        }
    },
    
    // 初始化学习页面
    initStudyPage: function() {
        console.log('初始化学习页面功能');
    },
    
    // 初始化测验页面
    initTestPage: function() {
        console.log('初始化测验页面功能');
    },
    
    // 加载用户统计
    loadUserStats: function(userId) {
        const statsContainer = document.getElementById('userStatsGrid');
        if (!statsContainer) return;
        
        ApiClient.get(`/users/${userId}/dashboard`)
            .then(response => {
                if (response.success) {
                    this.renderUserStats(response.data, statsContainer);
                }
            })
            .catch(error => {
                console.error('加载用户统计失败:', error);
                this.showAlert('加载统计数据失败', 'error');
            });
    },
    
    // 渲染用户统计
    renderUserStats: function(stats, container) {
        const html = `
            <div class="stat-card">
                <div class="stat-icon">📖</div>
                <div class="stat-content">
                    <div class="stat-number">${stats.study_progress.total_studied}</div>
                    <div class="stat-label">已学习单词</div>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">⭐</div>
                <div class="stat-content">
                    <div class="stat-number">${stats.study_progress.mastered}</div>
                    <div class="stat-label">已掌握单词</div>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-content">
                    <div class="stat-number">${stats.study_progress.mastery_rate}%</div>
                    <div class="stat-label">掌握率</div>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">📝</div>
                <div class="stat-content">
                    <div class="stat-number">${stats.test_statistics.total_tests}</div>
                    <div class="stat-label">测验次数</div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
        
        // 添加动画效果
        const cards = container.querySelectorAll('.stat-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                card.offsetHeight; // 触发重绘
                card.style.transition = 'all 0.3s ease-out';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    },
    
    // 处理窗口大小变化
    handleResize: function() {
        // 在窗口大小变化时执行的逻辑
        const isMobile = window.innerWidth <= 768;
        
        // 可以根据需要添加响应式处理逻辑
        if (isMobile) {
            // 移动端特殊处理
        } else {
            // 桌面端特殊处理
        }
    },
    
    // 工具方法：格式化数字
    formatNumber: function(num) {
        return new Intl.NumberFormat('zh-CN').format(num);
    },
    
    // 工具方法：格式化日期
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-CN');
    },
    
    // 工具方法：格式化相对时间
    formatRelativeTime: function(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) {
            return '今天';
        } else if (diffDays === 1) {
            return '昨天';
        } else if (diffDays < 7) {
            return `${diffDays}天前`;
        } else {
            return this.formatDate(dateString);
        }
    }
};

// DOM加载完成后初始化应用
document.addEventListener('DOMContentLoaded', function() {
    WordApp.init();
});

// 导出到全局作用域，便于其他脚本使用
window.WordApp = WordApp;