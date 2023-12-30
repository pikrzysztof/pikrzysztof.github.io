#!/usr/bin/env python3
# Snippets and ideas taken from "Think Bayes Bayesian Statistics in Python" by Allen B. Downey
# https://github.com/AllenDowney/empiricaldist/blob/master/empiricaldist/empiricaldist.py
# Based on chapter 11 and chapter 13 of the book.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde, norm

from empiricaldist import Pmf

data_noht = [
    11.53,
    11.54,
    11.54,
    11.54,
    11.54,
    11.55,
    11.54,
    11.55,
    11.53,
    11.54,
    11.53,
    11.54,
    11.55,
    11.54,
    11.69,
    11.56,
    11.54,
    11.55,
    11.57,
    11.56,
]

data_ht = [
    31.17,
    31.10,
    31.20,
    31.19,
    31.12,
    30.96,
    31.08,
    30.85,
    31.18,
    31.17,
    31.19,
    31.15,
    31.20,
    31.18,
    31.20,
    31.17,
    31.18,
    31.17,
]


def make_uniform(qs: np.array, name: str) -> Pmf:
    pmf = Pmf(1.0, qs)
    pmf.normalize()
    pmf.index.name = name
    return pmf


def make_joint(pmf1, pmf2) -> pd.DataFrame:
    """Compute the outer product of two Pmfs"""
    X, Y = np.meshgrid(pmf1, pmf2)
    return pd.DataFrame(X * Y, columns=pmf1.qs, index=pmf2.qs)


def normalize(joint):
    """Normalize a joint distribution"""
    prob_data = joint.to_numpy().sum()
    joint /= prob_data
    return prob_data


def update_norm(prior, data):
    """Update the prior based on data."""
    mu_mesh, sigma_mesh, data_mesh = np.meshgrid(prior.columns, prior.index, data)
    densities = norm(mu_mesh, sigma_mesh).pdf(data_mesh)
    likelihood = densities.prod(axis=2)
    posterior = prior * likelihood
    normalize(posterior)
    return posterior


def marginal(joint, axis):
    """Compute a marginal distribution."""
    return Pmf(joint.sum(axis=axis))


def kde_from_pmf(pmf, n=101):
    """Make a kernel density estimae for a new PMF."""
    kde = gaussian_kde(pmf.qs, weights=pmf.ps)
    qs = np.linspace(pmf.qs.min(), pmf.qs.max(), n)
    ps = kde.evaluate(qs)
    pmf = Pmf(ps, qs)
    pmf.normalize()
    return pmf


# WARNING: the span described by start, stop arguments can't be too big - otherwise you'll get /0 errors.
qs = np.linspace(5, 35, num=101)
prior_mu = make_uniform(qs, name="mean no hyperthreading")

# WARNING: the span described by start, stop arguments can't be too big - otherwise you'll get /0 errors.
qs = np.linspace(5, 35, num=101)
prior_sigma = make_uniform(qs, name="std no hyperthreading")

prior = make_joint(prior_mu, prior_sigma)
posterior_noht = update_norm(prior, data_noht)
posterior_ht = update_norm(prior, data_ht)
pmf_mean_ht = marginal(posterior_ht, 0)
pmf_mean_noht = marginal(posterior_noht, 0)
prob_gt = Pmf.prob_gt(pmf_mean_ht, pmf_mean_noht)
print(f"Hyperthreading version is slower with probability of {prob_gt:.2f}.")
pmf_diff = Pmf.sub_dist(pmf_mean_ht, pmf_mean_noht)
# plot stuff if needed
# pmf_diff.bar()
# plt.show()
cdf_diff = pmf_diff.make_cdf()
kde_diff = kde_from_pmf(pmf_diff)
# plot smoothed out graph if needed
# kde_diff.bar()
# plt.show()
mean_diff = pmf_diff.mean()
credible_intvl = pmf_diff.credible_interval(0.95)
print(
    f"Hyperthreading version is on average {mean_diff:.2f}s slower than no-HT version."
    f" With 95% probability no-HT version is faster than HT version by a value between {credible_intvl[0]} and {credible_intvl[1]} seconds."
)
