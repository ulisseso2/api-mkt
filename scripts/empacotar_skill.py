#!/usr/bin/env python3
"""Monta o zip da skill para enviar no Claude Desktop (Settings → Capabilities → Skills).

  .venv/bin/python scripts/empacotar_skill.py

Gera (versionados no git, para baixar pelo GitHub):
  skill/analise-marketing-seducar.zip
    analise-marketing-seducar/SKILL.md          (de skill/SKILL.md)
    analise-marketing-seducar/references/*.md   (copiados de schema/, sempre atualizados)
  skill/seducar-analise-financeira.zip
    seducar-analise-financeira/SKILL.md         (de skill/financeiro/SKILL.md)
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

    nome_fin = "seducar-analise-financeira"
    destino_fin = RAIZ / "skill" / f"{nome_fin}.zip"
    with zipfile.ZipFile(destino_fin, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(RAIZ / "skill" / "financeiro" / "SKILL.md", f"{nome_fin}/SKILL.md")
    print(f"Skill empacotada em: {destino_fin}")


if __name__ == "__main__":
    main()
