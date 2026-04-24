# ColliderAgent — Container Images

**Dockerfiles for the containers that Magnus blueprints run inside.**

Each subdirectory is a standalone build context. Images are pushed to
`git.pku.edu.cn/rise-agi/<name>:latest` and referenced from blueprints'
`container_image` field.

## Images

| Directory | Image | Used by |
|---|---|---|
| [`micromegas/`](micromegas/) | `rise-agi/micromegas:latest` | `micromegas-compile`, `micromegas-calc` |

### What's baked in

All images include `magnus-sdk>=0.7.9` so that blueprint entry commands can
invoke `magnus` CLI and `import magnus` immediately, without paying a
10–30 s `pip install` cost per job. Bump the version in the Dockerfile and
rebuild when the station SDK advances.

| Image | Extra bundled tooling |
|---|---|
| `micromegas:latest` | `micromegas 6.2.3` with its CalcHEP symbolic engine **pre-compiled**, plus `gcc/g++/gfortran`, `libgsl`, `liblapack`, `libX11` (CalcHEP hard dep) |

## Build & Push

Each image is self-contained (downloads its dependencies at build time from
upstream sources such as Zenodo / apt). To publish:

```bash
cd src/images/<name>
docker build -t git.pku.edu.cn/rise-agi/<name>:latest .
docker login git.pku.edu.cn           # requires deploy token with write to rise-agi/*
docker push git.pku.edu.cn/rise-agi/<name>:latest
```

## Licensing

All bundled software is redistributable under its original license:

| Package | License | Notes |
|---|---|---|
| micrOmegas 6.2.3 | CC-BY-4.0 | DOI-backed Zenodo distribution, arXiv:2312.14894 |

The Dockerfiles fetch upstream tarballs directly; we do not vendor any
proprietary binaries. Images that depend on licensed software (e.g. Mathematica)
are expected to mount the license at runtime rather than bake it in —
see the existing `mma-het` image for that pattern.
