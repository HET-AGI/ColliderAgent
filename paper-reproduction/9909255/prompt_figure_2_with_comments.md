# 1. Target

Considering the KK graviton model, plot the cross section of the process $e^+ e^- \to \mu^+ \mu^-$ as a function of the center-of-mass energy $\sqrt{s}$.

---

# 2. Model

In this section, the Lagrangian of the KK graviton is given.


## 2.1 Lagrangian

$$
\mathcal{L}_{\mathrm{int}}^{\mathrm{SM}}
= -\frac{1}{\overline{M}_{Pl}}\,
  T^{\alpha\beta}(x)\,
  h^{(0)}_{\alpha\beta}(x) -\frac{1}{\Lambda_\pi}\,
  T^{\alpha\beta}(x)\,
  \sum_{n=1}^{\infty} h^{(n)}_{\alpha\beta}(x)\,,
$$
where $T^{\alpha\beta}$ is the sum of the symmetric, conserved energy–momentum tensors of all the SM fields:
$$
T^{\alpha\beta}
= T^{\alpha\beta}_{\mathrm{fermions}} + T^{\alpha\beta}_{\mathrm{gluon}} + T^{\alpha\beta}_{\gamma} + T^{\alpha\beta}_{W} + T^{\alpha\beta}_{Z} + T^{\alpha\beta}_{\mathrm{Higgs}}\,.
$$
The explicit expression for each term will be given in the following sections. The new partiles and paraeters are summarized below:
- $h^{(0)}_{\alpha\beta}$: massless 4D graviton (zero mode), coupling $\overline{M}_{Pl}^{-1}$.
- $h^{(n)}_{\alpha\beta}$: $n=1,2,3,4,5$ (i.e. $n \leq 5$) massive KK gravitons, mass $m_n$, coupling $\Lambda_\pi^{-1}$. 
  - comment: It's enough to consider the first 5 KK modes.
- Free parameters are $m_1,m_2,\ldots$, $\overline{M}_{Pl}$, $\Lambda_\pi$.



### Fermion sector $T^{\alpha\beta}_{\mathrm{fermions}}$

For a Dirac field $\psi$ (mass $m$), the Belinfante energy–momentum tensor is
$$
T^{\alpha\beta}_{(\psi)}
= \frac{i}{4}\Bigl[
  \bar{\psi}\gamma^\alpha \partial^\beta \psi - (\partial^\beta \bar{\psi})\gamma^\alpha \psi  + (\alpha \leftrightarrow \beta)
\Bigr]\,.
$$

Summing over all SM fermions (leptons $e,\mu,\tau$ and neutrinos $\nu_e,\nu_\mu,\nu_\tau$, quarks $u,d,c,s,t,b$):
$$
T^{\alpha\beta}_{\mathrm{fermions}}
= \sum_{\ell = e,\mu,\tau} T^{\alpha\beta}_{(\ell)} + \sum_{\nu=\nu_e,\nu_\mu,\nu_\tau} T^{\alpha\beta}_{(\nu)}  + \sum_{q = u,d,c,s,t,b} T^{\alpha\beta}_{(q)}\,.
$$


### Gauge boson sector $T^{\alpha\beta}_{\mathrm{gauge}}$

**Gluons ($G^a_\mu$, $SU(3)_c$)**

$$
T^{\alpha\beta}_{\mathrm{gluon}}
= F^{a\,\alpha\rho} F^{a\,\beta}{}_{\rho} - \frac{1}{4}\eta^{\alpha\beta} F^{a}_{\rho\sigma} F^{a\,\rho\sigma}\,,
$$
where $F^a_{\mu\nu} = \partial_\mu G^a_\nu - \partial_\nu G^a_\mu + g_s f^{abc} G^b_\mu G^c_\nu$.

**Photon ($A_\mu$, $U(1)_{\text{em}}$)**

$$
T^{\alpha\beta}_{\gamma}
= F^{\alpha\rho} F^{\beta}{}_{\rho} - \frac{1}{4}\eta^{\alpha\beta} F_{\rho\sigma} F^{\rho\sigma}\,,
$$
where $F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu$.

**W and Z ($W^\pm_\mu$, $Z_\mu$)**

$$
T^{\alpha\beta}_{W}
= W^{i\,\alpha\rho} W^{i\,\beta}{}_{\rho} - \frac{1}{4}\eta^{\alpha\beta} W^i_{\rho\sigma} W^{i\,\rho\sigma}\,,
$$
$$
T^{\alpha\beta}_{Z}
= Z^{\alpha\rho} Z^{\beta}{}_{\rho} - \frac{1}{4}\eta^{\alpha\beta} Z_{\rho\sigma} Z^{\rho\sigma}\,,
$$
where $W^i_{\mu\nu}$ and $Z_{\mu\nu}$ are the corresponding field strengths.



### Higgs sector $T^{\alpha\beta}_{\mathrm{Higgs}}$

$$
T^{\alpha\beta}_{\mathrm{Higgs}}
= (\partial^\alpha h)(\partial^\beta h)   - \eta^{\alpha\beta}\Bigl[ \frac{1}{2}(\partial_\rho h)(\partial^\rho h) - \frac{1}{2}m_h^2 h^2 \Bigr]\,.
$$

## 2.2 Note

The Lagrangian in this section is in the unitary gauge.

---

# Collider process

## Process
$$e^+ e^- \to \mu^+ \mu^-$$

## Collider Simulation settings
- $\sqrt{s} = 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200\,\mathrm{GeV}$
- The energy of $e^+$ ($E^+$) equals the energy of $e^-$ ($E^-$), i.e., taking $E^+ = E^- = \sqrt{s}/2$.
- Generate 100 events for each energy point.
- The widths of all the gravitons are computed automatically, considering only two-body decays.


## Parameter settings for each run


- $m_1 = 600\,\mathrm{GeV}$, $m_2 = 1098\,\mathrm{GeV}$, $m_3 = 1592\,\mathrm{GeV}$, $m_4 = 2086\,\mathrm{GeV}$, $m_5 = 2580\,\mathrm{GeV}$
- $\overline{M}_{Pl} = 2.4\times 10^{18}\,\mathrm{GeV}$
- $\Lambda_\pi = 522\,\mathrm{GeV}$

---

# Analysis

## Procedure to produce the figure

**Step 1: extract cross section data**:
Read $\sigma(e^+ e^- \to \mu^+ \mu^-)$ from the output of the collider simulation for each energy point.

**Step 2: plot the figure**:
Plot the cross section vs $\sqrt{s}$ for each energy point.

### Plot styles
- x-axis
  - $\sqrt{s}$ (GeV)
  - range: [50, 1500], linear scale
- y-axis
  - $\sigma$ (fb), 
  - range: [20^2, 5*10^6], logarithmic scale
- line color: blue