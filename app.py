
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="SkyPulse | Airline Intelligence",
    page_icon="✈️",
    layout="wide"
)


st.markdown("""
<style>
.stApp {
    background-color: #081323;
    color: #F4F8FF;
}

[data-testid="stMetric"] {
    background: #14253D;
    border: 1px solid #31445F;
    border-radius: 14px;
    padding: 20px;
}

[data-testid="stMetric"] *,
[data-testid="stMetric"] p {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

[data-testid="stSidebar"] {
    background: #101E32;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)




@st.cache_data
def load_data():
    df = pd.read_csv(
        "flights_dashboard.csv",
        header=None,
        names=[
            "flight_id",
            "airline",
            "departure",
            "arrival",
            "date",
            "delay_minutes",
            "status"
        ]
    )
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["delay_minutes"] = pd.to_numeric(
        df["delay_minutes"], errors="coerce"
    ).fillna(0)
    return df

df = load_data()

st.sidebar.title("✈️ SkyPulse")
st.sidebar.caption("Airline Operations Intelligence")
st.sidebar.divider()

airlines = st.sidebar.multiselect(
    "Select Airlines",
    sorted(df["airline"].dropna().unique()),
    default=sorted(df["airline"].dropna().unique())
)

statuses = st.sidebar.multiselect(
    "Flight Status",
    sorted(df["status"].dropna().unique()),
    default=sorted(df["status"].dropna().unique())
)

filtered = df[
    df["airline"].isin(airlines)
    & df["status"].isin(statuses)
]

st.title("✈️ SkyPulse")
st.caption("AIRLINE OPERATIONS INTELLIGENCE | SYNTHETIC DATA")
st.divider()

total = len(filtered)
delayed = (filtered["status"] == "Delayed").sum()
cancelled = (filtered["status"] == "Cancelled").sum()
delay_rate = 100 * delayed / total if total else 0
cancel_rate = 100 * cancelled / total if total else 0
avg_delay = filtered["delay_minutes"].mean() if total else 0


def kpi_card(label, value, icon, color, subtitle):
    st.markdown(
        f"""
        <div style="background:#14263F;
                    border:1px solid #304762;
                    border-radius:16px;
                    padding:22px 18px;
                    min-height:155px;
                    box-shadow:0 8px 24px rgba(0,0,0,0.18);">
            <div style="color:#B3C6DF;font-size:12px;
                        font-weight:700;letter-spacing:1px;">
                {icon} {label}
            </div>
            <div style="color:{color};font-size:38px;
                        font-weight:800;margin-top:14px;">
                {value}
            </div>
            <div style="color:#91A8C5;font-size:12px;
                        margin-top:10px;">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

a, b, c, d = st.columns(4)

with a:
    kpi_card("TOTAL FLIGHTS", f"{total:,}",
             "✈️", "#66D9FF", "Flight records")

with b:
    kpi_card("DELAY RATE", f"{delay_rate:.1f}%",
             "⏱️", "#FFBF69", "Delayed flights")

with c:
    kpi_card("CANCELLATION RATE", f"{cancel_rate:.1f}%",
             "🚫", "#FF738A", "Cancelled flights")

with d:
    kpi_card("AVERAGE DELAY", f"{avg_delay:.1f} min",
             "🕒", "#5CE1B6", "Average duration")

left, right = st.columns(2)

with left:
    st.subheader("Flight Status Distribution")
    status_data = (
        filtered["status"]
        .value_counts()
        .reset_index()
    )
    status_data.columns = ["Status", "Flights"]

    fig = px.pie(
        status_data,
        names="Status",
        values="Flights",
        hole=0.62,
        color="Status",
        color_discrete_map={
            "On Time": "#20c997",
            "Delayed": "#ffb347",
            "Cancelled": "#ff6575"
        }
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#14253d",
        plot_bgcolor="#14253d",
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Flights by Airline")
    airline_data = (
        filtered.groupby("airline")
        .size()
        .reset_index(name="Flights")
        .sort_values("Flights", ascending=False)
    )

    fig = px.bar(
        airline_data,
        x="Flights",
        y="airline",
        orientation="h",
        color="Flights",
        color_continuous_scale="Blues"
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#14253d",
        plot_bgcolor="#14253d",
        yaxis_title="",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig, use_container_width=True)


st.subheader("Daily Flight Operations")
st.caption("Daily flight volume, delays and cancellations | Synthetic data")

daily = (
    filtered.dropna(subset=["date"])
    .groupby("date")
    .agg(
        Total_Flights=("status", "size"),
        Delayed=("status", lambda x: (x == "Delayed").sum()),
        Cancelled=("status", lambda x: (x == "Cancelled").sum())
    )
    .reset_index()
)

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Bar(
    x=daily["date"],
    y=daily["Total_Flights"],
    name="Total Flights",
    marker_color="#315D86",
    opacity=0.65
))

fig.add_trace(go.Scatter(
    x=daily["date"],
    y=daily["Delayed"],
    name="Delayed",
    mode="lines+markers",
    line=dict(color="#FFBF69", width=3),
    marker=dict(size=5)
))

fig.add_trace(go.Scatter(
    x=daily["date"],
    y=daily["Cancelled"],
    name="Cancelled",
    mode="lines+markers",
    line=dict(color="#FF738A", width=3),
    marker=dict(size=5)
))

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#14263F",
    plot_bgcolor="#14263F",
    font=dict(color="#E7F1FF", size=13),
    height=440,
    hovermode="x unified",
    barmode="overlay",
    legend=dict(
        orientation="h",
        y=1.14,
        x=0,
        font=dict(color="#E7F1FF")
    ),
    xaxis=dict(
        title=None,
        showgrid=False,
        tickformat="%b %d",
        tickfont=dict(color="#B8C9E0")
    ),
    yaxis=dict(
        title="Number of flights",
        gridcolor="rgba(255,255,255,0.10)",
        rangemode="tozero",
        tickfont=dict(color="#B8C9E0")
    ),
    margin=dict(l=30, r=20, t=60, b=30)
)

st.plotly_chart(fig, use_container_width=True)



st.subheader("Most Popular Routes")
st.caption("Top 10 routes ranked by flight volume | Synthetic data")

routes = (
    filtered.groupby(["departure", "arrival"])
    .size()
    .reset_index(name="Flights")
    .sort_values("Flights", ascending=False)
    .head(10)
)

routes["Route"] = (
    routes["departure"] + " → " + routes["arrival"]
)

routes = routes.sort_values("Flights", ascending=True)

fig = px.bar(
    routes,
    x="Flights",
    y="Route",
    orientation="h",
    text="Flights"
)

fig.update_traces(
    marker_color="#55C9F5",
    marker_line_width=0,
    textposition="outside",
    textfont=dict(color="#E7F1FF", size=13),
    hovertemplate="<b>%{y}</b><br>Flights: %{x}<extra></extra>"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#14263F",
    plot_bgcolor="#14263F",
    font=dict(color="#E7F1FF", size=13),
    height=520,
    showlegend=False,
    xaxis=dict(
        title="Number of flights",
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)",
        rangemode="tozero",
        range=[0, max(routes["Flights"].max() * 1.15, 1)]
    ),
    yaxis=dict(
        title=None,
        showgrid=False,
        tickfont=dict(color="#E7F1FF", size=12)
    ),
    margin=dict(l=190, r=45, t=25, b=45),
    bargap=0.35
)

st.plotly_chart(fig, use_container_width=True)






st.subheader("✈️ Least Popular Routes")
st.caption("Low-traffic flight corridors | Synthetic data")

least_routes = (
    filtered.groupby(["departure", "arrival"])
    .size()
    .reset_index(name="Flights")
)

least_routes = (
    least_routes[least_routes["Flights"] <= 10]
    .sort_values(["Flights", "departure", "arrival"])
    .head(10)
)

if least_routes.empty:
    st.info("No low-traffic routes match the selected filters.")
else:
    st.markdown(
        """
        <div style="
            background:#0B1C30;
            border:1px solid #24435C;
            border-radius:14px;
            padding:8px 12px;
            margin-bottom:6px;
        ">
            <div style="
                color:#38BDF8;
                font-size:12px;
                letter-spacing:2px;
                font-weight:700;
            ">
                DEPARTURE BOARD / LOW-TRAFFIC CORRIDORS
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    from html import escape

    for number, (_, route) in enumerate(
        least_routes.iterrows(), start=1
    ):
        departure = escape(str(route["departure"]))
        arrival = escape(str(route["arrival"]))

        st.markdown(
            f"""
            <div style="
                background:#11263C;
                border:1px solid #1D3D57;
                border-left:3px solid #38BDF8;
                border-radius:10px;
                padding:6px 12px;
                margin-bottom:4px;
                display:flex;
                align-items:center;
                gap:8px;
            ">
                <span style="
                    color:#6E91AC;
                    font-size:12px;
                    font-weight:700;
                ">{number:02d}</span>
                <span style="
                    color:#F0F7FF;
                    font-size:12px;
                    font-weight:600;
                    flex:1;
                ">{departure}</span>
                <span style="
                    color:#38BDF8;
                    font-size:14px;
                ">✈</span>
                <span style="
                    color:#F0F7FF;
                    font-size:12px;
                    font-weight:600;
                    flex:1;
                    text-align:right;
                ">{arrival}</span>
            </div>
            """,
            unsafe_allow_html=True
        )


st.subheader("Operations Insights")
st.caption("Automatically calculated from selected flights | Synthetic data")

if filtered.empty:
    st.info("No flights match the selected filters.")
else:
    total_insights = len(filtered)

    status_counts = filtered["status"].value_counts()
    delayed_count = int(status_counts.get("Delayed", 0))
    cancelled_count = int(status_counts.get("Cancelled", 0))
    ontime_count = int(status_counts.get("On Time", 0))

    delay_pct = delayed_count / total_insights * 100
    cancel_pct = cancelled_count / total_insights * 100
    ontime_pct = ontime_count / total_insights * 100

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"✈️ **Flight Performance** — "
            f"{total_insights:,} flights analyzed. "
            f"{ontime_pct:.1f}% operated on time."
        )

        st.warning(
            f"⏱️ **Delay Monitoring** — "
            f"{delayed_count:,} flights were delayed "
            f"({delay_pct:.1f}%)."
        )

    with col2:
        st.error(
            f"🚫 **Cancellation Watch** — "
            f"{cancelled_count:,} flights were cancelled "
            f"({cancel_pct:.1f}%)."
        )

        route_counts = (
            filtered.groupby(["departure", "arrival"])
            .size()
            .sort_values(ascending=False)
        )

        if not route_counts.empty:
            top_route = route_counts.index[0]
            top_count = int(route_counts.iloc[0])

            st.success(
                f"🛫 **Busiest Route** — "
                f"{top_route[0]} → {top_route[1]} "
                f"with {top_count:,} flights."
            )



st.subheader("✈️ Flight Control Tower")
st.caption("Airline Operational Intelligence | Synthetic Flight Data")

if filtered.empty:
    st.info("No airline records match the selected filters.")
else:
    tower = (
        filtered.groupby("airline")
        .agg(
            Flights=("flight_id", "size"),
            On_Time=("status", lambda s: (s == "On Time").sum()),
            Delayed=("status", lambda s: (s == "Delayed").sum()),
            Cancelled=("status", lambda s: (s == "Cancelled").sum()),
            Avg_Delay=("delay_minutes", "mean")
        )
        .reset_index()
    )

    tower["On-Time %"] = (
        tower["On_Time"] / tower["Flights"] * 100
    ).round(1)

    tower["Cancellation %"] = (
        tower["Cancelled"] / tower["Flights"] * 100
    ).round(1)

    tower = tower.sort_values(
        ["On-Time %", "Cancellation %", "Flights"],
        ascending=[False, True, False]
    ).reset_index(drop=True)

    tower["Rank"] = range(1, len(tower) + 1)

    best = tower.iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("🏆 Top Airline", best["airline"])
    c2.metric("On-Time Performance", f"{best['On-Time %']:.1f}%")
    c3.metric("Airlines Tracked", len(tower))

    st.markdown("#### 📡 Performance Radar")

    import math

    n = len(tower)
    angles = [360 * i / n for i in range(n)]

    fig_radar = go.Figure()

    for i, (_, airline) in enumerate(tower.iterrows()):
        performance = float(airline["On-Time %"])

        fig_radar.add_trace(
            go.Scatterpolar(
                r=[performance],
                theta=[angles[i]],
                mode="markers+text",
                marker=dict(
                    size=15 + min(int(airline["Flights"]) / 50, 12),
                    color=performance,
                    colorscale=[
                        [0, "#FB7185"],
                        [0.7, "#F59E0B"],
                        [0.85, "#38BDF8"],
                        [1, "#2DD4BF"]
                    ],
                    cmin=0,
                    cmax=100,
                    showscale=False,
                    line=dict(color="#E8F4FF", width=1)
                ),
                text=[str(i + 1)],
                textposition="middle center",
                textfont=dict(color="#081323", size=10),
                customdata=[[
                    airline["airline"],
                    int(airline["Flights"]),
                    float(airline["Avg_Delay"]),
                    float(airline["Cancellation %"])
                ]],
                hovertemplate=(
                    "<b>%{customdata[0]}</b>"
                    "<br>On-Time: %{r:.1f}%"
                    "<br>Flights: %{customdata[1]}"
                    "<br>Avg Delay: %{customdata[2]:.1f} min"
                    "<br>Cancellation: %{customdata[3]:.1f}%"
                    "<extra></extra>"
                ),
                showlegend=False
            )
        )

    fig_radar.update_layout(
        template="plotly_dark",
        paper_bgcolor="#14263F",
        height=480,
        margin=dict(l=35, r=35, t=30, b=30),
        polar=dict(
            bgcolor="#0A1D30",
            radialaxis=dict(
                range=[0, 100],
                tickvals=[25, 50, 75, 100],
                gridcolor="#24506A",
                tickfont=dict(color="#8BAAC4", size=10)
            ),
            angularaxis=dict(
                tickmode="array",
                tickvals=angles,
                ticktext=tower["airline"].tolist(),
                gridcolor="#24506A",
                tickfont=dict(color="#B8D5E9", size=10),
                direction="clockwise"
            )
        )
    )

    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("#### 🏅 Airline Rankings")

    for _, airline in tower.iterrows():
        score = float(airline["On-Time %"])
        color = (
            "#2DD4BF" if score >= 90
            else "#38BDF8" if score >= 80
            else "#F59E0B"
        )

        rank = int(airline["Rank"])
        name = str(airline["airline"])
        flights = int(airline["Flights"])
        avg_delay = float(airline["Avg_Delay"])
        cancel_rate = float(airline["Cancellation %"])

        st.markdown(
            f"""
            <div style="background:#10263D;
                        border:1px solid #24435C;
                        border-radius:7px;
                        padding:6px 12px;
                        margin-bottom:4px;">
                <div style="display:flex;
                            justify-content:space-between;
                            color:#E8F4FF;
                            font-weight:600;">
                    <span>#{rank:02d} &nbsp; ✈️ {name}</span>
                    <span style="color:{color};">{score:.1f}%</span>
                </div>
                <div style="background:#284157;
                            height:4px;
                            border-radius:10px;
                            margin-top:5px;
                            overflow:hidden;">
                    <div style="background:{color};
                                width:{score}%;
                                height:100%;"></div>
                </div>
                <div style="color:#8BAAC4;
                            font-size:10px;
                            margin-top:4px;">
                    {flights} flights analyzed |
                    Avg delay: {avg_delay:.1f} min |
                    Cancelled: {cancel_rate:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.subheader("Delay Duration Distribution")
st.caption("Duration of positive flight delays | Synthetic data")

delay_data = filtered.copy()
delay_data["delay_minutes"] = pd.to_numeric(
    delay_data["delay_minutes"], errors="coerce"
)

delay_data = delay_data[
    delay_data["delay_minutes"] > 0
].copy()

if delay_data.empty:
    st.info("No positive delays in the selected flights.")
else:
    bins = [0, 15, 30, 60, 120, float("inf")]
    labels = [
        "1–15 min",
        "16–30 min",
        "31–60 min",
        "61–120 min",
        "120+ min"
    ]

    delay_data["Duration"] = pd.cut(
        delay_data["delay_minutes"],
        bins=bins,
        labels=labels,
        include_lowest=False
    )

    distribution = (
        delay_data["Duration"]
        .value_counts(sort=False)
        .reindex(labels, fill_value=0)
        .reset_index()
    )
    distribution.columns = ["Duration", "Flights"]

    fig_delay = px.bar(
        distribution,
        x="Duration",
        y="Flights",
        text="Flights",
        color="Duration",
        color_discrete_map={
            "1–15 min": "#5CE1B6",
            "16–30 min": "#55D6FF",
            "31–60 min": "#FFBF69",
            "61–120 min": "#FF8A65",
            "120+ min": "#FF738A"
        }
    )

    fig_delay.update_traces(
        textposition="outside",
        textfont=dict(color="#E7F1FF", size=14),
        marker_line_width=0,
        hovertemplate="%{x}<br>Flights: %{y}<extra></extra>"
    )

    fig_delay.update_layout(
        template="plotly_dark",
        paper_bgcolor="#14263F",
        plot_bgcolor="#14263F",
        font=dict(color="#E7F1FF", size=13),
        height=430,
        showlegend=False,
        bargap=0.35,
        xaxis=dict(
            title="Delay duration",
            showgrid=False
        ),
        yaxis=dict(
            title="Number of flights",
            rangemode="tozero",
            gridcolor="rgba(255,255,255,0.10)"
        ),
        margin=dict(l=35, r=25, t=45, b=45)
    )

    st.plotly_chart(fig_delay, use_container_width=True)

st.subheader("Flight Records")
st.dataframe(filtered, use_container_width=True, hide_index=True)

st.caption(
    "SkyPulse portfolio project. All flight data is synthetic "
    "and does not represent real airline performance."
);

# Sidebar heading contrast fix

st.markdown("""
<style>
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #F4F8FF !important;
}
</style>
""", unsafe_allow_html=True)
