import re
from collections import Counter
LEVEL_RE = re.compile(r'(?i)\b(ERROR|WARN|WARNING|INFO|DEBUG|TRACE|FATAL|CRITICAL)\b')
def count_levels(lines_iter):
    """
    Count log levels in given lines using regex.
    :param lines_iter: Iterable of log lines
    :return: Counter of level names
    """
    counts = Counter()
    for line in lines_iter:
        match = LEVEL_RE.search(line)
        if match:
            counts[match.group(1).upper()] += 1
    return counts