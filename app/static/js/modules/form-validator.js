// 前端表单验证组件

window.FormValidator = {
    // 验证规则
    rules: {
        required: {
            validate: (value) => value !== null && value !== undefined && value.toString().trim() !== '',
            message: '此字段是必填的'
        },
        
        minLength: {
            validate: (value, minLen) => value.toString().length >= minLen,
            message: (minLen) => `长度至少需要${minLen}个字符`
        },
        
        maxLength: {
            validate: (value, maxLen) => value.toString().length <= maxLen,
            message: (maxLen) => `长度不能超过${maxLen}个字符`
        },
        
        pattern: {
            validate: (value, regex) => regex.test(value),
            message: (regex) => '格式不正确'
        },
        
        email: {
            validate: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
            message: '请输入有效的邮箱地址'
        },
        
        username: {
            validate: (value) => /^[\u4e00-\u9fa5a-zA-Z0-9_]{2,20}$/.test(value),
            message: '用户名只能包含中文、英文、数字和下划线，长度2-20个字符'
        },
        
        grade: {
            validate: (value) => {
                const num = parseInt(value);
                return !isNaN(num) && num >= 3 && num <= 6;
            },
            message: '年级必须在3-6之间'
        },
        
        unit: {
            validate: (value) => {
                const num = parseInt(value);
                return !isNaN(num) && num >= 1 && num <= 20;
            },
            message: '单元必须在1-20之间'
        },
        
        word: {
            validate: (value) => /^[a-zA-Z\s'-]{1,50}$/.test(value),
            message: '单词只能包含英文字母、空格、撇号和连字符，长度1-50个字符'
        },
        
        chineseMeaning: {
            validate: (value) => value.trim().length >= 1 && value.length <= 200,
            message: '中文含义不能为空且长度不能超过200个字符'
        }
    },
    
    // 验证单个字段
    validateField: function(value, rules, fieldName) {
        const errors = [];
        
        for (const rule of rules) {
            if (typeof rule === 'string') {
                // 简单规则
                const ruleConfig = this.rules[rule];
                if (ruleConfig && !ruleConfig.validate(value)) {
                    errors.push(ruleConfig.message);
                }
            } else if (typeof rule === 'object') {
                // 带参数的规则
                const ruleName = rule.rule;
                const ruleConfig = this.rules[ruleName];
                if (ruleConfig) {
                    if (!ruleConfig.validate(value, rule.param)) {
                        const message = typeof ruleConfig.message === 'function' 
                            ? ruleConfig.message(rule.param)
                            : ruleConfig.message;
                        errors.push(message);
                    }
                }
            }
        }
        
        return errors;
    },
    
    // 验证整个表单
    validateForm: function(formData, validationRules) {
        const errors = {};
        let hasErrors = false;
        
        for (const [fieldName, rules] of Object.entries(validationRules)) {
            const value = formData[fieldName];
            const fieldErrors = this.validateField(value, rules, fieldName);
            
            if (fieldErrors.length > 0) {
                errors[fieldName] = fieldErrors;
                hasErrors = true;
            }
        }
        
        return {
            isValid: !hasErrors,
            errors: errors
        };
    },
    
    // 显示字段错误
    showFieldError: function(fieldElement, errors) {
        // 移除旧的错误信息
        this.clearFieldError(fieldElement);
        
        if (errors && errors.length > 0) {
            fieldElement.classList.add('error');
            
            // 创建错误信息元素
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error';
            errorDiv.innerHTML = errors.map(error => `<span>${error}</span>`).join('');
            
            // 插入错误信息
            fieldElement.parentNode.insertBefore(errorDiv, fieldElement.nextSibling);
        }
    },
    
    // 清除字段错误
    clearFieldError: function(fieldElement) {
        fieldElement.classList.remove('error');
        
        const errorDiv = fieldElement.parentNode.querySelector('.field-error');
        if (errorDiv) {
            errorDiv.remove();
        }
    },
    
    // 显示表单错误
    showFormErrors: function(form, errors) {
        // 清除所有旧错误
        this.clearFormErrors(form);
        
        for (const [fieldName, fieldErrors] of Object.entries(errors)) {
            const fieldElement = form.querySelector(`[name="${fieldName}"]`);
            if (fieldElement) {
                this.showFieldError(fieldElement, fieldErrors);
            }
        }
    },
    
    // 清除表单错误
    clearFormErrors: function(form) {
        const errorElements = form.querySelectorAll('.field-error');
        errorElements.forEach(element => element.remove());
        
        const fieldElements = form.querySelectorAll('.error');
        fieldElements.forEach(element => element.classList.remove('error'));
    },
    
    // 初始化表单验证
    initFormValidation: function(form, validationRules) {
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            // 实时验证
            input.addEventListener('blur', () => {
                const fieldName = input.name;
                const rules = validationRules[fieldName];
                
                if (rules) {
                    const errors = this.validateField(input.value, rules, fieldName);
                    this.showFieldError(input, errors);
                }
            });
            
            // 清除错误（当用户开始修改时）
            input.addEventListener('input', () => {
                this.clearFieldError(input);
            });
        });
        
        // 表单提交验证
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = {};
            
            for (const [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            const result = this.validateForm(data, validationRules);
            
            if (result.isValid) {
                // 验证通过，可以提交
                form.dispatchEvent(new CustomEvent('validSubmit', { detail: data }));
            } else {
                // 显示错误
                this.showFormErrors(form, result.errors);
                
                // 滚动到第一个错误字段
                const firstError = form.querySelector('.error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
        });
    }
};

// 表单验证样式
const validationStyles = `
<style>
.field-error {
    color: var(--danger-color);
    font-size: var(--font-size-sm);
    margin-top: var(--spacing-xs);
    line-height: var(--line-height-relaxed);
}

.field-error span {
    display: block;
    margin-bottom: var(--spacing-xs);
}

.field-error span:last-child {
    margin-bottom: 0;
}

input.error,
select.error,
textarea.error {
    border-color: var(--danger-color);
    box-shadow: 0 0 0 2px rgba(220, 53, 69, 0.25);
}

.form-group.has-error .form-label {
    color: var(--danger-color);
}

.validation-summary {
    background: var(--danger-light);
    border: 1px solid var(--danger-color);
    border-radius: var(--border-radius-md);
    padding: var(--spacing-md);
    margin-bottom: var(--spacing-lg);
    color: var(--danger-color);
}

.validation-summary h4 {
    margin: 0 0 var(--spacing-sm) 0;
    font-size: var(--font-size-md);
}

.validation-summary ul {
    margin: 0;
    padding-left: var(--spacing-lg);
}

.validation-summary li {
    margin-bottom: var(--spacing-xs);
}
</style>
`;

// 注入样式
if (!document.querySelector('#validation-styles')) {
    const styleElement = document.createElement('div');
    styleElement.id = 'validation-styles';
    styleElement.innerHTML = validationStyles;
    document.head.appendChild(styleElement);
}

// 预定义的验证规则集
window.ValidationRules = {
    // 用户创建表单
    createUser: {
        username: ['required', 'username'],
        grade: ['required', 'grade']
    },
    
    // 单词创建表单
    createWord: {
        word: ['required', 'word'],
        chinese_meaning: ['required', 'chineseMeaning'],
        grade: ['required', 'grade'],
        unit: ['required', 'unit'],
        phonetic: [{ rule: 'maxLength', param: 200 }],
        phonics_breakdown: [{ rule: 'maxLength', param: 500 }],
        memory_method: [{ rule: 'maxLength', param: 500 }]
    },
    
    // 用户更新表单
    updateUser: {
        username: ['username'],
        grade: ['grade']
    }
};

// 自动初始化表单验证
document.addEventListener('DOMContentLoaded', function() {
    // 为具有 data-validation 属性的表单自动初始化验证
    const validationForms = document.querySelectorAll('[data-validation]');
    
    validationForms.forEach(form => {
        const ruleName = form.getAttribute('data-validation');
        const rules = ValidationRules[ruleName];
        
        if (rules) {
            FormValidator.initFormValidation(form, rules);
        }
    });
});