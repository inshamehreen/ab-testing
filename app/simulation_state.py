import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from engine.traffic_simulator import run_thompson_sampling_simulation


DEFAULT_CONFIG = {
    "true_rate_a": 0.05,
    "true_rate_b": 0.08,
    "visitors": 1500,
    "seed": 42,
}


def _run_current_simulation():
    config = st.session_state.simulation_config
    effective_seed = config["seed"] + st.session_state.simulation_run_count
    st.session_state.simulation_results = run_thompson_sampling_simulation(
        true_rate_a=config["true_rate_a"],
        true_rate_b=config["true_rate_b"],
        visitors=config["visitors"],
        seed=effective_seed,
    )
    st.session_state.simulation_results["summary"]["effective_seed"] = effective_seed


def ensure_simulation_state():
    if "simulation_config" not in st.session_state:
        st.session_state.simulation_config = DEFAULT_CONFIG.copy()

    if "simulation_run_count" not in st.session_state:
        st.session_state.simulation_run_count = 0

    if "simulation_results" not in st.session_state:
        _run_current_simulation()


def render_simulation_controls():
    ensure_simulation_state()

    with st.sidebar:
        st.header("Simulation Controls")
        with st.form("simulation_controls"):
            true_rate_a = st.slider(
                "True conversion rate A",
                min_value=0.01,
                max_value=0.20,
                value=float(st.session_state.simulation_config["true_rate_a"]),
                step=0.005,
            )
            true_rate_b = st.slider(
                "True conversion rate B",
                min_value=0.01,
                max_value=0.20,
                value=float(st.session_state.simulation_config["true_rate_b"]),
                step=0.005,
            )
            visitors = st.slider(
                "Number of users",
                min_value=200,
                max_value=5000,
                value=int(st.session_state.simulation_config["visitors"]),
                step=100,
            )
            seed = st.number_input(
                "Base random seed",
                min_value=0,
                max_value=100000,
                value=int(st.session_state.simulation_config["seed"]),
                step=1,
            )
            rerun = st.form_submit_button("Run Thompson sampling", use_container_width=True)

    proposed_config = {
        "true_rate_a": true_rate_a,
        "true_rate_b": true_rate_b,
        "visitors": visitors,
        "seed": int(seed),
    }

    if rerun:
        st.session_state.simulation_config = proposed_config
        st.session_state.simulation_run_count += 1
        _run_current_simulation()

    return st.session_state.simulation_results
