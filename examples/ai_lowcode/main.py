# 构建AI低代码平台的对话能力
from tp_utils import add

# 虚拟化对话的 prompt 模版： 测试下模型的理解能力

print("欢迎使用TP-Utils", add(1, 5))


# 根据元数据构建对话的 prompt 可选项；
def build_meta_prompt():
    return """你是一个AI低代码平台的对话助手，用户会通过你来生成代码。请根据用户的需求生成相应的代码片段，并确保代码符合最佳实践和用户的具体要求。"""


def build_prompt(text):
    return f"{text}"
