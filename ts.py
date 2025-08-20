from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
filename = "tinyllama-1.1b-chat-v1.0.Q6_K.gguf"

tokenizer = AutoTokenizer.from_pretrained(model_id, gguf_file=filename)
model = AutoModelForCausalLM.from_pretrained(model_id, gguf_file=filename)

# 编码输入
inputs = tokenizer("你好", return_tensors="pt")

# 生成回复
outputs = model.generate(**inputs, max_new_tokens=100)

# 解码输出
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
