#!/usr/bin/env python3
"""Quick [estimate] of endothermic spin-independent DM-xenon rates for the LZ extended window.

dR/dE = (rho/m_chi) * sigma_eff * A^2/(2 mu_n^2) * F_Helm^2(E) * eta(vmin)   [per unit target mass]
  vmin = |m_N E/mu_N + delta| / sqrt(2 m_N E)
  sigma_eff = "isoscalar-equivalent" DM-nucleon cross section (f_p = f_n normalisation, as in LZ Fig. S7)

Inputs [assumed]: Standard Halo Model of Baxter et al. arXiv:2105.00599
  rho = 0.3 GeV/cm^3, v0 = 238 km/s, v_esc = 544 km/s, v_E = 254 km/s (annual average; June: ~267 km/s)
Exposure: 2.84 t yr (LZ, arXiv:2609.02823); efficiency: flat 0.96 inside [5.4, 269.9] keV (crude box, [assumed]).
Not a likelihood fit: no energy resolution, no S1/S2 response.
"""
import numpy as np
from math import erf, sqrt, pi, exp

C = 299792.458  # km/s
GEV2_TO_CM2 = 3.8938e-28
AMU = 0.93149410  # GeV
M_NUCLEON = 0.9389  # GeV
XE = {128: 0.0191, 129: 0.264, 130: 0.0407, 131: 0.212, 132: 0.269, 134: 0.104, 136: 0.0886}


def eta(vmin, v0=238.0, vesc=544.0, vE=254.0):
    """Mean inverse speed for a truncated Maxwellian boosted by vE (km/s) -> (km/s)^-1."""
    x, y, z = vmin / v0, vE / v0, vesc / v0
    N = erf(z) - 2 * z * exp(-z * z) / sqrt(pi)
    if x > y + z:
        return 0.0
    if z < y and x < abs(y - z):
        return 1.0 / (v0 * y)
    if x < abs(z - y):
        r = (erf(x + y) - erf(x - y) - 4 * y * exp(-z * z) / sqrt(pi)) / (2 * N * v0 * y)
    else:
        r = (erf(z) - erf(x - y) - 2 * (y + z - x) * exp(-z * z) / sqrt(pi)) / (2 * N * v0 * y)
    return max(r, 0.0)


def helm2(E_keV, A):
    mN = A * AMU
    q = np.sqrt(2 * mN * E_keV * 1e-6)  # GeV
    qf = q / 0.1973269804  # fm^-1
    s, a = 0.9, 0.52
    c = 1.23 * A ** (1 / 3.0) - 0.6
    rn = np.sqrt(c * c + 7.0 / 3.0 * pi * pi * a * a - 5 * s * s)
    x = qf * rn
    j1 = (np.sin(x) - x * np.cos(x)) / x ** 2
    return (3 * j1 / x) ** 2 * np.exp(-(qf * s) ** 2)


def spectrum(E, mchi, delta_keV, sigma_cm2, vE=254.0, rho=0.3):
    """dR/dE in events / (tonne yr keV)."""
    out = np.zeros_like(E)
    mu_n = mchi * M_NUCLEON / (mchi + M_NUCLEON)
    for A, frac in XE.items():
        mN = A * AMU
        mu = mchi * mN / (mchi + mN)
        vmin = np.abs(mN * E * 1e-6 / mu + delta_keV * 1e-6) / np.sqrt(2 * mN * E * 1e-6) * C  # km/s
        et = np.array([eta(v, vE=vE) for v in vmin])  # s/km
        # rate per nucleus: (rho/mchi) * sigma*A^2/(2 mu_n^2) * F^2 * eta  * mN  [natural units -> convert]
        # dR/dE [1/(GeV s) per nucleus] = rho/mchi [1/cm^3] * sigma[cm^2]*A^2 * mN[GeV] /(2 mu_n^2 [GeV^2]) * F^2 * eta [s/cm] * c^2
        pref = (rho / mchi) * sigma_cm2 * A ** 2 * mN / (2 * mu_n ** 2)  # 1/(cm GeV)
        eta_cm = et / 1e5  # s/cm
        per_nucleus = pref * helm2(E, A) * eta_cm * (C * 1e5) ** 2  # 1/(GeV s)
        n_per_tonne = frac * 1e6 / (131.29) * 6.02214076e23  # nuclei of this isotope per tonne (mean molar mass)
        out += per_nucleus * n_per_tonne * 3.15576e7 * 1e-6  # -> /(tonne yr keV)
    return out


def counts(mchi, delta, sigma, vE=254.0):
    E = np.linspace(1.0, 900.0, 3600)
    s = spectrum(E, mchi, delta, sigma, vE=vE)
    dE = E[1] - E[0]
    def win(lo, hi, eff=0.96):
        m = (E >= lo) & (E < hi)
        return s[m].sum() * dE * 2.84 * eff
    peak = E[np.argmax(s)] if s.max() > 0 else float("nan")
    return dict(roi=win(5.4, 269.9), lo=win(5.4, 70.0), mid=win(70.0, 200.0), hi=win(200.0, 269.9),
                above=win(269.9, 700.0, eff=1.0), peak=peak)


if __name__ == "__main__":
    print("Helm F^2(Xe-131) at 50, 100, 200, 248, 300 keV:", [float("%.3g" % helm2(np.array([e]), 131)[0]) for e in (50, 100, 200, 248, 300)])
    print("\n(1) events predicted at the edges of LZ's two-sided 90% CL interval (Fig. S7 of 2609.02823, read off by eye), m_chi = 1 TeV")
    lz = {150: (1.3e-45, 2.0e-44), 200: (1.2e-44, 1.7e-43), 250: (8e-44, 1.1e-42), 300: (3.5e-43, 7.5e-42), 350: (4e-41, 6.5e-40)}
    for d, (lo, up) in lz.items():
        a, b = counts(1000.0, d, lo), counts(1000.0, d, up)
        print(f" delta={d:3d} keV: N_ROI(lower)={a['roi']:.2f}  N_ROI(upper)={b['roi']:.2f} | shape: <70: {b['lo']/max(b['roi'],1e-30):.2f}, 70-200: {b['mid']/max(b['roi'],1e-30):.2f}, 200-270: {b['hi']/max(b['roi'],1e-30):.2f}; above-ROI/ROI={b['above']/max(b['roi'],1e-30):.2f}; peak at {b['peak']:.0f} keV")
    print("\n(2) sigma_eff giving N(200-270 keV) = 1 event, versus m_chi and delta (annual-average vE; June vE=267 in brackets)")
    for m in (300.0, 500.0, 1000.0, 2000.0):
        row = []
        for d in (150, 200, 250, 300, 325, 350):
            c1 = counts(m, d, 1e-42); c2 = counts(m, d, 1e-42, vE=267.0)
            s1 = 1e-42 / c1['hi'] if c1['hi'] > 0 else float('inf'); s2 = 1e-42 / c2['hi'] if c2['hi'] > 0 else float('inf')
            row.append(f"d={d}: {s1:.1e} ({s2:.1e}) lo/hi={c1['lo']/c1['hi'] if c1['hi']>0 else float('nan'):.2f} ab/hi={c1['above']/c1['hi'] if c1['hi']>0 else float('nan'):.2f}")
        print(f" m={m:6.0f}: " + " | ".join(row))
