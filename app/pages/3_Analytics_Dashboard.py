import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import numpy as np
import streamlit as st

from simulation_state import render_simulation_controls
from visualization.charts import plot_posterior


results = render_simulation_controls()
summary = results["summary"]

st.title("Bayesian Engine")
st.write("Final posterior view after the full Thompson sampling simulation.")

st.pyplot(
    plot_posterior(
        summary["alpha_A"],
        summary["beta_A"],
        summary["alpha_B"],
        summary["beta_B"],
    ),
    clear_figure=True,
)

samples_a = np.random.beta(summary["alpha_A"], summary["beta_A"], 20000)
samples_b = np.random.beta(summary["alpha_B"], summary["beta_B"], 20000)
prob_b_better = float((samples_b > samples_a).mean())

metric_1, metric_2, metric_3 = st.columns(3)
metric_1.metric("Posterior mean A", f"{summary['alpha_A'] / (summary['alpha_A'] + summary['beta_A']):.2%}")
metric_2.metric("Posterior mean B", f"{summary['alpha_B'] / (summary['alpha_B'] + summary['beta_B']):.2%}")
metric_3.metric("P(B > A)", f"{prob_b_better:.2%}")

st.latex(r"P(\theta \mid data) \propto P(data \mid \theta) \cdot P(\theta)")
st.caption("Each variant starts with a Beta(1,1) prior and gets updated after every simulated Bernoulli outcome.")
