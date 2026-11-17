def simulate_self_play(
    agent_a_moves: list[str], agent_b_moves: list[str], max_turns: int
) -> list[tuple[str, str]]:
    transcript = []
    for turn in range(max_turns):
        is_agent_a = turn % 2 == 0
        moves = agent_a_moves if is_agent_a else agent_b_moves
        move_index = turn // 2
        if move_index >= len(moves):
            break
        agent_name = "A" if is_agent_a else "B"
        transcript.append((agent_name, moves[move_index]))
    return transcript
