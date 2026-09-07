import re
from pathlib import Path
from typing import Any

from comicbox.box import Comicbox

from comicbookguy.models import ComicMetadata


def get_dict(
    data: dict[str, Any],
    key: str,
) -> dict[str, Any]:
    value = data.get(key)

    if isinstance(value, dict):
        return value

    return {}


def get_str(
    data: dict[str, Any],
    key: str,
) -> str | None:
    value = data.get(key)

    if isinstance(value, str):
        return value

    return None


def get_int(
    data: dict[str, Any],
    key: str,
) -> int | None:
    value = data.get(key)

    if isinstance(value, int):
        return value

    return None


def extract_volume(filename: str) -> int | None:

    VOLUME_PATTERN = re.compile(
        r"[_\s-]+vol[_\s.-]*(\d+)",
        re.IGNORECASE,
    )

    match = VOLUME_PATTERN.search(filename)

    if match:
        return int(match.group(1))

    return None


def format_issue(issue: str) -> str:
    try:
        return f"{int(issue):03d}"
    except ValueError:
        return issue


def extract_metadata(file_path: Path) -> ComicMetadata:

    with Comicbox(file_path) as cb:
        raw_metadata = cb.to_dict()

    metadata = get_dict(raw_metadata, "comicbox")

    series = get_dict(metadata, "series")
    issue = get_dict(metadata, "issue")
    date = get_dict(metadata, "date")

    volume = extract_volume(file_path.stem)

    # ComicBox sometimes interprets "vol_01" as issue "01".
    # If the filename explicitly says volume, don't treat it as an issue.
    if volume is not None:
        issue_number = None
    else:
        issue_number = get_str(issue, "name")
        if issue_number is not None:
            issue_number = format_issue(issue=issue_number)

    return ComicMetadata(
        series=get_str(series, "name"),
        issue=issue_number,
        volume=volume,
        year=get_int(date, "year"),
        month=get_int(date, "month"),
        day=get_int(date, "day"),
        page_count=get_int(metadata, "page_count"),
        format=get_str(
            metadata,
            "original_format",
        ),
        scan_information=get_str(
            metadata,
            "scan_info",
        ),
        extension=file_path.suffix.lstrip(".").lower(),
    )
