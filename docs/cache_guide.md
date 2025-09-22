# 缓存服务使用指南

## 概述
本应用实现了一套内存缓存系统，用于提高数据访问性能，减少数据库查询次数。

## 缓存服务架构

### 核心组件
1. **MemoryCache**: 基础内存缓存实现
2. **CacheService**: 缓存服务封装，提供装饰器和工具方法
3. **专门缓存服务**: WordCacheService、UserCacheService、AudioCacheService

### 缓存特性
- TTL（生存时间）支持
- 自动过期清理
- 访问统计
- 内存使用估算
- 线程安全

## 使用方法

### 1. 装饰器使用

```python
from app.services.cache_service import CacheService

@CacheService.cached(ttl=3600, key_prefix='words')
def get_word_list(grade, unit):
    # 实际的数据查询逻辑
    return Word.query.filter_by(grade=grade, unit=unit).all()
```

### 2. 直接使用缓存

```python
from app.services.cache_service import CacheService

cache = CacheService.get_cache()

# 设置缓存
cache.set('my_key', my_data, ttl=1800)

# 获取缓存
data = cache.get('my_key')

# 删除缓存
cache.delete('my_key')
```

### 3. 专门缓存服务

```python
from app.services.cache_service import WordCacheService

# 缓存词库统计
stats = WordCacheService.get_word_statistics()

# 清除单词缓存
WordCacheService.clear_word_cache()
```

## 缓存策略

### TTL配置
- 词库数据: 30分钟 - 1小时
- 用户进度: 10分钟
- 音频信息: 24小时
- 统计数据: 1小时

### 自动清理
- 数据更新时自动清除相关缓存
- 后台定期清理过期缓存（每5分钟）
- 支持手动清理

## 缓存管理

### API接口
- `GET /api/cache/stats` - 获取缓存统计
- `POST /api/cache/clear` - 清除缓存
- `POST /api/cache/warmup` - 缓存预热
- `GET /api/cache/health` - 健康检查

### 管理页面
系统信息页面提供缓存管理功能：
- 查看缓存统计信息
- 缓存预热操作
- 清除缓存功能

## 性能优化

### 缓存命中率优化
1. 合理设置TTL时间
2. 预热常用数据
3. 避免缓存太小的数据

### 内存管理
1. 监控内存使用情况
2. 定期清理过期数据
3. 设置合理的缓存大小限制

## 注意事项

1. **线程安全**: 所有缓存操作都是线程安全的
2. **内存限制**: 当前使用内存缓存，注意内存使用量
3. **数据一致性**: 数据更新时及时清理相关缓存
4. **错误处理**: 缓存失败时自动降级到数据库查询

## 监控与调试

### 日志记录
缓存操作会记录到日志文件中，包括：
- 缓存命中/未命中
- 缓存设置和清理
- 错误信息

### 统计信息
可通过API或管理页面查看：
- 缓存项目数量
- 内存使用量
- 访问统计
- 命中率等

## 扩展性

### Redis支持
当前版本使用内存缓存，后续可扩展支持Redis：

```python
# 配置Redis缓存
CACHE_TYPE = 'redis'
REDIS_URL = 'redis://localhost:6379/0'
```

### 分布式缓存
多实例部署时可考虑使用分布式缓存方案。