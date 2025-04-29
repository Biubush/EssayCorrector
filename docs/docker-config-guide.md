# Docker环境变量配置指南 - 论文纠错系统

本文档详细介绍如何通过环境变量配置论文纠错系统的参数。

## 文档导航
- [返回项目主页](../README.md)
- [Docker部署指南](docker-guide.md)
- **当前文档**：Docker环境变量配置指南

## 环境变量配置

系统已更新，支持通过环境变量覆盖默认配置。您可以在`docker-compose.yml`文件的`environment`部分设置以下参数：

### 应用基本配置

```yaml
environment:
  # 应用配置
  - DEBUG=False                     # 是否启用调试模式
  - HOST=0.0.0.0                    # 服务器监听的IP地址
  - PORT=8329                       # 服务器监听的端口号
  - TEMP_FOLDER=/tmp/essay_corrector_temp  # 临时文件存储路径
  - DATABASE_URI=sqlite:///data/tasks.db   # 数据库连接URI
```

### AI相关配置

```yaml
environment:
  # AI配置
  - AI_API_KEY=your_api_key_here    # AI API密钥
  - AI_MODEL=deepseek-chat          # AI模型名称
```

### 定时任务与文本处理

```yaml
environment:
  # 定时任务配置
  - CLEANUP_INTERVAL_HOURS=24       # 临时文件清理间隔（小时）
  
  # 文本处理配置
  - MAX_CHARS_PER_PARAGRAPH=3000    # 段落合并的最大字符数
```

### AI提示词配置

系统支持通过提示词文件自定义AI校对规则。您可以通过环境变量配置提示词文件的路径：

```yaml
environment:
  # AI提示词配置
  - PROMPTS_FILE=/app/custom_prompts.txt
```

同时，您需要确保通过卷挂载将提示词文件挂载到容器中：

```yaml
volumes:
  # 提示词文件挂载
  - /path/to/your/custom_prompts.txt:/app/custom_prompts.txt
```

提示词文件支持多种格式和复杂内容结构，包括：
- 简单的列表（每行一条规则）
- Markdown格式（标题、列表、表格等）
- 复杂的结构化内容
- 包含大括号的JSON示例（系统会自动处理格式）

#### 提示词文件示例

**简单列表格式**：
```
1. 校对学术论文中的语法错误
2. 修正不恰当的学术表达
3. 纠正不一致的时态和语态
```

**结构化内容格式**：
```
# 校对范围

## 必须处理
- 语法错误：主谓宾残缺/动宾搭配不当
- 标点错误：句子结束无标点/引号不匹配

## 不处理内容
- 专业术语：各学科专有名词
- 公式和符号：所有数学和物理公式
```

**包含特殊元素的格式**：
```
# 输出格式

使用JSON格式：[{"theorigin":"原句","corrected":"修正后的句子"}]
```

> 注意：即使提示词文件包含大括号、特殊符号或Markdown格式，系统也能正确处理。无需担心格式问题。

### 调试配置

添加以下环境变量可以在容器启动时打印所有配置参数的值，有助于排查配置问题：

```yaml
environment:
  - PRINT_CONFIG=True               # 是否在启动时打印配置信息
```

## 配置应用方法

1. 编辑`docker-compose.yml`文件，在`environment`部分添加或修改需要的环境变量：

```yaml
services:
  essay-corrector:
    # ... 其他配置 ...
    environment:
      - HOST=0.0.0.0
      - PORT=8329
      - AI_API_KEY=your_custom_key_here
      - PRINT_CONFIG=True
```

2. 保存修改后，重启容器以应用新的配置：

```bash
docker-compose down
docker-compose up -d
```

3. 查看日志，确认配置是否正确应用：

```bash
docker-compose logs -f
```

如果启用了`PRINT_CONFIG=True`，日志中会显示所有配置参数的值。

## 常见问题排查

1. **配置未生效**
   - 确保在`docker-compose.yml`中正确设置了环境变量
   - 确保重新启动了容器
   - 检查日志中是否有相关错误信息

2. **多个配置参数**
   如果需要配置多个参数，请确保每个参数都在单独的行上：
   
   ```yaml
   environment:
     - PARAM1=value1
     - PARAM2=value2
   ```
   
   而不是：
   
   ```yaml
   environment:
     - PARAM1=value1 PARAM2=value2  # 错误格式
   ```

3. **布尔值配置**
   对于布尔值配置（如`DEBUG`），可以使用以下值：
   - 真值：`True`, `true`, `1`, `t`
   - 假值：`False`, `false`, `0`, `f`

## 示例配置

### 生产环境配置示例

```yaml
environment:
  - DEBUG=False
  - MODE=production
  - AI_API_KEY=your_production_key
  - CLEANUP_INTERVAL_HOURS=48
```

### 开发环境配置示例

```yaml
environment:
  - DEBUG=True
  - MODE=development
  - PRINT_CONFIG=True
```

## 所有可配置的环境变量

以下是系统中所有可以通过环境变量配置的参数列表：

| 环境变量 | 描述 | 默认值 | 示例 |
|---------|------|-------|------|
| DEBUG | 是否启用调试模式 | True | False |
| HOST | 服务器监听的IP地址 | 0.0.0.0 | 127.0.0.1 |
| PORT | 服务器监听的端口号 | 8329 | 8080 |
| TEMP_FOLDER | 临时文件存储路径 | tempfile.gettempdir()/essay_corrector_temp | /app/temp |
| DATABASE_URI | 数据库连接URI | sqlite:///tasks.db | sqlite:///data/db.sqlite |
| AI_API_KEY | AI API密钥 | sk-d308f9abe71e4127980612c6aa5cfd19 | your_key_here |
| AI_MODEL | AI模型名称 | deepseek-chat | deepseek-reasoner |
| PROMPTS_FILE | 提示词文件路径 | prompts.txt | /app/custom_prompts.txt |
| CLEANUP_INTERVAL_HOURS | 临时文件清理间隔(小时) | 24 | 48 |
| MAX_CHARS_PER_PARAGRAPH | 段落合并的最大字符数 | 3000 | 5000 |
| PRINT_CONFIG | 是否打印配置信息 | False | True |
| MODE | 容器运行模式 | production | development | 

## 相关文档
- [项目README](../README.md) - 项目主要说明文档
- [Docker部署指南](docker-guide.md) - Docker部署详细步骤