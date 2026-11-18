def queue_with_two_stacks(ops):
    inbox = []
    outbox = []
    out = []

    def move():
        if not outbox:
            while inbox:
                outbox.append(inbox.pop())

    for op in ops:
        if op.startswith("push"):
            inbox.append(int(op.split()[1]))
        elif op == "pop":
            move()
            out.append(outbox.pop())
        elif op == "peek":
            move()
            out.append(outbox[-1])
        else:
            out.append(0 if inbox or outbox else 1)
    return out
