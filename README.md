# WSJT-Z

WSJT-X fork with JTDX decoder enhancements and WSJT-Z extensions by SQ9FVE.

Based on WSJT-X 3.0.0 + JTDX FT8 multi-thread decoder + WSJT-Z UI/filter additions.

## Features beyond upstream WSJT-X
- Multi-thread FT8 decoder (Decode → Number of FT8 threads, Auto or 1–12)
- Auto CQ / Auto Call, pounce mode, priority call queue
- Advanced filters: ignored stations, prefix/state/continent/CQ-target, new-on-band
- Before-worked alerts (CQ Zone / ITU Zone / grid / continent / country, per-band variants)
- QRZ callsign lookup panel
- Band-hopper, custom alerts, NA_VHF/EU_VHF contest flows

## Build
See full details at [INSTALL](INSTALL)

### Windows via JTSDK:
[JTSDK64 Setup Guide](https://jtsdk.github.io/jtsdk64-tools/setup/overview/)
- **64-bit:** `E:\JTSDK64-Tools` → `jtsdk64.cmd` → `jtbuild rinstall` (or `jtbuild package`)
[JTSDK Guide](https://sourceforge.net/projects/hamlib-sdk/files/Windows/JTSDK-3.3-x86-Stream/)
- **32-bit:** `E:\JTSDK-Tools` → `jtsdk-env.cmd` → `jtbuild package`
- Source path is read from `tmp/build.txt` (`SRCD`). Build artifacts land in `E:\JTSDK-Build\output\_\build{32,64}`.

### Linux:
[Environment Setup Guide](https://groups.io/g/WSJT-Z/files/Building%20WSJT%20From%20Source-1.2.pdf)

```bash
cmake -S . -B build \
      -D CMAKE_INSTALL_PREFIX="$HOME/wsjtz" \
      -D WSJT_SKIP_MANPAGES=ON \
      -D WSJT_GENERATE_DOCS=OFF \
      -D CMAKE_BUILD_TYPE=Release
```

```bash
cmake --build build
cmake --install build
```

```bash
cmake --build build --target clean
```
## Version
`3.0.0-2.0.8` — WSJT-X 3.0.0 base, WSJT-Z mod v2.0.8.

See `NEWS` file for upstream changelog.

## License
GPL-3 (inherited from WSJT-X).
