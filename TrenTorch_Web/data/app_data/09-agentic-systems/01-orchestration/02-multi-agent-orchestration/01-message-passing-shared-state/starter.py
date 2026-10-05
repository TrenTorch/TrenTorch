def process_message_log(messages: list[tuple[str, str, str]]) -> dict[str, tuple[str, str]]:
    """
    messages: (sender, key, value) -- each message writes `value` into a
    shared blackboard under `key`, in order.

    Process the messages in order. Return the final state: a dict from
    key to (value, last_writer), where value/last_writer reflect
    whichever message most recently wrote that key (last write wins).
    """
    # TODO: Implement the shared-state blackboard from Theory.
    pass
