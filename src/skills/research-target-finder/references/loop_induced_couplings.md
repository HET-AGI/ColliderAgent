# Loop-Induced Couplings of a Neutral Spin-0 State

Companion to [model_building_guide.md](model_building_guide.md), Section 4. The pipeline is tree-level, so the $Sgg$ and $S\gamma\gamma$ couplings of a new scalar or pseudoscalar must be supplied as effective operators with explicit coefficients. This file fixes their normalization, gives the loop functions and the contributions of new heavy particles, and lists the caveats for rates computed through such vertices. Label every evaluated coefficient `[estimate]`.

## Effective operators and normalization

Fix the normalization as follows ($v=246$ GeV; $\tilde X^{\mu\nu}=\tfrac12\epsilon^{\mu\nu\rho\sigma}X_{\rho\sigma}$):

$$\mathcal{L}_\text{eff}^{S} = c_g\frac{\alpha_s}{12\pi v}\,S\,G^a_{\mu\nu}G^{a\mu\nu} + c_\gamma\frac{\alpha}{8\pi v}\,S\,F_{\mu\nu}F^{\mu\nu},\qquad \mathcal{L}_\text{eff}^{A} = \tilde c_g\frac{\alpha_s}{8\pi v}\,A\,G^a_{\mu\nu}\tilde G^{a\mu\nu} + \tilde c_\gamma\frac{\alpha}{8\pi v}\,A\,F_{\mu\nu}\tilde F^{\mu\nu}$$

- Widths at LO: $\Gamma(S\to\gamma\gamma)=\dfrac{\alpha^2m^3|c_\gamma|^2}{256\pi^3v^2}$ (same for $A$ with $\tilde c_\gamma$); $\Gamma(S\to gg)=\dfrac{\alpha_s^2m^3|c_g|^2}{72\pi^3v^2}$; $\Gamma(A\to gg)=\dfrac{\alpha_s^2m^3|\tilde c_g|^2}{32\pi^3v^2}$
- Coefficients from SM particles in the loop, with coupling modifiers $\kappa_i$ relative to an SM Higgs and $\tau_i=m^2/(4m_i^2)$:
  $c_g=\tfrac34\sum_q\kappa_qA_{1/2}(\tau_q)$, $\quad c_\gamma=\sum_fN_cQ_f^2\kappa_fA_{1/2}(\tau_f)+\kappa_VA_1(\tau_W)$, $\quad\tilde c_g=\tfrac12\sum_q\tilde\kappa_qA^A_{1/2}(\tau_q)$, $\quad\tilde c_\gamma=\sum_fN_cQ_f^2\tilde\kappa_fA^A_{1/2}(\tau_f)$
- Loop functions (conventions of hep-ph/0503172, hep-ph/0503173), with $f(\tau)=\arcsin^2\sqrt\tau$ for $\tau\le1$ and $f(\tau)=-\tfrac14\big[\ln\tfrac{1+\sqrt{1-1/\tau}}{1-\sqrt{1-1/\tau}}-i\pi\big]^2$ for $\tau>1$:
  $A_{1/2}=2[\tau+(\tau-1)f]/\tau^2$, $\;A_1=-[2\tau^2+3\tau+3(2\tau-1)f]/\tau^2$, $\;A_0=-[\tau-f]/\tau^2$, $\;A^A_{1/2}=2f/\tau$.
  Heavy-loop limits ($\tau\to0$): $A_{1/2}\to\tfrac43$, $A_1\to-7$, $A_0\to\tfrac13$, $A^A_{1/2}\to2$. So a heavy top gives $c_g=\kappa_t$, $\tilde c_g=\tilde\kappa_t$; and the $W$ and top loops interfere destructively in $c_\gamma$ (SM Higgs at 125 GeV: $c_\gamma\approx-6.5$)
- New heavy particles ($m\ll2M$): a vector-like fermion with coupling $-y_FS\bar FF$, mass $M_F$, charge $Q$, colour multiplicity $N_c$ adds $\delta c_\gamma=\tfrac43N_cQ^2\,y_Fv/M_F$, and $\delta c_g=y_Fv/M_F$ if it is a colour triplet; a charged scalar with coupling $-g\,S\,H^+H^-$ ($g$ in GeV) adds $\delta c_\gamma=\dfrac{g\,v}{2m_{H^\pm}^2}A_0(\tau_{H^\pm})$
- Evaluate the loop functions numerically at the mass in question and quote the result as an `[estimate]`; check the normalization against the source when a paper uses a different operator basis

## Caveats for rates computed through these operators
- LO gluon fusion through the effective vertex underestimates the rate by a factor of roughly 2–3. Do not quote LO cross sections: normalize to the SM-like reference cross section at that mass (LHC Higgs Working Group, arXiv:1610.07922) times $|c_g/c_g^\text{SM-like}|^2$, or to the experiment's own reference rate
- A $2\to1$ process has no transverse momentum at matrix-element level; observables that depend on the resonance $p_T$ or on recoil jets are unreliable without jet matching
- Automatically computed widths are LO and contain only the channels present in the model (light-quark Yukawas may be absent). For rates, prefer $\sigma\times\text{BR}$ built from reference branching ratios rescaled by the coupling modifiers
