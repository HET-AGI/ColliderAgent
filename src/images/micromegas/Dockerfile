# micrOmegas container for ColliderAgent / Magnus execution
#
# Provides micrOmegas 6.3.0 (CC-BY-4.0, arXiv:2312.14894) with its bundled
# CalcHEP symbolic engine pre-built, plus the Fortran/C toolchain needed
# to compile per-model user projects at blueprint runtime.
#
# Used by:
#   - micromegas-compile  (builds a user project from CalcHEP model + main.c)
#   - micromegas-calc     (runs the compiled project for relic / DD / ID)
#
# Published as: docker://git.pku.edu.cn/rise-agi/micromegas:latest

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV MICROMEGAS_VERSION=6.3.0
ENV MICROMEGAS_ROOT=/opt/micromegas_${MICROMEGAS_VERSION}

# --- Build + runtime toolchain ---
# gcc/g++/gfortran   — compile CalcHEP-generated matrix-element code
# make/patch/tar/wget— fetch + build micrOmegas
# python3/pip        — host for magnus-sdk (baked below)
# X11 headers        — libX11-dev is a hard dependency of CalcHEP's symbolic engine
# libgsl, liblapack  — numerical backends used by micrOmegas physics routines
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc g++ gfortran make patch tar wget ca-certificates \
        python3 python3-pip \
        libx11-dev libxext-dev libxt-dev \
        libgsl-dev liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# --- Fetch + extract micrOmegas from Zenodo (stable DOI-backed URL) ---
# Placed before the pip layer so bumping magnus-sdk does not force a
# re-download of the ~40 MB micrOmegas tarball.
WORKDIR /opt
RUN wget --progress=dot:mega \
        "https://zenodo.org/api/records/17597395/files/micromegas_${MICROMEGAS_VERSION}.tgz/content" \
        -O "micromegas_${MICROMEGAS_VERSION}.tgz" \
    && tar -xzf "micromegas_${MICROMEGAS_VERSION}.tgz" \
    && rm "micromegas_${MICROMEGAS_VERSION}.tgz"

# --- Pre-build CalcHEP symbolic engine + physics library so per-job compile
#     only handles user code ---
# Without this, every micromegas-compile blueprint invocation pays a ~2-minute
# bootstrap cost for building the CalcHEP engine itself.
#
# Serial (-j1) on purpose: micrOmegas's CalcHEP_src/c_source/service2 Makefile
# has parallel siblings race on `ar r ../../lib/serv.a <obj>`, truncating archive
# members ("error reading getmem.o: file truncated"). Same root cause as the
# user-project compile in run_micromegas_compile.py. 6.2.3 happened to build
# clean with -j$(nproc); 6.3.0 trips the race reliably.
#
# ARFLAGS=Urv preserves real mtimes on archive members. Default `ar rv` on
# Ubuntu 22.04 binutils silently runs in deterministic mode (D flag) and zeroes
# every member's timestamp to 1970-01-01. micrOmegas's sources/Makefile uses
# GNU make's archive-member rule `lib/micromegas.a($(OBJ))` which compares
# member mtime to source-file mtime — and the bundled .c files carry their
# tarball mtime (Nov 2024). Without `U`, every member shows mtime=epoch < .c
# mtime, so make rebuilds the entire 50+ file physics library on every user
# project's first compile, and floods the user log with -Wformat-overflow noise
# from upstream printf format-string bugs in the micrOmegas sources. With `U`
# all members get image-build-time mtimes, the per-job `make -C ../sources`
# correctly skips with "Nothing to be done", and user logs only show their own
# main.c compile.
WORKDIR ${MICROMEGAS_ROOT}
RUN make -j1 ARFLAGS=Urv

# --- Bake magnus-sdk so blueprint entry_commands can use `magnus` CLI and
#     the Python API directly, without paying a 10-30s pip install per job.
#     Placed last because magnus-sdk is bumped more often than micrOmegas.
RUN pip3 install --no-cache-dir "magnus-sdk>=0.8.0"

# Make the micrOmegas root discoverable to blueprint scripts
ENV PATH=${MICROMEGAS_ROOT}:${PATH}

WORKDIR /work
