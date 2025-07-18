# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, Response, stream_with_context, jsonify
import os
import enum
import requests
import json

app = Flask(__name__)
app.secret_key = 'app-uWIUClU21goqYXge3pnZNJdv'

# Dify API配置（建议用环境变量管理）
DIFY_API_BASE_URL = 'http://localhost/v1'
DIFY_API_TOKEN = os.environ.get('DIFY_API_TOKEN', 'app-uWIUClU21goqYXge3pnZNJdv')

# 文件类型映射
EXT_TYPE_MAP = {
    'application/pdf': 'pdf',
    'application/msword': 'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'text/plain': 'txt',
    'text/markdown': 'markdown',
    'text/html': 'html',
    'application/vnd.ms-excel': 'xls',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
    'application/vnd.ms-powerpoint': 'ppt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
    'application/xml': 'xml',
    'application/epub+zip': 'epub',
    'image/jpeg': 'jpg',
    'image/png': 'png',
    'image/gif': 'gif',
    'image/webp': 'webp',
    'image/svg+xml': 'svg',
    'audio/mpeg': 'mp3',
    'audio/mp4': 'm4a',
    'audio/wav': 'wav',
    'audio/webm': 'webm',
    'audio/amr': 'amr',
    'video/mp4': 'mp4',
    'video/quicktime': 'mov',
    'video/mpeg': 'mpeg',
    'audio/mpga': 'mpga',
}
EXT_FILETYPE_MAP = {
    'pdf': 'document', 'doc': 'document', 'docx': 'document', 'txt': 'document', 'md': 'document', 'markdown': 'document', 'html': 'document',
    'xls': 'document', 'xlsx': 'document', 'ppt': 'document', 'pptx': 'document', 'xml': 'document', 'epub': 'document',
    'csv': 'document', 'eml': 'document', 'msg': 'document',
    'jpg': 'image', 'jpeg': 'image', 'png': 'image', 'gif': 'image', 'webp': 'image', 'svg': 'image',
    'mp3': 'audio', 'm4a': 'audio', 'wav': 'audio', 'webm': 'audio', 'amr': 'audio', 'mpga': 'audio',
    'mp4': 'video', 'mov': 'video', 'mpeg': 'video',
}
def guess_type(file):
    mime = getattr(file, 'mimetype', None)
    ext = EXT_TYPE_MAP.get(mime)
    if not ext:
        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    return EXT_FILETYPE_MAP.get(ext, 'custom')

def file_to_dify_input(file, file_id):
    file_type = guess_type(file)
    return {
        'type': file_type,
        'upload_file_id': file_id,
        'transfer_method': 'local_file'
    }

def filter_nones(obj):
    if isinstance(obj, dict):
        return {k: filter_nones(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [filter_nones(i) for i in obj if i is not None]
    else:
        return obj

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', result=None)

@app.route('/upload', methods=['POST'])
def upload():
    # 处理多文件上传和参数
    user_id = request.form.get('user_id', 'demo_user')
    files = {}
    file_fields = ['origin_article', 'imitate_article', 'Superior_docs']
    for field in file_fields:
        file = request.files.get(field)
        if file:
            temp_path = os.path.join('static', file.filename)
            file.save(temp_path)
            try:
                url = f"{DIFY_API_BASE_URL}/files/upload"
                headers = {"Authorization": f"Bearer {DIFY_API_TOKEN}"}
                with open(temp_path, 'rb') as f:
                    files_data = {'file': (file.filename, f, file.mimetype)}
                    data = {'user': user_id}
                    resp = requests.post(url, headers=headers, files=files_data, data=data)
                    resp.raise_for_status()
                    file_info = resp.json()
                    file_id = file_info['id']
                files[field] = file_to_dify_input(file, file_id)
            except Exception as e:
                flash(f'{field} 文件上传失败: {e}')
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return redirect(url_for('index'))
            if os.path.exists(temp_path):
                os.remove(temp_path)
        else:
            files[field] = None
    # 组装inputs
    inputs = {
        'query': request.form.get('query', ''),
        'if_rewriter': request.form.get('if_rewriter', ''),
        'origin_article': files['origin_article'],
        'if_database': request.form.get('if_database', ''),
        'keyword_database': request.form.get('keyword_database', ''),
        'if_online_search': request.form.get('if_online_search', ''),
        'online_search_topic': request.form.get('online_search_topic', ''),
        'if_imitate_writing': request.form.get('if_imitate_writing', ''),
        'imitate_article': files['imitate_article'],
        'Superior_docs': files['Superior_docs']
    }
    # 过滤None
    inputs = filter_nones(inputs)
    sys_query = request.form.get('sys_query', '')
    return Response(json.dumps({
        'inputs': inputs,
        'user_id': user_id,
        'sys_query': sys_query
    }, ensure_ascii=False), mimetype='application/json')

@app.route('/stream_chat', methods=['POST'])
def stream_chat():
    data = request.get_json()
    inputs = data.get('inputs')
    user_id = data.get('user_id')
    sys_query = data.get('sys_query')
    conversation_id = data.get('conversation_id', '')
    if not inputs or not user_id or not sys_query:
        return jsonify({'error': '参数缺失'}), 400
    def event_stream():
        try:
            url = f"{DIFY_API_BASE_URL}/chat-messages"
            headers = {
                "Authorization": f"Bearer {DIFY_API_TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "query": sys_query,
                "inputs": inputs,
                "user": user_id,
                "response_mode": "streaming",
                "conversation_id": conversation_id
            }
            with requests.post(url, headers=headers, json=payload, stream=True, timeout=120) as resp:
                for line in resp.iter_lines():
                    if line:
                        if line.startswith(b'data:'):
                            content = line[5:].decode('utf-8').strip()
                            yield f"data: {content}\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
    return Response(stream_with_context(event_stream()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True) 