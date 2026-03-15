# 1. Target

Considering the $U_1$ vector leptoquark model described in this document, plot the normalized pseudorapidity ($\eta$) distributions for the Drell-Yan process $\mu^+\mu^- \to b\bar{b}$ at a muon collider with $\sqrt{s} = 3$ TeV.

---

# 2. $U_1$ Leptoquark Model

## 2.1 Lagrangian

$$\mathcal{L}_{U_1} = -\frac{1}{2} U_{1\,\mu\nu}^{\dagger} U_{1}^{\mu\nu} + m_{\rm LQ}^2 U_{1\,\mu}^{\dagger} U_1^{\mu} - i g_s (1 - \kappa_U) U_{1\,\mu}^{\dagger} T^a U_{1\,\nu} G^{a\,\mu\nu} - i g_Y \frac{2}{3}(1 - \tilde{\kappa}_U) U_{1\,\mu}^{\dagger} U_{1\,\nu} B^{\mu\nu} + \frac{g_U}{\sqrt{2}} \left[ U_1^{\mu} \left( \beta^{ij}_L \bar{Q}_L^i \gamma_{\mu} L_L^j \right) + \text{h.c.} \right]$$

where
- $U_{1\,\mu\nu} = D_{\mu}U_{1\,\nu} - D_{\nu}U_{1\,\mu}$
- $U_1$ is a vector leptoquark in the $(\mathbf{3}, \mathbf{1}, 2/3)$ representation of the SM gauge group.
- $g_U$ is the overall LQ-fermion coupling (set to 1).
- $\kappa_U$, $\tilde{\kappa}_U$ are non-minimal gauge coupling modifiers (both set to 0).
- $\beta_L^{ij}$ is the left-handed flavor coupling matrix. Only $\beta_L^{32}$ (b-quark to muon) is non-zero in this study.

## 2.2 Parameters

The free parameters are:
- $m_{\rm LQ}$: mass of the $U_1$ leptoquark
- $\beta_L^{32}$: coupling of $U_1$ to $b$-quark and $\mu$-lepton

Fixed parameters:
- $g_U = 1.0$
- $\kappa_U = \tilde{\kappa}_U = 0$
- $\beta_L^{22} = \beta_L^{23} = \beta_L^{33} = 0$

---

# 3. Collider Simulation

## 3.1 Process

$$\mu^+ \mu^- \to b \bar{b}$$

This process receives contributions from:
- **SM diagrams** ($s$-channel): $\mu^+\mu^- \to \gamma^*/Z^* \to b\bar{b}$
- **LQ diagram** ($t$-channel): $\mu^- b \to U_1 \to b\mu^-$ exchange, with coupling $\propto g_U \beta_L^{32}$ at each vertex
- comment:
  - The interference between SM and LQ diagrams is the key observable.
  - In MadGraph, `NP=4` ensures both the SM diagrams (NP=0) and the LQ t-channel diagram (NP=4, two LQ-fermion vertices each contributing NP=2) are included, along with their interference.

## 3.2 Collider simulation settings

The simulation requires three separate runs.

**Common settings (all runs):**
- collider: 3 TeV muon collider ($E_{\rm beam}$ = 1500 GeV per beam)
- simulation level: parton-level

**Run 1: SM baseline**
- All $\beta_L^{ij} = 0$ (LQ decoupled)
- $m_{\rm LQ} = 10^5$ GeV (effectively decoupled)
- Events: 500,000
- Purpose: establish the SM $\eta$ distribution

**Run 2: LQ signal at $\beta_L^{32} = 1.0$**
- $\beta_L^{32} = 1.0$, all other $\beta_L^{ij} = 0$
- Mass scan: $m_{\rm LQ}$ = 1 TeV and 10 TeV 
- Events: 50,000 per mass point

**Run 3: LQ signal at $\beta_L^{32} = 0.1$**
- $\beta_L^{32} = 0.1$, all other $\beta_L^{ij} = 0$
- Mass scan: same mass points as Run 2
- Events: 50,000 per mass point

---

# 4. Numerical Analysis


## 4.1 Pseudorapidity distribution


**step 1: extract pseudorapidity**

From the output of the collider simulation for each run, extract the pseudorapidity distribution of the $b$ quark.

**step 2: histogram the pseudorapidity**

Histogram the pseudorapidity into 13 bins from 0 to 2.5: a narrow first bin [0, 0.1], then uniform 0.2-wide bins up to 2.5

**step 3: normalize the distribution**

Normalize the distribution obtained in step 2 to the total number of events in the run.


## 4.2. Plot figure

The figure has two panels side by side. Each panel contains:
1. **SM background**: gray filled bar histogram (normalized $|\eta|$ distribution)
2. **$m_{\rm LQ} = 1$ TeV**: blue dashed step histogram
3. **$m_{\rm LQ} = 10$ TeV**: orange dashed step histogram

- **Left panel**: $\beta_L^{32} = 1.0$
- **Right panel**: $\beta_L^{32} = 0.1$

### Plot styles
- Figure size: 14 × 6 (two side-by-side panels)
- x-axis: $\eta$, range [0, 2.6]
- y-axis: Normalized Distribution, range [0, 0.20], ticks at 0.05, 0.10, 0.15, 0.20
- Each panel shows text labels for $\beta_L^{32}$ value and $\sqrt{s} = 3$ TeV
- Legend with three entries in upper right of each panel
