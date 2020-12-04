#!/usr/bin/env python

"""
Main module of the document importer.
"""
from collections import Counter
from pathlib import Path
from typing import Optional, List

import pdftitle
import pydantic
import spacy
import typer
from PyPDF2.pdf import PdfFileReader
from pdfminer.high_level import extract_text
from spacy import displacy

nlp = spacy.load("en_core_web_sm")


class Mention(pydantic.BaseModel):
    """
    A mentioned entity with a count.
    """
    name: str
    count: int


class Mentions(pydantic.BaseModel):
    """
    Collection of mentioned entities.
    """
    organizations: List[Mention] = []
    countries: List[Mention] = []


class Metadata(pydantic.BaseModel):
    """
    Metadata for documents.
    """
    title: str
    author: Optional[str] = None
    page_count: Optional[int] = None
    mentions: Optional[Mentions] = None


def main(file: Path, serve_ner: bool = typer.Option(False, help="Open a web server visualising named entities")):
    """Reads a PDF file and prints its metadata to STDOUT as JSON."""
    typer.echo(f'Processing "{file}"', err=True)
    data = metadata(file)
    data = process_text(file, data, serve_ner=serve_ner)
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

    typer.echo(f'PDF metadata: {info}', err=True)

    # Decide which possible title to use:
    # - the title annotated in the PDF metadata
    # - the title read by pdftitle (largest text on the first page)
    # - the file name without extension
    pdftitle_title = pdftitle.get_title_from_file(str(path))
    typer.echo(f'Title according to pdftitle: {pdftitle_title}', err=True)

    title_candidates = [t for t in [info.title, pdftitle_title, path.stem] if t is not None]

    # The current heuristic is just to use the longest of the three candidates
    title = max(title_candidates, key=len)

    return Metadata(
        title=title,
        author=info.author,
        page_count=page_count
    )


def process_text(file: Path, data: Metadata, serve_ner: bool = False) -> Metadata:
    typer.echo('Extracting the document’s full text', err=True)
    with file.open('rb') as f:
        text = extract_text(f)

    typer.echo('Analyzing the full text with spaCy', err=True)
    doc = nlp(text)
    if serve_ner:
        displacy.serve(doc, style="ent")

    organizations = collect_ner_mentions(doc, 'ORG')
    countries = collect_ner_mentions(doc, 'GPE')

    typer.echo('Organizations mentioned at least twice: ' + ', '.join(x.name for x in organizations if x.count > 1), err=True)
    typer.echo('Countries mentioned at least twice: ' + ', '.join(x.name for x in countries if x.count > 1), err=True)

    data.mentions = Mentions(organizations=organizations, countries=countries)

    return data


def collect_ner_mentions(doc, tag: str) -> List[Mention]:
    texts = (ent.text.strip() for ent in doc.ents if ent.label_ == tag)
    counter = Counter(texts)
    mentions = [Mention(name=name, count=count) for name, count in counter.items()]
    mentions.sort(key=lambda x: x.count, reverse=True)
    return mentions


if __name__ == "__main__":
    typer.run(main)
