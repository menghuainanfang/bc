# 模拟测试样例

## 用户输入
帮我给这个函数写单元测试，用pytest。

```python
def calculate_discount(price: float, quantity: int, is_member: bool, coupon_code: str = None) -> float:
    """
    计算订单折扣后价格
    """
    if price <= 0 or quantity <= 0:
        raise ValueError("价格和数量必须大于0")
    
    if quantity < 0:
        raise ValueError("数量不能为负数")
    
    total = price * quantity
    
    # 会员折扣 10%
    if is_member:
        total *= 0.9
    
    # 批量折扣
    if quantity >= 100:
        total *= 0.85
    elif quantity >= 50:
        total *= 0.95
    
    # 优惠券
    if coupon_code:
        if coupon_code == "SAVE20":
            total -= 20
        elif coupon_code == "SAVE50":
            total -= 50
        else:
            raise ValueError(f"无效的优惠券代码: {coupon_code}")
    
    if total < 0:
        total = 0
    
    return round(total, 2)
```
