import numpy as np


class BayesianBandit:
    def __init__(self):
        self.alpha_A = 1
        self.beta_A = 1
        self.alpha_B = 1
        self.beta_B = 1

        self.traffic_A = 0
        self.traffic_B = 0
        self.conversions_A = 0
        self.conversions_B = 0

        self.history_A = []
        self.history_B = []

    def sample(self):
        sample_A = np.random.beta(self.alpha_A, self.beta_A)
        sample_B = np.random.beta(self.alpha_B, self.beta_B)
        return sample_A, sample_B

    def choose_variant(self):
        sample_A, sample_B = self.sample()
        return "A" if sample_A > sample_B else "B"

    def update(self, variant, reward):
        reward = int(bool(reward))

        if variant == "A":
            self.traffic_A += 1
            self.conversions_A += reward
            self.alpha_A += reward
            self.beta_A += 1 - reward
        else:
            self.traffic_B += 1
            self.conversions_B += reward
            self.alpha_B += reward
            self.beta_B += 1 - reward

        self.history_A.append(self.alpha_A / (self.alpha_A + self.beta_A))
        self.history_B.append(self.alpha_B / (self.alpha_B + self.beta_B))

    def posterior_means(self):
        return {
            "A": self.alpha_A / (self.alpha_A + self.beta_A),
            "B": self.alpha_B / (self.alpha_B + self.beta_B),
        }

    def summary(self):
        total_traffic = self.traffic_A + self.traffic_B
        total_conversions = self.conversions_A + self.conversions_B

        return {
            "traffic_A": self.traffic_A,
            "traffic_B": self.traffic_B,
            "conversions_A": self.conversions_A,
            "conversions_B": self.conversions_B,
            "total_traffic": total_traffic,
            "total_conversions": total_conversions,
            "rate_A": self.conversions_A / self.traffic_A if self.traffic_A else 0.0,
            "rate_B": self.conversions_B / self.traffic_B if self.traffic_B else 0.0,
        }
