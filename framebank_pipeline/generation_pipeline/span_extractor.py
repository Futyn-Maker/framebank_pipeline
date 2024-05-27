from typing import List, Tuple
import stanza

class SpanExtractor:
    skipped_pos = {"CCONJ", "SCONJ"}
    allowed_punct = {"\"", "'", "(", ")", "."}

    def __init__(self, lang: str = "ru", package: str = "syntagrus"):
        self.nlp = stanza.Pipeline(lang, package=package, processors='tokenize,pos,lemma,depparse')

    def __call__(self, text: str) -> str:
        doc = self.nlp(text)
        spans = []

        for sentence in doc.sentences:
            for token in sentence.tokens:
                word = token.words[0]
                if word.upos in {"NOUN", "PROPN", "PRON"}:
                    span = self._extract_span(word, sentence)
                    if span:
                        spans.append(span)
                elif word.deprel == "root":
                    span = self._extract_predicate_span(word, sentence)
                    if span:
                        spans.append(span)
                elif word.deprel in {"xcomp", "ccomp", "csubj", "conj"}:
                    clause_spans = self._extract_clause_span(word, sentence)
                    if clause_spans:
                        spans.extend(clause_spans)

        # Remove nested spans
        spans = self._merge_overlapping_spans(spans)

        # Sort spans by their start index
        spans = sorted(spans, key=lambda x: x[0])

        # Insert brackets into the text
        result_text = self._insert_brackets(text, spans)
        return result_text

    def _extract_span(self, word: stanza.models.common.doc.Word, sentence: stanza.models.common.doc.Sentence) -> Tuple[int, int]:
        start, end = word.start_char, word.end_char
        for token in reversed(sentence.tokens[:word.id-1]):
            prev_word = token.words[0]
            if not self._is_ancestor(sentence, word, prev_word) or self._is_skipped_pos(prev_word):
                break
            if prev_word.start_char < start:
                start = prev_word.start_char
        for token in sentence.tokens[word.id:]:
            next_word = token.words[0]
            if not self._is_ancestor(sentence, word, next_word) or self._is_skipped_pos(next_word):
                break
            if next_word.end_char > end:
                end = next_word.end_char

        # Handle conjunctions to extend the span
        conjunction_span = self._extend_with_conjunctions(sentence, word, start, end)
        return conjunction_span

    def _extend_with_conjunctions(self, sentence: stanza.models.common.doc.Sentence, word: stanza.models.common.doc.Word, start: int, end: int) -> Tuple[int, int]:
        for child in sentence.words:
            if child.head == word.id and child.deprel in {"conj", "cc"}:
                conj_start, conj_end = child.start_char, child.end_char
                if conj_start < start:
                    start = conj_start
                if conj_end > end:
                    end = conj_end
                # Recursively extend the span for conjunction children
                start, end = self._extend_with_conjunctions(sentence, child, start, end)
        return start, end

    def _extract_predicate_span(self, word: stanza.models.common.doc.Word, sentence: stanza.models.common.doc.Sentence) -> Tuple[int, int]:
        start, end = word.start_char, word.end_char
        for child in sentence.words:
            if child.head == word.id and child.deprel.startswith("aux"):
                if child.start_char < start:
                    start = child.start_char
                if child.end_char > end:
                    end = child.end_char
        return (start, end)

    def _extract_clause_span(self, word: stanza.models.common.doc.Word, sentence: stanza.models.common.doc.Sentence) -> List[Tuple[int, int]]:
        spans = []
        start, end = word.start_char, word.end_char
        predicate_span = self._extract_predicate_span(word, sentence)
        spans.append(predicate_span)

        # Extend the span to include dependents for xcomp and other relations
        if word.deprel == "xcomp":
            for token in sentence.tokens[word.id:]:
                next_word = token.words[0]
                if not self._is_ancestor(sentence, word, next_word):
                    break
                if next_word.end_char > end:
                    end = next_word.end_char
            spans[-1] = (start, end)

        for child in sentence.words:
            if child.head == word.id and child.deprel in {"ccomp", "xcomp", "csubj", "conj"}:
                sub_span = self._extract_span(child, sentence)
                if sub_span:
                    spans.append(sub_span)
                if child.deprel in {"ccomp", "conj"}:
                    predicate_span = self._extract_predicate_span(child, sentence)
                    if predicate_span:
                        spans.append(predicate_span)

        # Merge spans related to this clause
        merged_spans = self._merge_overlapping_spans(spans)
        return merged_spans

    def _merge_overlapping_spans(self, spans: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        if not spans:
            return spans

        # Sort spans by their start index
        spans.sort()

        merged_spans = [spans[0]]
        for current in spans[1:]:
            prev_start, prev_end = merged_spans[-1]
            current_start, current_end = current

            if current_start <= prev_end:  # Overlapping spans
                merged_spans[-1] = (prev_start, max(prev_end, current_end))
            else:
                merged_spans.append(current)

        return merged_spans

    def _insert_brackets(self, text: str, spans: List[Tuple[int, int]]) -> str:
        offset = 0
        for start, end in spans:
            text = text[:start + offset] + "[" + text[start + offset:end + offset] + "]" + text[end + offset:]
            offset += 2  # Adding two characters for the brackets
        return text

    @staticmethod
    def _is_ancestor(sentence: stanza.models.common.doc.Sentence, ancestor: stanza.models.common.doc.Word, descendant: stanza.models.common.doc.Word) -> bool:
        while descendant.head != 0:
            if descendant.head == ancestor.id:
                return True
            descendant = sentence.words[descendant.head - 1]
        return False

    @staticmethod
    def _is_skipped_pos(word: stanza.models.common.doc.Word) -> bool:
        return word.upos in SpanExtractor.skipped_pos or (word.upos == "PUNCT" and word.text not in SpanExtractor.allowed_punct)
