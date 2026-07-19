# 电商用户行为分析 Web 项目

## 个人信息

- 姓名：陈文卓
- 学号：24012446

## 项目结构

```
day07_24012446_陈文卓/
├── app.py                    # Flask 主应用
├── requirements.txt          # 依赖列表
├── README.md                 # 项目说明
├── data/                     # 数据文件
│   ├── segment_analysis.csv  # 生命周期分析结果
│   └── user_data.csv         # 用户数据
├── services/                 # 服务模块
│   ├── data_service.py       # 数据服务（指标卡、筛选）
│   └── qa_service.py         # 问答服务（离线问答）
├── static/
│   └── images/               # 图表文件
│       ├── 01_churn_bar.png
│       └── 03_ordered_line.png
├── templates/                # HTML 模板
│   ├── login.html            # 登录页
│   └── dashboard.html        # 看板页
└── screenshots/              # 验收截图
```

## 核心功能

1. **登录闭环** - 使用 Session 实现简化登录验证
2. **数据看板** - 展示4张指标卡、2张图表、1张数据表
3. **品类筛选** - 支持按偏好品类筛选数据
4. **离线问答** - 支持4类问题：总体规模、流失情况、偏好品类、生命周期、订单情况

## 运行方法

```bash
# 安装依赖
pip install -r requirements.txt

# 运行项目
python app.py

# 访问地址
http://127.0.0.1:5000

# 登录账号
用户名: student
密码: day07
```

## 必选拓展

### 拓展A：导出当前筛选结果

- 新增 `/download` 路由，支持按品类导出 CSV
- 使用方法：`http://127.0.0.1:5000/download?category=Fashion`
- 导出的文件名包含所选品类信息

## 未解决问题

无