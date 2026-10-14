#!/usr/bin/env python3
"""Monta o zip da skill para enviar no Claude Desktop (Settings → Capabilities → Skills).

  .venv/bin/python scripts/empacotar_skill.py

Gera skill/analise-marketing-seducar.zip (versionado no git, para baixar pelo GitHub) com:
  analise-marketing-seducar/SKILL.md          (de skill/SKILL.md)
  analise-marketing-seducar/references/*.md   (copiados de schema/, sempre atualizados)
"""

import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NOME = "analise-marketing-seducar"
REFERENCIAS = ["visao-geral.md", "dominios.md"]


def main() -> None:
    destino = RAIZ / "skill" / f"{NOME}.zip"
    destino.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(RAIZ / "skill" / "SKILL.md", f"{NOME}/SKILL.md")
        for ref in REFERENCIAS:
            z.write(RAIZ / "schema" / ref, f"{NOME}/references/{ref}")
    print(f"Skill empacotada em: {destino}")


if __name__ == "__main__":
    main()
