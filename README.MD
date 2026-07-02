# DevBoard

DevBoard to aplikacja webowa napisana w Django, służąca do zarządzania projektami i zadaniami. Projekt wykorzystuje wbudowany system użytkowników Django, panel administracyjny oraz szablony HTML z Bootstrapem.

## Najważniejsze funkcje

- logowanie i wylogowanie użytkownika,
- lista projektów zalogowanego użytkownika,
- szczegóły projektu z listą zadań,
- dodawanie nowych zadań,
- walidacja formularza zadania,
- panel administracyjny dla projektów, zadań i komentarzy,
- testy oparte o `pytest` i `pytest-django`,
- diagram klas UML w katalogu `docs`.

## Technologie

- Python
- Django 5.2
- SQLite lokalnie
- pytest / pytest-django
- Bootstrap 5
- Graphviz DOT / Pillow dla diagramów

## Struktura projektu

```text
Django_project/
├── config/                  # konfiguracja Django
├── devboard/                # główna aplikacja projektu
├── docs/                    # dokumentacja i diagramy
├── templates/               # szablony HTML
├── static/                  # pliki statyczne
├── manage.py
├── pytest.ini
└── requirements.txt
```

## Dokumentacja

Szczegółowa dokumentacja techniczna znajduje się tutaj:

```text
docs/PROJECT_DOCUMENTATION.md
```

Dokumentacja katalogu `docs`:

```text
docs/README.md
```

## Diagram klas UML

Aktualny diagram klas:

```text
docs/class_diagram.png
```

Źródło diagramu:

```text
docs/class_diagram.dot
```

Regenerowanie diagramu PNG:

```powershell
python docs\generate_class_diagram.py
```

## Instalacja lokalna

### 1. Utwórz i aktywuj środowisko wirtualne

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Zainstaluj zależności

```powershell
python -m pip install -r requirements.txt
```

### 3. Przygotuj plik `.env`

Ustawienia lokalne (`config/settings/dev.py`) ładują zmienne z pliku `.env`.

Minimalny przykład:

```env
SECRET_KEY=dev-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
```

### 4. Uruchom migracje

```powershell
python manage.py migrate --settings=config.settings.dev
```

### 5. Utwórz konto administratora

```powershell
python manage.py createsuperuser --settings=config.settings.dev
```

### 6. Uruchom serwer

```powershell
python manage.py runserver --settings=config.settings.dev
```

Aplikacja będzie dostępna pod adresem:

```text
http://127.0.0.1:8000/
```

Panel administratora:

```text
http://127.0.0.1:8000/admin/
```

## Testy

Uruchomienie testów:

```powershell
python -m pytest
```

Testy z pokryciem kodu:

```powershell
python -m pytest --cov=devboard
```

## Główne ścieżki aplikacji

| URL | Nazwa | Opis |
| --- | --- | --- |
| `/` | `devboard:project_list` | lista projektów użytkownika |
| `/project/<pk>/` | `devboard:project_details` | szczegóły projektu |
| `/zadania/nowe/` | `devboard:task_create` | dodawanie zadania |
| `/accounts/login/` | `login` | logowanie |
| `/accounts/logout/` | `logout` | wylogowanie |
| `/admin/` | admin | panel administracyjny |

## Modele domenowe

- `Project` — projekt należący do użytkownika,
- `Task` — zadanie przypisane do projektu,
- `Comment` — komentarz przypisany do zadania.

## Uwagi rozwojowe

- Obsługa komentarzy jest częściowo przygotowana, ale wymaga dopięcia routingu i szablonu.
- Do lokalnych komend zalecane jest jawne używanie `--settings=config.settings.dev`.
- Szczegółowe ograniczenia i rekomendacje są opisane w `docs/PROJECT_DOCUMENTATION.md`.
