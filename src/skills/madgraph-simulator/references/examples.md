# madgraph-simulator — worked examples

All commands run from the working directory; paths are relative. Each launch also gets a matching `scripts/mg5_<label>.mg5`.

## Parton level, custom UFO

```bash
magnus run madgraph-compile -- \
  --ufo models/HeavyN_UFO \
  --process "p p > mu- n1" \
  --output events/pp_muN_7TeV

magnus run madgraph-launch -- \
  --process events/pp_muN_7TeV \
  --commands "done
set nevents 10000
set ebeam1 3500
set ebeam2 3500
set param_card MASS 9900012 500
set param_card DECAY 9900012 Auto
set use_syst False
done" \
  --output events/pp_muN_7TeV
```

Events: `events/pp_muN_7TeV/Events/run_01/unweighted_events.lhe.gz`.

## Pythia8 + Delphes (CMS card), SM built-in model

```bash
magnus run madgraph-compile -- --model sm --process "p p > t t~" --output events/pp_ttbar

magnus run madgraph-launch -- \
  --process events/pp_ttbar \
  --commands "shower=Pythia8
detector=Delphes
done
set nevents 10000
set ebeam1 6500
set ebeam2 6500
set param_card MASS 6 172.76
set delphes_card cms
done" \
  --output events/pp_ttbar
```

Events: `unweighted_events.lhe.gz`, `tag_1_pythia8_events.hepmc.gz`, `tag_1_delphes_events.root` in `Events/run_01/`.

## BSM signal, mass scan, auto width, decay chains

```bash
magnus run madgraph-compile -- \
  --ufo models/ScalarModel_UFO \
  --process "p p > t h0, t > b l+ vl, h0 > mu+ mu-
p p > t~ h0, t~ > b~ l- vl~, h0 > mu+ mu-" \
  --output events/pp_tS \
  --definitions "l+ = e+ mu+
l- = e- mu-
vl = ve vm
vl~ = ve~ vm~"

magnus run madgraph-launch -- \
  --process events/pp_tS \
  --commands "shower=Pythia8
detector=Delphes
done
set nevents 20000
set ebeam1 6500
set ebeam2 6500
set param_card YQLU 2 3 0.001
set param_card MASS 50001 scan:[20,40,60,80,100,120,140,160]
set param_card DECAY 50001 Auto
set delphes_card cms
done" \
  --output events/pp_tS
```

One job; runs `run_01` … `run_08`, one per scan value, each reported in the job log with its cross section.

## Lepton-initiated process with the LUXlep PDF

```bash
magnus run madgraph-compile -- --model sm --process "e+ u > e+ u" --output events/ep_u

magnus run madgraph-launch -- \
  --process events/ep_u \
  --pdf LUXlep-NNPDF31_nlo_as_0118_luxqed \
  --commands "done
set run_card pdlabel lhapdf
set run_card lhaid 82400
set nevents 10000
set ebeam1 6500
set ebeam2 6500
done" \
  --output events/ep_u
```

## MadSpin decays + Pythia8 + Delphes

```bash
magnus run madgraph-compile -- --model sm --process "p p > t t~" --output events/pp_ttbar_madspin \
  --definitions "l+ = e+ mu+
l- = e- mu-
vl = ve vm
vl~ = ve~ vm~"

magnus run madgraph-launch -- \
  --process events/pp_ttbar_madspin \
  --commands "shower=Pythia8
detector=Delphes
madspin=ON
done
set nevents 10000
set ebeam1 6500
set ebeam2 6500
set delphes_card cms
set spinmode onshell
decay t > b l+ vl
decay t~ > b~ l- vl~
done" \
  --output events/pp_ttbar_madspin
```

Decayed events (the ones Pythia8 and Delphes consumed) are in `Events/run_01_decayed_1/`; the undecayed hard events stay in `Events/run_01/`.

## A second launch in a directory that already has a run

The next launch in `events/pp_ttbar` produces `run_02`; the result JSON's `run_name` tells you which. Record that name in the sidecar and use it in downstream paths.
