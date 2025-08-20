
# 演示模式说明

由于llama-cpp-python安装失败，Unlimited Agent将以演示模式运行。

## 演示模式特点：
- 不需要下载大型语言模型
- 提供预设的回复来演示界面和功能
- 可以体验完整的用户界面
- 所有功能都可以正常使用，只是回复是模拟的

## 如何启用完整功能：
1. 手动安装llama-cpp-python:
   ```
   pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
   ```

2. 或者安装支持CUDA的版本（如果有NVIDIA GPU）:
   ```
   pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
   ```

3. 重新运行程序即可使用真实的AI模型

## 系统要求：
- Windows: 需要Visual Studio Build Tools
- macOS: 需要Xcode Command Line Tools
- Linux: 需要gcc和cmake
