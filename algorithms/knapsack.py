
def knapsack(tasks, capacity):

    n = len(tasks)

    dp = [
        [0 for _ in range(capacity + 1)]
        for _ in range(n + 1)
    ]

    for i in range(1, n + 1):

        hours = tasks[i - 1]["hours"]
        priority = tasks[i - 1]["priority"]

        for w in range(capacity + 1):

            dp[i][w] = dp[i - 1][w]

            if hours <= w:

                dp[i][w] = max(
                    dp[i - 1][w],
                    priority + dp[i - 1][w - hours]
                )

    selected = []
    w = capacity

    for i in range(n, 0, -1):

        if dp[i][w] != dp[i - 1][w]:

            task = tasks[i - 1]
            selected.append(task)
            w -= task["hours"]

    selected.reverse()

    return selected, dp[n][capacity]
