# 从 core 模块导入 add 函数，对外暴露（用户可直接 from my_private_package import add）
from .core import add

# 定义 __all__，控制 from xxx import * 时导入的内容
__all__ = ["add", "__version__", "__author__"]
