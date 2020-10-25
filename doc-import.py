import typer


def main(file: str):
    typer.echo(f"Pretending to read {file}")


if __name__ == "__main__":
    typer.run(main)
