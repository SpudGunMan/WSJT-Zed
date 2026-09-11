# WSJT-Zed

This project has offical page here https://github.com/sq9fve/wsjt-z

This is a archive/backup of my submissions on offical.

Scripts to quick build SDK
- [doc/build-linux.sh](doc/build-linux.sh)
- [doc/build-osx.sh](doc/build-osx.sh)
- Not as quick, windows ..https://hamlib-sdk.sourceforge.io


# Compile

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

# License
GPL-3 (inherited from WSJT-X).