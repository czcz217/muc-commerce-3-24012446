import sys
from io import StringIO

trains = {
    "G1001": {"start": "上海", "end": "南京", "price": 145, "seat": 30},
    "G1002": {"start": "上海", "end": "杭州", "price": 95, "seat": 50},
    "G1003": {"start": "上海", "end": "北京", "price": 680, "seat": 20}
}
orders = []


def show_menu():
    print("========== 高铁订票系统 ==========")
    print("1. 查看所有车次")
    print("2. 查询车次")
    print("3. 购买车票")
    print("4. 查看我的订单")
    print("5. 退票")
    print("6. 统计收入")
    print("7. 退出")
    print("==================================")


def show_trains():
    print(f"{'车次':<8}{'起点':<8}{'终点':<8}{'票价':<8}{'剩余座位':<8}")
    for train_id, info in trains.items():
        print(f"{train_id:<8}{info['start']:<8}{info['end']:<8}{info['price']:<8}{info['seat']:<8}")


def search_train(end):
    found = False
    print(f"{'车次':<8}{'起点':<8}{'终点':<8}{'票价':<8}{'剩余座位':<8}")
    for train_id, info in trains.items():
        if info['end'] == end:
            print(f"{train_id:<8}{info['start']:<8}{info['end']:<8}{info['price']:<8}{info['seat']:<8}")
            found = True
    if not found:
        print(f"没有找到到{end}的列车")


def buy_ticket(name, id_card, train_id, count):
    if train_id not in trains:
        print("车次不存在")
        return False

    train = trains[train_id]
    if train['seat'] < count:
        print("余票不足")
        return False

    train['seat'] -= count
    money = train['price'] * count

    order = {"name": name, "id": id_card, "train": train_id, "count": count, "money": money}
    orders.append(order)
    print(f"购票成功！{name} 购买了 {train_id} {count}张，共{money}元")
    return True


def show_orders():
    if not orders:
        print("暂无订单")
        return

    for order in orders:
        print(f"{order['name']}")
        print(f"  {order['train']}")
        print(f"  {order['count']}张")
        print(f"  {order['money']}元")
        print("-" * 20)


def refund(id_card):
    for i, order in enumerate(orders):
        if order['id'] == id_card:
            train_id = order['train']
            trains[train_id]['seat'] += order['count']
            print(f"退票成功！已恢复{order['count']}张座位")
            del orders[i]
            return True

    print("未找到订单")
    return False


def count_money():
    total_orders = len(orders)
    total_money = sum(order['money'] for order in orders)
    total_seats = sum(train['seat'] for train in trains.values())

    print(f"今日订单：{total_orders}")
    print(f"销售额：{total_money}")
    print(f"剩余座位：{total_seats}")


print("=" * 50)
print("测试：功能一 - 查看所有车次")
print("=" * 50)
show_trains()

print("\n" + "=" * 50)
print("测试：功能二 - 查询车次（北京）")
print("=" * 50)
search_train("北京")

print("\n" + "=" * 50)
print("测试：功能三 - 购买车票")
print("=" * 50)
buy_ticket("张三", "320xxxx", "G1003", 2)
buy_ticket("李四", "310xxxx", "G1001", 3)
buy_ticket("王五", "330xxxx", "G1002", 5)

print("\n" + "=" * 50)
print("测试：功能四 - 查看我的订单")
print("=" * 50)
show_orders()

print("\n" + "=" * 50)
print("测试：功能六 - 统计收入")
print("=" * 50)
count_money()

print("\n" + "=" * 50)
print("测试：功能五 - 退票")
print("=" * 50)
refund("320xxxx")

print("\n" + "=" * 50)
print("测试：退票后统计")
print("=" * 50)
count_money()

print("\n" + "=" * 50)
print("测试：余票不足情况")
print("=" * 50)
buy_ticket("赵六", "340xxxx", "G1003", 20)

print("\n" + "=" * 50)
print("测试：无效车次")
print("=" * 50)
buy_ticket("孙七", "350xxxx", "G9999", 1)

print("\n" + "=" * 50)
print("所有测试完成！")
print("=" * 50)