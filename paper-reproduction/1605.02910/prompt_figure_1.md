# 1. Target

Considering a New Physics model involving a $Z'$ boson, plot a figure with three panels. Each panel shows the exclusion contours in the $(\tilde{g}, g_1')$ plane for a different Z' mass at the LHC Run 1 dilepton search at $\sqrt{s} = 8$ TeV with $\mathcal{L} = 20$ fb$^{-1}$. The model, the processes at the LHC which are necessary to reproduce the figure, and the numerical analysis steps to produce the figure are given in the following sections.

---

# 2. Model

## 2.1 Lagrangian

$$\mathcal{L}_{Z'ff} = \sum_{f} Z'_\mu \bar{f} \gamma^\mu (C_{f,L} P_L + C_{f,R} P_R) f$$

## 2.2 Parameters

The couplings in the Lagrangian are given by:

$$C_{f,L} = -e \frac{\sin\theta'}{\sin\theta_W \cos\theta_W} (T_f^3 - \sin^2\theta_W  Q_f) + (\tilde{g}  Y_{f,L} + g_1'  z_f) \cos\theta'$$

$$C_{f,R} = e \frac{\sin\theta_W \sin\theta'}{\cos\theta_W} Q_f + (\tilde{g}  Y_{f,R} + g_1'  z_f) \cos\theta'$$

In the above equations:

- The mixing angle takes the form: $$\theta' = \tilde{g}\frac{ M_Z (v/2)}{M_{Z'}^2 - M_Z^2}$$
- $z_f$ is the $B-L$ charge of the fermion $f$, i.e., $Y_{B-L}$ in the table below.
- Therefore, $C_{f,L}$ and $C_{f,R}$ can be determined by 
  - $g_1'$: B-L gauge coupling
  - $\tilde{g}$: Kinetic mixing
  - $M_{Z'}$: $Z'$ mass
  - Choose these three parameters as input parameters.
- All the other parameters not mentioned above are the SM parameters.

## 2.3 Particles

The particles appearing in the Lagrangian are summarized below:

- $Z'$: $Z'$ boson is a new vector boson beyond the SM.
- $f$ denotes the SM fermions and the heavy neutrinos:


| Field              | $Y$ (hypercharge) | $Y_{B-L}$ ($z_f$) | 
| ------------------ | ----------------- | ----------------- | 
| $Q_L = (u_L, d_L)$ | $+1/6$            | $+1/3$            | 
| $u_R$              | $+2/3$            | $+1/3$            | 
| $d_R$              | $-1/3$            | $+1/3$            | 
| $L = (\nu_L, e_L)$ | $-1/2$            | $-1$              | 
| $e_R$              | $-1$              | $-1$              | 
| $\nu_h$            | $0$               | $-1$              | 

- Note: $\nu_R$ is the gauge eigenstate (right-handed neutrino field in the Lagrangian). After the type-I seesaw mechanism, the mass eigenstates are: light neutrinos (mostly $\nu_L$) and heavy neutrinos $\nu_h$ (mostly $\nu_R$). Since the mixing is tiny ($\sim m_D/M \ll 1$), $\nu_h \approx \nu_R$ and inherits its quantum numbers.


---

# 3. Collider Process

## 3.1 Signal Process: $pp \to Z'$

### Process
$$pp \to Z'$$  

### Collider settings

- $\sqrt{s} = 8$ TeV at the LHC


### Parameter settings for each run

Since the Z' production cross section is an exact quadratic form in the couplings:
$$\sigma(pp \to Z') = A  g_1'^2 + B  g_1' \tilde{g} + C  \tilde{g}^2$$
only 3 MadGraph runs per $M_{Z'}$ are needed (9 runs total for 3 mass points). The parameter settings are listed below:

- For **$M_{Z'} = 2$ TeV** at $\sqrt{s} = 8$ TeV:


| Run | $g_1'$ | $\tilde{g}$ | Purpose                 |
| --- | ------ | ----------- | ----------------------- |
| 1   | 0.10   | 0           | Determines $A$          |
| 2   | 0.10   | $-0.10$     | Mixed point             |
| 3   | 0.15   | $-0.05$     | Third independent point |


- For **$M_{Z'} = 2.5$ TeV** at $\sqrt{s} = 8$ TeV:


| Run | $g_1'$ | $\tilde{g}$ | Purpose                 |
| --- | ------ | ----------- | ----------------------- |
| 4   | 0.10   | 0           | Determines $A$          |
| 5   | 0.10   | $-0.10$     | Mixed point             |
| 6   | 0.15   | $-0.05$     | Third independent point |


- For **$M_{Z'} = 3$ TeV** at $\sqrt{s} = 8$ TeV:


| Run | $g_1'$ | $\tilde{g}$ | Purpose                 |
| --- | ------ | ----------- | ----------------------- |
| 7   | 0.30   | 0           | Determines $A$          |
| 8   | 0.30   | $-0.30$     | Mixed point             |
| 9   | 0.50   | $-0.60$     | Third independent point |


**Solving for coefficients:**
From the 3 runs for each mass, solve the linear system:
$$\begin{pmatrix} g_{1,1}'^2 & g_{1,1}' \tilde{g}*1 & \tilde{g}1^2  g{1,2}'^2 & g*{1,2}' \tilde{g}*2 & \tilde{g}2^2  g{1,3}'^2 & g*{1,3}' \tilde{g}_3 & \tilde{g}_3^2 \end{pmatrix} \begin{pmatrix} A  B  C \end{pmatrix} = \begin{pmatrix} \sigma_1  \sigma_2  \sigma_3 \end{pmatrix}$$
to determine $A, B, C$ for each mass point.


## 3.2 Background Process

### Process
- SM Drell-Yan dilepton production
$$pp \to \ell^+\ell^- \quad (\ell = e, \mu)$$

### Collider settings

- $\sqrt{s} = 8$ TeV at the LHC
- Generator-level invariant mass cut: $m_{\ell\ell} > 0.9 \times M_{Z'}$ (to select events near the Z' resonance)

---

# 4. Numerical Analysis

## 4.1 Procedure to produce the figure

You can follow the steps below to produce the figure:

### Step 1: Extract cross sections from MadGraph output
Read $\sigma(pp \to Z')$ from the MadGraph banner/log for each of the 9 signal runs and 3 background runs.

### Step 2: Determine quadratic coefficients
For each $M_{Z'}$, solve for $(A, B, C)$ from the 3 signal runs by using the method mentioned in section 3.1.

### Step 3: Compute branching ratio analytically
The branching ratio $\text{BR}(Z' \to e^+e^- + \mu^+\mu^-)$ is computed analytically from the Z' partial width formulas, which are given below:

**SM fermion partial widths** 

$$\Gamma(Z' \to f\bar{f}) = \frac{M_{Z'}}{12\pi} N_c \left(C_{f,L}^2 + C_{f,R}^2\right)$$

where $N_c = 3$ for quarks and $N_c = 1$ for leptons. The SM fermion channels are:
- 3 generations of up-type quarks ($\times 3$ colors)
- 3 generations of down-type quarks ($\times 3$ colors)
- 3 generations of charged leptons
- 3 SM neutrinos (left-handed only, coupling $C_{\nu_L,L}$)

**Heavy neutrino partial width:**

$$\Gamma(Z' \to \nu_h \nu_h) = \frac{M_{Z'}}{24\pi} (z_{\nu_R}\, g_1'\, \cos\theta')^2 \left(1 - \frac{4m_{\nu_h}^2}{M_{Z'}^2}\right)^{3/2}$$

- The model contains 3 heavy Majorana neutrinos $\nu_h$. They are degenerate in mass.

**Total width:**

$$\Gamma(Z') = 3\Gamma(Z' \to \nu_h \nu_h) + \sum_{f\in \text{SM}}\Gamma(Z' \to f\bar{f})$$



**Branching ratio:**

$$\text{BR}(Z' \to e^+e^- + \mu^+\mu^-) = \frac{\Gamma(Z' \to e^+e^-) + \Gamma(Z' \to \mu^+\mu^-)}{\Gamma(Z')}$$

### Step 4: Compute signal and background event counts on a 2D grid in $(\tilde{g}, g_1')$

Signal events:
$$S(\tilde{g}, g_1') = \sigma_{\text{LO}}(g_1', \tilde{g}) \times \text{BR}(Z' \to e^+e^- + \mu^+\mu^-) \times k_{\text{NNLO}}(M_{Z'}) \times \epsilon_{\text{acc}} \times \mathcal{L}$$

Background events:
$$B = \sigma_{\text{bg}}(M_{Z'}) \times k_{\text{NNLO}}(M_{Z'}) \times \epsilon_{\text{acc}} \times \mathcal{L}$$


**Input parameters:**

- $k_{\text{NNLO}}$: mass-dependent NNLO QCD k-factor from Accomando et al. (arXiv:1010.6058):

  | $M_{Z'}$ | $k_{\text{NNLO}}$ |
  | -------- | ----------------- |
  | 2 TeV    | 1.35              |
  | 2.5 TeV  | 1.40              |
  | 3 TeV    | 1.50              |

- $\epsilon_{\text{acc}} = 0.6$: combined acceptance $\times$ efficiency for dilepton selection
- $\mathcal{L} = 20$ fb$^{-1}$: LHC Run 1 integrated luminosity at 8 TeV
- heavy neutrinomass $m_{\nu_h} = 95$ GeV (degenerate, 3 generations)


## Step 5: Apply exclusion criterion

Definition and the criterion of significance are given below:
$$\text{Sig} = 2\left(\sqrt{S + B} - \sqrt{B}\right) \geq 2$$

This is equivalent to requiring $S \geq 1 + 2\sqrt{B}$. It means the exclusion contour is the locus of points in $(\tilde{g}, g_1')$ where $\text{Sig} = 2$.

## Step 6: Plot the exclusion contours

Three panels side by side:

- **Panel (a):** $M_{Z'} = 2.0$ TeV
- **Panel (b):** $M_{Z'} = 2.5$ TeV
- **Panel (c):** $M_{Z'} = 3.0$ TeV

Each panel shows:

- A black contour line at $\text{Sig} = 2$ (the exclusion boundary)

### Plot styles

- all panels:
  - aspect ratio: 1:1
  - x-axis: $\tilde{g}$
  - y-axis: $g_1'$
- panel A:
  - x-axis range: [-0.6, 0.4]
  - y-axis range: [0.0, 0.6]
- panel B:
  - x-axis range: [-1.0, 0.6]
  - y-axis range: [0.0, 0.75]
- panel C:
  - x-axis range: [-1.0, 0.8]
  - y-axis range: [0.0, 0.9]