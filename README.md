# WSJT-Z

This project has moved find the offical here https://github.com/sq9fve/wsjt-z

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

## License
GPL-3 (inherited from WSJT-X).
