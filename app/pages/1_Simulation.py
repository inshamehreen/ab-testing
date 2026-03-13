import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st

from simulation_state import render_simulation_controls
from visualization.charts import plot_allocation_breakdown, plot_allocation_share


results = render_simulation_controls()
summary = results["summary"]
events = results["events"]

st.title("Traffic Allocation")
st.write("This page shows where Thompson sampling sent traffic and how the allocation changed as evidence accumulated.")

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Users to A", summary["traffic_A"], f"{summary['traffic_A'] / summary['visitors']:.1%}")
metric_2.metric("Users to B", summary["traffic_B"], f"{summary['traffic_B'] / summary['visitors']:.1%}")
metric_3.metric("Observed CVR A", f"{summary['rate_A']:.2%}")
metric_4.metric("Observed CVR B", f"{summary['rate_B']:.2%}")

chart_col, detail_col = st.columns([1.3, 1])
with chart_col:
    st.pyplot(plot_allocation_share(events), clear_figure=True)
with detail_col:
    st.pyplot(plot_allocation_breakdown(summary), clear_figure=True)

st.caption(
    f"Ground truth in this run: A = {summary['true_rate_A']:.2%}, B = {summary['true_rate_B']:.2%}. "
    "The algorithm does not know these values and only learns from user outcomes."
)
