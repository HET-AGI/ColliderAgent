# 1. Target

Consider the $Z'$ model described in this document, plot the cross section of the process $pp \to Z' \to \mu^+ \mu^-$ as a function of the $Z'$ mass.

# 2. Model

In this section, the general $Z'$ model is described.

## 2.1 Lagrangian

$$
\mathcal{L}_{NP} = -\frac{1}{4} Z'_{\mu\nu} Z'^{\mu\nu} + \frac{1}{2} M_{Z'}^2 Z'_\mu Z'^{\mu} - Z'_\mu \left[
  \sum_{i=1}^{3} \bar{u}_i \gamma^\mu (g_{Lu} P_L + g_{Ru} P_R) u_i + \sum_{i=1}^{3} \bar{d}_i \gamma^\mu (g_{Ld} P_L + g_{Rd} P_R) d_i + \sum_{i=1}^{3} \bar{\ell}_i \gamma^\mu (g_{Le} P_L + g_{Re} P_R) \ell_i + \sum_{i=1}^{3} \bar{\nu}_i \gamma^\mu\, g_{Lv} P_L\, \nu_i
\right]
$$

where:
- $Z'$ is a new neutral vector boson beyond the SM.
- $i = 1,2,3$ sums over the three generations
- $u_i = \{u, c, t\}$, $d_i = \{d, s, b\}$, $\ell_i = \{e, \mu, \tau\}$, $\nu_i = \{\nu_e, \nu_\mu, \nu_\tau\}$ are all the SM fermions.
- $P_{L,R} = (1 \mp \gamma^5)/2$ are chiral projectors
- $Z'_{\mu\nu} = \partial_\mu Z'_\nu - \partial_\nu Z'_\mu$

## 2.2 Parameters

The free parameters are:
- $m_{Z'}$: Z' mass [GeV]
- $g_{Lu}$: Left-handed coupling to up-type quarks
- $g_{Ru}$: Right-handed coupling to up-type quarks
- $g_{Ld}$: Left-handed coupling to down-type quarks
- $g_{Rd}$: Right-handed coupling to down-type quarks
- $g_{Le}$: Left-handed coupling to charged leptons
- $g_{Re}$: Right-handed coupling to charged leptons
- $g_{Lv}$: Left-handed coupling to neutrinos


# 3. Collider Process

## 3.1 Process
$$p p \to Z' \to \mu^+ \mu^-$$

## 3.2 Collider simulation settings
- $\sqrt{s} = 13$ TeV at the LHC
- Width of $Z'$ is computed automatically, considering only two-body decays.

## 3.3 Parameter settings for each run

We have two runs: run 1 for SSM scenario and run 2 for E6 scenario. For each run, we need to scan the Z' mass: 200, 400, 600, 800, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500 GeV. The coupling values in the two runs are given in the following table:

| Parameter | Run 1 value | Run 2 value |
|-----------|-------------|------------|
| $g_{Lu}$       | $\frac{e}{s_W c_W}(\frac{1}{2} - \frac{2}{3}s_W^2)$ | $g_\psi$ |
| $g_{Ru}$       | $\frac{e}{s_W c_W}(-\frac{2}{3}s_W^2)$ | $g_\psi$ |
| $g_{Ld}$       | $\frac{e}{s_W c_W}(-\frac{1}{2} + \frac{1}{3}s_W^2)$ | $g_\psi$ |
| $g_{Rd}$       | $\frac{e}{s_W c_W}(\frac{1}{3}s_W^2)$ | $g_\psi$ |
| $g_{Le}$       | $\frac{e}{s_W c_W}(-\frac{1}{2} + s_W^2)$ | $g_\psi$ |
| $g_{Re}$       | $\frac{e}{s_W c_W} s_W^2$ | $g_\psi$ |
| $g_{Lv}$       | $\frac{e}{2 s_W c_W}$ | $g_\psi$ |

Here:
- $s_W = \sin\theta_W$, $c_W = \cos\theta_W$ with $\sin^2\theta_W = 0.2312$
- $e = 0.3134$
- $g_\psi = 0.0942$


# 4. Numerical Analysis

## 4.1 Procedure to reproduce the figure

**step 1: extract cross section** 

Read cross section from the output of the collider simulation for each run.

**step 2: plot the cross section**

Plot the cross section vs. $Z'$ mass for each run.


### Plot styles

- x-axis
  - $Z'$ mass [GeV], 
  - range: [200, 5500], linear scale
- y-axis
  - cross section [pb], 
  - range: [5*10^-6, 5*10^-1], log scale
- two curves:
  - $Z'_{\text{SSM}}$: green dotted line
  - $Z'_ψ$: blue solid line