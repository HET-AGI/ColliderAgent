#!/usr/bin/env python3
"""[estimate] One-parameter C_VL fit to the HFLAV CKM-2025 R(D), R(D*) average, and the implied U1 coupling band.
Inputs: HFLAV web page (last update 28.09.2025); PDG 2025 CKM review Eq. (12.27); eta_QCD = 1.12 from arXiv:2405.06062."""
import numpy as np

RD, sRD, RDs, sRDs, rho = 0.358, 0.024, 0.281, 0.011, -0.374      # HFLAV CKM 2025
RDsm, sRDsm, RDssm, sRDssm = 0.298, 0.004, 0.254, 0.005           # HFLAV arithmetic-average SM predictions
v, Vcs, Vcb = 246.22, 0.97349, 0.04183
ETA = 1.12


def chi2(x):
    d = np.array([RD - x * RDsm, RDs - x * RDssm])
    C = np.array([[sRD**2 + (x * sRDsm)**2, rho * sRD * sRDs], [rho * sRD * sRDs, sRDs**2 + (x * sRDssm)**2]])
    return d @ np.linalg.inv(C) @ d


xs = np.linspace(0.9, 1.4, 50001)
c = np.array([chi2(x) for x in xs])
i = c.argmin()
e = lambda x: np.sqrt(x) - 1
lo1, hi1 = xs[c <= c[i] + 1][[0, -1]]
lo2, hi2 = xs[c <= c[i] + 4][[0, -1]]
print(f"chi2_SM={chi2(1.0):.2f} chi2_min={c[i]:.2f}")
print(f"C_VL best={e(xs[i]):.4f} 1s=[{e(lo1):.4f},{e(hi1):.4f}] 2s=[{e(lo2):.4f},{e(hi2):.4f}]")
for beta in (0.2, 1.0, 2.2):
    for M in (1500, 2000, 2500, 3000):
        g = lambda ep: 2 * M / v * np.sqrt(ep / (ETA * (1 + Vcs / Vcb * beta)))
        print(f"beta23={beta} M={M}: gU best {g(e(xs[i])):.3f} 1s [{g(e(lo1)):.3f},{g(e(hi1)):.3f}] 2s [{g(e(lo2)):.3f},{g(e(hi2)):.3f}]")
