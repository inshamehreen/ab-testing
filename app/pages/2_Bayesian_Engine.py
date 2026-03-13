import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st

from simulation_state import render_simulation_controls
from visualization.charts import plot_user_dynamics


results = render_simulation_controls()
events = results["events"]
summary = results["summary"]

st.title("User Dynamics")
st.write("Scrub through the simulation to see how individual users changed the traffic split and posterior beliefs.")

focus_user = st.slider(
    "Show the simulation up to user",
    min_value=25,
    max_value=summary["visitors"],
    value=min(summary["visitors"], 250),
    step=25,
)

st.pyplot(plot_user_dynamics(events, focus_user), clear_figure=True)

current_event = events[focus_user - 1]
info_1, info_2, info_3, info_4 = st.columns(4)
info_1.metric("Current user", current_event["user"])
info_2.metric("Assigned variant", current_event["variant"])
info_3.metric("Posterior mean A", f"{current_event['posterior_mean_A']:.2%}")
info_4.metric("Posterior mean B", f"{current_event['posterior_mean_B']:.2%}")

st.caption(
    "Top chart: cumulative users routed to each variant. Bottom chart: user outcomes plus the current posterior mean for each variant."
)
