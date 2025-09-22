// 用户体验增强组件 - 加载状态、进度条、反馈等

// 加载状态管理器
window.LoadingManager = {
    loadingElements: new Map(),
    
    // 显示加载状态
    show: function(target, options = {}) {
        const config = {
            text: '加载中...',
            type: 'spinner', // spinner, dots, progress
            overlay: false,
            size: 'md', // sm, md, lg
            ...options
        };
        
        const loadingElement = this.createLoadingElement(config);
        
        if (config.overlay) {
            this.showOverlay(target, loadingElement);
        } else {
            this.showInline(target, loadingElement);
        }
        
        this.loadingElements.set(target, loadingElement);
    },
    
    // 隐藏加载状态
    hide: function(target) {
        const loadingElement = this.loadingElements.get(target);
        if (loadingElement) {
            if (loadingElement.overlay) {
                loadingElement.overlay.remove();
            } else {
                loadingElement.remove();
            }
            this.loadingElements.delete(target);
        }
        
        // 恢复目标元素
        if (target && target.style) {
            target.style.pointerEvents = '';
            target.style.opacity = '';
        }
    },
    
    // 创建加载元素
    createLoadingElement: function(config) {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = `loading-indicator loading-${config.type} loading-${config.size}`;
        
        let innerHTML = '';
        
        switch (config.type) {
            case 'spinner':
                innerHTML = `
                    <div class="spinner">
                        <div class="spinner-border"></div>
                    </div>
                    <span class="loading-text">${config.text}</span>
                `;
                break;
            case 'dots':
                innerHTML = `
                    <div class="dots-loading">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                    <span class="loading-text">${config.text}</span>
                `;
                break;
            case 'progress':
                innerHTML = `
                    <div class="progress-loading">
                        <div class="progress-bar"></div>
                    </div>
                    <span class="loading-text">${config.text}</span>
                `;
                break;
        }
        
        loadingDiv.innerHTML = innerHTML;
        return loadingDiv;
    },
    
    // 显示覆盖层加载
    showOverlay: function(target, loadingElement) {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';\n        \n        if (target === document.body) {\n            overlay.classList.add('loading-overlay-fullscreen');\n        } else {\n            overlay.classList.add('loading-overlay-element');\n            const rect = target.getBoundingClientRect();\n            overlay.style.position = 'absolute';\n            overlay.style.top = rect.top + 'px';\n            overlay.style.left = rect.left + 'px';\n            overlay.style.width = rect.width + 'px';\n            overlay.style.height = rect.height + 'px';\n        }\n        \n        overlay.appendChild(loadingElement);\n        document.body.appendChild(overlay);\n        \n        loadingElement.overlay = overlay;\n    },\n    \n    // 显示内联加载\n    showInline: function(target, loadingElement) {\n        if (target.querySelector('.loading-indicator')) {\n            return; // 已经有加载指示器了\n        }\n        \n        target.style.position = 'relative';\n        target.style.pointerEvents = 'none';\n        target.style.opacity = '0.7';\n        \n        loadingElement.style.position = 'absolute';\n        loadingElement.style.top = '50%';\n        loadingElement.style.left = '50%';\n        loadingElement.style.transform = 'translate(-50%, -50%)';\n        loadingElement.style.zIndex = '9999';\n        \n        target.appendChild(loadingElement);\n    }\n};\n\n// 进度条管理器\nwindow.ProgressBar = {\n    // 创建进度条\n    create: function(container, options = {}) {\n        const config = {\n            max: 100,\n            value: 0,\n            showText: true,\n            animated: true,\n            color: 'primary',\n            height: 'md', // sm, md, lg\n            ...options\n        };\n        \n        const progressWrapper = document.createElement('div');\n        progressWrapper.className = `progress-wrapper progress-${config.height}`;\n        \n        const progressBar = document.createElement('div');\n        progressBar.className = 'progress-bar-container';\n        \n        const progressFill = document.createElement('div');\n        progressFill.className = `progress-fill progress-${config.color} ${config.animated ? 'animated' : ''}`;\n        \n        const progressText = document.createElement('div');\n        progressText.className = 'progress-text';\n        progressText.style.display = config.showText ? 'block' : 'none';\n        \n        progressBar.appendChild(progressFill);\n        progressWrapper.appendChild(progressBar);\n        progressWrapper.appendChild(progressText);\n        \n        if (container) {\n            container.appendChild(progressWrapper);\n        }\n        \n        const progressInstance = {\n            element: progressWrapper,\n            fill: progressFill,\n            text: progressText,\n            config: config,\n            \n            // 设置进度\n            setValue: function(value) {\n                const percentage = Math.min(100, Math.max(0, (value / this.config.max) * 100));\n                this.fill.style.width = percentage + '%';\n                \n                if (this.config.showText) {\n                    this.text.textContent = Math.round(percentage) + '%';\n                }\n                \n                // 触发进度变化事件\n                this.element.dispatchEvent(new CustomEvent('progress', {\n                    detail: { value, percentage }\n                }));\n            },\n            \n            // 增加进度\n            increase: function(amount = 1) {\n                const currentValue = (parseFloat(this.fill.style.width) || 0) / 100 * this.config.max;\n                this.setValue(currentValue + amount);\n            },\n            \n            // 设置最大值\n            setMax: function(max) {\n                this.config.max = max;\n            },\n            \n            // 重置进度\n            reset: function() {\n                this.setValue(0);\n            },\n            \n            // 销毁进度条\n            destroy: function() {\n                if (this.element && this.element.parentNode) {\n                    this.element.parentNode.removeChild(this.element);\n                }\n            }\n        };\n        \n        return progressInstance;\n    }\n};\n\n// 反馈通知管理器\nwindow.FeedbackManager = {\n    notifications: [],\n    \n    // 显示通知\n    show: function(message, type = 'info', options = {}) {\n        const config = {\n            duration: 4000,\n            position: 'top-right', // top-left, top-right, bottom-left, bottom-right, center\n            closable: true,\n            icon: true,\n            ...options\n        };\n        \n        const notification = this.createNotification(message, type, config);\n        this.addNotification(notification, config);\n        \n        if (config.duration > 0) {\n            setTimeout(() => {\n                this.removeNotification(notification);\n            }, config.duration);\n        }\n        \n        return notification;\n    },\n    \n    // 显示成功消息\n    success: function(message, options = {}) {\n        return this.show(message, 'success', options);\n    },\n    \n    // 显示错误消息\n    error: function(message, options = {}) {\n        return this.show(message, 'error', { duration: 6000, ...options });\n    },\n    \n    // 显示警告消息\n    warning: function(message, options = {}) {\n        return this.show(message, 'warning', options);\n    },\n    \n    // 显示信息消息\n    info: function(message, options = {}) {\n        return this.show(message, 'info', options);\n    },\n    \n    // 创建通知元素\n    createNotification: function(message, type, config) {\n        const notification = document.createElement('div');\n        notification.className = `notification notification-${type}`;\n        \n        const iconMap = {\n            success: '✅',\n            error: '❌',\n            warning: '⚠️',\n            info: 'ℹ️'\n        };\n        \n        let innerHTML = '';\n        \n        if (config.icon) {\n            innerHTML += `<span class=\"notification-icon\">${iconMap[type] || 'ℹ️'}</span>`;\n        }\n        \n        innerHTML += `<span class=\"notification-message\">${message}</span>`;\n        \n        if (config.closable) {\n            innerHTML += '<button class=\"notification-close\">×</button>';\n        }\n        \n        notification.innerHTML = innerHTML;\n        \n        // 添加关闭事件\n        if (config.closable) {\n            const closeBtn = notification.querySelector('.notification-close');\n            closeBtn.addEventListener('click', () => {\n                this.removeNotification(notification);\n            });\n        }\n        \n        return notification;\n    },\n    \n    // 添加通知到页面\n    addNotification: function(notification, config) {\n        let container = document.querySelector(`.notification-container.${config.position}`);\n        \n        if (!container) {\n            container = document.createElement('div');\n            container.className = `notification-container ${config.position}`;\n            document.body.appendChild(container);\n        }\n        \n        container.appendChild(notification);\n        this.notifications.push(notification);\n        \n        // 添加动画\n        setTimeout(() => {\n            notification.classList.add('show');\n        }, 10);\n    },\n    \n    // 移除通知\n    removeNotification: function(notification) {\n        notification.classList.add('hide');\n        \n        setTimeout(() => {\n            if (notification.parentNode) {\n                notification.parentNode.removeChild(notification);\n            }\n            \n            const index = this.notifications.indexOf(notification);\n            if (index > -1) {\n                this.notifications.splice(index, 1);\n            }\n        }, 300);\n    },\n    \n    // 清除所有通知\n    clearAll: function() {\n        this.notifications.forEach(notification => {\n            this.removeNotification(notification);\n        });\n    }\n};\n\n// 响应式反馈增强器\nwindow.ResponsiveFeedback = {\n    // 为按钮添加响应式效果\n    enhanceButton: function(button) {\n        if (button.classList.contains('enhanced')) {\n            return;\n        }\n        \n        button.classList.add('enhanced');\n        \n        // 添加波纹效果\n        button.addEventListener('click', function(e) {\n            const ripple = document.createElement('span');\n            ripple.className = 'ripple-effect';\n            \n            const rect = this.getBoundingClientRect();\n            const size = Math.max(rect.width, rect.height);\n            const x = e.clientX - rect.left - size / 2;\n            const y = e.clientY - rect.top - size / 2;\n            \n            ripple.style.width = ripple.style.height = size + 'px';\n            ripple.style.left = x + 'px';\n            ripple.style.top = y + 'px';\n            \n            this.appendChild(ripple);\n            \n            setTimeout(() => {\n                ripple.remove();\n            }, 600);\n        });\n        \n        // 添加加载状态支持\n        button.setLoading = function(loading = true) {\n            if (loading) {\n                this.classList.add('loading');\n                this.disabled = true;\n                \n                const originalText = this.textContent;\n                this.setAttribute('data-original-text', originalText);\n                this.textContent = '加载中...';\n            } else {\n                this.classList.remove('loading');\n                this.disabled = false;\n                \n                const originalText = this.getAttribute('data-original-text');\n                if (originalText) {\n                    this.textContent = originalText;\n                    this.removeAttribute('data-original-text');\n                }\n            }\n        };\n    },\n    \n    // 为表单添加响应式验证反馈\n    enhanceForm: function(form) {\n        const inputs = form.querySelectorAll('input, select, textarea');\n        \n        inputs.forEach(input => {\n            // 添加焦点效果\n            input.addEventListener('focus', function() {\n                this.parentNode.classList.add('focused');\n            });\n            \n            input.addEventListener('blur', function() {\n                this.parentNode.classList.remove('focused');\n                \n                if (this.value) {\n                    this.parentNode.classList.add('has-value');\n                } else {\n                    this.parentNode.classList.remove('has-value');\n                }\n            });\n            \n            // 实时验证反馈\n            input.addEventListener('input', function() {\n                this.parentNode.classList.remove('error');\n            });\n        });\n    },\n    \n    // 为卡片添加悬停效果\n    enhanceCard: function(card) {\n        if (card.classList.contains('enhanced')) {\n            return;\n        }\n        \n        card.classList.add('enhanced');\n        \n        card.addEventListener('mouseenter', function() {\n            this.classList.add('hover');\n        });\n        \n        card.addEventListener('mouseleave', function() {\n            this.classList.remove('hover');\n        });\n    }\n};\n\n// 自动初始化\ndocument.addEventListener('DOMContentLoaded', function() {\n    // 自动增强所有按钮\n    document.querySelectorAll('.btn').forEach(button => {\n        ResponsiveFeedback.enhanceButton(button);\n    });\n    \n    // 自动增强所有表单\n    document.querySelectorAll('form').forEach(form => {\n        ResponsiveFeedback.enhanceForm(form);\n    });\n    \n    // 自动增强所有卡片\n    document.querySelectorAll('.card, .word-card, .user-card').forEach(card => {\n        ResponsiveFeedback.enhanceCard(card);\n    });\n});\n\n// 全局快捷方法\nwindow.showLoading = (target, options) => LoadingManager.show(target, options);\nwindow.hideLoading = (target) => LoadingManager.hide(target);\nwindow.showNotification = (message, type, options) => FeedbackManager.show(message, type, options);\nwindow.createProgress = (container, options) => ProgressBar.create(container, options);