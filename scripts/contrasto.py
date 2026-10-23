#!/usr/bin/env python3
"""Calcola il rapporto di contrasto WCAG 2.x tra due colori CSS.

Serve a misurare il contrasto invece di stimarlo: il calcolo a mente è
inaffidabile, e con colori oklch() (Tailwind 4, shadcn/ui) lo è ancora di più.

Formati accettati (sintassi CSS):
  #rgb  #rgba  #rrggbb  #rrggbbaa
  rgb() / rgba()   virgole o spazi; canali 0-255 o percentuali; alfa dopo / o
                   come quarto argomento
  hsl() / hsla()   tinta in gradi (deg facoltativo); saturazione e luminosità in %
  oklch()          L in % o tra 0 e 1, C (numero o %), H in gradi
                   es. oklch(62.3% 0.214 259.815)

Regole applicate:
  - il colore in primo piano può essere semitrasparente: viene composto sullo
    sfondo in spazio sRGB, come fa il browser;
  - lo sfondo deve essere opaco: se è semitrasparente, passa il colore
    risultante (lo script non sa cosa c'è sotto);
  - il rapporto non si arrotonda: 4,49:1 non supera la soglia di 4,5:1.

Categorie (WCAG 2.2, livelli AA / AAA):
  testo normale          4,5:1 / 7:1    (1.4.3 / 1.4.6)
  testo grande           3:1 / 4,5:1    almeno 24px, o 18,67px se in grassetto
                                        (18pt / 14pt; 1pt CSS = 4/3 px)
  componenti e grafica   3:1            (1.4.11; nessun livello AAA)
Grassetto significa font-weight 700 o superiore.

Limiti dichiarati:
  - i colori fuori dal gamut sRGB (possibili con oklch) vengono ritagliati
    canale per canale; il browser applica un gamut mapping diverso, quindi per
    quei colori il risultato è approssimato e lo script lo segnala;
  - non gestisce colori con nome, var(), gradienti o immagini di sfondo:
    risolvi prima il valore calcolato (getComputedStyle) e passa quello.

Uso:
  python contrasto.py '#6b7280' '#ffffff'
  python contrasto.py 'oklch(55.1% 0.027 264.364)' '#fff' --dimensione 16
  python contrasto.py '#777' '#fff' --dimensione 18.67 --grassetto
  python contrasto.py 'rgb(0 0 0 / 40%)' '#fff' --ui

Esito: 0 soglia AA superata per la categoria valutata; 1 non superata;
2 errore d'uso (colore non leggibile, sfondo semitrasparente).
"""
import argparse
import math
import re
import sys
from dataclasses import dataclass

SOGLIE = {
    "normale": {"nome": "testo normale", "AA": 4.5, "AAA": 7.0},
    "grande": {"nome": "testo grande", "AA": 3.0, "AAA": 4.5},
    "ui": {"nome": "componenti e grafica", "AA": 3.0, "AAA": None},
}
GRANDE_PX = 24.0  # 18pt
GRANDE_GRASSETTO_PX = 14 * 4 / 3  # 14pt = 18,666…px
TOLLERANZA_PX = 0.01  # accetta valori arrotondati come 18.67 o 23.99 scritti a mano
TOLLERANZA_GAMUT = 1e-4  # rumore numerico della conversione oklch


@dataclass(frozen=True)
class Colore:
    """Colore sRGB con canali codificati (gamma) tra 0 e 1."""

    r: float
    g: float
    b: float
    a: float = 1.0
    fuori_gamut: bool = False

    def esadecimale(self):
        return "#" + "".join(f"{round(c * 255):02x}" for c in (self.r, self.g, self.b))


def _limita(valore, minimo=0.0, massimo=1.0):
    return max(minimo, min(massimo, valore))


def _da_lineare(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def _a_lineare(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _numero(token, contesto):
    try:
        return float(token)
    except ValueError:
        raise ValueError(f"valore non numerico '{token}' in {contesto}") from None


def _alfa(token, contesto):
    if token.endswith("%"):
        return _limita(_numero(token[:-1], contesto) / 100)
    return _limita(_numero(token, contesto))


def _gradi(token, contesto):
    if token.endswith("deg"):
        token = token[:-3]
    return _numero(token, contesto)


def _argomenti(interno, contesto):
    """Divide gli argomenti di una funzione colore; restituisce (canali, alfa)."""
    if "/" in interno:
        canali, alfa = interno.split("/", 1)
        alfa = alfa.strip()
    else:
        canali, alfa = interno, None
    token = canali.replace(",", " ").split()
    if alfa is None and len(token) == 4:  # sintassi legacy: rgba(r, g, b, a)
        alfa = token.pop()
    if len(token) != 3:
        raise ValueError(f"{contesto}: servono tre canali, trovati {len(token)}")
    return token, (1.0 if alfa is None else _alfa(alfa, contesto))


def _da_hsl(h, s, l):
    h = (h % 360) / 360
    if s == 0:
        return l, l, l

    def canale(t):
        t %= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p

    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q
    return canale(h + 1 / 3), canale(h), canale(h - 1 / 3)


def _da_oklch(L, C, H):
    """oklch -> sRGB lineare (matrici di Björn Ottosson, CSS Color 4)."""
    a = C * math.cos(math.radians(H))
    b = C * math.sin(math.radians(H))
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (
        +4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
        -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
        -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_,
    )


def leggi_colore(testo):
    """Converte una stringa colore CSS in Colore. Solleva ValueError se non valida."""
    t = testo.strip().lower()

    esa = re.fullmatch(r"#([0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})", t)
    if esa:
        cifre = esa.group(1)
        if len(cifre) <= 4:
            cifre = "".join(c * 2 for c in cifre)
        valori = [int(cifre[i : i + 2], 16) / 255 for i in range(0, len(cifre), 2)]
        return Colore(*valori[:3], a=valori[3] if len(valori) == 4 else 1.0)

    funzione = re.fullmatch(r"(rgba?|hsla?|oklch)\((.*)\)", t)
    if not funzione:
        raise ValueError(
            f"formato non riconosciuto: '{testo}' "
            "(usa #hex, rgb(), hsl() o oklch(); niente nomi o var())"
        )
    nome, interno = funzione.groups()
    canali, alfa = _argomenti(interno, nome)

    if nome.startswith("rgb"):
        valori = [
            _numero(c[:-1], nome) / 100 if c.endswith("%") else _numero(c, nome) / 255
            for c in canali
        ]
        return Colore(*(_limita(v) for v in valori), a=alfa)

    if nome.startswith("hsl"):
        h = _gradi(canali[0], nome)
        s, l = (_numero(c.rstrip("%"), nome) / 100 for c in canali[1:])
        return Colore(*_da_hsl(h, _limita(s), _limita(l)), a=alfa)

    # oklch
    L = canali[0]
    L = _numero(L[:-1], nome) / 100 if L.endswith("%") else _numero(L, nome)
    if not 0 <= L <= 1:
        raise ValueError(f"oklch: L fuori intervallo ({canali[0]}); usa 0-1 o 0%-100%")
    C = canali[1]
    C = _numero(C[:-1], nome) / 100 * 0.4 if C.endswith("%") else _numero(C, nome)
    lineari = _da_oklch(L, max(C, 0.0), _gradi(canali[2], nome))
    fuori = any(v < -TOLLERANZA_GAMUT or v > 1 + TOLLERANZA_GAMUT for v in lineari)
    return Colore(*(_da_lineare(_limita(v)) for v in lineari), a=alfa, fuori_gamut=fuori)


def componi(primo_piano, sfondo):
    """Compone un primo piano semitrasparente su uno sfondo opaco (spazio sRGB)."""
    if sfondo.a < 1:
        raise ValueError(
            "lo sfondo è semitrasparente: passa il colore effettivo risultante"
        )
    a = primo_piano.a
    return Colore(
        *(p * a + s * (1 - a) for p, s in zip(
            (primo_piano.r, primo_piano.g, primo_piano.b), (sfondo.r, sfondo.g, sfondo.b)
        )),
        fuori_gamut=primo_piano.fuori_gamut,
    )


def luminanza(colore):
    r, g, b = (_a_lineare(c) for c in (colore.r, colore.g, colore.b))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def rapporto(primo_piano, sfondo):
    """Rapporto di contrasto WCAG tra primo piano (anche semitrasparente) e sfondo."""
    effettivo = componi(primo_piano, sfondo)
    chiara, scura = sorted((luminanza(effettivo), luminanza(sfondo)), reverse=True)
    return (chiara + 0.05) / (scura + 0.05)


def categoria(dimensione_px=None, grassetto=False, ui=False):
    if ui:
        return "ui"
    if dimensione_px is None:
        return "normale"
    soglia = GRANDE_GRASSETTO_PX if grassetto else GRANDE_PX
    return "grande" if dimensione_px + TOLLERANZA_PX >= soglia else "normale"


def mostra(valore):
    """Tronca (non arrotonda) a due decimali, così 4.499 non appare come 4.50."""
    return f"{math.floor(valore * 100) / 100:.2f}"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("primo_piano", help="colore del testo o dell'elemento")
    parser.add_argument("sfondo", help="colore dello sfondo (opaco)")
    parser.add_argument("--dimensione", type=float, metavar="PX",
                        help="dimensione del testo in px calcolati")
    parser.add_argument("--grassetto", action="store_true",
                        help="testo con font-weight 700 o superiore")
    parser.add_argument("--ui", action="store_true",
                        help="componente d'interfaccia o grafica (1.4.11)")
    args = parser.parse_args(argv)

    try:
        primo_piano = leggi_colore(args.primo_piano)
        sfondo = leggi_colore(args.sfondo)
        valore = rapporto(primo_piano, sfondo)
    except ValueError as errore:
        print(f"Errore: {errore}", file=sys.stderr)
        return 2

    print(f"Rapporto: {mostra(valore)}:1")
    for chiave, s in SOGLIE.items():
        aa = f"AA {s['AA']:g}:1"
        riga = f"  {s['nome']:<22} {aa:<9} {'sì' if valore >= s['AA'] else 'NO':<4}"
        if s["AAA"] is not None:
            aaa = f"AAA {s['AAA']:g}:1"
            riga += f"{aaa:<11} {'sì' if valore >= s['AAA'] else 'NO'}"
        print(riga)

    if primo_piano.a < 1:
        print(f"Nota: primo piano semitrasparente, colore effettivo "
              f"{componi(primo_piano, sfondo).esadecimale()}")
    if primo_piano.fuori_gamut or sfondo.fuori_gamut:
        print("Attenzione: colore fuori dal gamut sRGB, risultato approssimato")

    cat = categoria(args.dimensione, args.grassetto, args.ui)
    superata = valore >= SOGLIE[cat]["AA"]
    print(f"Categoria valutata: {SOGLIE[cat]['nome']}, AA "
          f"{'superata' if superata else 'NON superata'}")
    return 0 if superata else 1


if __name__ == "__main__":
    sys.exit(main())
