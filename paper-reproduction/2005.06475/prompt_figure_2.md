# 1. Target

Considering the scalar leptoquark model described in this document, plot the $m_{ej}$ distribution for the signal process.

---

# 2. Scalar Leptoquark Model

## 2.1 Lagrangian

$$\mathcal{L} = \lambda_{eu}\,\text{LQ}_{eu}\,(E^c U^c)^* + \text{h.c.}$$

where the spinor indices of $E^c$ and $U^c$ are contracted anti-symmetrically, i.e., $\epsilon^{\alpha\beta} E^c_\alpha U^c_\beta \equiv (E^c)^T i \sigma^2 U^c$.

In four-component Dirac spinor notation, this can be written as:
$$\mathcal{L} = \lambda_{eu}\,\text{LQ}_{eu}\,e_R^T i \sigma^2 u_R + \text{h.c.} = \lambda_{eu}\,\text{LQ}_{eu}\,e^T i \gamma^0 \gamma^2 P_R u + \text{h.c.}$$

where $e = (e_L, e_R)^T$ and $u = (u_L, u_R)^T$ are the Dirac spinors, and $P_R = (1 + \gamma_5)/2$ is the right-handed chirality projector. Note that the leptoquark $\text{LQ}_{eu}$ couples to a lepton and a quark (no anti-particles).

Here,
- $\text{LQ}_{eu}$ is a scalar leptoquark. It is an $SU(2)_L$ singlet under the SM gauge group, carrying color triplet and electric charge $Q = -1/3$.
- $E^c = i \sigma^2 e_R^*$ is the left-handed charge conjugate field of the right-handed singlet electron field.
- $U^c$ is the left-handed charge conjugate field of the right-handed singlet up-quark field.
- $\lambda_{eu}$ is the Yukawa coupling (real).

## 2.2 Parameters

The benchmark point for the signal:
- mass of LQ: $M_\text{LQ} = 3000$ GeV
- total width of LQ: $\Gamma_\text{LQ} = 60$ GeV
- $\lambda_{eu} = 1$



---

# 3. Collider Simulation

## 3.1 Process

$$p\,p \to \text{LQ} \to e\,j$$

This is resonant single leptoquark production via lepton-quark fusion. 



Here, the underlying process is a lepton ($e$) from one proton PDF and a quark ($u$) from the other proton fusion to produce the LQ, which then decays back to $e + j$. This requires the LUXlep PDF, which provides lepton parton distribution functions inside the proton.

## 3.2 Collider simulation settings

- Collider: 13 TeV LHC
- Event number: 100000
- Parton shower: Pythia8
- Detector simulation: Delphes with ATLAS card (anti-$k_T$ jets with $R = 0.4$)
- PDF: LUXlep; redefine the proton content to include leptons and the photon
- Generation-level cuts: $p_T(\ell, j) > 500$ GeV, $|\eta| < 2.5$
- Store the generated events in LHCO format

## 3.3 Pythia8 lepton-to-photon workaround

Pythia8 cannot backward-evolve leptons from proton PDFs. The correct steps are:

1. After MadGraph generates the LHE file, replace all initial-state leptons with photons in the LHE file.
2. Set `Check:event = off` in Pythia8 settings, because the replacement breaks charge conservation.
3. Perform shower and detector simulation.

---

# 4. Numerical Analysis

## 4.1 Event selection

Read the reconstructed events from the Delphes output and apply the following selection cuts:

1. Electron: $p_T > 500$ GeV, $|\eta| < 2.5$
2. Jet: $p_T > 500$ GeV, $|\eta| < 2.5$ (anti-$k_T$, $R = 0.4$)
3. Missing transverse energy: $E_T^\text{miss} < 50$ GeV
4. Lepton veto: veto events with additional leptons ($|\eta| < 2.5$, $p_{T,\ell} > 7$ GeV)
5. Jet veto: veto events with additional subleading jets ($|\eta| < 2.5$, $p_{T,j} > 30$ GeV)


## 4.2 Signal histogram


Compute the invariant mass $m_{ej}$ of the leading electron and leading jet for events passing all cuts.

- Bin the $m_{ej}$ distribution in 100 GeV bins from 0 to 5000 GeV.
- Weight each event by:
$$w = \frac{\sigma \times \mathcal{L}}{N_\text{gen}}$$
  where $\sigma$ is the cross section, $\mathcal{L} = 100\;\text{fb}^{-1}$, and $N_\text{gen}$ is the total number of generated events.

---

# 5. Plot Figure

Plot the signal $m_{ej}$ distribution with solid black line.

## Plot styles

- Aspect ratio: 1:1
- x-axis:
  - Label: $m_{ej}$ [GeV]
  - Range: [1000, 5000]
- y-axis:
  - Label: events / bin / 100 fb$^{-1}$
  - Scale: logarithmic
  - Range: [$10^{-3}$, $5 \times 10^{2}$]
- Title: LHC, $\sqrt{s} = 13$ TeV (centered, top)
