# 智能文件撰写系统

## 项目简介

智能文件撰写系统是一个基于 Flask 和 Dify API 的多功能公文/文章自动生成与辅助写作平台。系统支持改写、仿写、数据库查询、联网搜索等多种写作场景，适用于政务、企事业单位等需要高效文档处理的用户。

## 主要特性

- 支持多种公文类型（如工作报告、领导讲话、工作要点、处室总结、表态发言等）
- 支持原文改写、仿写（可上传多种格式文件）
- 可选数据库关键词查询与联网主题搜索
- 前端页面简洁，交互友好，支持多文件上传
- 后端对接 Dify API，流式返回 AI 生成内容
- 支持多种文件格式（文档、图片、音频、视频等）

## 技术栈

- 后端：Python 3.x, Flask, requests
- 前端：HTML5, 原生 JavaScript, CSS
- 依赖：Dify API（需本地或远程部署 Dify 服务）

## 安装与部署

1. **环境准备**
   - Python 3.7 及以上
   - pip

2. **创建虚拟环境（推荐）**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **安装依赖（使用清华源）**
   ```bash
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
   ```

4. **配置 Dify API**
   - 默认 Dify API 地址为 `http://localhost/v1`
   - 默认 Token 为 `app-×××××`
   - 推荐通过环境变量设置 Token：
     ```bash
     set DIFY_API_TOKEN=your_token_here  # Windows
     export DIFY_API_TOKEN=your_token_here  # Linux/macOS
     ```

5. **启动服务**
   ```bash
   python app.py
   ```
   默认监听 http://127.0.0.1:5000

## 使用说明

1. 访问首页（如 http://127.0.0.1:5000），填写表单，按需上传文件。
2. 选择公文类型、主题、是否改写/仿写/查数据库/联网搜索等选项。
3. 支持多种写作模式与辅助选项，上传相关文件（如原文、仿写文章、上级文件等）。
4. 点击“提交生成”，系统将实时流式返回 AI 生成内容。
5. **结果区支持美观的 Markdown 渲染**，标题、列表、加粗等格式与 Dify 后台一致。
6. **结果区为固定高度（250px），支持滚动浏览**，点击结果区可弹出模态窗口显示完整内容。
7. **弹窗内可一键“下载”生成的内容为 docx 文件**，下载前会自动去除所有 <think>…</think> 标签及其内容，导出文件名自动带有时间戳（如“公文输出_2024-06-09_221530.docx”）。

## 目录结构

```
Dify-artilcle-writing-sys/
  ├── app.py                # 后端主程序
  ├── requirements.txt      # 依赖列表
  ├── templates/
  │     └── index.html      # 前端页面（含markdown渲染、弹窗、docx导出等功能）
  └── static/
        ├── favicon.ico     # 静态资源
        ├── marked.min.js   # Markdown渲染库
        └── html-docx.js    # HTML转docx导出库
```

## 配置说明

- Dify API 地址与 Token 支持环境变量配置。
- 默认 Token 仅供演示，生产环境请更换为安全的 Token。
- 如需对接数据库或外部 API，请参考 app.py 相关代码进行扩展。

## 常见问题

- **文件上传失败**：请检查 Dify API 服务是否正常运行，Token 是否正确。
- **AI 接口异常**：请检查网络连接、Dify API 配置及日志输出。
- **依赖安装失败**：请确保 Python 版本和 pip 工具可用。
- **端口冲突**：如 5000 端口被占用，可在 app.py 中修改端口。

## 贡献与许可

欢迎社区贡献代码、反馈问题或提出建议。请 fork 本仓库后提交 Pull Request。

本项目采用 MIT 许可证。

## 致谢

- 感谢 Dify 团队及相关开源项目的支持。
- 感谢所有贡献者和用户。 