#!/usr/bin/env python3
#  Base declaration for network scan parsing 
#
#
##########################################################################

import argparse
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class WordlistEntry(Base):
    __tablename__ = 'wordlist'
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    count = Column(Integer, default=1)

class Sorter:
    def __init__(self, db_url=None):
        self.db_url = db_url
        if db_url:
            self.engine = create_engine(db_url)
            self.Session = sessionmaker(bind=self.engine)
            Base.metadata.create_all(self.engine)

    # --- Sortieralgorithmen ---
    def bubble_sort(self, data):
        n = len(data)
        for i in range(n):
            already_sorted = True
            for j in range(n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    already_sorted = False
            if already_sorted:
                break
        return data

    def quicksort(self, array):
        if len(array) < 2:
            return array
        pivot = array[0]
        low = [x for x in array[1:] if x < pivot]
        high = [x for x in array[1:] if x >= pivot]
        return self.quicksort(low) + [pivot] + self.quicksort(high)

    def timsort(self, data):
        data.sort()
        return data

    # --- Duplikate entfernen ---
    def remove_duplicates(self, data):
        seen = set()
        result = []
        for item in data:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    # --- Flexible Sortierung ---
    def sort_data(self, data, algorithm='timsort', key=None, reverse=False):
        if key:
            data = [(item, key(item)) for item in data]
            if algorithm == 'bubble':
                data = self.bubble_sort(data)
            elif algorithm == 'quicksort':
                data = self.quicksort(data)
            else:
                data.sort(key=lambda x: x[1], reverse=reverse)
            data = [item[0] for item in data]
        else:
            if algorithm == 'bubble':
                data = self.bubble_sort(data)
            elif algorithm == 'quicksort':
                data = self.quicksort(data)
            else:
                data = self.timsort(data)
            if reverse:
                data = list(reversed(data))
        return data

    # --- Dateioperationen ---
    def load_file(self, filename):
        lines = []
        with open(filename, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line)
        return lines

    def save_file(self, filename, lines):
        with open(filename, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(f"{line}\n")

    # --- CLI-Workflow ---
    def cli_sort(self, infile, outfile, algorithm='timsort', remove_dupes=True, sort_by_length=False, reverse=False):
        try:
            lines = self.load_file(infile)
            if remove_dupes:
                lines = self.remove_duplicates(lines)
            if sort_by_length:
                lines = self.sort_data(lines, algorithm, key=len, reverse=reverse)
            else:
                lines = self.sort_data(lines, algorithm, reverse=reverse)
            self.save_file(outfile, lines)
            print(f"Datei {infile} wurde sortiert und als {outfile} gespeichert.")
        except Exception as e:
            print(f"Fehler: {e}")

    # --- DB-Integration (SQLAlchemy) ---
    def fetch_wordlist(self):
        session = self.Session()
        try:
            entries = session.query(WordlistEntry).all()
            clean_entries = []
            for e in entries:
                try:
                    word = str(e.word).strip()
                    count = int(e.count)
                    if word:
                        clean_entries.append((word, count))
                except Exception as ex:
                    print(f"WARNUNG: Fehler beim Umwandeln von {e}: {ex}")
            return clean_entries
        except SQLAlchemyError as err:
            print(f"DB-Fehler: {err}")
            return []
        finally:
            session.close()

    def save_wordlist(self, wordlist):
        session = self.Session()
        try:
            session.query(WordlistEntry).delete()
            for idx, (word, count) in enumerate(wordlist):
                session.add(WordlistEntry(id=idx+1, word=word, count=count))
            session.commit()
        except SQLAlchemyError as err:
            print(f"DB-Fehler beim Speichern: {err}")
        finally:
            session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flexible Sortier- und Wordlist-Utility")
    parser.add_argument("infile", help="Eingabedatei (Wordlist/Textdatei)")
    parser.add_argument("outfile", help="Ausgabedatei")
    parser.add_argument("--algorithm", choices=["timsort", "quicksort", "bubble"], default="timsort",
                        help="Sortieralgorithmus")
    parser.add_argument("--no-dupes", action="store_true", help="Duplikate nicht entfernen")
    parser.add_argument("--by-length", action="store_true", help="Nach Wortlänge sortieren")
    parser.add_argument("--reverse", action="store_true", help="Absteigend sortieren")
    args = parser.parse_args()

    sorter = Sorter()
    sorter.cli_sort(
        infile=args.infile,
        outfile=args.outfile,
        algorithm=args.algorithm,
        remove_dupes=not args.no_dupes,
        sort_by_length=args.by_length,
        reverse=args.reverse
    )
