# Dokumentacja katalogu `docs`

Ten katalog zawiera dokumentację techniczną i diagramy projektu DevBoard.

## Pliki

| Plik | Opis |
| --- | --- |
| `PROJECT_DOCUMENTATION.md` | szczegółowa dokumentacja techniczna projektu |
| `class_diagram.dot` | źródło diagramu klas w formacie Graphviz DOT |
| `class_diagram.png` | wygenerowany diagram klas UML w formacie PNG |
| `generate_class_diagram.py` | skrypt generujący `class_diagram.png` |

## Regenerowanie diagramu

```powershell
python docs\generate_class_diagram.py
```

