from pathlib import Path


def run_confirmed(input_path: Path, output_path: Path, confirmed: bool) -> None:
    if not confirmed:
        raise PermissionError("A person must confirm this action.")
    temporary = output_path.with_suffix(".tmp")
    temporary.write_text(input_path.read_text(encoding="utf-8"), encoding="utf-8")
    temporary.replace(output_path)
