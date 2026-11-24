"""Comprueba que las páginas listas para Moodle enlazan los recursos del aula Git."""

import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://diegomezapy.github.io/curso_visualiza_datos_UNC/aula/index.html"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.add(href)


def links(path):
    parser = Links()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.hrefs


class MoodleResourceParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        js = (ROOT / "site/aula/data.js").read_text(encoding="utf-8")
        cls.data = json.loads(js.removeprefix("window.CURSO=").removesuffix(";"))

    def test_session_resources(self):
        for session in self.data["sesiones"]:
            number = session["n"]
            with self.subTest(session=number):
                actual = links(ROOT / f"moodle/paginas/sesion_{number}.html")
                expected = {urljoin(BASE, resource["u"]) for resource in session["recursos"]}
                expected.update(lecture["u"] for lecture in session["lecturas"])
                expected.update(
                    ("https://www.youtube.com/playlist?list=" if video["tipo"] == "playlist"
                     else "https://www.youtube.com/watch?v=") + video["id"]
                    for video in session["videos"]
                )
                for practice in session["practicas_reales"]:
                    expected.add(practice["colab"])
                    if practice["rmd"]:
                        expected.add(practice["rmd"])
                media = session["media"]
                for deck in media if isinstance(media, list) else [media] if media else []:
                    expected.update(urljoin(BASE, deck[key]) for key in ("pdf", "pptx"))
                    if deck.get("infografia"):
                        expected.add(urljoin(BASE, deck["infografia"]["src"]))
                self.assertFalse(expected - actual, f"Faltan enlaces: {sorted(expected - actual)}")

    def test_general_resources(self):
        actual = links(ROOT / "moodle/paginas/recursos_generales.html")
        base = "https://diegomezapy.github.io/curso_visualiza_datos_UNC"
        raw = self.data["config"]["raw"]
        expected = {f"{base}/materiales/pdf/{name}.pdf" for name, _ in self.data["materiales"]}
        expected.update(f"{raw}/datos/{name}" for name, _ in self.data["datasets"])
        self.assertFalse(expected - actual, f"Faltan enlaces: {sorted(expected - actual)}")

    def test_moodle_compatible_text(self):
        for page in (ROOT / "moodle/paginas").glob("*.html"):
            with self.subTest(page=page.name):
                self.assertFalse(
                    [character for character in page.read_text(encoding="utf-8") if ord(character) > 0xFFFF],
                    "FACET Moodle rechazó los caracteres fuera del plano básico Unicode",
                )


if __name__ == "__main__":
    unittest.main()
