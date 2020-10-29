"""
Main module of the document importer.
"""

from pathlib import Path
from typing import Optional

import pdftitle
import pydantic
import typer
from PyPDF2.pdf import PdfFileReader


class Metadata(pydantic.BaseModel):
    """
    Metadata for documents.
    """
    title: str
    author: Optional[str] = None
    page_count: Optional[int] = None


def main(file: Path):
    """Reads a PDF file and prints its metadata to STDOUT as JSON."""
    typer.echo(f"Reading {file}", err=True)
    data = metadata(file)
    typer.echo(data.json())


def metadata(path: Path) -> Metadata:
    """
    Reads a given PDF file and produces a Metadata object.

    :param path: path to a PDF file
    :return: the metadata extracted from the PDF file
    """
    with path.open('rb') as f:
        reader = PdfFileReader(f)
        info = reader.getDocumentInfo()
        page_count = reader.getNumPages()

    typer.echo(info, err=True)

    title = info.title
    if title is None:
        title = pdftitle.get_title_from_file(str(path))

        if title is None:
            title = path.name

    return Metadata(
        title=title,
        author=info.author,
        page_count=page_count
    )


if __name__ == "__main__":
    typer.run(main)
