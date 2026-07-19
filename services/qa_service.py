import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def load_user_data():
    file_path = os.path.join(DATA_DIR, 'user_data.csv')
    return pd.read_csv(file_path)

def load_segment_data():
    file_path = os.path.join(DATA_DIR, 'segment_analysis.csv')
    return pd.read_csv(file_path)

def answer_question(question):
    question = question.lower().strip()
    
    if '用户' in question and ('多少' in question or '规模' in question):
        df = load_user_data()
        total = len(df)
        return f"系统中共有 {total} 名用户。"
    
    elif '流失率' in question or '流失' in question:
        df = load_user_data()
        total = len(df)
        churn = df['Churn'].sum()
        rate = (churn / total) * 100 if total > 0 else 0
        return f"总体流失率为 {rate:.1f}%，共有 {int(churn)} 名流失用户。"
    
    elif '品类' in question and ('最多' in question or '偏好' in question):
        df = load_user_data()
        category_counts = df['PreferedOrderCat'].value_counts()
        top_category = category_counts.idxmax()
        top_count = category_counts.max()
        return f"用户最多的品类是 {top_category}，共有 {top_count} 名用户偏好该品类。"
    
    elif '阶段' in question and ('风险' in question or '最高' in question):
        df = load_segment_data()
        df['流失率'] = df['流失率'] * 100
        highest_risk = df.loc[df['流失率'].idxmax()]
        return f"风险最高的生命周期阶段是 {highest_risk['Tenure']}，流失率为 {highest_risk['流失率']:.1f}%。"
    
    elif '订单数' in question or '订单' in question:
        df = load_user_data()
        avg_orders = df['OrderCount'].mean()
        median_orders = df['OrderCount'].median()
        return f"平均订单数为 {avg_orders:.1f}，中位数订单数为 {median_orders:.1f}。"
    
    else:
        return "抱歉，我暂时无法回答这个问题。支持的问题类型包括：总体规模、流失情况、偏好品类、生命周期风险、订单情况。"