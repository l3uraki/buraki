"""
Общие абстракции для бизнес-моделей.

@toc
    * [public class ISpecification](#public-class-ispecification)
    * [public class CompositeSpecification](#public-class-compositespecification)
    * [public class AndSpecification](#public-class-andspecification)
    * [public class OrSpecification](#public-class-orspecification)
    * [public class NotSpecification](#public-class-notspecification)

@author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
@copyright Copyright (c) 2024-present Rasim Eminov
@license MIT
@since 0.1.0
"""

from __future__ import annotations

import abc
import typing
from typing import Tuple

__all__ = (
    "ISpecification",
    "CompositeSpecification"
)


class ISpecification[T](typing.Protocol):
    """
    Абстрактная спецификация бизнес-модели.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @since 0.1.0
    """

    @abc.abstractmethod
    def get_filters(self) -> Tuple:
        """
        Получить фильтры спецификации.

        @return
            Фильтры спецификации.
        @rtype
            typing.Tuple
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @since 0.1.0
        """

    @abc.abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """
        Проверить соответствие бизнес-модели спецификации.

        @parameter candidate
            Проверяемая бизнес-модель.
        @ptype candidate
            object
        @return
            Истина, если бизнес-модель соответствует спецификации, иначе ложь.
        @rtype
            bool
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @since 0.1.0
        """

    @abc.abstractmethod
    def get_and_spec(self, other: ISpecification[T]) -> AndSpecification[T]:
        """
        Получить конъюнктивную композицию спецификаций бизнес-модели.

        @parameter other
            Присоединяемая спецификация бизнес-модели.
        @ptype other
            buraki.core.common.ISpecification
        @return
            Конъюнктивная композиция спецификаций бизнес-модели.
        @rtype
            buraki.core.common.AndSpecification
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.common.AndSpecification
        @since 0.1.0
        """

    @abc.abstractmethod
    def get_or_spec(self, other: ISpecification[T]) -> OrSpecification[T]:
        """
        Получить дизъюнктивную композицию спецификаций бизнес-модели.

        @parameter other
            Присоединяемая спецификация бизнес-модели.
        @ptype other
            buraki.core.common.ISpecification
        @return
            Дизъюнктивная композиция спецификаций бизнес-модели.
        @rtype
            buraki.core.common.OrSpecification
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.common.OrSpecification
        @since 0.1.0
        """

    @abc.abstractmethod
    def get_not_spec(self) -> NotSpecification[T]:
        """
        Получить инверсию спецификации бизнес-модели.

        @return
            Инверсия спецификации бизнес-модели.
        @rtype
            buraki.core.common.NotSpecification
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.common.NotSpecification
        @since 0.1.0
        """


class CompositeSpecification[T](abc.ABC, ISpecification[T]):
    """
    Абстрактная композитная спецификация бизнес-модели.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.common.ISpecification
    @since 0.1.0
    """

    @typing.override
    def get_and_spec(self, other: ISpecification[T]) -> AndSpecification[T]:
        return AndSpecification(self, other)

    @typing.override
    def get_or_spec(self, other: ISpecification[T]) -> OrSpecification[T]:
        return OrSpecification(self, other)

    @typing.override
    def get_not_spec(self) -> NotSpecification[T]:
        return NotSpecification(self)


class AndSpecification[T](CompositeSpecification[T]):
    """
    Конъюнктивная композиция спецификаций бизнес-модели.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.common.CompositeSpecification
    @since 0.1.0
    """

    __slots__ = (
        "_inner_left_spec",
        "_inner_right_spec"
    )

    def __init__(
        self,
        left_spec: ISpecification[T],
        right_spec: ISpecification[T]
    ):
        """
        Конструктор конъюнктивной композиции спецификаций бизнес-модели.

        @parameter left_spec
            Левая соединяемая спецификация бизнес-модели.
        @ptype left_spec
            buraki.core.common.ISpecification
        @parameter right_spec
            Правая соединяемая спецификация бизнес-модели.
        @ptype right_spec
            buraki.core.common.ISpecification
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.common.ISpecification
        @since 0.1.0
        """
        self._inner_left_spec = left_spec
        self._inner_right_spec = right_spec

    @typing.override
    def get_filters(self) -> Tuple:
        return self._inner_left_spec.get_filters() + self._inner_right_spec.get_filters()

    @typing.override
    def is_satisfied_by(self, candidate: T) -> bool:
        return (
            self._inner_left_spec.is_satisfied_by(candidate) and
            self._inner_right_spec.is_satisfied_by(candidate)
        )


class OrSpecification[T](CompositeSpecification[T]):
    """
    Дизъюнктивная композиция спецификаций бизнес-модели.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.common.CompositeSpecification
    @since 0.1.0
    """

    __slots__ = (
        "_inner_left_spec",
        "_inner_right_spec"
    )

    def __init__(
        self,
        left_spec: ISpecification[T],
        right_spec: ISpecification[T]
    ):
        """
        Конструктор дизъюнктивной композиции спецификаций бизнес-модели.

        @parameter left_spec
            Левая соединяемая спецификация бизнес-модели.
        @ptype left_spec
            buraki.core.common.ISpecification
        @parameter right_spec
            Правая соединяемая спецификация бизнес-модели.
        @ptype right_spec
            buraki.core.common.ISpecification
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.common.ISpecification
        @since 0.1.0
        """
        self._inner_left_spec = left_spec
        self._inner_right_spec = right_spec

    @typing.override
    def get_filters(self) -> Tuple:
        return self._inner_left_spec.get_filters() + self._inner_right_spec.get_filters()

    @typing.override
    def is_satisfied_by(self, candidate: T) -> bool:
        return (
            self._inner_left_spec.is_satisfied_by(candidate) or
            self._inner_right_spec.is_satisfied_by(candidate)
        )


class NotSpecification[T](CompositeSpecification[T]):
    """
    Инверсия спецификации бизнес-модели.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.common.CompositeSpecification
    @since 0.1.0
    """

    __slots__ = (
        "_inner_spec",
    )

    def __init__(self, spec: ISpecification[T]):
        """
        Конструктор инверсии спецификации бизнес-модели.

        @parameter spec
            Инвертируемая спецификация бизнес-модели.
        @ptype spec
            buraki.core.common.ISpecification
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.common.ISpecification
        @since 0.1.0
        """
        self._inner_spec = spec

    @typing.override
    def get_filters(self) -> Tuple:
        return self._inner_spec.get_filters()

    @typing.override
    def is_satisfied_by(self, candidate: T) -> bool:
        return not self._inner_spec.is_satisfied_by(candidate)
