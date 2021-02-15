from subprocess import Popen, PIPE
from itertools import islice
import logging
import re


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def find_invalid_words(words: set[str]):
    print(f"Words to prcess: {len(words)}")
    invalid_words = set()
    sorted_words = sorted(words)
    batch_size = 1000  # 59984 // 90
    for i, sorted_batches in enumerate(chunks(sorted_words, batch_size)):
        print(f"Batch {i} of {len(sorted_words)//batch_size}")
        while True:
            batch = set(sorted_batches) - invalid_words
            inp = "\n".join(batch).encode()
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
            else:
                # Write to rules.csv after each batch
                with open("rules.csv", "w") as f:
                    for invalid_word in sorted(invalid_words):
                        f.write(f"{invalid_word},\n")
                break

    return invalid_words


def load_file(filename, encoding="utf-8"):
    with open(filename, encoding=encoding) as f:
        # print(f"Loading {filename}")
        for word in re.findall(r"\w+", f.read()):
            yield word.lower()


def load_files(mini=False):
    utf_16_le_files = """GORENJE LP 2006.txt
GORENJE LP 2007.txt
GORENJE LP 2008.txt
GORENJE LP 2009.txt
GORENJE LP 2010.txt
GORENJE LP 2011.txt
GORENJE LP 2012.txt
GORENJE LP 2013.txt
GORENJE LP 2014.txt
GORENJE LP 2015.txt""".splitlines()

    files = """INTEREUROPA LP 2006.txt
INTEREUROPA LP 2007.txt
INTEREUROPA LP 2008.txt
INTEREUROPA LP 2009.txt
INTEREUROPA LP 2010.txt
INTEREUROPA LP 2011.txt
INTEREUROPA LP 2012.txt
INTEREUROPA LP 2013.txt
INTEREUROPA LP 2014.txt
INTEREUROPA LP 2015.txt
KRKA LP 2006.txt
KRKA LP 2007.txt
KRKA LP 2008.txt
KRKA LP 2009.txt
KRKA LP 2010 .txt
KRKA LP 2011.txt
KRKA LP 2012.txt
KRKA LP 2013.txt
KRKA LP 2014.txt
KRKA LP 2015 .txt
LUKA KOPER LP 2006.txt
LUKA KOPER LP 2007.txt
LUKA KOPER LP 2008.txt
LUKA KOPER LP 2009.txt
LUKA KOPER LP 2010.txt
LUKA KOPER LP 2011.txt
LUKA KOPER LP 2012.txt
LUKA KOPER LP 2013.txt
LUKA KOPER LP 2014.txt
LUKA KOPER LP 2015.txt
MERCATOR LP 2006.txt
MERCATOR LP 2007.txt
MERCATOR LP 2008.txt
MERCATOR LP 2009.txt
MERCATOR LP 2010.txt
MERCATOR LP 2011.txt
MERCATOR LP 2012.txt
MERCATOR LP 2013.txt
MERCATOR LP 2014.txt
MERCATOR LP 2015.txt
PETROL LP 2006.txt
PETROL LP 2007.txt
PETROL LP 2008.txt
PETROL LP 2009.txt
PETROL LP 2010.txt
PETROL LP 2011.txt
PETROL LP 2012.txt
PETROL LP 2013.txt
PETROL LP 2014.txt
PETROL LP 2015.txt
POZAVAROVALNICA SAVA LP 2006.txt
POZAVAROVALNICA SAVA LP 2007.txt
POZAVAROVALNICA SAVA LP 2008.txt
POZAVAROVALNICA SAVA LP 2009.txt
POZAVAROVALNICA SAVA LP 2010.txt
POZAVAROVALNICA SAVA LP 2011.txt
POZAVAROVALNICA SAVA LP 2012.txt
POZAVAROVALNICA SAVA LP 2013.txt
POZAVAROVALNICA SAVA LP 2014.txt
POZAVAROVALNICA SAVA LP 2015.txt
TELEKOM LP 2006.txt
TELEKOM LP 2007.txt
TELEKOM LP 2008.txt
TELEKOM LP 2009.txt
TELEKOM LP 2010.txt
TELEKOM LP 2011.txt
TELEKOM LP 2012.txt
TELEKOM LP 2013.txt
TELEKOM LP 2014.txt
TELEKOM LP 2015.txt
ZAVAROVALNICA TRIGLAV LP 2006.txt
ZAVAROVALNICA TRIGLAV LP 2007.txt
ZAVAROVALNICA TRIGLAV LP 2008.txt
ZAVAROVALNICA TRIGLAV LP 2009.txt
ZAVAROVALNICA TRIGLAV LP 2010.txt
ZAVAROVALNICA TRIGLAV LP 2011.txt
ZAVAROVALNICA TRIGLAV LP 2012.txt
ZAVAROVALNICA TRIGLAV LP 2013.txt
ZAVAROVALNICA TRIGLAV LP 2014.txt
ZAVAROVALNICA TRIGLAV LP 2015.txt""".splitlines()

    for filename in utf_16_le_files:
        yield from load_file(filename, encoding="utf-16-le")

    for filename in files:
        yield from load_file(filename)


find_invalid_words(set(load_files()))
