# 1. Target

Considering the ALP EFT in this document, plot the normalized $E_T^{\text{miss}}$ distribution for $pp \to a\,W^\pm\gamma$ ($W^\pm \to \ell^\pm\nu$) at $\sqrt{s} = 13$ TeV LHC.


---

# 2. ALP EFT

## 2.1 Lagrangian

The ALP bosonic EFT Lagrangian reads:

$$\delta\mathscr{L}_a^{\text{bosonic}} = c_{\tilde{W}} \mathcal{A}_{\tilde{W}} + c_{\tilde{B}} \mathcal{A}_{\tilde{B}}$$

where the operators are

$$\mathcal{A}_{\tilde{B}} = -B_{\mu\nu} \tilde{B}^{\mu\nu} \frac{a}{f_a}, \qquad \mathcal{A}_{\tilde{W}} = -W^a_{\mu\nu} \tilde{W}^{a\mu\nu} \frac{a}{f_a}.$$

Here,
- $a$ is the ALP (axion-like particle), a pseudo-scalar singlet, with mass $m_a$.
- $f_a$ is the ALP decay constant (dimension of mass).
- $B_{\mu\nu} = \partial_\mu B_\nu - \partial_\nu B_\mu$ is the U(1)$_Y$ hypercharge field strength tensor.
- $W^a_{\mu\nu} = \partial_\mu W^a_\nu - \partial_\nu W^a_\mu + g \epsilon^{abc} W^b_\mu W^c_\nu$ is the SU(2)$_L$ weak isospin field strength tensor ($a = 1,2,3$).
- $\tilde{B}^{\mu\nu} = \frac{1}{2}\epsilon^{\mu\nu\rho\sigma}B_{\rho\sigma}$, $\tilde{W}^{a\mu\nu} = \frac{1}{2}\epsilon^{\mu\nu\rho\sigma}W^a_{\rho\sigma}$ are the dual field strength tensors.
- $c_{\tilde{W}}, c_{\tilde{B}}$ are dimensionless Wilson coefficients. They satisfy the relation $$c_{\tilde{B}} =  -\tan^2\theta_W \cdot c_{\tilde{W}}$$ to enforce $g_{a\gamma\gamma} = 0$, where $\theta_W$ is the weak mixing angle.
- In the collider simulation, $f_a = 1000$ GeV and $m_a=0.001$ GeV is chosen. So the free parameter is $c_{\tilde{W}}$.


---

# 3. Collider Simulation

## 3.1 Process

$$p\,p \to a\,W^\pm\,\gamma , \quad W^\pm \to \ell^\pm \nu$$

## 3.2 Collider Simulation Settings

- Collider: 13 TeV LHC
- Event number: 500,000
- Analysis level: Parton-level (no parton shower or detector simulation)
- PDF: nn23lo1
- $f_a = 1000$ GeV, $m_1 = 0.001$ GeV, and $c_{\tilde{W}} = 1$

---

# 4. Numerical Analysis

## 4.1 Event Selection

Read the LHE events and apply the following selection cuts:
- photon $p_T$ > 20 GeV
- photon $\eta$ < 2.5
- lepton $p_T$ > 20 GeV
- lepton $\eta$ < 2.5

## 4.2 Histogram and Normalization

- Histogram: $E_T^{\text{miss}}$
  - definition: $E_T^{\text{miss}} = |\vec{p}_T^{\,a} + \vec{p}_T^{\,\nu}|$, the vector sum of the transverse momenta of all invisible particles (ALP + neutrino).

- Binning: 50 bins, 0–1000 GeV

## 4.3 Plot Figure

Plot the histogram. The height of the histogram is the normalized events, which are defined as the ratio of the number of events in the bin to the total number of events.

- comment: the height of the histogram in figure 8 in the paper is not correct. The above definition is the actual used in the paper.



### Plot styles
- aspect ratio: 4:3
- x-axis: 
    - label: $E_T^{\text{miss}}$ [GeV]
    - range: [0, 1000]
- y-axis: 
    - label: normalized events
    - range: [$10^{-4}$, 1], log scale
