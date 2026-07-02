# Dokumentacja techniczna projektu DevBoard

## 1. Cel projektu

DevBoard to aplikacja webowa oparta o Django, służąca do zarządzania projektami i zadaniami. Użytkownik po zalogowaniu widzi wyłącznie własne projekty, może przejść do szczegółów projektu oraz dodać zadanie do wybranego projektu.

Projekt ma charakter aplikacji typu CRUD z panelem administracyjnym Django i prostym interfejsem użytkownika przygotowanym w szablonach HTML z Bootstrapem.

## 2. Zakres funkcjonalny

### Dostępne funkcje

- logowanie i wylogowanie użytkownika przez wbudowane widoki Django,
- lista projektów przypisanych do zalogowanego użytkownika,
- szczegóły projektu z listą zadań,
- dodawanie zadania do projektu,
- walidacja formularza zadania,
- panel administracyjny dla projektów, zadań i komentarzy,
- testy jednostkowe modeli i podstawowy test widoku tworzenia zadania,
- diagram klas UML w katalogu `docs`.

### Funkcje częściowo przygotowane

W modelach istnieje obsługa komentarzy (`Comment`), a w widokach znajduje się szkic widoku dodawania komentarza. Funkcja komentarzy nie jest jeszcze podpięta w `devboard/urls.py` i nie ma kompletnego szablonu `comment_add.html` w katalogu `templates`.

## 3. Technologie

| Obszar | Technologia |
| --- | --- |
| Backend | Python, Django 5.2 |
| Baza danych lokalna | SQLite |
| Testy | pytest, pytest-django, pytest-cov |
| Frontend | Django Templates, Bootstrap 5 |
| Konfiguracja środowiska | python-dotenv |
| Diagramy | Graphviz DOT, Pillow |

## 4. Struktura katalogów

```text
Django_project/
├── config/                  # konfiguracja projektu Django
│   ├── urls.py              # główne routingi
│   └── settings/            # ustawienia base/dev/prod
├── devboard/                # główna aplikacja biznesowa
│   ├── models.py            # modele Project, Task, Comment
│   ├── forms.py             # formularze TaskForm, CommentForm
│   ├── views.py             # widoki klasowe
│   ├── urls.py              # routingi aplikacji devboard
│   ├── admin.py             # konfiguracja panelu admina
│   └── tests/               # testy pytest
├── docs/                    # dokumentacja i diagramy
│   ├── PROJECT_DOCUMENTATION.md
│   ├── class_diagram.dot
│   ├── class_diagram.png
│   └── generate_class_diagram.py
├── templates/               # szablony HTML
│   ├── base.html
│   ├── devboard/
│   └── registration/
├── static/                  # pliki statyczne projektu
├── manage.py
├── pytest.ini
└── requirements.txt
```

## 5. Model domenowy

### `Project`

Reprezentuje projekt użytkownika.

Najważniejsze pola:

- `name` — nazwa projektu,
- `description` — opis projektu,
- `owner` — właściciel projektu (`User`),
- `created_at`, `updated_at` — metadane czasu.

Metody:

- `task_count()` — zwraca liczbę zadań w projekcie,
- `__str__()` — zwraca nazwę projektu.

### `Task`

Reprezentuje zadanie w projekcie.

Najważniejsze pola:

- `title` — tytuł zadania,
- `description` — opis,
- `project` — projekt, do którego należy zadanie,
- `assignee` — opcjonalnie przypisany użytkownik,
- `status` — status: `TODO`, `IN_PROGRESS`, `DONE`,
- `priority` — priorytet: niski, średni, wysoki,
- `due_date` — opcjonalny termin wykonania.

Logika:

- `is_overdue` zwraca `True`, jeśli zadanie ma termin w przeszłości i nie jest ukończone.

### `Comment`

Reprezentuje komentarz do zadania.

Najważniejsze pola:

- `task` — zadanie,
- `author` — autor komentarza,
- `body` — treść komentarza,
- `created_at`, `updated_at` — metadane czasu.

## 6. Diagram klas

Diagram UML znajduje się w pliku:

```text
docs/class_diagram.png
```

Źródło diagramu Graphviz DOT:

```text
docs/class_diagram.dot
```

Generator PNG:

```text
docs/generate_class_diagram.py
```

Regenerowanie diagramu:

```powershell
python docs\generate_class_diagram.py
```

## 7. Widoki i routing

### Główne URL-e

| URL | Nazwa | Widok | Opis |
| --- | --- | --- | --- |
| `/` | `devboard:project_list` | `ProjectListView` | lista projektów użytkownika |
| `/project/<pk>/` | `devboard:project_details` | `ProjectDataView` | szczegóły projektu i zadania |
| `/zadania/nowe/` | `devboard:task_create` | `TaskCreateView` | formularz dodawania zadania |
| `/accounts/login/` | `login` | Django auth | logowanie |
| `/accounts/logout/` | `logout` | Django auth | wylogowanie |
| `/admin/` | admin | Django admin | panel administracyjny |

### Zabezpieczenia dostępu

Widoki aplikacji `devboard` korzystają z `LoginRequiredMixin`, dlatego użytkownik musi być zalogowany, aby przeglądać projekty i dodawać zadania.

Dodatkowo:

- `ProjectListView` filtruje projekty po `owner=self.request.user`,
- `ProjectDataView` pozwala pobrać tylko projekt właściciela,
- `TaskCreateView` ogranicza listę projektów w formularzu do projektów właściciela.

## 8. Formularze

### `TaskForm`

Formularz obsługuje tworzenie zadań. Pola formularza:

- `title`,
- `description`,
- `due_date`,
- `priority`,
- `assignee`,
- `project`,
- `status`.

Reguła walidacyjna:

- zadanie o wysokim priorytecie musi mieć ustawiony termin wykonania.

### `CommentForm`

Formularz przygotowany dla komentarzy. Pola:

- `task`,
- `body`.

## 9. Panel administracyjny

Panel Django Admin jest dostępny pod adresem:

```text
/admin/
```

Konfiguracja panelu znajduje się w `devboard/admin.py`.

Dostępne elementy:

- `ProjectAdmin` z wyszukiwaniem, filtrowaniem i inline dla zadań,
- `TaskAdmin` z filtrami, wyszukiwaniem, hierarchią dat i kolorową etykietą statusu,
- standardowa rejestracja `Comment`.

## 10. Konfiguracja środowisk

Projekt ma rozdzielone ustawienia:

| Plik | Przeznaczenie |
| --- | --- |
| `config/settings/base.py` | wspólna konfiguracja Django |
| `config/settings/dev.py` | konfiguracja lokalna z SQLite |
| `config/settings/prod.py` | szkic konfiguracji produkcyjnej z PostgreSQL |

`pytest.ini` wskazuje ustawienia testowe/deweloperskie:

```ini
DJANGO_SETTINGS_MODULE = config.settings.dev
```

Dla lokalnego uruchomienia zalecane jest jawne wskazanie ustawień:

```powershell
python manage.py runserver --settings=config.settings.dev
```

## 11. Instalacja i uruchomienie lokalne

### 1. Utworzenie środowiska wirtualnego

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalacja zależności

```powershell
python -m pip install -r requirements.txt
```

### 3. Przygotowanie zmiennych środowiskowych

Ustawienia `dev.py` ładują plik `.env`. Plik powinien zawierać co najmniej:

```env
SECRET_KEY=dev-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Uwaga: aktualna implementacja `ALLOWED_HOSTS` odczytuje wartość jako jeden element listy, więc dla prostego uruchomienia lokalnego wystarczy pojedynczy host, np. `127.0.0.1`.

### 4. Migracje

```powershell
python manage.py migrate --settings=config.settings.dev
```

### 5. Konto administratora

```powershell
python manage.py createsuperuser --settings=config.settings.dev
```

### 6. Start serwera

```powershell
python manage.py runserver --settings=config.settings.dev
```

Po uruchomieniu aplikacja powinna być dostępna pod adresem:

```text
http://127.0.0.1:8000/
```

## 12. Testy

Uruchamianie testów:

```powershell
python -m pytest
```

Uruchamianie testów z pokryciem:

```powershell
python -m pytest --cov=devboard
```

Aktualnie w projekcie są testy dla:

- domyślnego statusu zadania,
- reprezentacji tekstowej zadania,
- podstawowego scenariusza wejścia w widok tworzenia zadania.

## 13. Znane ograniczenia i rekomendacje

- Widok komentarzy jest rozpoczęty, ale nie jest jeszcze kompletny ani podpięty w routingu.
- `manage.py` domyślnie wskazuje `config.settings`, dlatego w komendach warto jawnie podawać `--settings=config.settings.dev`.
- `config/settings/prod.py` definiuje bazę pod kluczem `production`; Django standardowo oczekuje aliasu `default`.
- `ALLOWED_HOSTS` w `dev.py` i `prod.py` traktuje zawartość zmiennej środowiskowej jako pojedynczy wpis listy.
- Warto dodać testy dla autoryzacji dostępu do projektów oraz walidacji formularza `TaskForm`.

## 14. Możliwe kierunki rozwoju

- pełna obsługa komentarzy do zadań,
- edycja i usuwanie projektów oraz zadań,
- tablica Kanban,
- filtrowanie i sortowanie zadań,
- API REST na bazie Django REST Framework,
- role użytkowników i uprawnienia zespołowe,
- wdrożenie produkcyjne z PostgreSQL.

