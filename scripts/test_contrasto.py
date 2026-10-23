"""Test di contrasto.py. Esecuzione: python -m unittest discover -s scripts -p "test_*.py"."""
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import contrasto  # noqa: E402

SCRIPT = Path(__file__).parent / "contrasto.py"
BIANCO = contrasto.leggi_colore("#fff")


def esegui(*argomenti):
    r = subprocess.run([sys.executable, str(SCRIPT), *argomenti], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def canali(colore):
    return (colore.r, colore.g, colore.b)


class TestRapporto(unittest.TestCase):
    def test_nero_su_bianco_vale_21(self):
        self.assertAlmostEqual(contrasto.rapporto(contrasto.leggi_colore("#000"), BIANCO), 21.0, places=6)

    def test_stesso_colore_vale_1(self):
        grigio = contrasto.leggi_colore("#808080")
        self.assertAlmostEqual(contrasto.rapporto(grigio, grigio), 1.0, places=6)

    def test_ordine_dei_colori_non_conta(self):
        a, b = contrasto.leggi_colore("#1e40af"), contrasto.leggi_colore("#fde68a")
        self.assertAlmostEqual(contrasto.rapporto(a, b), contrasto.rapporto(b, a), places=9)

    def test_grigio_777_non_supera_aa_e_767676_si(self):
        # Coppia di riferimento nota: #767676 è il grigio più chiaro che supera 4,5:1 su bianco.
        self.assertLess(contrasto.rapporto(contrasto.leggi_colore("#777"), BIANCO), 4.5)
        self.assertGreaterEqual(contrasto.rapporto(contrasto.leggi_colore("#767676"), BIANCO), 4.5)


class TestFormati(unittest.TestCase):
    def test_formati_equivalenti_del_rosso(self):
        attesi = (1.0, 0.0, 0.0)
        for testo in ("#f00", "#FF0000", "rgb(255, 0, 0)", "rgb(255 0 0)", "rgb(100% 0% 0%)",
                      "rgba(255,0,0,1)", "hsl(0 100% 50%)", "hsl(0deg, 100%, 50%)"):
            with self.subTest(testo=testo):
                for ottenuto, atteso in zip(canali(contrasto.leggi_colore(testo)), attesi):
                    self.assertAlmostEqual(ottenuto, atteso, places=6)

    def test_oklch_estremi_sono_bianco_e_nero(self):
        for testo, atteso in (("oklch(100% 0 0)", 1.0), ("oklch(1 0 0)", 1.0), ("oklch(0 0 0)", 0.0)):
            with self.subTest(testo=testo):
                colore = contrasto.leggi_colore(testo)
                self.assertFalse(colore.fuori_gamut)
                for c in canali(colore):
                    self.assertAlmostEqual(c, atteso, places=4)

    def test_oklch_del_rosso_srgb(self):
        # Valore oklch pubblicato per #ff0000 (CSS Color 4).
        rosso = contrasto.leggi_colore("oklch(62.796% 0.25768 29.2339)")
        for ottenuto, atteso in zip(canali(rosso), (1.0, 0.0, 0.0)):
            self.assertAlmostEqual(ottenuto, atteso, places=3)

    def test_oklch_fuori_gamut_viene_segnalato(self):
        self.assertTrue(contrasto.leggi_colore("oklch(70% 0.4 150)").fuori_gamut)

    def test_alfa_esadecimale_e_funzionale(self):
        self.assertAlmostEqual(contrasto.leggi_colore("#00000080").a, 128 / 255, places=6)
        self.assertAlmostEqual(contrasto.leggi_colore("rgb(0 0 0 / 50%)").a, 0.5, places=6)
        self.assertAlmostEqual(contrasto.leggi_colore("oklch(50% 0.1 200 / 0.25)").a, 0.25, places=6)

    def test_formati_non_validi(self):
        for testo in ("red", "var(--primary)", "#12", "rgb(1 2)", "oklch(150 0.1 20)", "hsl(a b c)"):
            with self.subTest(testo=testo), self.assertRaises(ValueError):
                contrasto.leggi_colore(testo)


class TestComposizione(unittest.TestCase):
    def test_nero_al_50_per_cento_su_bianco_da_grigio_medio(self):
        effettivo = contrasto.componi(contrasto.leggi_colore("rgb(0 0 0 / 50%)"), BIANCO)
        for c in canali(effettivo):
            self.assertAlmostEqual(c, 0.5, places=6)

    def test_sfondo_semitrasparente_e_un_errore(self):
        with self.assertRaises(ValueError):
            contrasto.rapporto(contrasto.leggi_colore("#000"), contrasto.leggi_colore("#ffffff80"))


class TestCategoria(unittest.TestCase):
    def test_soglie_del_testo_grande(self):
        casi = [
            ((None, False, False), "normale"),
            ((24, False, False), "grande"),
            ((23.9, False, False), "normale"),
            ((18.67, True, False), "grande"),
            ((18.66, True, False), "grande"),
            ((18, True, False), "normale"),
            ((18, False, False), "normale"),  # 18px non è 18pt
            ((12, False, True), "ui"),
        ]
        for argomenti, attesa in casi:
            with self.subTest(argomenti=argomenti):
                self.assertEqual(contrasto.categoria(*argomenti), attesa)

    def test_mostra_tronca_senza_arrotondare(self):
        self.assertEqual(contrasto.mostra(4.4999), "4.49")
        self.assertEqual(contrasto.mostra(21.0), "21.00")


class TestRigaDiComando(unittest.TestCase):
    def test_esito_zero_quando_supera(self):
        codice, uscita, _ = esegui("#000", "#fff")
        self.assertEqual(codice, 0)
        self.assertIn("Rapporto: 21.00:1", uscita)

    def test_esito_uno_quando_non_supera(self):
        codice, uscita, _ = esegui("#777", "#fff")
        self.assertEqual(codice, 1)
        self.assertIn("NON superata", uscita)

    def test_stesso_colore_supera_come_testo_grande(self):
        codice, uscita, _ = esegui("#777", "#fff", "--dimensione", "24")
        self.assertEqual(codice, 0)
        self.assertIn("testo grande", uscita)

    def test_esito_due_su_errore_d_uso(self):
        codice, _, errore = esegui("red", "#fff")
        self.assertEqual(codice, 2)
        self.assertIn("formato non riconosciuto", errore)

    def test_segnala_primo_piano_semitrasparente(self):
        _, uscita, _ = esegui("rgb(0 0 0 / 50%)", "#fff")
        self.assertIn("colore effettivo #808080", uscita)


if __name__ == "__main__":
    unittest.main()
