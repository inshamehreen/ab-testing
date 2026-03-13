import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta


def plot_allocation_breakdown(summary):
    fig, ax = plt.subplots(figsize=(6, 4))
    traffic = [summary["traffic_A"], summary["traffic_B"]]
    colors = ["#1f77b4", "#ff7f0e"]

    ax.bar(["Variant A", "Variant B"], traffic, color=colors, width=0.6)
    ax.set_ylabel("Users")
    ax.set_title("Traffic Allocation")

    max_height = max(traffic) if traffic else 0
    for index, value in enumerate(traffic):
        ax.text(index, value + (max_height * 0.02 if max_height else 0.5), str(value), ha="center")

    fig.tight_layout()
    return fig


def plot_allocation_share(events):
    fig, ax = plt.subplots(figsize=(8, 4))
    users = [event["user"] for event in events]
    share_a = [event["share_A"] for event in events]
    share_b = [event["share_B"] for event in events]

    ax.plot(users, share_a, label="Variant A share", color="#1f77b4", linewidth=2)
    ax.plot(users, share_b, label="Variant B share", color="#ff7f0e", linewidth=2)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Users observed")
    ax.set_ylabel("Traffic share")
    ax.set_title("How Thompson sampling reallocates traffic")
    ax.legend()
    ax.grid(alpha=0.2)

    fig.tight_layout()
    return fig


def plot_user_dynamics(events, upto_user):
    visible_events = events[:upto_user]
    users = [event["user"] for event in visible_events]

    fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)

    axes[0].plot(users, [event["traffic_A"] for event in visible_events], color="#1f77b4", label="Users sent to A")
    axes[0].plot(users, [event["traffic_B"] for event in visible_events], color="#ff7f0e", label="Users sent to B")
    axes[0].set_ylabel("Cumulative users")
    axes[0].set_title("User-by-user allocation")
    axes[0].legend()
    axes[0].grid(alpha=0.2)

    reward_y = [1 if event["reward"] else 0 for event in visible_events]
    reward_colors = ["#1f77b4" if event["variant"] == "A" else "#ff7f0e" for event in visible_events]
    axes[1].scatter(users, reward_y, c=reward_colors, s=35, alpha=0.75)
    axes[1].plot(users, [event["posterior_mean_A"] for event in visible_events], color="#1f77b4", linewidth=2, label="Posterior mean A")
    axes[1].plot(users, [event["posterior_mean_B"] for event in visible_events], color="#ff7f0e", linewidth=2, label="Posterior mean B")
    axes[1].set_xlabel("User number")
    axes[1].set_ylabel("Conversion / belief")
    axes[1].set_title("Observed conversions and posterior belief")
    axes[1].set_ylim(-0.05, 1.05)
    axes[1].legend()
    axes[1].grid(alpha=0.2)

    fig.tight_layout()
    return fig


def plot_posterior(alpha_A, beta_A, alpha_B, beta_B):
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(0, 0.25, 500)

    ax.plot(x, beta.pdf(x, alpha_A, beta_A), color="#1f77b4", linewidth=2, label="Variant A posterior")
    ax.plot(x, beta.pdf(x, alpha_B, beta_B), color="#ff7f0e", linewidth=2, label="Variant B posterior")
    ax.set_xlabel("Conversion rate")
    ax.set_ylabel("Density")
    ax.set_title("Posterior distributions")
    ax.legend()
    ax.grid(alpha=0.2)

    fig.tight_layout()
    return fig
