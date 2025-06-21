"""定义输入类型枚举"""

from enum import Enum


class InputType(Enum):
    """表示输入内容的类型枚举"""

    WORD_PHRASE = "单词/词组"
    PARAGRAPH = "段落"
    FULL_ESSAY = "全文"
