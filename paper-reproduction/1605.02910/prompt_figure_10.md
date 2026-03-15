


# Model

## Lagrangian

$$\mathcal{L}_{Z'ff} = \sum_{f} Z'_\mu \bar{f} \gamma^\mu (C_{f,L} P_L + C_{f,R} P_R) f$$


## Parameters

The couplings in the Lagrangian are given by:

$$C_{f,L} = -e \frac{\sin\theta'}{\sin\theta_W \cos\theta_W} (T_f^3 - \sin^2\theta_W \, Q_f) + (\tilde{g} \, Y_{f,L} + g_1' \, z_f) \cos\theta'$$

$$C_{f,R} = e \frac{\sin\theta_W \sin\theta'}{\cos\theta_W} Q_f + (\tilde{g} \, Y_{f,R} + g_1' \, z_f) \cos\theta'$$

In the above equations:
- The mixing angle takes the form: $$\theta' = \tilde{g}\frac{ M_Z (v/2)}{M_{Z'}^2 - M_Z^2}$$
- $z_f$ is the $B-L$ charge of the fermion $f$, i.e., $Y_{B-L}$ in the table below.
- Therefore, $C_{f,L}$ and $C_{f,R}$ can be determined by 
    - $g_1'$: B-L gauge coupling
    - $\tilde{g}$: Kinetic mixing
    - $M_{Z'}$: $Z'$ mass
    - We choose these three parameters as input parameters.
- All the other parameters not mentioned above are the SM parameters.




## Particles

The particles appearing in the Lagrangian are summarized below:
- $Z'$: $Z'$ boson is a new vector boson beyond the SM.
- $f$ denotes the SM fermions. It can be any of the following:

| Field | $Y$ (hypercharge) | $Y_{B-L}$ ($z_f$) |
|-------|-------------------|-----------|
| $Q_L = (u_L, d_L)$ | $+1/6$ | $+1/3$ |
| $u_R$ | $+2/3$ | $+1/3$ |
| $d_R$ | $-1/3$ | $+1/3$ |
| $L = (\nu_L, e_L)$ | $-1/2$ | $-1$ |
| $e_R$ | $-1$ | $-1$ |
| $\nu_R$ | $0$ | $-1$ |


# Collider Process

## Process
$$pp \to Z'$$

## Collider settings
- $\sqrt{s} = 13$ TeV at the LHC


## Parameter settings for each run

Since $\sigma(pp \to Z') = A \, g_1'^2 + B \, g_1' \tilde{g} + C \, \tilde{g}^2$, only 3 runs per $M_{Z'}$ are needed:

For **$M_{Z'} = 2$ TeV:**
| Run | $g_1'$ | $\tilde{g}$ | Purpose |
|-----|--------|------------|---------|
| 1 | 0.10 | 0 | Determines $A$ |
| 2 | 0.10 | $-0.10$ | Mixed point |
| 3 | 0.15 | $-0.05$ | Third independent point |

For **$M_{Z'} = 3$ TeV:**
| Run | $g_1'$ | $\tilde{g}$ | Purpose |
|-----|--------|------------|---------|
| 4 | 0.30 | 0 | Determines $A$ |
| 5 | 0.30 | $-0.30$ | Mixed point |
| 6 | 0.50 | $-0.60$ | Third independent point |

**Solving for coefficients:**
From Run 1: $\sigma_1 = A (0.1)^2 \Rightarrow A = 100 \sigma_1$
From Run 2: $\sigma_2 = A(0.1)^2 + B(0.1)(-0.1) + C(-0.1)^2 = 0.01A - 0.01B + 0.01C$
From Run 3: $\sigma_3 = A(0.15)^2 + B(0.15)(-0.05) + C(-0.05)^2 = 0.0225A - 0.0075B + 0.0025C$

These 3 equations uniquely determine $A, B, C$.

---

# Numerical Analysis

## Primary observable
- Total production cross section $\sigma(pp \to Z')$.
- You can use $\sigma(g_1', \tilde{g}) = A g_1'^2 + B g_1' \tilde{g} + C \tilde{g}^2$ obtained from the last section to calculate the cross section.


## Target

- Plot $\sigma(pp \to Z')$ vs $g_1'$ for two parameter settings
  - Panel A
    - $M_{Z'} = 2$ TeV
    - $\tilde{g} = 0$ (black), $\tilde{g} = -0.05$ (blue), $\tilde{g} = -0.1$ (red)
  - Panel B
    - $M_{Z'} = 3$ TeV
    - $\tilde{g} = 0$ (black), $\tilde{g} = -0.3$ (blue), $\tilde{g} = -0.6$ (red)


### Plot styles

- for all the panels
    - y-axis: $\sigma$ (pb), logarithmic scale
    - x-axis: $g_1'$, linear scale
- panel A
    - x-axis range: [0.0, 0.20]
    - y-axis range: [10^-4, 10^-1]
- panel B
    - x-axis range: [0.0, 0.70]
    - y-axis range: [10^-4, 10^1]

