import re
from pathlib import Path

from comicbookguy.models import ComicMetadata


def organise_comic(comic: ComicMetadata) -> tuple[Path, str]:
    """Organise a comic into a folder structure."""

    if not comic.series:
        raise ValueError("Cannot organise comic without a series name")

    series = comic.series

    # Normalise series names such as "Dark Ages (2021-)"
    series = re.sub(r"\s*\(\d{4}-?\)$", "", series).strip()

    path = Path(series)

    if comic.volume is not None:
        path /= f"Volume {comic.volume:02d}"

    filename = series

    if comic.issue:
        filename += f" #{comic.issue}"

    if comic.year:
        filename += f" ({comic.year})"

    if comic.extension:
        filename += f".{comic.extension.lstrip('.')}"

    return (path, filename)
