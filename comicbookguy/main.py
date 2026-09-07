import logging
import time

from watchdog.observers import Observer

from comicbookguy.config import settings
from comicbookguy.services.handlers import ComicbookHandler


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    logger = logging.getLogger(__name__)

    handler = ComicbookHandler(
        inbox=settings.comicbooks_inbox,
        library=settings.comicbooks_library,
    )

    observer = Observer()

    observer.schedule(
        handler,
        str(settings.comicbooks_inbox),
        recursive=False,
    )

    observer.start()

    logger.info(
        "Watching comicbook inbox: %s",
        settings.comicbooks_inbox,
    )

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Stopping watcher...")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
