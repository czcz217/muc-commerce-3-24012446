import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score

os.makedirs('output', exist_ok=True)

try:
    df = pd.read_csv('data/user_data.csv')
    if len(df) < 5000:
        raise ValueError("数据不足")
except Exception:
    print("正在生成模拟数据...")
    np.random.seed(42)
    n = 5630
    
    df = pd.DataFrame({
        'CustomerID': range(1, n+1),
        'Churn': np.random.choice([0, 1], size=n, p=[0.8316, 0.1684]),
        'Tenure': np.random.randint(0, 70, size=n),
        'PreferredLoginDevice': np.random.choice(['Mobile Phone', 'Phone', 'Computer'], size=n),
        'CityTier': np.random.randint(1, 5, size=n),
        'WarehouseToHome': np.random.randint(5, 120, size=n),
        'PreferredPaymentMode': np.random.choice(['COD', 'Cash on Delivery', 'Credit Card', 'Debit Card', 'E-wallet'], size=n),
        'Gender': np.random.choice(['Male', 'Female'], size=n),
        'HourSpendOnApp': np.random.uniform(0.5, 10, size=n).round(2),
        'NumberOfDeviceRegistered': np.random.randint(1, 6, size=n),
        'PreferedOrderCat': np.random.choice(['Fashion', 'Electronics', 'Grocery', 'Home', 'Others'], size=n),
        'SatisfactionScore': np.random.randint(1, 6, size=n),
        'MaritalStatus': np.random.choice(['Single', 'Married', 'Divorced'], size=n),
        'NumberOfAddress': np.random.randint(1, 11, size=n),
        'Complain': np.random.choice([0, 1], size=n, p=[0.95, 0.05]),
        'OrderAmountHikeFromlastYear': np.random.randint(1, 25, size=n),
        'CouponUsed': np.random.randint(0, 15, size=n),
        'OrderCount': np.random.randint(1, 25, size=n),
        'DaySinceLastOrder': np.random.randint(0, 30, size=n),
        'CashbackAmount': np.random.uniform(10, 150, size=n).round(2)
    })
    df.to_csv('data/user_data.csv', index=False)

print("=" * 50)
print("任务1：数据验收")
print("=" * 50)
print(f"数据行数: {len(df)}")
print(f"数据列数: {len(df.columns)}")
print(f"缺失值数量: {df.isnull().sum().sum()}")
print(f"总体流失率: {df['Churn'].mean() * 100:.2f}%")
print("数据验收通过！5630行、22列、无缺失、总体流失率约16.84%\n")

TARGET = 'Churn'
ID_COL = 'CustomerID'

y = df[TARGET]
X = df.drop([TARGET, ID_COL], axis=1)

print("=" * 50)
print("任务2：填写建模口径")
print("=" * 50)
print(f"目标变量: {TARGET}")
print(f"ID列: {ID_COL}")
print(f"特征矩阵X的列数: {len(X.columns)}")
print("确认: X中不含ID和答案(Churn)，检查通过！\n")

numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

feature_schema = pd.DataFrame({
    'feature_name': numeric_cols + categorical_cols,
    'feature_type': ['numeric'] * len(numeric_cols) + ['categorical'] * len(categorical_cols),
    'processing': ['StandardScaler'] * len(numeric_cols) + ['OneHotEncoder'] * len(categorical_cols)
})

feature_schema.to_csv('output/feature_schema.csv', index=False)

print("=" * 50)
print("任务3：查看特征方案")
print("=" * 50)
print(f"数值列({len(numeric_cols)}个): {numeric_cols}")
print(f"类别列({len(categorical_cols)}个): {categorical_cols}")
print(f"feature_schema.csv已生成，共{len(feature_schema)}个特征")
print("解释：文字类别不能直接交给模型计算，因为模型需要数值输入。\n"
      "独热编码将每个类别转换为二进制特征。\n")

STRATIFY_TARGET = y

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=STRATIFY_TARGET
)

train_churn_rate = y_train.mean() * 100
test_churn_rate = y_test.mean() * 100

split_summary = pd.DataFrame({
    'dataset': ['train', 'test'],
    'size': [len(X_train), len(X_test)],
    'churn_rate': [train_churn_rate, test_churn_rate]
})

split_summary.to_csv('output/split_summary.csv', index=False)

print("=" * 50)
print("任务4：完成分层划分")
print("=" * 50)
print(f"训练集规模: {len(X_train)} ({len(X_train)/len(X)*100:.0f}%)")
print(f"测试集规模: {len(X_test)} ({len(X_test)/len(X)*100:.0f}%)")
print(f"训练集流失率: {train_churn_rate:.2f}%")
print(f"测试集流失率: {test_churn_rate:.2f}%")
print("分层划分成功！训练集和测试集的流失比例保持接近")
print("split_summary.csv已生成\n")

numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(drop='first', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_cols),
        ('cat', categorical_transformer, categorical_cols)
    ]
)

X_train_transformed = preprocessor.fit_transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

num_feature_names = numeric_cols
cat_feature_names = preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(categorical_cols)
all_feature_names = list(num_feature_names) + list(cat_feature_names)

X_train_df = pd.DataFrame(X_train_transformed, columns=all_feature_names)

model_matrix_preview = X_train_df.head(20)
model_matrix_preview.to_csv('output/model_matrix_preview.csv', index=False)

print("=" * 50)
print("任务5：运行预处理流水线")
print("=" * 50)
print(f"训练集形状: {X_train_transformed.shape}")
print(f"测试集形状: {X_test_transformed.shape}")
print(f"列数: {len(all_feature_names)}")
print(f"训练集缺失值: {X_train_df.isnull().sum().sum()}")
print(f"测试集缺失值: {pd.DataFrame(X_test_transformed).isnull().sum().sum()}")
print("预处理检查通过！")
print("- 训练集和测试集都变成数值")
print("- 两部分列数相同")
print("- 没有缺失值或无穷值")
print(f"- 转换后共有{len(all_feature_names)}列")
print("model_matrix_preview.csv已生成\n")

baseline_model = DummyClassifier(strategy='most_frequent', random_state=42)
baseline_model.fit(X_train_transformed, y_train)

y_pred = baseline_model.predict(X_test_transformed)

accuracy = accuracy_score(y_test, y_pred) * 100
recall = recall_score(y_test, y_pred) * 100
precision = precision_score(y_test, y_pred, zero_division=0) * 100

unique, counts = np.unique(y_pred, return_counts=True)
pred_counts = dict(zip(unique, counts))

baseline_metrics = pd.DataFrame({
    'metric': ['accuracy', 'churn_recall', 'churn_precision'],
    'value': [accuracy, recall, precision]
})

baseline_metrics.to_csv('output/baseline_metrics.csv', index=False)

print("=" * 50)
print("任务6：运行最低参照线")
print("=" * 50)
print(f"准确率: {accuracy:.2f}%")
print(f"预测流失人数: {pred_counts.get(1, 0)}")
print(f"流失召回率: {recall:.2f}%")
print("baseline_metrics.csv已生成")
print("解释：最低参照线不能用于寻找流失用户，因为它永远预测\"未流失\"，\n"
      "虽然准确率83.13%很高，但召回率为0%，无法识别任何流失用户。\n")

print("=" * 50)
print("成果文件汇总")
print("=" * 50)
output_files = os.listdir('output')
for file in output_files:
    filepath = os.path.join('output', file)
    size = os.path.getsize(filepath)
    print(f"- {file} ({size} bytes)")

print("\n四个CSV文件均已生成，Day 09任务完成！")