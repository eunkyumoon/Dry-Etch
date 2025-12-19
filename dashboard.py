"""
Y2O3 Focus Ring 실시간 모니터링 대시보드
통합 분석 대시보드 - 4가지 레이아웃 스타일 통합
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

# refactored 모듈 import
sys.path.insert(0, str(Path(__file__).parent))
from refactored.anomaly_detector import AnomalyDetector
from refactored.config import Config
from refactored.data_collector import DataCollector
from refactored.models import (
    OESData,
    ProcessData,
    RFParameters,
    SimulationParameters,
    SystemStatus,
)
from refactored.rul_predictor import RULPredictor
from refactored.wear_estimator import WearEstimator

# 페이지 설정
st.set_page_config(
    page_title="Y2O3 Focus Ring 분석 대시보드",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS 스타일
CUSTOM_CSS = """
<style>
    .main {
        background-color: #ffffff;
        padding: 10px;
    }
    
    h1 {
        color: #333333;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
        font-size: 20px;
    }
    
    /* 네비게이션 바 */
    .nav-bar {
        background-color: #e9ecef;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-around;
    }
    
    .nav-item {
        padding: 5px 15px;
        cursor: pointer;
        color: #333333;
        font-weight: 500;
        font-size: 14px;
    }
    
    .nav-item:hover {
        background-color: #dee2e6;
        border-radius: 3px;
    }
    
    /* KPI 카드 */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .kpi-label {
        font-size: 12px;
        color: #666666;
        margin-bottom: 5px;
    }
    
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: #333333;
        margin: 10px 0;
    }
    
    .kpi-change {
        font-size: 11px;
        font-weight: bold;
    }
    
    .kpi-change.positive {
        color: #28a745;
    }
    
    .kpi-change.negative {
        color: #dc3545;
    }
    
    /* 테이블 스타일 */
    .dataframe {
        font-size: 11px;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def calculate_simulation_parameters(hour: int) -> SimulationParameters:
    """시뮬레이션 파라미터 계산"""
    wear_progress = hour / Config.WEAR_PROGRESS_BASE_HOURS
    return SimulationParameters(
        wear_progress=wear_progress,
        vpp=Config.INITIAL_VPP * (1 + wear_progress * Config.VPP_INCREASE_RATE),
        vdc=Config.INITIAL_VDC * (1 + wear_progress * Config.VDC_INCREASE_RATE),
        phase=Config.INITIAL_PHASE + wear_progress * Config.PHASE_INCREASE_RATE,
        yttrium_peak=Config.INITIAL_YTTRIUM_PEAK
        * (1 - wear_progress * Config.YTTRIUM_DECREASE_RATE),
        fo_ratio=Config.DEFAULT_FO_RATIO,
    )


def create_navigation_bar():
    """네비게이션 바 생성"""
    nav_items = ["실적 요약", "트렌드 분석", "파라미터 분석", "위험 분석"]
    nav_html = '<div class="nav-bar">'
    for item in nav_items:
        nav_html += f'<div class="nav-item">{item}</div>'
    nav_html += '</div>'
    return nav_html


def create_kpi_card(label: str, value: str, change: float = None):
    """KPI 카드 생성"""
    change_html = ""
    if change is not None:
        change_class = "positive" if change >= 0 else "negative"
        change_symbol = "▲" if change >= 0 else "▼"
        change_html = f'<div class="kpi-change {change_class}">{change_symbol}{abs(change):.1f}%</div>'
    
    return f'''
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {change_html}
    </div>
    '''


def main():
    """메인 대시보드"""
    # 헤더
    st.markdown("<h1>분석 대시보드</h1>", unsafe_allow_html=True)
    
    # 네비게이션 바
    st.markdown(create_navigation_bar(), unsafe_allow_html=True)
    
    # 사이드바
    with st.sidebar:
        st.header("⚙️ 설정")
        chamber = st.selectbox("챔버 선택", ["Chamber1", "Chamber2", "Chamber3", "Chamber4"])
        hours = st.slider("누적 시간 (시간)", 0, 2000, 500, 50)
        auto_refresh = st.checkbox("자동 새로고침", value=False)
    
    # 시뮬레이션 데이터 생성
    sim_params = calculate_simulation_parameters(hours)
    
    # 컴포넌트 초기화
    collector = DataCollector()
    wear_estimator = WearEstimator(initial_thickness=Config.INITIAL_THICKNESS)
    rul_predictor = RULPredictor()
    anomaly_detector = AnomalyDetector()
    
    wear_estimator.set_initial_state(Config.INITIAL_VPP, Config.INITIAL_YTTRIUM_PEAK)
    
    # 데이터 수집 및 계산
    rf_params = RFParameters(
        vpp=sim_params.vpp,
        vdc=sim_params.vdc,
        phase=sim_params.phase,
        matcher_pos=Config.DEFAULT_MATCHER_POS,
        timestamp=datetime.now(),
    )
    oes_data = OESData(
        yttrium_peak=sim_params.yttrium_peak,
        fo_ratio=sim_params.fo_ratio,
        timestamp=datetime.now(),
    )
    
    collector.collect_rf_parameters(rf_params)
    collector.collect_oes_data(oes_data)
    
    wear_state = wear_estimator.calculate_wear_state(
        sim_params.vpp, sim_params.yttrium_peak, float(hours)
    )
    
    process_data = ProcessData(
        rf_params=rf_params,
        oes_data=oes_data,
        cumulative_rf_time=float(hours),
    )
    rul_prediction = rul_predictor.predict(process_data)
    arcing_risk, risk_level = anomaly_detector.detect_arcing_risk(process_data, wear_state)
    
    # ========== 레이아웃 1: 상단 좌측 ==========
    col1, col2 = st.columns(2)
    
    with col1:
        # 상단 테이블들
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.markdown("#### RF 파라미터 요약")
            rf_table = pd.DataFrame({
                '항목': ['Total', 'Vpp', 'Vdc', 'Phase'],
                'CE': [f"{sim_params.vpp * 100:.0f}", f"{sim_params.vpp:.1f}", f"{abs(sim_params.vdc):.1f}", f"{sim_params.phase:.1f}"],
                'MC': [f"{sim_params.vpp * 80:.0f}", f"{sim_params.vpp * 0.9:.1f}", f"{abs(sim_params.vdc) * 0.9:.1f}", f"{sim_params.phase * 0.95:.1f}"],
                'OC': [f"{sim_params.vpp * 60:.0f}", f"{sim_params.vpp * 0.85:.1f}", f"{abs(sim_params.vdc) * 0.85:.1f}", f"{sim_params.phase * 0.9:.1f}"],
            })
            st.dataframe(rf_table, use_container_width=True, hide_index=True)
        
        with col_t2:
            st.markdown("#### 마모 상태 요약")
            wear_table = pd.DataFrame({
                '항목': ['Total', '마모 진행도', '잔여 두께', 'RUL'],
                '누적 마모': [f"{wear_state.degradation_index * 1000:.0f}", f"{wear_state.degradation_index:.1f}%", f"{wear_state.remaining_thickness:.1f}μm", f"{rul_prediction.rul_hours:.0f}시간"],
                '마모율': [f"{(wear_state.degradation_index / max(hours, 1) * 100):.2f}%", f"{wear_state.degradation_index:.1f}%", f"{(wear_state.degradation_index / 10):.1f}%", f"{(rul_prediction.rul_hours / 100):.0f}%"],
                '위험도': [f"{arcing_risk * 100:.0f}", f"{arcing_risk:.1f}%", f"{arcing_risk * 0.8:.1f}%", f"{arcing_risk * 0.6:.1f}%"],
            })
            st.dataframe(wear_table, use_container_width=True, hide_index=True)
        
        # 스택 바 차트들
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            st.markdown("#### 마모 진행도 분포")
            stacked1 = go.Figure()
            stacked1.add_trace(go.Bar(
                name='정상',
                x=['마모 상태'],
                y=[100 - wear_state.degradation_index],
                marker_color='#28a745',
            ))
            stacked1.add_trace(go.Bar(
                name='마모',
                x=['마모 상태'],
                y=[wear_state.degradation_index],
                marker_color='#ffc107',
            ))
            stacked1.update_layout(
                barmode='stack',
                height=200,
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=20, b=20),
                font=dict(size=10, color='#333333'),
            )
            st.plotly_chart(stacked1, use_container_width=True)
        
        with col_s2:
            st.markdown("#### 위험도 분포")
            stacked2 = go.Figure()
            stacked2.add_trace(go.Bar(
                name='안전',
                x=['위험 상태'],
                y=[100 - arcing_risk],
                marker_color='#28a745',
            ))
            stacked2.add_trace(go.Bar(
                name='위험',
                x=['위험 상태'],
                y=[arcing_risk],
                marker_color='#dc3545',
            ))
            stacked2.update_layout(
                barmode='stack',
                height=200,
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=20, b=20),
                font=dict(size=10, color='#333333'),
            )
            st.plotly_chart(stacked2, use_container_width=True)
        
        # 라인 차트
        st.markdown("#### 시간별 추이")
        time_points = []
        vpp_values = []
        for h in range(max(0, hours - 60), hours + 1, 5):
            params = calculate_simulation_parameters(h)
            time_points.append(datetime.now() - timedelta(hours=hours - h))
            vpp_values.append(params.vpp)
        
        trend_df = pd.DataFrame({
            'timestamp': time_points,
            'Vpp': vpp_values,
        })
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=trend_df['timestamp'],
            y=trend_df['Vpp'],
            mode='lines',
            line=dict(color='#28a745', width=2),
            fill='tozeroy',
            fillcolor='rgba(40, 167, 69, 0.1)',
        ))
        fig_trend.update_layout(
            height=200,
            xaxis=dict(tickfont=dict(color='#666666'), gridcolor='rgba(0,0,0,0.1)'),
            yaxis=dict(tickfont=dict(color='#666666'), gridcolor='rgba(0,0,0,0.1)'),
            margin=dict(l=50, r=20, t=20, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        # 상단 테이블들
        col_t3, col_t4 = st.columns(2)
        
        with col_t3:
            st.markdown("#### RF 파라미터 상세")
            rf_detail_table = pd.DataFrame({
                '항목': ['Total', 'Vpp', 'Vdc', 'Phase'],
                'CE': [f"{sim_params.vpp * 100:.0f}", f"{sim_params.vpp:.1f}", f"{abs(sim_params.vdc):.1f}", f"{sim_params.phase:.1f}"],
                'MC': [f"{sim_params.vpp * 80:.0f}", f"{sim_params.vpp * 0.9:.1f}", f"{abs(sim_params.vdc) * 0.9:.1f}", f"{sim_params.phase * 0.95:.1f}"],
                'OC': [f"{sim_params.vpp * 60:.0f}", f"{sim_params.vpp * 0.85:.1f}", f"{abs(sim_params.vdc) * 0.85:.1f}", f"{sim_params.phase * 0.9:.1f}"],
            })
            st.dataframe(rf_detail_table, use_container_width=True, hide_index=True)
        
        with col_t4:
            st.markdown("#### OES 데이터 상세")
            oes_detail_table = pd.DataFrame({
                '항목': ['Total', 'Yttrium Peak', 'F/O Ratio'],
                '누적 값': [f"{sim_params.yttrium_peak * 1000:.0f}", f"{sim_params.yttrium_peak:.3f}", f"{sim_params.fo_ratio:.2f}"],
                '현재 값': [f"{sim_params.yttrium_peak * 100:.1f}", f"{sim_params.yttrium_peak:.3f}", f"{sim_params.fo_ratio:.2f}"],
                '변화율': [f"{(sim_params.yttrium_peak / Config.INITIAL_YTTRIUM_PEAK - 1) * 100:.1f}%", f"{(sim_params.yttrium_peak / Config.INITIAL_YTTRIUM_PEAK - 1) * 100:.1f}%", "0.0%"],
            })
            st.dataframe(oes_detail_table, use_container_width=True, hide_index=True)
        
        # 파이 차트들
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown("#### 마모 비율")
            pie1 = go.Figure(data=[go.Pie(
                labels=['정상', '주의', '위험'],
                values=[
                    100 - wear_state.degradation_index if wear_state.degradation_index < 50 else 50,
                    wear_state.degradation_index - 30 if wear_state.degradation_index > 30 else 0,
                    30 if wear_state.degradation_index > 30 else wear_state.degradation_index,
                ],
                hole=0.4,
                marker=dict(colors=['#28a745', '#ffc107', '#dc3545']),
                textinfo='label+percent',
                textfont=dict(size=10, color='#333333'),
            )])
            pie1.update_layout(
                height=200,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(font=dict(size=9, color='#666666')),
            )
            st.plotly_chart(pie1, use_container_width=True)
        
        with col_p2:
            st.markdown("#### 위험 비율")
            pie2 = go.Figure(data=[go.Pie(
                labels=['안전', '주의', '위험'],
                values=[
                    100 - arcing_risk if arcing_risk < 50 else 50,
                    arcing_risk - 30 if arcing_risk > 30 else 0,
                    30 if arcing_risk > 30 else arcing_risk,
                ],
                hole=0.4,
                marker=dict(colors=['#28a745', '#ffc107', '#dc3545']),
                textinfo='label+percent',
                textfont=dict(size=10, color='#333333'),
            )])
            pie2.update_layout(
                height=200,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(font=dict(size=9, color='#666666')),
            )
            st.plotly_chart(pie2, use_container_width=True)
        
        # 누적 라인 차트
        st.markdown("#### 누적 추이")
        cumulative_data = []
        for h in range(max(0, hours - 50), hours + 1, 5):
            params = calculate_simulation_parameters(h)
            ws = wear_estimator.calculate_wear_state(params.vpp, params.yttrium_peak, float(h))
            cumulative_data.append({
                'timestamp': datetime.now() - timedelta(hours=hours - h),
                '마모 진행도': ws.degradation_index,
                '위험도': arcing_risk * (h / max(hours, 1)),
                'Vpp': params.vpp,
            })
        
        cum_df = pd.DataFrame(cumulative_data)
        fig_cum = go.Figure()
        colors = ['#28a745', '#dc3545', '#007bff']
        for i, col in enumerate(['마모 진행도', '위험도', 'Vpp']):
            fig_cum.add_trace(go.Scatter(
                x=cum_df['timestamp'],
                y=cum_df[col],
                mode='lines',
                name=col,
                line=dict(color=colors[i], width=2),
                fill='tonexty' if i > 0 else 'tozeroy',
            ))
        
        fig_cum.update_layout(
            height=200,
            xaxis=dict(tickfont=dict(color='#666666'), gridcolor='rgba(0,0,0,0.1)'),
            yaxis=dict(tickfont=dict(color='#666666'), gridcolor='rgba(0,0,0,0.1)'),
            margin=dict(l=40, r=20, t=20, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(font=dict(size=9, color='#666666'), orientation='h', y=-0.2),
        )
        st.plotly_chart(fig_cum, use_container_width=True)
    
    # ========== 레이아웃 2: 하단 좌측 ==========
    st.markdown("---")
    
    col3, col4 = st.columns([2, 1])
    
    with col3:
        # KPI 카드들 (라인 차트 포함)
        st.markdown("#### 주요 지표")
        kpi_cols = st.columns(5)
        
        kpi_metrics = [
            ('마모 진행도', f"{wear_state.degradation_index:.1f}%", wear_state.degradation_index),
            ('잔여 두께', f"{wear_state.remaining_thickness:.1f}μm", wear_state.remaining_thickness),
            ('RUL', f"{rul_prediction.rul_hours:.0f}시간", rul_prediction.rul_hours),
            ('위험도', f"{arcing_risk:.1f}%", arcing_risk),
            ('Vpp', f"{sim_params.vpp:.1f}V", sim_params.vpp),
        ]
        
        for i, (label, value, base_value) in enumerate(kpi_metrics):
            with kpi_cols[i]:
                # 작은 라인 차트 생성
                trend_values = [base_value + np.random.randn() * base_value * 0.05 for _ in range(20)]
                fig_kpi = go.Figure()
                fig_kpi.add_trace(go.Scatter(
                    y=trend_values,
                    mode='lines',
                    line=dict(color='#28a745', width=1.5),
                    showlegend=False,
                    fill='tozeroy',
                    fillcolor='rgba(40, 167, 69, 0.1)',
                ))
                fig_kpi.update_layout(
                    height=80,
                    margin=dict(l=5, r=5, t=5, b=5),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showticklabels=False, showgrid=False),
                    yaxis=dict(showticklabels=False, showgrid=False),
                )
                st.plotly_chart(fig_kpi, use_container_width=True)
                st.markdown(f"**{value}**")
                st.markdown(f"<div style='font-size: 11px; color: #666;'>{label}</div>", unsafe_allow_html=True)
        
        # 수평 라인 차트 (파라미터별)
        st.markdown("#### 파라미터별 추이")
        param_data = []
        for h in range(max(0, hours - 30), hours + 1, 2):
            params = calculate_simulation_parameters(h)
            param_data.append({
                'timestamp': datetime.now() - timedelta(hours=hours - h),
                'Vpp': params.vpp,
                'Vdc': abs(params.vdc),
                'Phase': params.phase,
                'Yttrium': params.yttrium_peak * 100,
            })
        
        param_df = pd.DataFrame(param_data)
        fig_params = make_subplots(
            rows=4,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=['Vpp', 'Vdc', 'Phase', 'Yttrium Peak'],
        )
        
        params_list = ['Vpp', 'Vdc', 'Phase', 'Yttrium']
        for i, param in enumerate(params_list):
            fig_params.add_trace(
                go.Scatter(
                    x=param_df['timestamp'],
                    y=param_df[param],
                    mode='lines',
                    name=param,
                    line=dict(color='#28a745', width=1.5),
                    showlegend=False,
                ),
                row=i+1,
                col=1,
            )
        
        fig_params.update_layout(
            height=300,
            margin=dict(l=50, r=20, t=60, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_params, use_container_width=True)
    
    with col4:
        # 히트맵
        st.markdown("#### 시간대별 활동도")
        categories = ['Chamber1', 'Chamber2', 'Chamber3', 'Chamber4']
        time_slots = ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00']
        
        heatmap_data = []
        for cat in categories:
            for time_slot in time_slots:
                activity = np.random.rand()
                heatmap_data.append({
                    '카테고리': cat,
                    '시간': time_slot,
                    '활동도': activity,
                })
        
        heatmap_df = pd.DataFrame(heatmap_data)
        pivot_df = heatmap_df.pivot(index='카테고리', columns='시간', values='활동도')
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale='Greens',
            showscale=True,
        ))
        fig_heat.update_layout(
            height=400,
            margin=dict(l=80, r=20, t=40, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#666666')),
            yaxis=dict(tickfont=dict(color='#666666')),
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
        # 수평 바 차트
        st.markdown("#### 챔버별 마모도")
        chamber_wear = [
            wear_state.degradation_index,
            wear_state.degradation_index * 0.9,
            wear_state.degradation_index * 0.85,
            wear_state.degradation_index * 0.95,
        ]
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=chamber_wear,
            y=categories,
            orientation='h',
            marker_color='#28a745',
            text=[f"{v:.1f}%" for v in chamber_wear],
            textposition='outside',
        ))
        fig_bar.update_layout(
            height=200,
            xaxis=dict(tickfont=dict(color='#666666'), gridcolor='rgba(0,0,0,0.1)'),
            yaxis=dict(tickfont=dict(color='#666666')),
            margin=dict(l=80, r=50, t=20, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # ========== 레이아웃 3: 하단 우측 ==========
    st.markdown("---")
    
    # KPI 카드들 (6개)
    st.markdown("#### 주요 성과 지표")
    kpi_cols2 = st.columns(6)
    
    kpi_metrics2 = [
        ('마모 진행도', f"{wear_state.degradation_index:.1f}%", (wear_state.degradation_index - 50) / 5),
        ('잔여 두께', f"{wear_state.remaining_thickness:.1f}μm", (wear_state.remaining_thickness - 500) / 50),
        ('RUL', f"{rul_prediction.rul_hours:.0f}시간", (rul_prediction.rul_hours - 5000) / 100),
        ('위험도', f"{arcing_risk:.1f}%", (arcing_risk - 30) / 3),
        ('Vpp', f"{sim_params.vpp:.1f}V", (sim_params.vpp - 450) / 5),
        ('상태', wear_state.status, 0),
    ]
    
    for i, (label, value, change) in enumerate(kpi_metrics2):
        with kpi_cols2[i]:
            st.markdown(create_kpi_card(label, value, change), unsafe_allow_html=True)
    
    # 하단 차트들
    col5, col6 = st.columns([1, 1])
    
    with col5:
        # 월별 데이터 테이블
        st.markdown("#### 월별 요약")
        monthly_data = []
        for month in range(7, 13):
            month_hours = month * 150
            params = calculate_simulation_parameters(month_hours)
            ws = wear_estimator.calculate_wear_state(params.vpp, params.yttrium_peak, float(month_hours))
            monthly_data.append({
                '월': f"2024년 {month}월",
                '마모도': f"{ws.degradation_index:.1f}%",
                'RUL': f"{rul_prediction.rul_hours:.0f}시간",
                '위험도': f"{arcing_risk:.1f}%",
            })
        
        monthly_df = pd.DataFrame(monthly_data)
        st.dataframe(monthly_df, use_container_width=True, hide_index=True)
    
    with col6:
        # 멀티 라인 차트
        st.markdown("#### 연도별 비교")
        trend_data = []
        for year_offset in [0, -1]:
            for month in range(1, 13):
                month_hours = (2024 + year_offset - 2020) * 12 * 150 + month * 150
                params = calculate_simulation_parameters(month_hours)
                ws = wear_estimator.calculate_wear_state(params.vpp, params.yttrium_peak, float(month_hours))
                trend_data.append({
                    'year': f"{2024 + year_offset}",
                    'month': month,
                    'value': ws.degradation_index,
                })
        
        trend_df = pd.DataFrame(trend_data)
        fig_trend2 = go.Figure()
        colors2 = ['#28a745', '#95a5a6']
        for i, year in enumerate(trend_df['year'].unique()):
            year_df = trend_df[trend_df['year'] == year]
            fig_trend2.add_trace(go.Scatter(
                x=year_df['month'],
                y=year_df['value'],
                mode='lines+markers',
                name=year,
                line=dict(color=colors2[i % len(colors2)], width=2),
            ))
        
        fig_trend2.update_layout(
            height=200,
            xaxis=dict(tickfont=dict(color='#666666'), gridcolor='rgba(0,0,0,0.1)'),
            yaxis=dict(tickfont=dict(color='#666666'), gridcolor='rgba(0,0,0,0.1)'),
            margin=dict(l=40, r=20, t=20, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(font=dict(size=9, color='#666666'), orientation='h', y=-0.2),
        )
        st.plotly_chart(fig_trend2, use_container_width=True)
        
        # 바 차트 + 트렌드 라인
        st.markdown("#### 월별 추이")
        bar_trend_data = []
        for month in range(1, 13):
            month_hours = month * 150
            params = calculate_simulation_parameters(month_hours)
            ws = wear_estimator.calculate_wear_state(params.vpp, params.yttrium_peak, float(month_hours))
            bar_trend_data.append({
                'month': f"2024.{month:02d}",
                'value': ws.degradation_index,
            })
        
        bar_trend_df = pd.DataFrame(bar_trend_data)
        fig_bar_trend = go.Figure()
        
        fig_bar_trend.add_trace(go.Bar(
            x=bar_trend_df['month'],
            y=bar_trend_df['value'],
            marker_color='#28a745',
            name='마모 진행도',
        ))
        
        z = np.polyfit(range(len(bar_trend_df)), bar_trend_df['value'], 1)
        trend_line = np.poly1d(z)(range(len(bar_trend_df)))
        fig_bar_trend.add_trace(go.Scatter(
            x=bar_trend_df['month'],
            y=trend_line,
            mode='lines',
            name='트렌드',
            line=dict(color='#dc3545', width=2, dash='dash'),
        ))
        
        fig_bar_trend.update_layout(
            height=200,
            xaxis=dict(tickfont=dict(color='#666666'), gridcolor='rgba(0,0,0,0.1)'),
            yaxis=dict(tickfont=dict(color='#666666'), gridcolor='rgba(0,0,0,0.1)'),
            margin=dict(l=40, r=20, t=20, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(font=dict(size=9, color='#666666'), orientation='h', y=-0.2),
        )
        st.plotly_chart(fig_bar_trend, use_container_width=True)
    
    # 자동 새로고침
    if auto_refresh:
        st.rerun()


if __name__ == "__main__":
    main()
