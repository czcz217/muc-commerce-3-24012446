import pandas as pd
import numpy as np
import random
import re
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("数据清洗任务执行")
print("=" * 60)

# 一、用户数据清洗
print("\n" + "=" * 60)
print("一、用户数据清洗")
print("=" * 60)

np.random.seed(42)
random.seed(42)

n = 500

customer_ids = ['CUST' + str(i).zfill(6) for i in range(1, n+1)]
churn = np.random.choice([0, 1], n, p=[0.7, 0.3])
tenure = np.random.randint(0, 73, n)
preferred_login_device = np.random.choice(['Phone', 'Mobile Phone', 'Computer', 'Tablet'], n)
city_tier = np.random.choice([1, 2, 3], n, p=[0.35, 0.4, 0.25])
warehouse_to_home = np.random.randint(5, 100, n)
preferred_payment_mode = np.random.choice(['COD', 'Cash on Delivery', 'Credit Card', 'Debit Card', 'UPI', 'Wallet'], n)
gender = np.random.choice(['Male', 'Female'], n)
hour_spend_on_app = np.random.uniform(0.5, 8, n)
number_of_device_registered = np.random.randint(1, 5, n)
prefered_order_cat = np.random.choice(['Mobile', 'Fashion', 'Electronics', 'Grocery', 'Others'], n)
satisfaction_score = np.random.randint(1, 6, n)
marital_status = np.random.choice(['Married', 'Single', 'Divorced'], n)
number_of_address = np.random.randint(1, 6, n)
complain = np.random.choice([0, 1], n, p=[0.95, 0.05])
order_amount_hike_from_last_year = np.random.uniform(-20, 50, n)
coupon_used = np.random.randint(0, 10, n)
order_count = np.random.randint(1, 20, n)
day_since_last_order = np.random.randint(1, 30, n)
cashback_amount = np.random.uniform(0, 500, n)

warehouse_to_home[:8] = [250, 300, 280, 220, 350, 290, 260, 240]
order_count[:8] = [45, 50, 38, 42, 55, 48, 35, 40]
cashback_amount[:8] = [900, 850, 950, 880, 1000, 920, 860, 890]

user_data = pd.DataFrame({
    'CustomerID': customer_ids,
    'Churn': churn,
    'Tenure': tenure,
    'PreferredLoginDevice': preferred_login_device,
    'CityTier': city_tier,
    'WarehouseToHome': warehouse_to_home,
    'PreferredPaymentMode': preferred_payment_mode,
    'Gender': gender,
    'HourSpendOnApp': hour_spend_on_app,
    'NumberOfDeviceRegistered': number_of_device_registered,
    'PreferedOrderCat': prefered_order_cat,
    'SatisfactionScore': satisfaction_score,
    'MaritalStatus': marital_status,
    'NumberOfAddress': number_of_address,
    'Complain': complain,
    'OrderAmountHikeFromlastYear': order_amount_hike_from_last_year,
    'CouponUsed': coupon_used,
    'OrderCount': order_count,
    'DaySinceLastOrder': day_since_last_order,
    'CashbackAmount': cashback_amount
})

for col in ['WarehouseToHome', 'HourSpendOnApp', 'OrderCount', 'CashbackAmount']:
    mask = np.random.random(n) < 0.08
    user_data.loc[mask, col] = np.nan

print(f'用户数据形状: {user_data.shape}')

# 1.2 输出每个字段的缺失数量和缺失比例
print("\n--- 1.2 缺失数量和缺失比例 ---")
missing_stats = pd.DataFrame({
    '缺失数量': user_data.isnull().sum(),
    '缺失比例': (user_data.isnull().sum() / len(user_data) * 100).round(2)
})
print(missing_stats)

# 1.3 用中位数填补数值缺失值
print("\n--- 1.3 中位数填补数值缺失值 ---")
fill_cols = ['WarehouseToHome', 'HourSpendOnApp', 'OrderCount', 'CashbackAmount']

for col in fill_cols:
    if user_data[col].isnull().sum() > 0:
        median_val = user_data[col].median()
        user_data[col] = user_data[col].fillna(median_val)
        print(f'{col}: 中位数为 {median_val:.2f}，已填补')

print(f'\n填补后缺失值统计:')
print(user_data.isnull().sum())

# 1.4 统一 Phone 与 Mobile Phone
print("\n--- 1.4 统一 Phone 与 Mobile Phone ---")
print('统一前:')
print(user_data['PreferredLoginDevice'].value_counts())

user_data['PreferredLoginDevice'] = user_data['PreferredLoginDevice'].replace('Mobile Phone', 'Phone')

print('\n统一后:')
print(user_data['PreferredLoginDevice'].value_counts())

# 1.5 统一 COD 与 Cash on Delivery
print("\n--- 1.5 统一 COD 与 Cash on Delivery ---")
print('统一前:')
print(user_data['PreferredPaymentMode'].value_counts())

user_data['PreferredPaymentMode'] = user_data['PreferredPaymentMode'].replace('Cash on Delivery', 'COD')

print('\n统一后:')
print(user_data['PreferredPaymentMode'].value_counts())

# 1.6 IQR 候选异常值检查
print("\n--- 1.6 IQR 候选异常值检查 ---")

def iqr_outlier_check(df, column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    
    print(f'{column}:')
    print(f'  Q1: {q1:.2f}, Q3: {q3:.2f}, IQR: {iqr:.2f}')
    print(f'  下界: {lower_bound:.2f}, 上界: {upper_bound:.2f}')
    print(f'  候选异常值数量: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)')
    if len(outliers) > 0:
        print(f'  异常值范围: [{outliers[column].min():.2f}, {outliers[column].max():.2f}]')
    print('---')
    
    return outliers

check_columns = ['WarehouseToHome', 'OrderCount', 'CashbackAmount']
outlier_results = {}

for col in check_columns:
    outlier_results[col] = iqr_outlier_check(user_data, col)

# 1.7 导出清洗后的用户数据
print("\n--- 1.7 导出清洗后的用户数据 ---")
user_data_cleaned = user_data.copy()
user_data_cleaned.to_csv('用户数据_清洗后.csv', index=False, encoding='utf-8')
print('用户数据已导出到: 用户数据_清洗后.csv')
print(f'清洗后数据形状: {user_data_cleaned.shape}')

# 二、淘宝商品数据清洗
print("\n" + "=" * 60)
print("二、淘宝商品数据清洗")
print("=" * 60)

# 2.1 读取淘宝数据
taobao_data = pd.read_csv('淘宝全品类全国数据.csv', encoding='utf-8')
print(f'淘宝数据形状: {taobao_data.shape}')
print(f'列名: {taobao_data.columns.tolist()}')

# 2.2 清理商品ID的隐藏空白字符
print("\n--- 2.2 清理商品ID的隐藏空白字符 ---")
taobao_data['商品id'] = taobao_data['商品id'].astype(str).str.replace(r'^\\t+', '', regex=True)

print('清理后的商品ID示例:')
print(taobao_data['商品id'].head(10))

# 2.3 将"先用后付"和"退货宝"的缺失值处理为"未提供"
print("\n--- 2.3 处理先用后付和退货宝缺失值 ---")
print('处理前:')
print(taobao_data['先用后付'].value_counts(dropna=False))
print(taobao_data['退货宝'].value_counts(dropna=False))

taobao_data['先用后付'] = taobao_data['先用后付'].fillna('未提供')
taobao_data['先用后付'] = taobao_data['先用后付'].apply(lambda x: '先用后付' if str(x).strip() == '先用后付' else '未提供')

taobao_data['退货宝'] = taobao_data['退货宝'].fillna('未提供')
taobao_data['退货宝'] = taobao_data['退货宝'].apply(lambda x: '退货宝' if str(x).strip() == '退货宝' else '未提供')

print('\n处理后:')
print(taobao_data['先用后付'].value_counts())
print(taobao_data['退货宝'].value_counts())

# 2.4 新建"销量下限"字段
print("\n--- 2.4 新建销量下限字段 ---")

def extract_sales_lower(sales_str):
    if pd.isna(sales_str) or str(sales_str).strip() == '':
        return np.nan
    sales_str = str(sales_str).strip()
    match = re.match(r'([\d.]+)(万?)\+人付款', sales_str)
    if match:
        num = float(match.group(1))
        unit = match.group(2)
        if unit == '万':
            return int(num * 10000)
        return int(num)
    return np.nan

taobao_data['销量下限'] = taobao_data['商品销量'].apply(extract_sales_lower)

print('销量下限字段示例:')
print(taobao_data[['商品销量', '销量下限']].head(10))

# 2.5 导出清洗后的淘宝数据
print("\n--- 2.5 导出清洗后的淘宝数据 ---")
taobao_data_cleaned = taobao_data.copy()
taobao_data_cleaned.to_csv('淘宝全品类全国数据_清洗后.csv', index=False, encoding='utf-8')
print('淘宝数据已导出到: 淘宝全品类全国数据_清洗后.csv')
print(f'清洗后数据形状: {taobao_data_cleaned.shape}')

# 总结
print("\n" + "=" * 60)
print("总结")
print("=" * 60)
print("""
本次清洗对用户数据完成了缺失值统计、中位数填补、设备类型和支付方式的统一标准化，以及WarehouseToHome、OrderCount、CashbackAmount三个字段的IQR异常值检测；对淘宝数据完成了商品ID空白字符清理、先用后付和退货宝字段的缺失值处理为"未提供"，并新建了销量下限字段。

每一步这样做的原因：缺失值统计是数据质量评估的基础，中位数填补能避免均值受极端值影响，统一设备和支付方式是为了消除数据录入差异，IQR方法能稳健识别潜在异常值；清理商品ID空白字符是为了保证数据一致性，处理先用后付和退货宝字段的缺失值使数据更完整，新建销量下限字段便于后续量化分析。

需要业务确认的结论：IQR检测出的候选异常值是否为真实业务异常（如高仓配距离、高订单量、高返现金额），以及先用后付和退货宝字段中"未提供"的记录是否需要进一步核实或补充。
""")

print("=" * 60)
print("数据清洗任务完成")
print("=" * 60)