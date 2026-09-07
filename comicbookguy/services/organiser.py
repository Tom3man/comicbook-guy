import logging
import shutil
from pathlib import Path

from comicbookguy.services.metadata_lookup import extract_metadata
from comicbookguy.utils.utils import organise_comic

log = logging.getLogger(__name__)


def restructure_file(
    destination_path: Path,
    input_filepath: Path,
) -> Path | None:
    """Organise a comic using extracted metadata.

    The function is defensive: on any failure it logs and returns None,
    leaving the original file in place so a watcher can retry later.
    """

    try:
        # Extract metadata
        comic = extract_metadata(input_filepath)
        log.info("Metadata: %s", comic)

        # Build destination structure
        output_folder, filename = organise_comic(comic)

        destination_folder = destination_path / output_folder

        log.debug("Destination: %s", destination_folder)

        # Don't overwrite an existing comic
        if destination_folder.exists():
            log.warning("Destination already exists: %s", destination_folder)
            return None

        # Ensure destination directory exists
        destination_folder.mkdir(parents=True, exist_ok=True)

        # Final destination filepath
        dest_file = destination_folder / filename

        if dest_file.exists():
            log.warning("Destination file already exists: %s", dest_file)
            return None

        # Move file
        shutil.move(str(input_filepath), str(dest_file))

        log.info("Moved %s -> %s", input_filepath, dest_file)

        return dest_file

    except Exception:
        log.exception("Failed to restructure file: %s", input_filepath)
        return None
