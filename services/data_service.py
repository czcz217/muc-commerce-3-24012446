import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def load_user_data():
    file_path = os.path.join(DATA_DIR, 'user_data.csv')
    return pd.read_csv(file_path)

def load_segment_data():
    file_path = os.path.join(DATA_DIR, 'segment_analysis.csv')
    return pd.read_csv(file_path)

def get_filtered_dataframe(category='全部'):
    df = load_user_data()
    
    if category != '全部':
        df = df[df['PreferedOrderCat'] == category]
    
    return df

def get_metrics(df):
    total_users = len(df)
    churn_users = df['Churn'].sum()
    churn_rate = (churn_users / total_users) * 100 if total_users > 0 else 0
    avg_orders = df['OrderCount'].mean()
    
    return {
        'total_users': int(total_users),
        'churn_users': int(churn_users),
        'churn_rate': round(churn_rate, 1),
        'avg_orders': round(avg_orders, 1)
    }

def get_highest_risk_segment():
    df = load_segment_data()
    df['流失率'] = df['流失率'] * 100
    highest_risk = df.loc[df['流失率'].idxmax()]
    
    return {
        'segment': highest_risk['Tenure'],
        'churn_rate': round(highest_risk['流失率'], 1),
        'user_count': int(highest_risk['用户数']),
        'churn_count': int(highest_risk['流失人数'])
    }

def get_category_options():
    df = load_user_data()
    categories = ['全部'] + sorted(df['PreferedOrderCat'].unique().tolist())
    return categories

def get_table_data(df):
    display_cols = ['CustomerID', 'PreferedOrderCat', 'OrderCount', 'CashbackAmount', 'Churn']
    return df[display_cols].head(10).to_dict('records')

def get_dashboard_data(category='全部'):
    df = get_filtered_dataframe(category)
    metrics = get_metrics(df)
    highest_risk = get_highest_risk_segment()
    categories = get_category_options()
    table_data = get_table_data(df)
    
    return {
        'metrics': metrics,
        'highest_risk': highest_risk,
        'categories': categories,
        'table_data': table_data,
        'filtered_count': len(df)
    }