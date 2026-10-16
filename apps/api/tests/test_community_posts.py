"""Community — нийтлэл, шошго, лайк, сэтгэгдэл, устгах эрх, гомдол."""

import uuid
from datetime import UTC, datetime, timedelta

import httpx
import pytest
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.content.community import OFFICIAL_POSTS, OfficialPost
from app.core.config import settings
from app.core.rate_limit import InMemoryRateLimitBackend
from app.models.community_post import CommunityComment, CommunityPost, CommunityPostLike
from app.models.enums import FeedbackKind, PostLanguage, PostType, UserRole
from app.models.feedback import Feedback
from app.models.user import User
from app.seed import _sync_official_posts
from app.services.community_post_service import EXCERPT_LENGTH, excerpt
from tests.conftest import login_as, make_user

STUDENT = "suragch@test.mn"
OTHER = "busad@test.mn"
ADMIN = "admin@test.mn"

POST = {
    "title": "Python-д list-ийг яаж эрэмбэлэх вэ?",
    "body": "Тоонуудын жагсаалтыг багаас их рүү эрэмбэлмээр байна.\n\n```python\nprint(1)\n```",
    "language": "python",
    "type": "help",
}


async def _join(client: httpx.AsyncClient, api: str, email: str) -> None:
    """Нэвтэрч, Community-ийн дүрмийг зөвшөөрнө — бичихэд шаардлагатай."""
    await login_as(client, api, email)
    accepted = await client.post(f"{api}/community/guidelines")
    assert accepted.status_code == 200, accepted.text


async def _create(client: httpx.AsyncClient, api: str, **overrides: str) -> dict:
    response = await client.post(f"{api}/community/posts", json={**POST, **overrides})
    assert response.status_code == 201, response.text
    return response.json()


async def _official(db: AsyncSession, **fields: object) -> CommunityPost:
    post = CommunityPost(
        author_id=None,
        title="MedlegHub-ийн мэдэгдэл",
        body="Community-д тавтай морил!",
        language=PostLanguage.GENERAL,
        type=PostType.DISCUSSION,
        **fields,
    )
    db.add(post)
    await db.commit()
    return post


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("GET", "/community/posts"),
        ("POST", "/community/posts"),
        ("GET", f"/community/posts/{uuid.uuid4()}"),
        ("PUT", f"/community/posts/{uuid.uuid4()}/like"),
        ("POST", f"/community/posts/{uuid.uuid4()}/comments"),
        ("POST", f"/community/posts/{uuid.uuid4()}/report"),
    ],
)
async def test_requires_login(client: httpx.AsyncClient, api: str, method: str, path: str) -> None:
    response = await client.request(method, f"{api}{path}", json={})
    assert response.status_code == 401


async def test_create_list_and_read_post(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    user = await make_user(db, STUDENT)
    await _join(client, api, STUDENT)

    created = await _create(client, api)
    assert created["title"] == POST["title"]
    assert created["body"] == POST["body"]
    assert created["language"] == "python"
    assert created["type"] == "help"
    assert created["pinned"] is False
    assert created["author"] == {
        "id": str(user.id),
        "name": user.name,
        "avatar_key": None,
        "profile_hidden": False,
    }
    assert (created["like_count"], created["comment_count"], created["liked"]) == (0, 0, False)
    assert created["comments"] == []

    page = (await client.get(f"{api}/community/posts")).json()
    assert page["total"] == 1
    [item] = page["items"]
    assert item["id"] == created["id"]
    # Жагсаалтад код блокгүй, нэг мөр хэсэг л — бүтэн бие биш.
    assert item["excerpt"] == "Тоонуудын жагсаалтыг багаас их рүү эрэмбэлмээр байна."
    assert "body" not in item
    # Хувийн мэдээлэл ил гарахгүй.
    assert "email" not in item["author"]

    detail = await client.get(f"{api}/community/posts/{created['id']}")
    assert detail.status_code == 200
    assert detail.json()["body"] == POST["body"]

    missing = await client.get(f"{api}/community/posts/{uuid.uuid4()}")
    assert missing.status_code == 404


@pytest.mark.parametrize(
    "overrides",
    [
        {"language": "rust"},
        {"type": "question"},
        {"language": None},
        {"type": None},
        {"title": "  Hi  "},
        {"title": "а" * 151},
        {"body": "богино"},
        {"body": "а" * 10_001},
    ],
)
async def test_create_rejects_invalid_input(
    client: httpx.AsyncClient, api: str, db: AsyncSession, overrides: dict
) -> None:
    await make_user(db, STUDENT)
    await _join(client, api, STUDENT)
    payload = {key: value for key, value in {**POST, **overrides}.items() if value is not None}
    response = await client.post(f"{api}/community/posts", json=payload)
    assert response.status_code == 422


async def test_list_filters_by_tags_and_puts_pinned_first(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    pinned = await _official(db, pinned=True)
    await make_user(db, STUDENT)
    await _join(client, api, STUDENT)
    python_help = await _create(client, api)
    c_fact = await _create(client, api, language="c", type="fun_fact")
    python_talk = await _create(client, api, type="discussion")

    async def ids(**params: str) -> list[str]:
        page = (await client.get(f"{api}/community/posts", params=params)).json()
        return [item["id"] for item in page["items"]]

    # Онцолсон нь хамгийн хуучин ч эхэнд, бусад нь шинэ нь эхэндээ.
    assert await ids() == [
        str(pinned.id),
        python_talk["id"],
        c_fact["id"],
        python_help["id"],
    ]
    assert await ids(language="python") == [python_talk["id"], python_help["id"]]
    assert await ids(type="fun_fact") == [c_fact["id"]]
    assert await ids(language="python", type="help") == [python_help["id"]]
    assert await ids(language="general") == [str(pinned.id)]

    page = (await client.get(f"{api}/community/posts", params={"page_size": 2})).json()
    assert (page["total"], page["total_pages"], len(page["items"])) == (4, 2, 2)

    bad = await client.get(f"{api}/community/posts", params={"language": "rust"})
    assert bad.status_code == 422


async def test_official_post_has_no_author(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    post = await _official(db)
    await make_user(db, STUDENT)
    await _join(client, api, STUDENT)

    [item] = (await client.get(f"{api}/community/posts")).json()["items"]
    assert item["author"] is None
    assert (await client.get(f"{api}/community/posts/{post.id}")).json()["author"] is None


async def test_hidden_profile_is_flagged_on_posts_and_comments(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    user = await make_user(db, STUDENT)
    user.profile_hidden = True
    await db.commit()
    await _join(client, api, STUDENT)

    post = await _create(client, api)
    await client.post(f"{api}/community/posts/{post['id']}/comments", json={"body": "Нэмэлт"})

    detail = (await client.get(f"{api}/community/posts/{post['id']}")).json()
    assert detail["author"]["profile_hidden"] is True
    assert detail["comments"][0]["author"]["profile_hidden"] is True


async def test_like_is_idempotent_and_per_user(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, STUDENT)
    await make_user(db, OTHER)
    await _join(client, api, STUDENT)
    post = await _create(client, api)
    like_url = f"{api}/community/posts/{post['id']}/like"

    assert (await client.put(like_url)).json() == {"liked": True, "like_count": 1}
    assert (await client.put(like_url)).json() == {"liked": True, "like_count": 1}

    await _join(client, api, OTHER)
    assert (await client.put(like_url)).json() == {"liked": True, "like_count": 2}
    assert (await client.delete(like_url)).json() == {"liked": False, "like_count": 1}
    assert (await client.delete(like_url)).json() == {"liked": False, "like_count": 1}

    [item] = (await client.get(f"{api}/community/posts")).json()["items"]
    assert (item["like_count"], item["liked"]) == (1, False)

    await _join(client, api, STUDENT)
    detail = (await client.get(f"{api}/community/posts/{post['id']}")).json()
    assert (detail["like_count"], detail["liked"]) == (1, True)

    missing = await client.put(f"{api}/community/posts/{uuid.uuid4()}/like")
    assert missing.status_code == 404


async def test_comments_are_listed_oldest_first(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, STUDENT)
    other = await make_user(db, OTHER)
    await _join(client, api, STUDENT)
    post = await _create(client, api)
    comments_url = f"{api}/community/posts/{post['id']}/comments"

    await _join(client, api, OTHER)
    first = await client.post(comments_url, json={"body": "  sorted() ашиглаарай.  "})
    assert first.status_code == 201, first.text
    assert first.json()["body"] == "sorted() ашиглаарай."
    assert first.json()["author"]["id"] == str(other.id)
    second = (await client.post(comments_url, json={"body": "list.sort() ч болно."})).json()

    detail = (await client.get(f"{api}/community/posts/{post['id']}")).json()
    assert [comment["id"] for comment in detail["comments"]] == [first.json()["id"], second["id"]]
    assert detail["comment_count"] == 2
    [item] = (await client.get(f"{api}/community/posts")).json()["items"]
    assert item["comment_count"] == 2

    for body in ("   ", "а" * 3001):
        assert (await client.post(comments_url, json={"body": body})).status_code == 422
    missing = await client.post(
        f"{api}/community/posts/{uuid.uuid4()}/comments", json={"body": "Сайн уу"}
    )
    assert missing.status_code == 404


async def test_only_author_or_admin_can_delete(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, STUDENT)
    await make_user(db, OTHER)
    await make_user(db, ADMIN, role=UserRole.ADMIN)
    official = await _official(db)

    await _join(client, api, STUDENT)
    post = await _create(client, api)
    comment = (
        await client.post(f"{api}/community/posts/{post['id']}/comments", json={"body": "Би"})
    ).json()

    await _join(client, api, OTHER)
    other_comment = (
        await client.post(f"{api}/community/posts/{post['id']}/comments", json={"body": "Чи"})
    ).json()
    assert (await client.delete(f"{api}/community/posts/{post['id']}")).status_code == 403
    assert (await client.delete(f"{api}/community/comments/{comment['id']}")).status_code == 403
    assert (await client.delete(f"{api}/community/posts/{official.id}")).status_code == 403
    deleted = await client.delete(f"{api}/community/comments/{other_comment['id']}")
    assert deleted.status_code == 200

    await _join(client, api, ADMIN)
    assert (await client.delete(f"{api}/community/comments/{comment['id']}")).status_code == 200
    assert (await client.delete(f"{api}/community/posts/{official.id}")).status_code == 200
    missing = await client.delete(f"{api}/community/comments/{comment['id']}")
    assert missing.status_code == 404

    await _join(client, api, STUDENT)
    assert (await client.delete(f"{api}/community/posts/{post['id']}")).status_code == 200
    assert (await client.get(f"{api}/community/posts/{post['id']}")).status_code == 404


async def test_deleting_post_removes_its_comments_and_likes(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, STUDENT)
    await _join(client, api, STUDENT)
    post = await _create(client, api)
    await client.put(f"{api}/community/posts/{post['id']}/like")
    await client.post(f"{api}/community/posts/{post['id']}/comments", json={"body": "Сэтгэгдэл"})

    await client.delete(f"{api}/community/posts/{post['id']}")

    for model in (CommunityComment, CommunityPostLike):
        count = (await db.execute(select(func.count()).select_from(model))).scalar_one()
        assert count == 0


async def test_deleting_account_removes_its_posts_comments_and_likes(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, STUDENT)
    leaving = await make_user(db, OTHER)
    official = await _official(db)
    await _join(client, api, STUDENT)
    kept = await _create(client, api)

    await _join(client, api, OTHER)
    await _create(client, api)
    await client.put(f"{api}/community/posts/{kept['id']}/like")
    await client.put(f"{api}/community/posts/{official.id}/like")
    await client.post(f"{api}/community/posts/{kept['id']}/comments", json={"body": "Баяртай"})

    await db.execute(delete(User).where(User.id == leaving.id))
    await db.commit()

    posts = (await db.execute(select(CommunityPost.id))).scalars().all()
    assert sorted(posts) == sorted([uuid.UUID(kept["id"]), official.id])
    for model in (CommunityComment, CommunityPostLike):
        count = (await db.execute(select(func.count()).select_from(model))).scalar_one()
        assert count == 0


async def test_reports_reach_admin_feedback_with_a_copy_of_the_content(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, STUDENT)
    reporter = await make_user(db, OTHER)
    await make_user(db, ADMIN, role=UserRole.ADMIN)
    official = await _official(db)
    await _join(client, api, STUDENT)
    post = await _create(client, api)
    comment = (
        await client.post(
            f"{api}/community/posts/{post['id']}/comments", json={"body": "Муу үг энд байна"}
        )
    ).json()

    await _join(client, api, OTHER)
    reported = await client.post(
        f"{api}/community/posts/{post['id']}/report",
        json={"reason": "spam", "details": "Зар сурталчилгаа"},
    )
    assert reported.status_code == 201, reported.text
    reported = await client.post(
        f"{api}/community/comments/{comment['id']}/report", json={"reason": "abuse"}
    )
    assert reported.status_code == 201, reported.text
    reported = await client.post(
        f"{api}/community/posts/{official.id}/report", json={"reason": "other"}
    )
    assert reported.status_code == 201, reported.text

    invalid = await client.post(
        f"{api}/community/posts/{post['id']}/report", json={"reason": "boring"}
    )
    assert invalid.status_code == 422
    missing = await client.post(
        f"{api}/community/comments/{uuid.uuid4()}/report", json={"reason": "spam"}
    )
    assert missing.status_code == 404

    # Зохиогч устгасан ч гомдол ба агуулгын хуулбар нь үлдэнэ.
    await _join(client, api, STUDENT)
    await client.delete(f"{api}/community/posts/{post['id']}")

    await _join(client, api, ADMIN)
    items = (await client.get(f"{api}/admin/feedback")).json()["items"]
    by_page = {item["page"]: item for item in items}
    assert {item["kind"] for item in items} == {"report"}
    assert {item["user"]["email"] for item in items} == {reporter.email}

    post_report = by_page[f"/community/{post['id']}"]["message"]
    assert "Нийтлэл · Спам" in post_report
    assert "Тайлбар: Зар сурталчилгаа" in post_report
    assert f"«{POST['title']}»" in post_report
    assert "Тоонуудын жагсаалтыг" in post_report

    comment_report = by_page[f"/community/{post['id']}#comment-{comment['id']}"]["message"]
    assert "Сэтгэгдэл · Доромжилсон" in comment_report
    assert "Муу үг энд байна" in comment_report
    assert "Тайлбар" not in comment_report

    assert "Зохиогч: MedlegHub" in by_page[f"/community/{official.id}"]["message"]


async def test_feedback_form_cannot_send_reports(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    await make_user(db, STUDENT)
    await _join(client, api, STUDENT)
    response = await client.post(
        f"{api}/feedback", json={"kind": "report", "message": "Гомдол байна."}
    )
    assert response.status_code == 422


async def test_reports_share_the_feedback_rate_limit(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    await make_user(db, STUDENT)
    await _join(client, api, STUDENT)
    post = await _create(client, api)
    monkeypatch.setattr(settings, "rate_limit_enabled", True)
    monkeypatch.setattr(settings, "feedback_rate_limit_max", 2)
    monkeypatch.setattr("app.core.rate_limit.backend", InMemoryRateLimitBackend())

    report = await client.post(
        f"{api}/community/posts/{post['id']}/report", json={"reason": "spam"}
    )
    feedback = await client.post(
        f"{api}/feedback", json={"kind": "idea", "message": "Шинэ санаа байна."}
    )
    blocked = await client.post(
        f"{api}/community/posts/{post['id']}/report", json={"reason": "spam"}
    )

    assert [report.status_code, feedback.status_code, blocked.status_code] == [201, 201, 429]
    count = (
        await db.execute(
            select(func.count()).select_from(Feedback).where(Feedback.kind == FeedbackKind.REPORT)
        )
    ).scalar_one()
    assert count == 1


async def test_posts_and_comments_are_rate_limited_per_user(
    client: httpx.AsyncClient, api: str, db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "rate_limit_enabled", True)
    monkeypatch.setattr(settings, "community_post_rate_limit_max", 1)
    monkeypatch.setattr(settings, "community_comment_rate_limit_max", 1)
    monkeypatch.setattr("app.core.rate_limit.backend", InMemoryRateLimitBackend())
    await make_user(db, STUDENT)
    await _join(client, api, STUDENT)

    post = await _create(client, api)
    assert (await client.post(f"{api}/community/posts", json=POST)).status_code == 429

    comments_url = f"{api}/community/posts/{post['id']}/comments"
    assert (await client.post(comments_url, json={"body": "1"})).status_code == 201
    assert (await client.post(comments_url, json={"body": "2"})).status_code == 429


async def test_seed_adds_official_posts_once_and_keeps_likes(
    client: httpx.AsyncClient, api: str, db: AsyncSession
) -> None:
    older = OfficialPost(
        id=uuid.uuid4(),
        title="Хуучин",
        body="Эхний нийтлэл",
        language=PostLanguage.PYTHON,
        type=PostType.FUN_FACT,
    )
    newer = OfficialPost(
        id=uuid.uuid4(),
        title="Шинэ",
        body="Хоёр дахь нийтлэл",
        language=PostLanguage.GENERAL,
        type=PostType.DISCUSSION,
    )
    await _sync_official_posts(db, (older, newer))
    await db.commit()

    await make_user(db, STUDENT)
    await _join(client, api, STUDENT)
    await client.put(f"{api}/community/posts/{older.id}/like")

    edited = OfficialPost(
        id=older.id,
        title="Засварласан",
        body="Шинэчилсэн бие",
        language=PostLanguage.C,
        type=PostType.HELP,
        pinned=True,
    )
    await _sync_official_posts(db, (edited, newer))
    await db.commit()

    items = (await client.get(f"{api}/community/posts")).json()["items"]
    assert [item["id"] for item in items] == [str(older.id), str(newer.id)]
    first = items[0]
    assert (first["title"], first["language"], first["type"], first["pinned"]) == (
        "Засварласан",
        "c",
        "help",
        True,
    )
    assert (first["author"], first["like_count"]) == (None, 1)

    created = (await db.execute(select(CommunityPost.created_at))).scalars().all()
    assert len(created) == 2
    assert all(abs(datetime.now(UTC) - at) < timedelta(minutes=1) for at in created)


def test_official_posts_are_valid() -> None:
    assert len({post.id for post in OFFICIAL_POSTS}) == len(OFFICIAL_POSTS)
    assert sum(post.pinned for post in OFFICIAL_POSTS) == 1
    for post in OFFICIAL_POSTS:
        assert 5 <= len(post.title) <= 150
        assert 10 <= len(post.body) <= 10_000


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ("# Гарчиг\n\n**Тод** ба `код`", "Гарчиг Тод ба код"),
        ("Эхлэл\n```c\nint x;\n```\nТөгсгөл", "Эхлэл Төгсгөл"),
        ("Хаагаагүй\n```js\nlet a = 1;", "Хаагаагүй"),
        ("Хэрэглэх `` ``` `` тэмдэгт", "Хэрэглэх тэмдэгт"),
        ("[Холбоос](https://example.com) энд", "Холбоос энд"),
        ("```\nзөвхөн код\n```", ""),
        (
            "Жагсаалт:\n\n- нэг\n* хоёр\n1. гурав\n\n---\n\nТөгсгөл",
            "Жагсаалт: нэг хоёр гурав Төгсгөл",
        ),
        ("-1 ба 2-3", "-1 ба 2-3"),
    ],
)
def test_excerpt_strips_markdown(body: str, expected: str) -> None:
    assert excerpt(body) == expected


def test_excerpt_is_cut_at_a_word() -> None:
    result = excerpt("үг " * 200)
    assert result.endswith("…")
    assert len(result) <= EXCERPT_LENGTH + 1
    assert not result.removesuffix("…").endswith(" ")
