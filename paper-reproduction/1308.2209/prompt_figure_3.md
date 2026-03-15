
# 1. Target


Consider the BSM model with a single heavy Majorana neutrino described in this document, plot the cross section of the process $pp \to \mu^\pm N$ as a function of the heavy neutrino mass.


# 2. Model

In this section, the BSM model with a single heavy Majorana neutrino $N$ is introduced.

## 2.1 Lagrangian


$$\mathcal{L}_N = -\frac{g_2}{\sqrt{2}} V_{\mu N} \left(\bar{\mu} \gamma^\mu P_L N\right) W^-_\mu - \frac{g_2}{2 c_W} V_{\mu N} \left(\bar{\nu}_\mu \gamma^\mu P_L N\right) Z_\mu + \text{h.c.}$$

where
- $N$ is the heavy Majorana neutrino beyond the SM.
- $V_{\mu N}$ is the neutrino mixing parameter (real, dimensionless).
- $g_2$ is the $SU(2)_L$ gauge coupling
- $c_W \equiv \cos\theta_W$ is the cosine of the weak mixing angle
- $P_L = \frac{1}{2}(1-\gamma^5)$ is the left-chiral projector.


# 3. Collider Process

## 3.1 Process

$$pp \to \mu^\pm N$$


## 3.2 Collider simulation settings

There are three runs.

- Run 1: $\sqrt{s} = 7$ TeV at the LHC
- Run 2: $\sqrt{s} = 8$ TeV at the LHC
- Run 3: $\sqrt{s} = 14$ TeV at the LHC


For each run:
- PDF: CTEQ6L



## 3.3 Parameter settings for each run

- $|V_{\mu N}| = 1$
- $m_N$ = 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000 GeV


# 4. Numerical Analysis

## 4.1 Procedure to produce the figure

**Step 1: extract cross section date**

Read the cross section data from the existing MadGraph output directories for $\sqrt{s} = 7, 8, 14$ TeV. 

**Step 2: plot the figure**

Plot the cross section vs $m_N$ for the three runs.


### Plot styles
- Label the run information above each plot, e.g. $\sqrt{s} = 7$ TeV, $\sqrt{s} = 8$ TeV, $\sqrt{s} = 14$ TeV
- aspect ratio: 1:1
- x-axis
  - $m_N$ [GeV]
  - range: [100, 1000]
  - scale: linear
- y-axis
  - cross section [fb]  
  - range: [0.1, 4x10^4]
  - scale: logarithmic