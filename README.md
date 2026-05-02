# AI 测试用例生成工具

基于 DeepSeek API 的智能测试用例生成工具，支持 GUI 界面操作和 Excel 导出。

## 功能

- 输入产品需求，AI 自动生成高质量测试用例
- 支持功能测试 / 异常测试 / 全部测试三种模式
- 测试用例自动优化（补充场景、边界情况）
- 一键导出格式美观的 Excel 文件

## 使用

```bash
pip install -r requirements.txt

# 设置 DeepSeek API Key
set DEEPSEEK_API_KEY=your_api_key_here

# 启动 GUI
python gui_app.py
```

## 目录结构

```
├── core.py                  # 核心逻辑
├── gui_app.py               # Tkinter 图形界面
├── config/
│   └── settings.py          # 应用配置
├── services/
│   └── deepseek_client.py   # API 客户端
└── requirements.txt
```
