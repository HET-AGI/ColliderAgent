Runs found: 31 (successful 28, failed 2, unjudged 1)

### Table S3: resource usage (successful runs, mean over runs)

| Benchmark | Model | Runs | Wall-clock (h) | Subagent calls | Magnus jobs | Files written | Tokens in (M) | Tokens out (k) | Cost (USD) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1308.2209 Fig. 3 | claude-opus-4-6 | 3 | 0.60 | 3.0 | 9.0 | 14.3 | 3.88 | 17.2 | 4.81 |
| 1605.02910 Fig. 1 | claude-opus-4-6 | 3 | 0.92 | 3.3 | 17.0 | 22.3 | 4.43 | 29.5 | 7.58 |
| 1605.02910 Fig. 1 | claude-opus-5 | 1 | 0.88 | 4.0 | 7.0 | 16.0 | 9.06 | 53.4 | 14.32 |
| 1605.02910 Fig. 1 | gpt-5.5 | 1 | 1.03 | 2.0 | 21.0 | 11.0 | 11.05 | 51.0 | ? |
| 1701.05379 Fig. 8 | claude-opus-4-6 | 3 | 1.01 | 3.0 | 6.7 | 16.7 | 15.06 | 30.5 | 12.81 |
| 1701.05379 Fig. 8 | claude-opus-4-8 | 1 | 1.05 | 3.0 | 9.0 | 16.0 | 10.96 | 43.3 | 12.55 |
| 1701.05379 Fig. 8 | claude-opus-5 | 1 | 0.87 | 3.0 | 5.0 | 17.0 | 5.72 | 37.5 | 9.06 |
| 1701.05379 Fig. 8 | claude-sonnet-5 | 1 | 1.38 | 3.0 | 14.0 | 24.0 | 18.19 | 34.3 | 7.54 |
| 1701.05379 Fig. 8 | gpt-5.5 | 1 | 0.99 | 4.0 | 9.0 | 14.0 | 13.44 | 52.2 | ? |
| 1811.07920 Fig. 3 | gpt-5.5 | 1 | 2.55 | 3.0 | 20.0 | 14.0 | 49.37 | 90.3 | ? |
| 2005.06475 Fig. 2 | gpt-5.5 | 1 | 4.41 | 5.0 | 24.0 | 15.0 | 74.99 | 160.4 | ? |
| 2103.02708 Fig. 4 | claude-opus-4-6 | 3 | 0.73 | 3.0 | 7.3 | 14.3 | 8.29 | 25.1 | 7.18 |
| 2104.05720 Fig. 11 | claude-opus-4-6 | 2 | 0.68 | 3.0 | 14.0 | 6.0 | 4.43 | 18.4 | 7.81 |
| 2104.05720 Fig. 12 | claude-opus-4-6 | 3 | 1.22 | 3.0 | 19.0 | 21.7 | 13.26 | 38.9 | 12.65 |
| 9909255 Fig. 2 | claude-opus-4-6 | 3 | 0.95 | 2.7 | 9.3 | 14.3 | 3.80 | 28.2 | 6.37 |

### Table S4: successful/attempted per benchmark and model (`?` = attempted, not yet judged)

| Benchmark | claude-opus-4-6 | claude-opus-4-8 | claude-opus-5 | claude-sonnet-5 | gpt-5.5 |
|---|---:|---:|---:|---:|---:|
| 1308.2209 Fig. 3 | 3/3 | - | - | - | - |
| 1605.02910 Fig. 1 | 3/3 | - | 1/1 | - | 1/1 |
| 1701.05379 Fig. 8 | 3/3 | 1/1 | 1/1 | 1/1 | 1/1 |
| 1811.07920 Fig. 3 | 0/1 | - | - | - | 1/1 |
| 2005.06475 Fig. 2 | 0/1 (1 ?) | - | - | - | 1/1 |
| 2103.02708 Fig. 4 | 3/3 | - | - | - | - |
| 2104.05720 Fig. 11 | 2/3 | - | - | - | - |
| 2104.05720 Fig. 12 | 3/3 | - | - | - | - |
| 9909255 Fig. 2 | 3/3 | - | - | - | - |

### Table S5: successful/attempted per benchmark with failure modes

| Benchmark | Successful/attempted | Failure modes |
|---|---:|---|
| 1308.2209 Fig. 3 | 3/3 | - |
| 1605.02910 Fig. 1 | 5/5 | - |
| 1701.05379 Fig. 8 | 7/7 | - |
| 1811.07920 Fig. 3 | 1/2 | infrastructure (1) |
| 2005.06475 Fig. 2 | 1/2 (1 ?) | unjudged ? (1) |
| 2103.02708 Fig. 4 | 3/3 | - |
| 2104.05720 Fig. 11 | 2/3 | model (1) |
| 2104.05720 Fig. 12 | 3/3 | - |
| 9909255 Fig. 2 | 3/3 | - |

Footnotes (quantitative deviations of runs counted as successful):

1. 1701.05379 Fig. 8, claude-opus-4-6: The reference shows seven overlaid curves (c1, c2, c6, c8, cB, cW and SM) while the reproduction shows a single distribution; its shape tracks the c1/c2/cW-type curves (peak 40-80 GeV, ~3e-4 at 1 TeV) rather than the much softer SM curve, which dies out by ~250 GeV. The y-axis is a per-bin fraction ('normalized events') rather than the reference's density (1/sigma)(dsigma/dE_T^miss) in GeV^-1, so the absolute level differs by roughly the 20 GeV bin width (peak ~0.18 per bin vs ~0.2 GeV^-1); the intermediate region near 200 GeV sits about a factor of 2 above the c1 curve and below c2.
2. 1605.02910 Fig. 1, claude-opus-4-6: Contour tips are systematically slightly lower/narrower than the reference: panel (a) peaks at g₁′≈0.13 at g̃≈−0.15 vs ≈0.12 at ≈−0.13 (close); panel (b) peaks at ≈0.24 vs ≈0.27 and its left tail closes near g̃≈−0.3 vs ≈−0.32; panel (c) is the largest deviation, peaking at g₁′≈0.47 at g̃≈−0.55 versus ≈0.65 at ≈−0.7 in the reference, i.e. the 3 TeV exclusion region is roughly 25-30% smaller in the vertical extent. The g̃-axis zero crossings (≈0.05, ≈0.1, ≈0.2 for the three masses) agree well with the reference.
3. 2103.02708 Fig. 4, claude-opus-4-6: The produced curves sit high relative to the reference theory lines: σB(Z'_SSM) ≈ 2.6×10⁻¹ pb at 1 TeV versus ≈2–3×10⁻² pb in the reference (factor ~10), narrowing to ≈4×10⁻⁵ pb versus ≈2×10⁻⁵ pb at 5 TeV (factor ~2), i.e. the falling slope is somewhat shallower than the reference. The SSM/ψ ratio is roughly constant at ~3 across the mass range, close to the reference ordering and spacing.
4. 9909255 Fig. 2, claude-opus-4-6: Sampled on a coarse 100 GeV grid (200-1200 GeV), so the 600 GeV resonance is sampled rather than resolved: the peak reaches ~3.5e4 fb versus ~4e4 fb in the reference, and the interpolated line makes the resonance triangular rather than Breit-Wigner shaped. The scan omits the Z-pole region below 200 GeV shown in the reference and stops at 1200 GeV rather than 1500 GeV, so any second KK resonance near 1100 GeV is not probed. The low-energy end is somewhat high (~3e3 fb at 200 GeV versus ~2e3 fb for the corresponding reference curve), and the 800 GeV dip minimum is shallower/shifted by up to one grid spacing.
5. 2104.05720 Fig. 11, claude-opus-4-6: Produced curves deviate from SM by at most ~2-3% in any bin for both m_LQ = 1 TeV and 10 TeV at β_L^32 = 1, versus the reference where the 1 TeV curve is shifted by O(100%) at |η| > 1.2 and suppressed by a factor ~3 in the first bin. The 10 TeV curve and the β_L^32 = 0.1 panel agree with the reference at the few-percent level. Normalisation convention also differs (produced uses 1/N dN/d|η| peaking at ~1.5; reference plots per-bin normalized fractions peaking at ~0.15), which is a bin-width factor, not a shape difference.
6. 2104.05720 Fig. 12, claude-opus-4-6: The produced x-range stops near ~50 TeV like the reference but the low-mass end is largely consistent (3 TeV 95% CL ~0.035 vs ~0.04, 14 TeV 5-sigma ~0.022 vs ~0.02 at m_LQ = 1 TeV); the 14 TeV 95% CL curve sits ~2-3x higher than the reference at low mass (~0.017 vs ~0.006 at 1 TeV) and shows a spurious bump/dip structure around m_LQ = 1-2 TeV that is absent in the smooth reference contours; at the high-mass end the produced 3 TeV curves rise somewhat faster (5-sigma reaching ~2 vs ~1 near 50 TeV), and the gap between 95% CL and 5-sigma is narrower for the 14 TeV pair than in the reference.
7. 2005.06475 Fig. 2, gpt-5.5: The signal peak sits at ~1.5 events/bin versus ~3 in the reference (roughly a factor 2 lower normalisation), and the produced distribution terminates at ~3.8 TeV whereas the reference LQ curve extends to 5 TeV with a low tail; the low-mass shoulder is also ~2-5x below the reference near 1-2 TeV, and the x-axis is drawn linearly rather than logarithmically.
8. 1701.05379 Fig. 8, gpt-5.5: The produced histogram falls more slowly than the reference's c_1/c_2/c_W/c_B curves and faster than c_6/c_8: at 1000 GeV it sits at ~2e-4, versus ~3e-4 (c_1/c_2/c_W), ~3e-3 (c_6) and ~6e-3 (c_8) in the reference. The peak height is ~0.18 vs ~0.2-0.25 for most reference curves, and the low-E_T rise is smoother (finer binning) than the reference's sharp SM-like spike at ~50 GeV. The produced curve is a per-bin normalized fraction rather than the reference's 1/sigma dsigma/dE_T density, so absolute y-values differ by the bin width.
9. 1605.02910 Fig. 1, gpt-5.5: Panel (a) and (c) contours match the reference almost exactly (tip at g₁'≈0.12 at g̃≈−0.13, and g₁'≈0.65 at g̃≈−0.72 respectively); panel (b) reproduces the tip height (g₁'≈0.26) and right-hand crossing (g̃≈+0.09) but the lobe is somewhat narrower/more pinched than the reference, whose contour is fuller in the 0.1<g₁'<0.25 region.
10. 1811.07920 Fig. 3, gpt-5.5: The LH and RH R_D(*) bands agree closely with the reference (LH from ~0.3 at 0.8 TeV to ~1.95 at 5 TeV; RH from ~0.65 to ~4). The exclusion boundary is somewhat weaker/steeper than the reference: it starts near 1.07 at 0.8 TeV (vs ~0.8 in the reference, where the boundary essentially tracks the RH band at low mass) and reaches 4.0 near M_U1 ≈ 3.9 TeV, whereas the reference excluded region hugs the RH band up to ~5 TeV. The reference's EFT-validity line and the 150 fb^-1 and 3 ab^-1 projection curves are not drawn.
11. 1605.02910 Fig. 1, claude-opus-4-6: The contour tips are close for the two lighter masses (g1' ≈ 0.13 vs 0.117 at 2 TeV; 0.24 vs 0.265 at 2.5 TeV) but the 3 TeV panel is noticeably smaller: peak g1' ≈ 0.47 vs ≈ 0.65 in the reference, and the left edge reaches g̃ ≈ −0.57 instead of ≈ −0.78, i.e. a ~25-30% under-coverage of the excluded region at the highest mass. Zero-crossings on the g̃ axis agree to within ~0.05 in all panels. The session ended with 'OAuth session expired and could not be refreshed' after the figure and the step-4 sidecar were written (only the execution summary is missing); the figure is judged as produced.
12. 1308.2209 Fig. 3, claude-opus-4-6: Normalisation convention matches (|V_muN| = 1 vs the reference's sigma/|V_lN|^2). Point-by-point the 14 TeV curve sits ~20-30% below the reference at the low-mass end (1.4e4 vs ~2e4 fb at m_N = 100 GeV, 1.2e3 vs ~1.4e3 fb at 200 GeV) and agrees to within ~10-20% above 400 GeV; the produced curve uses CTEQ6L, and no PDF/scale uncertainty band is shown.
13. 2103.02708 Fig. 4, claude-opus-4-6: The reference y-axis is the normalized ratio ((σB)Z'/(σB)Z)×1928 pb rather than a raw cross section; agreement is good at high mass (both ~1e-5 pb for Z'_SSM near 5 TeV) but the produced curves sit roughly a factor of a few higher below ~1.5 TeV (produced Z'_ψ ≈ 0.1 pb at 1 TeV vs ~2e-2 in the reference), and the Z'_ψ curve stops at ~5.0 TeV instead of extending to 5.5 TeV.
14. 2104.05720 Fig. 12, claude-opus-4-6: Overall normalisation is close (3 TeV 5σ ≈ 0.05 at 1 TeV and ≈1–2 at ~50 TeV, matching the reference within tens of percent), but the 14 TeV 95% CL curve sits high at low mass (≈0.016 at m_LQ = 1 TeV versus ≈0.006 in the reference), so the exclusion–discovery gap at 14 TeV is compressed relative to the paper; the produced 14 TeV curves also show small non-physical kinks near m_LQ ≈ 1.5–3 TeV where the reference is smooth.
15. 1701.05379 Fig. 8, claude-opus-4-6: The produced histogram plots normalized events per bin rather than the reference's (1/σ)dσ/dE_T density in GeV^-1, so absolute ordinate values differ by the bin width (peak 0.18 per 25 GeV bin vs ~0.2-0.25 GeV^-1 in the reference). The tail at 1 TeV lands at ~3x10^-4, consistent with the reference's c_1/c_2/c_W curves but ~20x below its c_6/c_8 curves; only one benchmark coefficient is shown, and no SM curve is overlaid.
16. 9909255 Fig. 2, claude-opus-4-6: Sampled on a coarse 100 GeV grid from 200–1200 GeV, so the Z pole near 91 GeV and the 1500 GeV endpoint of the reference are not covered, and the 600 GeV resonance peak is captured by a single grid point (~3×10^4 fb vs ~4×10^4 fb for the reference blue curve), understating the true peak height and width. The off-resonance minimum near 400 GeV sits at ~9×10^2 fb versus ~2×10^3 fb in the reference, a factor ~2 low; the high-energy tail at 1200 GeV (~2.5×10^4 fb) agrees with the reference blue curve to within tens of percent.
17. 2104.05720 Fig. 11, claude-opus-4-6: In the left panel (β_L^32 = 1) the 1 TeV curve peaks at η ≈ 1.3–1.5 with a normalized height of ≈0.118, slightly broader and ~20% lower than the reference peak of ≈0.145 at η ≈ 1.1–1.3, and it stays somewhat above the reference at large η (≈0.04 vs ≈0.01 in the last bin). The right panel agrees to within a few percent bin-by-bin. Axis is labelled η rather than η_μ.
18. 2005.06475 Fig. 2, claude-opus-4-6: TBD (handed over). Stopped by the operator after 6.4 h without a figure: model, validation and the 100k-event LUXlep parton sample were done; two Pythia8+Delphes launches failed at upload with 'No space left on device' (27 GB Delphes ROOT against the job's 10 GB packing space); a third launch with post-run cleanup was running when stopped.
19. 1605.02910 Fig. 1, claude-opus-4-6: The 2 TeV and 2.5 TeV contours match the reference to within about 10% (tips at (-0.155, 0.13) vs (-0.14, 0.12) and (-0.28, 0.245) vs (-0.30, 0.265)). At 3 TeV the base on g1'=0 matches but the tip is at (-0.55, 0.48) vs (-0.74, 0.65), about 25% smaller in both g1' and |gt|. An Opus 5 run and the Opus 4.6 attempt 3 gave the same 3 TeV tip, whereas the Codex/gpt-5.5 run of 2026-09-24 reproduced the paper's tip (-0.72, 0.65): the shortfall is an analysis choice made in the Claude runs, not a limitation of the prompt (earlier wording 'systematic to the prompt' is withdrawn).
20. 1811.07920 Fig. 3, claude-opus-4-6: Attempt 1 generated all 18 Delphes runs (4.0 h, 106 USD; four 9-run launches were lost to the 10 GB job limit before the agent split them), then the orchestrator ended its turn 'waiting for event file downloads' and the headless session terminated without the analysis stage. A continuation session in the same workspace produced the figure in 1.7 h / 29.5 USD with the reference's shape but a 20-35% weaker exclusion. Counted as a failure (infrastructure).
21. 9909255 Fig. 2, claude-opus-4-6: The 11-point sqrt(s) grid (200-1200 GeV, 100 GeV steps) and the single coupling point are what the benchmark prompt specifies, so the reference's Z-pole region, its 1.2-1.5 TeV range and its other coupling curves are outside the task. The grid under-resolves the 600 GeV KK resonance: produced peak about 1.5e4 fb against about 3e4 fb in the reference; off-peak values follow the reference curve.
22. 2104.05720 Fig. 11, claude-opus-4-6: The orchestrator was not triggered: the main session ran the pipeline itself (0 sub-agent calls); the result is correct.
23. 2104.05720 Fig. 12, claude-opus-4-6: The produced limits are weaker than the reference throughout: the 14 TeV 95% CL curve at m_LQ = 1 TeV is about 0.015 against about 0.006 (roughly 2.5x weaker); at 70 TeV the 14 TeV curves are about 0.25 (exclusion) and 0.4 (discovery) against about 0.18 and 0.25. The 3 TeV curves agree within 20-30% at low mass but are about 1.6x weaker at 70 TeV for the exclusion.
24. 1701.05379 Fig. 8, claude-sonnet-5: Cross section 0.04909 pb instead of the 0.04135 pb obtained by Opus 5 and Opus 4.8, from looser generation-level eta cuts (5 instead of 2.5); the normalization removes the difference.
25. 1605.02910 Fig. 1, claude-opus-5: At M_Z' = 3 TeV the produced contour tip is at g1' about 0.48 (gt about -0.55) against about 0.65 (gt about -0.73) in the reference, about 25% lower; the g1' = 0 intercepts (about +-0.17) agree. 2 TeV tip about 0.135 against 0.12; 2.5 TeV tip about 0.245 against 0.265. Same 3 TeV contour as the Opus 4.6 runs; see the 1605.02910 Opus 4.6 attempt-1 note.
