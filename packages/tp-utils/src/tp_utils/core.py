"""核心功能模块：包含 add 函数"""

from typing import Union, Tuple, List


def add(
    a: Union[int, float, Tuple[Union[int, float], ...], List[Union[int, float]]],
    b: Union[int, float] = None,
    strict_type: bool = True,
) -> Union[int, float]:
    """
    加法函数：支持单个数值相加、多个数值批量相加（元组/列表）

    Args:
        a: 第一个数值，或包含多个数值的元组/列表（批量相加时）
        b: 第二个数值（单个相加时必传；批量相加时不传）
        strict_type: 是否严格校验数值类型（默认 True，仅允许 int/float；False 允许自动转换）

    Returns:
        相加结果（int 或 float）

    Examples:
        >>> add(1, 2)
        3

        >>> add(3.5, 4.5)
        8.0

        >>> add([1, 2, 3, 4])  # 批量相加（列表）
        10

        >>> add((5, 6, 7))     # 批量相加（元组）
        18

        >>> add(10, 20.5)
        30.5

        >>> add("1", 2, strict_type=False)  # 非严格模式，自动转换字符串为int
        3

    Raises:
        TypeError: 严格模式下传入非 int/float 类型
        ValueError: 参数组合错误（如批量相加时传了 b，或单个相加时 a 不是单个数值）
    """

    # 处理参数类型校验
    def _validate_number(
        num: Union[int, float, str], strict: bool
    ) -> Union[int, float]:
        if isinstance(num, (int, float)):
            return num
        if not strict:
            try:
                return int(num) if num.isdigit() else float(num)
            except (ValueError, AttributeError):
                raise TypeError(f"无法将 {type(num).__name__} 类型 '{num}' 转换为数值")
        raise TypeError(
            f"仅支持 int/float 类型，传入了 {type(num).__name__} 类型 '{num}'"
        )

    # 场景1：批量相加（a 是元组/列表，b 不传）
    if b is None:
        if not isinstance(a, (tuple, list)):
            raise ValueError("批量相加时，a 必须是元组或列表")
        total = 0.0
        for item in a:
            validated_item = _validate_number(item, strict_type)
            total += validated_item
        # 若结果是整数（如 10.0 → 10），自动转换为 int
        return int(total) if total.is_integer() else total

    # 场景2：单个相加（a 和 b 都传）
    validated_a = _validate_number(a, strict_type)
    validated_b = _validate_number(b, strict_type)
    result = validated_a + validated_b
    return int(result) if isinstance(result, float) and result.is_integer() else result
