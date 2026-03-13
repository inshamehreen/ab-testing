import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import streamlit as st

from simulation_state import render_simulation_controls


st.set_page_config(page_title="Thompson Sampling A/B Test", layout="wide")

results = render_simulation_controls()
summary = results["summary"]

st.title("Thompson Sampling A/B Testing Simulator")
st.write(
    """
    This multipage Streamlit app simulates an A/B test where incoming users are assigned with Thompson sampling.
    Adjust the true conversion rates and traffic volume in the sidebar, then move between pages to inspect allocation and user-level behavior.
    """
)

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Users", summary["visitors"])
metric_2.metric("Traffic to A", summary["traffic_A"])
metric_3.metric("Traffic to B", summary["traffic_B"])
metric_4.metric("Observed winner", f"Variant {summary['winning_variant']}")

st.subheader("Pages")
st.write(
    """
    `Traffic Allocation` shows how the algorithm shifts user share between variants.
    `User Dynamics` visualizes user-by-user assignments, conversions, and belief updates.
    `Bayesian Engine` summarizes the final posterior distributions.
    """
)
