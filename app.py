import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta

st.set_page_config(
    page_title='홈앤쇼핑 일일 매출 현황',
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.markdown("""
<style>
    body { font-family: 'Malgun Gothic', sans-serif; }
    h1, h2, h3 { font-family: 'Malgun Gothic', sans-serif; }
</style>
""", unsafe_allow_html=True)

df = pd.read_csv('주문_데이터.csv')
df['주문일자'] = pd.to_datetime(df['주문일자'])

today = df['주문일자'].max().date()
yesterday = today - timedelta(days=1)

today_sales = df[df['주문일자'].dt.date == today]['상품취급액'].sum()
yesterday_sales = df[df['주문일자'].dt.date == yesterday]['상품취급액'].sum()
growth_rate = ((today_sales - yesterday_sales) / yesterday_sales * 100) if yesterday_sales > 0 else 0

st.title('홈앤쇼핑 일일 매출 현황')

col1, col2, col3 = st.columns(3)
with col1:
    st.metric('오늘 매출', f'₩{today_sales:,.0f}')
with col2:
    st.metric('어제 매출', f'₩{yesterday_sales:,.0f}')
with col3:
    delta_text = f'+{growth_rate:.1f}%' if growth_rate >= 0 else f'{growth_rate:.1f}%'
    st.metric('어제 대비 증감률', delta_text, delta_color='normal')

st.divider()

chart_col1, chart_col2 = st.columns(2)

daily_sales = df.groupby(df['주문일자'].dt.date)['상품취급액'].sum().reset_index()
daily_sales.columns = ['date', 'sales']
daily_sales['date'] = pd.to_datetime(daily_sales['date'])

with chart_col1:
    st.subheader('일별 매출 추이')
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=daily_sales['date'],
        y=daily_sales['sales'],
        mode='lines+markers',
        name='매출',
        line=dict(color='#4A90D9', width=3),
        marker=dict(size=10, color='#4A90D9'),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>매출: ₩%{y:,.0f}<extra></extra>'
    ))
    fig_line.update_layout(
        font_family='Malgun Gothic',
        hovermode='x unified',
        showlegend=False,
        margin=dict(l=0, r=0, t=30, b=0),
        height=400
    )
    fig_line.update_xaxes(title_text='날짜')
    fig_line.update_yaxes(title_text='매출 (₩)')
    st.plotly_chart(fig_line, use_container_width=True)

today_category_sales = df[df['주문일자'].dt.date == today].groupby('카테고리')['상품취급액'].sum().reset_index()
today_category_sales.columns = ['category', 'sales']

with chart_col2:
    st.subheader('카테고리별 매출 비중 (오늘)')
    colors = ['#4A90D9', '#5BA85F', '#E8734A', '#9B7FB5', '#F5A623', '#7ED321']
    fig_pie = go.Figure(data=[go.Pie(
        labels=today_category_sales['category'],
        values=today_category_sales['sales'],
        marker=dict(colors=colors),
        hovertemplate='<b>%{label}</b><br>매출: ₩%{value:,.0f}<br>비중: %{percent}<extra></extra>'
    )])
    fig_pie.update_layout(
        font_family='Malgun Gothic',
        margin=dict(l=0, r=0, t=30, b=0),
        height=400
    )
    st.plotly_chart(fig_pie, use_container_width=True)
