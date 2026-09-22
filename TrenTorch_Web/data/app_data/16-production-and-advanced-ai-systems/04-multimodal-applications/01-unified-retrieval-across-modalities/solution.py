def retrieve_across_modalities(
    chunks: list[tuple[str, str, str]], query_keywords: list[str]
) -> list[str]:
    lowered_keywords = [keyword.lower() for keyword in query_keywords]
    scored = []
    for index, (chunk_id, _modality, text) in enumerate(chunks):
        lowered_text = text.lower()
        score = sum(1 for keyword in lowered_keywords if keyword in lowered_text)
        if score > 0:
            scored.append((score, index, chunk_id))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [chunk_id for _score, _index, chunk_id in scored]
