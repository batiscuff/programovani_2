import json
from pathlib import Path
from utils import load_file, remove_punctuation, save_file


fname = "bag_of_words_lesson5.json"
current_dir = Path.cwd()
files_dir = current_dir / "files_lesson5"  # programovani_2/files_lesson5
files = list(files_dir.glob("*.txt"))  # seznam všech souborů .txt ve složce
output_file = str(current_dir / fname)


def load_all_txt_files() -> list:
    texts = []
    for _file in files:
        text = load_file(str(_file))  # protože _file je Path objekt
        texts.append(text)
    return texts


def clean_text(text: str) -> list:
    text = remove_punctuation(text)
    clean_text = text.replace("\n", "")
    text_list = clean_text.lower().split()
    return text_list


def create_tokens_set(cleaned_texts: list) -> set:
    tokens = set()
    for text in cleaned_texts:
        filtered_text = set(text)  # filtruju při pomoci setu
        tokens.update(filtered_text)
    return sorted(tokens)


def get_cleaned_texts() -> list:
    texts = load_all_txt_files()

    cleaned_texts_list = []
    for text in texts:
        cleaned_text = clean_text(text)
        cleaned_texts_list.append(cleaned_text)
    return cleaned_texts_list


def vectorize(cleaned_texts: list, global_vocabulary: set) -> list:
    vectors = []
    for text in cleaned_texts:
        sent_vec = []
        for token in global_vocabulary:
            sent_vec.append(1 if token in text else 0)
        vectors.append(sent_vec)
    return vectors


def save_result(vectorized_list: list, global_vocabulary: set, texts: list):
    result = [
        {"Vectors": vectorized_list},
        {"Global Vocabulary": global_vocabulary},
        {"Texts": texts}
    ]

    with open(output_file, "w+", encoding="utf-8") as of:
        json.dump(result, of, ensure_ascii=False,)


def folder_to_bow():
    cleaned_texts = get_cleaned_texts()
    print(f"Počet nahraných souborů: {len(cleaned_texts)}",
          f"Texty jsou načtené a zpracované!", sep="\n")
    global_vocabulary = create_tokens_set(cleaned_texts)
    print(f"Globální slovník byl vytvořen!",
          f"Počet tokenů ve slovníku: {len(global_vocabulary)}", sep="\n")
    vectorized = vectorize(cleaned_texts, global_vocabulary)
    save_result(vectorized, global_vocabulary, cleaned_texts)
    print(f"Data byla uložena do souboru {fname}")


if __name__ == "__main__":
    folder_to_bow()
