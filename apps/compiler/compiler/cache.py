"""Хөрвүүлэлтийн үр дүнгийн санах ойн кэш.

Сурагч бүрийн хөндөгдөөгүй анхны код яг ижил байдаг. Тиймээс хичээл бүрийн
анхны «Ажиллуулах» нь хөрвүүлэлтгүйгээр кэшээс шууд ирнэ — сурагчид зөвхөн
сүлжээний хугацаа үлдэнэ. Хөрвүүлэлтийн алдаа ч кэшлэгдэнэ: «Алдаа унших»
хичээлийн анхны код зориуд алдаатай бөгөөд бүх анги түүнийг ажиллуулна.

Процесс бүр өөрийн кэштэй. Image шинэчлэгдэхэд процесс дахин эхэлж, хуучин
хөрвүүлэгчийн гаргасан модуль үлдэхгүй.
"""

import hashlib
from collections import OrderedDict
from typing import Generic, TypeVar

T = TypeVar("T")


def cache_key(language: str, flags: tuple[str, ...], source: str) -> str:
    """Хэл, тугууд, кодоос тогтвортой түлхүүр гаргана.

    Хэсэг бүрийн хооронд тэг байт тавина — ингэснээр `("c", "x")` ба
    `("cx", "")` зэрэг хослол ижил түлхүүр болохгүй.
    """
    digest = hashlib.sha256()
    for part in (language, "\0".join(flags), source):
        digest.update(part.encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


class SizedLRUCache(Generic[T]):
    """Нийт БАЙТААР хязгаарлагдсан LRU кэш.

    Элементийн тоогоор биш байтаар хязгаарлана: C модуль хэдэн KB, C++ модуль
    хэдэн зуун KB — тоогоор хязгаарлавал санах ойн хэрэглээ урьдчилан
    тооцоологдохгүй.

    Бүх хандалт asyncio-ийн нэг thread дээр болдог тул түгжээ шаардлагагүй.
    """

    def __init__(self, max_bytes: int) -> None:
        self._max_bytes = max_bytes
        self._items: OrderedDict[str, tuple[T, int]] = OrderedDict()
        self._size = 0

    def get(self, key: str) -> T | None:
        item = self._items.get(key)
        if item is None:
            return None
        self._items.move_to_end(key)
        return item[0]

    def put(self, key: str, value: T, size: int) -> None:
        # Ганц үр дүн кэшээс том бол бусдыг бүгдийг шахаж гаргахгүй.
        if size > self._max_bytes:
            return
        previous = self._items.pop(key, None)
        if previous is not None:
            self._size -= previous[1]
        self._items[key] = (value, size)
        self._size += size
        while self._size > self._max_bytes:
            _, (_, evicted_size) = self._items.popitem(last=False)
            self._size -= evicted_size

    def __len__(self) -> int:
        return len(self._items)

    @property
    def size_bytes(self) -> int:
        return self._size
