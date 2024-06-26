"""
Точка версионирования приложения.

Используется семантическое версионирование в соответствии со
спецификацией [SemVer](https://semver.org/).

Требуется нормализация для соответствия со спецификацией
[PEP 440](https://peps.python.org/pep-0440/).

@author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
@copyright Copyright (c) 2024-present Rasim Eminov
@license MIT
@since 0.1.0
"""

__version__ = "0.1.0-1"
__version_info__ = tuple(
    int(version_part) if version_part.isdigit() else version_part
    for version_part in __version__.split("+")[0].replace("-", ".", 1).split(".")
)
