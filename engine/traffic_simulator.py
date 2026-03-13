import numpy as np

from engine.bayesian_bandit import BayesianBandit


def simulate_user(true_rate, rng):
    return int(rng.random() < true_rate)


def run_thompson_sampling_simulation(true_rate_a, true_rate_b, visitors, seed=None):
    rng = np.random.default_rng(seed)
    np.random.seed(seed)

    model = BayesianBandit()
    events = []

    for user_id in range(1, visitors + 1):
        sampled_a, sampled_b = model.sample()
        variant = "A" if sampled_a > sampled_b else "B"

        reward = simulate_user(true_rate_a, rng) if variant == "A" else simulate_user(true_rate_b, rng)
        model.update(variant, reward)

        posterior_means = model.posterior_means()
        summary = model.summary()

        events.append(
            {
                "user": user_id,
                "variant": variant,
                "reward": reward,
                "sampled_a": sampled_a,
                "sampled_b": sampled_b,
                "traffic_A": summary["traffic_A"],
                "traffic_B": summary["traffic_B"],
                "share_A": summary["traffic_A"] / user_id,
                "share_B": summary["traffic_B"] / user_id,
                "conversions_A": summary["conversions_A"],
                "conversions_B": summary["conversions_B"],
                "posterior_mean_A": posterior_means["A"],
                "posterior_mean_B": posterior_means["B"],
            }
        )

    final_summary = model.summary()
    final_summary.update(
        {
            "alpha_A": model.alpha_A,
            "beta_A": model.beta_A,
            "alpha_B": model.alpha_B,
            "beta_B": model.beta_B,
            "true_rate_A": true_rate_a,
            "true_rate_B": true_rate_b,
            "visitors": visitors,
            "winning_variant": "A" if final_summary["rate_A"] >= final_summary["rate_B"] else "B",
        }
    )

    return {
        "events": events,
        "summary": final_summary,
    }
