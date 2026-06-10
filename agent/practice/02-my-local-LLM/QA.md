# 本地部署大语言模型 - QA 问答记录

> Hello-Agents 第三章实践问题与解决方案

---

## 💡 提示：下载速度问题

在实践过程中，最常见的问题是下载速度慢。以下是完整的解决方案：

### 问题 1：PyTorch 下载太慢

**现象**：使用 `pip install torch` 时，下载速度约 21.5 KB/s，预计需要 2 小时。

**解决**：使用国内镜像源

```bash
pip install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**效果**：下载速度提升到 1-5 MB/s，几分钟内完成。

---

### 问题 2：Transformers 下载慢

**解决**：同样使用清华镜像

```bash
pip install transformers -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

### 问题 3：模型下载慢

**现象**：运行代码时从 Hugging Face Hub 下载模型很慢。

**解决**：设置镜像环境变量

```bash
# Git Bash / Linux / macOS
export HF_ENDPOINT="https://hf-mirror.com"

# Windows PowerShell
$env:HF_ENDPOINT="https://hf-mirror.com"

# Windows CMD
set HF_ENDPOINT=https://hf-mirror.com
```

**国内可用镜像**：

| 镜像 | 地址 | 说明 |
|------|------|------|
| HF-Mirror | https://hf-mirror.com | 推荐，稳定 |
| 阿里云 | https://mirrors.aliyun.com/huggingface | 备选 |

---

## 📁 模型存储位置

### 默认缓存目录

模型下载后会自动缓存到以下位置：

| 操作系统 | 默认路径 |
|---------|---------|
| Windows | `C:\Users\<用户名>\.cache\huggingface\hub` |
| macOS | `~/.cache/huggingface/hub` |
| Linux | `~/.cache/huggingface/hub` |

### 查看你的缓存位置

```bash
# Windows (Git Bash)
ls ~/.cache/huggingface/hub

# 或直接查看
ls "C:\Users\Administrator\.cache\huggingface\hub"
```

### 缓存目录结构

```
.cache/huggingface/hub/
├── models--Qwen--Qwen1.5-0.5B-Chat/
│   ├── blobs/              # 模型权重文件
│   ├── refs/               # 版本引用
│   └── snapshots/          # 快照
└── models--Qwen--Qwen1.5-1.8B-Chat/
    └── ...
```

---

## 🗑️ 如何清理模型缓存

### 方法 1：手动删除

直接删除缓存目录中的模型文件夹：

```bash
# 删除特定模型
rm -rf ~/.cache/huggingface/hub/models--Qwen--Qwen1.5-0.5B-Chat

# 删除所有模型缓存（谨慎使用）
rm -rf ~/.cache/huggingface/hub
```

### 方法 2：使用 Python 清理

```python
from huggingface_hub import scan_cache_dir, delete_cache

# 扫描缓存
cache_info = scan_cache_dir()
print(cache_info)

# 删除特定模型（需要确认）
# delete_cache(repo_id="Qwen/Qwen1.5-0.5B-Chat")
```

### 方法 3：使用 huggingface-cli

```bash
# 查看缓存信息
huggingface-cli scan-cache

# 删除缓存
huggingface-cli delete-cache
```

---

## 📦 如何迁移模型到其他位置

### 方法 1：修改默认缓存路径

在代码开头设置新的缓存目录：

```python
import os

# 设置新的缓存目录
os.environ['HF_HOME'] = 'D:/models/huggingface'

# 或者只修改 hub 缓存
os.environ['HF_HUB_CACHE'] = 'D:/models/huggingface/hub'

# 然后加载模型
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen1.5-0.5B-Chat")
```

### 方法 2：手动迁移后使用本地路径

```bash
# 1. 先复制模型到新位置
cp -r ~/.cache/huggingface/hub/models--Qwen--Qwen1.5-0.5B-Chat D:/models/

# 2. 使用本地路径加载
```

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# 使用本地路径
model_path = "D:/models/models--Qwen--Qwen1.5-0.5B-Chat/snapshots/xxx"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)
```

### 方法 3：下载模型到指定位置

```python
from huggingface_hub import snapshot_download

# 下载到指定目录
snapshot_download(
    repo_id="Qwen/Qwen1.5-0.5B-Chat",
    local_dir="D:/models/Qwen1.5-0.5B-Chat",
    local_dir_use_symlinks=False  # 不使用符号链接，直接复制文件
)
```

---

## 🔧 其他常见问题

### Q1：没有 GPU 能运行吗？

**可以！** 

- 选择小模型（如 Qwen1.5-0.5B-Chat，约 1GB）
- CPU 模式完全可运行，只是速度稍慢
- 本次实践已验证：PyTorch 2.12.0+cpu 运行正常

### Q2：如何验证安装成功？

```bash
python -c "import torch; import transformers; print(f'PyTorch: {torch.__version__}'); print(f'Transformers: {transformers.__version__}')"
```

预期输出：
```
PyTorch: 2.12.0+cpu
Transformers: 5.10.2
```

---

## ✅ 实践成功记录

**运行环境**：
- 设备：CPU 模式
- 模型：Qwen/Qwen1.5-0.5B-Chat
- PyTorch：2.12.0+cpu
- Transformers：5.10.2

**测试对话**：

| 用户输入 | 模型回答 |
|---------|---------|
| "你好，请介绍一下你自己" | "我是来自阿里云的大规模语言模型，我叫通义千问..." |
| "你的数据训练截止时间是什么时候" | "由于涉及敏感信息...对于这些数据的使用期限没有明确的规定..." |

**验证结论**：
- ✅ 模型加载成功
- ✅ 对话交互正常  
- ✅ 多轮对话支持
- ✅ CPU 模式可正常运行

---

## 📚 参考链接

- [Hugging Face 官方文档](https://huggingface.co/docs/transformers/)
- [HF-Mirror 国内镜像](https://hf-mirror.com/)
- [清华 PyPI 镜像](https://pypi.tuna.tsinghua.edu.cn/simple)
- [Hello-Agents 教程](https://datawhalechina.github.io/hello-agents/)