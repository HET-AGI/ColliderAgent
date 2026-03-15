# 1. Target

Considering the $U_1$ vector leptoquark model described in this document, plot the expected exclusion and discovery contours for the coupling $\beta_L^{32}$ and the LQ mass at a muon collider at $\sqrt{s} = 3$ (1 ab$^{-1}$) and $14$ TeV (20 ab$^{-1}$).

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

$$\mu^+\mu^- \to b\bar b$$

This receives contributions from:
- **SM (s-channel)**: $\mu^+\mu^- \to \gamma^*/Z^* \to b\bar b$
- **LQ (t-channel)**: $\mu^-$ exchanges a virtual $U_1$ with the $b$ quark, interfering with the SM amplitude


## 3.3 Collider settings

- collider: Muon collider
- simulation level: parton-level

## 3.4 SM background runs

Perform 2 SM background runs:
- $\sqrt{s} = 3$ TeV, $N_{\rm events} = 100,000$
- $\sqrt{s} = 14$ TeV, $N_{\rm events} = 100,000$

## 3.5 LQ signal runs

Perform 4 LQ signal runs with mass scans:
- $\sqrt{s} = 3$ TeV, $\beta_L^{32} = 1.0$
- $\sqrt{s} = 3$ TeV, $\beta_L^{32} = 2.0$      
- $\sqrt{s} = 14$ TeV, $\beta_L^{32} = 1.0$
- $\sqrt{s} = 14$ TeV, $\beta_L^{32} = 2.0$

For each run:
- number of events: 50,000
- perform mass scan over the points: 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 15.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0 TeV


---

# 4. Numerical Analysis

## 4.1 Observable: binned $|\eta|$ distribution

For the 2-body final state $\mu^+\mu^- \to b\bar b$, both $b$ and $\bar b$ have $|\eta_b| = |\eta_{\bar b}|$, so each event gives one $|\eta|$ value.

**Binning**: 10 equal-width bins in $|\eta| \in [0,\, 2.5]$ (bin width = 0.25).

### Step 1: extract per-bin cross sections

For each simulation run (SM or LQ signal at a given mass point):

1. Read the total cross section $\sigma_{\rm total}$ from the simulation output (in pb).
2. Compute the pesudorapidity $|\eta|$ of the final-state $b$ quark for each event.
3. Bin the events into 10 $|\eta|$ bins, giving counts $n_i$ and total events $N_{\rm total}$.
4. Compute per-bin cross section: $\sigma_i = \sigma_{\rm total} \times n_i / N_{\rm total}$ (pb).

### Step 2: obtain the cross section for arbitrary $\beta_L^{32}$

For each $\sqrt{s}$ and each LQ mass point $m$, the per-bin cross section follows:

$$\sigma_i(m,\,\beta) = b_i + \beta^2\, I_i(m) + \beta^4\, J_i(m)$$

where $b_i$ is the SM per-bin cross section, $I_i(m)$ is the interference coefficient, and $J_i(m)$ is the LQ-squared coefficient.


From the cross sections corresponding to the two runs with $\beta_L^{32} = 1.0$ and $2.0$, extract the coefficients $I_i$ and $J_i$ by solving the $2 \times 2$ linear system. Then, the cross sections for arbitrary $\beta_L^{32}$ can be obtained.

## 4.2 Statistical analysis: binned likelihood ratio

**signal event counts** per bin:
$$\mu_i(m, \beta) = \sigma_i(m, \beta) \times \mathcal{L} \times 1000 $$
- the factor 1000 is to convert from pb to fb.

**background event counts** per bin:
$$b_i^{\rm events} = b_i \times \mathcal{L} \times 1000$$

**Luminosity**:
- $\sqrt{s} = 3$ TeV: $\mathcal{L} = 1000\,{\rm fb}^{-1}$
- $\sqrt{s} = 14$ TeV: $\mathcal{L} = 20{,}000\,{\rm fb}^{-1}$

### 95% CL exclusion

Assume observed data equals SM prediction ($n_i = b_i^{\rm events}$):

$$-2\log\lambda = 2\sum_{i=1}^{10}\left[\mu_i - b_i + b_i \ln\frac{b_i}{\mu_i}\right]$$

Exclusion at 95% CL is defined by $-2\log\lambda > \chi^2(10,\,0.95) = 18.307$.

### 5$\sigma$ discovery

Assume observed data equals LQ prediction ($n_i = \mu_i$):

$$-2\log\lambda = 2\sum_{i=1}^{10}\left[b_i - \mu_i + \mu_i \ln\frac{\mu_i}{b_i}\right]$$

Discovery at 5$\sigma$ is defined by $-2\log\lambda > \chi^2(10,\,p = 5.7\times 10^{-7}) \approx 48.2$.

---

## 4.3. Plot Figure

**step1: extract the exclusion and discovery contours**

For each $\sqrt{s}$: 
1. At each simulated LQ mass point, scan over $\beta$ values to find where $-2\log\lambda$ crosses the critical threshold.
2. The locus of (LQ mass, crossing points) forms the exclusion / discovery contour.

**step2: plot the figure**
Plot the exclusion and discovery contours for each $\sqrt{s}$.

### Plot style
- x-axis: $m_{\rm LQ}$ [TeV], range [1, 75], log scale
- y-axis: $\beta_L^{32}$, range [10⁻³, 2], log scale
- aspect ratio: 1
- exclusion and discovery contours
  - $\sqrt{s} = 3$ TeV: red color
  - $\sqrt{s} = 14$ TeV: purple color
  - for both $\sqrt{s}$: dashed line for exclusion, solid line for discovery