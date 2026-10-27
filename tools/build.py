#!/usr/bin/env python3
"""Empaqueta src/<id>/ en mods/<id>.zip y genera manifest.json.

Lo ejecuta GitHub Actions en cada push; también puedes correrlo a mano:
    python tools/build.py usuario/repo [rama]
Los zips son deterministas (fecha fija), así que solo cambian si cambia su contenido.
"""
import sys, os, json, re, hashlib, zipfile, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
slug = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_REPOSITORY")
branch = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("GITHUB_REF_NAME", "main")
if not slug:
    sys.exit("Uso: python tools/build.py usuario/repo [rama]")
base = f"https://raw.githubusercontent.com/{slug}/{branch}"

out = root / "mods"
out.mkdir(exist_ok=True)
for old in out.glob("*.zip"):
    old.unlink()

mods = []
for src in sorted((root / "src").iterdir()):
    if not src.is_dir() or src.name.startswith("_"):
        continue
    if not re.fullmatch(r"[A-Za-z0-9_-]+", src.name):
        sys.exit(f"Nombre de carpeta inválido: {src.name}")
    info = json.loads((src / "mod.json").read_text(encoding="utf-8"))
    zpath = out / f"{src.name}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(p for p in src.rglob("*") if p.is_file()):
            zi = zipfile.ZipInfo(f.relative_to(src).as_posix(), (2020, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zf.writestr(zi, f.read_bytes())
    mods.append({
        "id": src.name,
        "version": str(info.get("version", "1")),
        "url": f"{base}/mods/{src.name}.zip",
        "sha256": hashlib.sha256(zpath.read_bytes()).hexdigest(),
    })

(root / "manifest.json").write_text(json.dumps({"mods": mods}, indent=2) + "\n")
print(f"{len(mods)} mod(s) -> manifest.json")
