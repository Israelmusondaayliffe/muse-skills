# Executable examples

Use this reference whenever a guide contains code, commands, or a script the reader is meant to run. The reader will copy the example into a real folder that may already hold files they care about. The example must be safe there, it must do exactly what the guide says, and the guide must show exactly what ran.

## Rules for the example itself

1. **Work-folder interface.** The example takes its work folder as its last command-line argument. With no argument it creates its own unique folder, for example `tempfile.mkdtemp(prefix="topic-demo-")`, and prints the folder path. With an argument it works only inside that folder. It never uses a fixed folder name such as `demo` or `scratch` and never writes into the reader's current folder. This interface is what lets a checker put pre-existing files and bad input where the example will actually meet them.
2. **No overwrites during setup.** Create sample files with exclusive creation (`open(path, "x")`). If the reader's own input already exists in the work folder, read it; never replace it.
3. **No overwrites in outputs.** Write outputs with exclusive creation, or check that the path is free first. If the name is taken, stop with a message that names the file.
4. **Recovery steps obey the same guard.** An undo, restore, or rename-back step checks its own destination before acting, and runs only when the step it undoes actually happened. A recovery step that runs unconditionally is a defect.
5. **Report what the text promises.** If the guide says bad rows, skipped items, or refusals are reported, the code prints them to stdout or stderr with enough detail to find them (the item and the reason). Collecting items in a list without printing them is not reporting.
6. **Stop messages tell the truth.** "Nothing was overwritten" appears only on paths where nothing was written.

## Rules for the guide text

1. **Display the exact executed code.** The code block in the guide is the file you ran, byte for byte. Edit the file, re-run it, then paste it again. Never tidy the displayed code after the run.
2. **Show the actual output** of that run as the expected result, including stderr lines the guide mentions.
3. **Teach the failure cases the example exercises**: what the reader sees on a name collision and on malformed input, and what to do next.
4. **Label run status honestly.** "Ran on <date>" only when you ran the displayed code. Otherwise say "not run".

## Checks before calling the guide usable

`scripts/check_guide_example.py` is not a sandbox. The example runs with your permissions and could write anywhere. Read the example first, and do not run it if it touches paths outside its work folder. The helper only observes the fresh work folder it creates for each run, so its results prove nothing about files elsewhere. Say that in the status note.

Run it from this skill's folder, once per case:

| Case | Command shape | What must hold |
|---|---|---|
| Normal | `python3 scripts/check_guide_example.py example.py --guide guide.md --workdir-arg --expect-output "<line the guide shows>"` | `valid: true`; displayed code matches; output matches |
| Collision | add `--collide`, plus `--collide-at <name>` for every name the example uses only in passing (a rename or move destination, a temporary file), and `--expect-exit N` if the example should refuse | `collision_exercised: true` and `no_overwrite: true` |
| Malformed input | add `--seed <input-name>=@<bad-file>` (or `=<text>` with `\n` for new lines) and `--expect-output "<the report line naming the bad item>"` | the bad item is reported; `no_overwrite: true` (the input file is unchanged) |

How the collision case works: a probe run records the files the example leaves in its work folder, then the checked run starts with sentinel files at exactly those paths plus every `--collide-at` name. A probe cannot see a file that the example creates and later renames or deletes, which is why destinations need `--collide-at`. If nothing was planted, `collision_exercised` is false and the case fails. A sentinel at a name the example never uses proves nothing, so do not add unrelated names.

If an example cannot take a work folder (a one-line shell command, for instance), the helper can check only the normal case. Such an example must demonstrate its own collision and malformed cases in the displayed code and print their results, checked with `--expect-output`. Label the check "self-reported cases only" in the status note.

Record each JSON report and the script SHA-256 in the working folder. If a case cannot apply (an example with no input has no malformed case), say so in the status note instead of skipping it silently.

When a check fails, fix the example, re-run every case, and paste the new code into the guide. One repair pass is allowed. If a case still fails, deliver the guide with that example marked "not safe to run as shown", say what failed, and do not call it usable.

## Short worked example (illustrative)

Task: a guide to removing empty lines from a text file.

- Wrong: the example writes `input.txt` in the current folder, writes `output.txt` over any existing file, and the text says undecodable lines are reported while the code only counts them.
- Right: the example reads `work = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp(prefix="blank-lines-"))`. It creates `work / "input.txt"` with `"x"` only when that file is absent, and writes `work / "output.txt"` with `"x"`, stopping with a named message if the file exists. It prints each undecodable line number to stderr and prints `work`.
- Checks run: normal case with `--workdir-arg`; collision with `--collide` (the probe finds `input.txt` and `output.txt`, so sentinels go exactly there, and the example must stop without changing either); malformed input with `--seed input.txt=@bad-bytes.txt --expect-output "line 3"`. When all three are valid, the guide displays the exact file and the real output.
