from subprocess import Popen, PIPE
import logging


def find_invalid_words(words: set[str]):
    invalid_words = set()
    while True:
        inp = "\n".join(words - invalid_words).encode()
        p = Popen(
            [
                "./tree-tagger",
                "-quiet",
                "-no-unknown",
                "-sgml",
                "-token",
                "-lemma",
                "slovenian-utf8.par",
            ],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
        )
        p.stdin.write(inp)
        p.stdin.close()
        p.wait()
        error_line = p.stderr.read().decode()
        if error_line:
            invalid_word = error_line.split('"')[1]
            logging.warning("Problematic word: %s", invalid_word)
            invalid_words.add(error_line.split('"')[1])
            continue

        return invalid_words


print(find_invalid_words(set(["kruh", "hkeik", "blsh", "mati"])))