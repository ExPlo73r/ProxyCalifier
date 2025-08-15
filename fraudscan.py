#!/usr/bin/env python3
import argparse, re, sys, time
from pathlib import Path
from typing import Iterable
import requests

BANNER = r"""
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░▒▓████████▓▒░  ░▒▓█▓▒░▒▓███████▓▒░                                                          
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░▒▓████▓▒░      ░▒▓█▓▒░                                                         
 ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░           ░▒▓██▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░                                                         
 ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░    ░▒▓██▓▒░     ░▒▓█▓▒░▒▓███████▓▒░                                                          
  ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░       ░▒▓██▓▒░       ░▒▓█▓▒░      ░▒▓█▓▒░                                                         
  ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓█▓▒░                                                         
   ░▒▓██▓▒░  ░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░  ░▒▓█▓▒░▒▓███████▓▒░                                                          
                                                                                                                                                                    
                                                                                                                                                                    
░▒▓███████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░       ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░       ░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓██████▓▒░ ░▒▓█▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░          ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░          ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░           ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
"""
URL_TPL = "https://scamalytics.com/ip/{ip}"
SCORE_RE = re.compile(r"Fraud\s*Score:\s*(\d+)", re.I)

def iter_ips(src: Path) -> Iterable[str]:
    with src.open("r", encoding="utf-8") as f:
        for line in f:
            ip = line.strip()
            if ip and not ip.startswith("#"):
                yield ip

def fetch_score(ip: str, timeout: float = 15.0) -> int | None:
    try:
        r = requests.get(
            URL_TPL.format(ip=ip),
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Python/requests"},
            timeout=timeout,
        )
        if r.status_code != 200:
            return None
        m = SCORE_RE.search(r.text)
        return int(m.group(1)) if m else None
    except Exception:
        return None

def main():
    ap = argparse.ArgumentParser(description="Filtra IPs seguras desde Scamalytics.")
    ap.add_argument("archivo_ips", type=Path, help="Archivo con IPs (una por línea)")
    ap.add_argument("--max-score", type=int, default=10,
                    help="Máximo Fraud Score para considerar 'seguro' (default: 10)")
    ap.add_argument("--salida", type=Path, default=Path("ips_seguras.csv"),
                    help="Archivo de salida SOLO con IPs (default: ips_seguras.csv)")
    ap.add_argument("--delay", type=float, default=1.5,
                    help="Segundos de espera entre consultas (default: 1.5)")
    args = ap.parse_args()

    print(BANNER)

    seguros: list[str] = []
    total = 0

    for ip in iter_ips(args.archivo_ips):
        total += 1
        score = fetch_score(ip)
        if score is not None:
            if score <= args.max_score:
                print(f"[SEGURO] {ip} -> {score}/100 ({score:.2f}%)")
                seguros.append(ip)  # Guardamos solo la IP
            else:
                print(f"[RIESGO] {ip} -> {score}/100 ({score:.2f}%)")
        else:
            print(f"[ERROR ] {ip} -> no se pudo leer score", file=sys.stderr)
        time.sleep(args.delay)

    # Guardar solo las IPs
    with args.salida.open("w", encoding="utf-8") as f:
        for ip in seguros:
            f.write(f"{ip}\n")

    print(f"\nHecho. {len(seguros)}/{total} IPs seguras (≤ {args.max_score}).")
    print(f"Archivo generado: {args.salida.resolve()} (solo IPs)")

if __name__ == "__main__":
    main()
