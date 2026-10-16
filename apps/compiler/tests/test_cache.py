"""Үр дүнгийн кэш — emcc шаардахгүй, хаана ч ажиллана."""

from compiler.cache import SizedLRUCache, cache_key


def test_key_is_stable_and_depends_on_every_part() -> None:
    key = cache_key("c", ("-O1",), "int main(){}")

    assert key == cache_key("c", ("-O1",), "int main(){}")
    assert key != cache_key("cpp", ("-O1",), "int main(){}")
    assert key != cache_key("c", ("-O2",), "int main(){}")
    assert key != cache_key("c", ("-O1",), "int main(){ }")


def test_key_keeps_part_boundaries() -> None:
    """Хэсгүүдийг зүгээр нийлүүлбэл ("c", "x") ба ("cx", "") ижил болох байсан."""
    assert cache_key("c", ("x",), "") != cache_key("cx", ("",), "")


def test_get_returns_stored_value() -> None:
    cache: SizedLRUCache[bytes] = SizedLRUCache(max_bytes=100)
    cache.put("a", b"12345", 5)

    assert cache.get("a") == b"12345"
    assert cache.get("missing") is None


def test_evicts_least_recently_used_when_over_budget() -> None:
    cache: SizedLRUCache[str] = SizedLRUCache(max_bytes=10)
    cache.put("a", "A", 4)
    cache.put("b", "B", 4)

    # `a`-г уншсан тул хамгийн сүүлд ашиглагдсан нь болно.
    cache.get("a")

    # 12 байт > 10 — хамгийн эрт ашиглагдсан `b` гарах ёстой.
    cache.put("c", "C", 4)

    assert cache.get("b") is None
    assert cache.get("a") == "A"
    assert cache.get("c") == "C"
    assert cache.size_bytes == 8


def test_oversized_value_is_skipped_without_evicting_others() -> None:
    cache: SizedLRUCache[str] = SizedLRUCache(max_bytes=10)
    cache.put("a", "A", 4)
    cache.put("huge", "H", 11)

    assert cache.get("huge") is None
    assert cache.get("a") == "A"


def test_replacing_a_key_updates_the_size() -> None:
    cache: SizedLRUCache[str] = SizedLRUCache(max_bytes=100)
    cache.put("a", "long", 5)
    cache.put("a", "short", 2)

    assert cache.size_bytes == 2
    assert len(cache) == 1
    assert cache.get("a") == "short"
