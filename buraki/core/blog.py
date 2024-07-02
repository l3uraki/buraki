"""
Бизнес-модели блога.

@toc
    * [public class Category](#public-class-category)
    * [public class Post](#public-class-post)
    * [public class PostCategorySpecification](#public-class-postcategoryspecification)
    * [public class PostPublishedAtSpecification](#public-class-postpublishedatspecification)
    * [public class PostTagsSpecification](#public-class-posttagsspecification)
    * [public class IPostRepository](#public-class-ipostrepository)

@author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
@copyright Copyright (c) 2024-present Rasim Eminov
@license MIT
@since 0.1.0
"""

import abc
import datetime
import enum
import typing
import uuid
from typing import List, Tuple

import buraki.core.common as core_common

__all__ = (
    "Category",
    "Post",
    "PostCategorySpecification",
    "PostPublishedAtSpecification",
    "PostTagsSpecification",
    "IPostRepository"
)


@enum.unique
class Category(enum.StrEnum):
    """
    Перечисление категорий постов в блоге.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.blog.Post
    @since 0.1.0
    """

    IT = "IT"
    BUSINESS = "Бизнес"
    SPORT = "Спорт"


class Post:
    """
    Бизнес-модель поста в блоге.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.blog.Category
    @since 0.1.0
    """

    __slots__ = (
        "_post_id",
        "_category",
        "_published_at",
        "_title",
        "_content",
        "_tags",
        "_likes",
        "_dislikes"
    )

    def __init__(
        self,
        post_id: uuid.UUID,
        category: Category,
        published_at: datetime.datetime,
        title: str,
        content: str,
        tags: List[str],
        likes: int,
        dislikes: int
    ):
        """
        Конструктор бизнес-модели поста в блоге.

        @parameter post_id
            Идентификатор поста.
        @ptype post_id
            uuid.UUID
        @parameter category
            Категория поста.
        @ptype category
            buraki.core.blog.Category
        @parameter published_at
            Дата и время публикации поста.
        @ptype published_at
            datetime.datetime
        @parameter title
            Заголовок поста.
        @ptype title
            str
        @parameter content
            Содержимое поста: текст, медиа, файлы и прочее.
        @ptype content
            str
        @parameter tags
            Теги поста.
        @ptype tags
            typing.List[str]
        @parameter likes
            Число отметок "Нравится" у поста.
        @ptype likes
            int
        @parameter dislikes
            Число отметок "Не нравится" у поста.
        @ptype dislikes
            int
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.blog.Category
        @since 0.1.0
        """
        self._post_id = post_id
        self._category = category
        self._published_at = published_at
        self._title = title
        self._content = content
        self._tags = tags
        self._likes = likes
        self._dislikes = dislikes

    @property
    def post_id(self) -> uuid.UUID:
        return self._post_id

    @property
    def category(self) -> Category:
        return self._category

    @property
    def published_at(self) -> datetime.datetime:
        return self._published_at

    @property
    def title(self) -> str:
        return self._title

    @property
    def content(self) -> str:
        return self._content

    @property
    def tags(self) -> List[str]:
        return self._tags.copy()

    @property
    def likes(self) -> int:
        return self._likes

    @property
    def dislikes(self) -> int:
        return self._dislikes

    def __eq__(self, other):
        return (
            self is other or (
                isinstance(other, Post) and
                self._post_id == other._post_id
            )
        )

    def __repr__(self):
        return (
            f"{type(self).__qualname__}("
            f"post_id={self._post_id!r}, "
            f"category={self._category!r}, "
            f"published_at={self._published_at!r}, "
            f"title={self._title!r}, "
            f"content={self._content!r}, "
            f"tags={self._tags!r}, "
            f"likes={self._likes!r}, "
            f"dislikes={self._dislikes!r})"
        )


class PostCategorySpecification(core_common.CompositeSpecification[Post]):
    """
    Спецификация категории поста в блоге.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.blog.Category
    @see buraki.core.blog.Post
    @see buraki.core.common.CompositeSpecification
    @since 0.1.0
    """

    __slots__ = (
        "_reference_category",
    )

    def __init__(self, reference_category: Category):
        """
        Конструктор спецификации категории поста в блоге.

        @parameter reference_category
            Эталонная категория поста.
        @ptype reference_category
            buraki.core.blog.Category
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.blog.Category
        @since 0.1.0
        """
        self._reference_category = reference_category

    @typing.override
    def get_filters(self) -> Tuple:
        return (
            self._reference_category,
        )

    @typing.override
    def is_satisfied_by(self, candidate: Post) -> bool:
        return candidate.category == self._reference_category


class PostPublishedAtSpecification(core_common.CompositeSpecification[Post]):
    """
    Спецификация даты и времени публикации поста в блоге.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.blog.Post
    @see buraki.core.common.CompositeSpecification
    @since 0.1.0
    """

    __slots__ = (
        "_published_from",
        "_published_to"
    )

    def __init__(self, published_from: datetime.datetime, published_to: datetime.datetime):
        """
        Конструктор спецификации даты и времени публикации поста в
        блоге.

        @parameter published_from
            Нижняя граница диапазона даты и времени публикации поста.
        @ptype published_from
            datetime.datetime
        @parameter published_to
            Верхняя граница диапазона даты и времени публикации поста.
        @ptype published_to
            datetime.datetime
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @since 0.1.0
        """
        self._published_from = published_from
        self._published_to = published_to

    @typing.override
    def get_filters(self) -> Tuple:
        return (
            self._published_from,
            self._published_to
        )

    @typing.override
    def is_satisfied_by(self, candidate: Post) -> bool:
        return self._published_from <= candidate.published_at <= self._published_to


class PostTagsSpecification(core_common.CompositeSpecification[Post]):
    """
    Спецификация тегов поста в блоге.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.blog.Post
    @see buraki.core.common.CompositeSpecification
    @since 0.1.0
    """

    __slots__ = (
        "_reference_tags",
    )

    def __init__(self, *reference_tags: str):
        """
        Конструктор спецификации тегов поста в блоге.

        @parameter reference_tags
            Эталонные теги поста.
        @ptype reference_tags
            typing.Tuple[str, ...]
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @since 0.1.0
        """
        self._reference_tags = reference_tags

    @typing.override
    def get_filters(self) -> Tuple:
        return (
            self._reference_tags,
        )

    @typing.override
    def is_satisfied_by(self, candidate: Post) -> bool:
        return any(
            reference_tag in candidate.tags
            for reference_tag in self._reference_tags
        )


class IPostRepository(typing.Protocol):
    """
    Абстрактное хранилище постов в блоге.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.blog.Post
    @since 0.1.0
    """

    @abc.abstractmethod
    def add(self, new_post: Post) -> typing.Awaitable[None]:
        """
        Добавить пост в блоге в хранилище.

        @parameter new_post
            Добавляемый пост.
        @ptype new_post
            buraki.core.blog.Post
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.blog.Post
        @since 0.1.0
        """

    @abc.abstractmethod
    def get_by_id(self, post_id: uuid.UUID) -> typing.Awaitable[Post]:
        """
        Получить пост в блоге из хранилища по идентификатору.

        @parameter post_id
            Идентификатор поста.
        @ptype post_id
            uuid.UUID
        @return
            Пост, соответствующий указанному идентификатору.
        @rtype
            buraki.core.blog.Post
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.blog.Post
        @since 0.1.0
        """

    @abc.abstractmethod
    def get_by_spec(
        self,
        spec: core_common.ISpecification[Post],
        limit: typing.Optional[int] = None,
        offset: typing.Optional[int] = None
    ) -> typing.AsyncIterator[Post]:
        """
        Получить посты в блоге из хранилища по спецификации.

        @parameter spec
            Спецификация поста.
        @ptype spec
            buraki.core.common.ISpecification
        @parameter limit
            Ограничение числа полученных постов.

            Если параметр не указан, то число полученных постов не будет
            ограничено.
        @ptype limit
            typing.Optional[int]
        @parameter offset
            Пропуск первых нескольких полученных постов.

            Если параметр не указан, то ни один полученный пост не будет
            пропущен.
        @ptype offset
            typing.Optional[int]
        @return
            Посты, соответствующие указанной спецификации.
        @rtype
            typing.AsyncIterator[buraki.core.blog.Post]
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.blog.Post
        @see buraki.core.common.ISpecification
        @since 0.1.0
        """

    @abc.abstractmethod
    def get_all(
        self,
        limit: typing.Optional[int] = None,
        offset: typing.Optional[int] = None
    ) -> typing.AsyncIterator[Post]:
        """
        Получить все посты в блоге из хранилища.

        @parameter limit
            Ограничение числа полученных постов.

            Если параметр не указан, то число полученных постов не будет
            ограничено.
        @ptype limit
            typing.Optional[int]
        @parameter offset
            Пропуск первых нескольких полученных постов.

            Если параметр не указан, то ни один полученный пост не будет
            пропущен.
        @ptype offset
            typing.Optional[int]
        @return
            Все посты из хранилища.
        @rtype
            typing.AsyncIterator[buraki.core.blog.Post]
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.blog.Post
        @since 0.1.0
        """

    @abc.abstractmethod
    def update(self, new_post: Post) -> typing.Awaitable[None]:
        """
        Обновить пост в блоге в хранилище.

        Обновление поста — замена значений атрибутов замещаемого поста
        на значения атрибутов заменяющего поста.

        Идентификаторы замещаемого и заменяющего постов эквивалентны.

        @parameter new_post
            Заменяющий пост.
        @ptype new_post
            buraki.core.blog.Post
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.blog.Post
        @since 0.1.0
        """

    @abc.abstractmethod
    def remove(self, old_post: Post) -> typing.Awaitable[None]:
        """
        Удалить пост в блоге из хранилища.

        @parameter old_post
            Удаляемый пост.
        @ptype old_post
            buraki.core.blog.Post
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.blog.Post
        @since 0.1.0
        """
