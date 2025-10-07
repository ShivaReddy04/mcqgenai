import re
import random
from typing import List, Dict, Tuple


STOPWORDS = {
    "the", "and", "for", "that", "with", "have", "this", "from", "your", "you",
    "into", "about", "there", "their", "were", "which", "will", "would", "could",
    "over", "been", "than", "then", "them", "they", "what", "when", "where",
    "how", "why", "here", "also", "such", "some", "more", "most", "much", "many",
    "like", "just", "into", "onto", "upon", "each", "other", "only", "very",
    "these", "those", "because", "between", "within", "without", "under", "above",
    "across", "after", "before", "while", "during", "against", "among", "per",
    "can", "may", "might", "should", "must", "shall", "is", "am", "are", "was",
    "be", "being", "been", "of", "in", "on", "at", "to", "by", "as", "an", "a",
    "it", "its", "we", "our", "us", "he", "she", "him", "her", "his", "hers",
    "do", "does", "did", "done", "not", "no", "nor", "or", "if", "so", "but"
}


def _split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in parts if s.strip()]


def _tokenize(text: str) -> List[str]:
    # Basic word tokenizer; keep alphabetic tokens of length >= 4
    return re.findall(r"[A-Za-z][A-Za-z\-]{3,}", text)


def _normalize(word: str) -> str:
    return word.lower()


def _keyword_candidates(text: str) -> List[str]:
    tokens = _tokenize(text)
    counts: Dict[str, int] = {}
    for t in tokens:
        n = _normalize(t)
        if n in STOPWORDS:
            continue
        counts[n] = counts.get(n, 0) + 1
    # Sort by frequency then by length (bias to content words)
    ranked = sorted(counts.items(), key=lambda kv: (kv[1], len(kv[0])), reverse=True)
    return [w for w, _ in ranked]


def _find_sentence_containing(sentences: List[str], word: str) -> str:
    pattern = re.compile(rf"\b{re.escape(word)}\b", flags=re.IGNORECASE)
    for s in sentences:
        if pattern.search(s):
            return s
    return sentences[0] if sentences else ""


def _make_cloze(sentence: str, answer: str) -> str:
    pattern = re.compile(rf"\b{re.escape(answer)}\b", flags=re.IGNORECASE)
    return pattern.sub("____", sentence, count=1)


def _select_distractors(answers_pool: List[str], correct: str, k: int, rng: random.Random) -> List[str]:
    candidates = [w for w in answers_pool if w != correct]
    # Prefer similar length words
    candidates.sort(key=lambda w: abs(len(w) - len(correct)))
    unique: List[str] = []
    for w in candidates:
        lw = w.lower()
        if lw == correct.lower() or lw in unique:
            continue
        unique.append(lw)
        if len(unique) >= max(k * 3, k):
            break
    rng.shuffle(unique)
    return [w for w in unique[:k]]


def generate_mcqs(text: str, num_questions: int = 5, num_choices: int = 4, seed: int = 42) -> List[Dict[str, object]]:
    if not text or not text.strip():
        return []
    if num_choices < 2:
        num_choices = 2

    rng = random.Random(seed)
    sentences = _split_sentences(text)
    keywords = _keyword_candidates(text)
    if not keywords:
        return []

    # Use top keywords but avoid duplicates by sentence
    selected: List[str] = []
    seen: set = set()
    for kw in keywords:
        sent = _find_sentence_containing(sentences, kw)
        key = (sent, kw)
        if key in seen:
            continue
        seen.add(key)
        selected.append(kw)
        if len(selected) >= num_questions:
            break

    result: List[Dict[str, object]] = []
    for ans in selected:
        sent = _find_sentence_containing(sentences, ans)
        question = _make_cloze(sent, ans)
        distractors_needed = max(0, num_choices - 1)
        distractors = _select_distractors(keywords, ans, distractors_needed, rng)
        options = [ans] + distractors
        rng.shuffle(options)
        correct_index = options.index(ans)
        result.append({
            "question": question,
            "options": options,
            "answer_index": correct_index
        })

    return result


