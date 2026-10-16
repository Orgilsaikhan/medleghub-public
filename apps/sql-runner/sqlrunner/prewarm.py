"""Image бүтээх үед цэвэр datadir загвар бэлдэнэ.

    python3 -m sqlrunner.prewarm

1. `mysqld --initialize-insecure` — хоосон сервер (~2 сек, ARM дээр удаан)
2. `reset()` — `student` данс, жишээ сангууд (`delguur`, `nomiin_san`,
   `medleg_hot`), шалгалт
3. Зөв унтрааж, datadir-ийг `SQLRUNNER_TEMPLATE_DIR`-д үлдээнэ

Runtime-д slot бүр энэ загварыг tmpfs руу хуулж эхэлнэ. `--initialize` дахин
хийхгүй тул контейнер хурдан бэлэн болно. Аль нэг алхам амжилтгүй бол build
зогсоно.
"""

import shutil
import tempfile
from pathlib import Path

from sqlrunner.mysqld import MysqlInstance
from sqlrunner.settings import settings


def build_template(template_dir: Path) -> None:
    shutil.rmtree(template_dir, ignore_errors=True)
    template_dir.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="sqlrunner-prewarm-") as work:
        instance = MysqlInstance(0, base=Path(work), datadir=template_dir)
        instance.initialize()
        instance.launch()
        try:
            instance.reset()
        except BaseException:
            instance.kill()
            raise
        instance.shutdown()


def main() -> None:
    build_template(settings.template_dir)
    print(f"SQL sandbox загвар бэлэн: {settings.template_dir}")


if __name__ == "__main__":
    main()
