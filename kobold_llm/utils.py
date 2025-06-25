def size(name):
    parts = name.split("-")
    for part in reversed(parts):
        if part.endswith("B"):
            return float(part.replace("B", ""))

# This parser finally works
def log_to_df(log_str):
    entries = []
    current = {}

    for line in log_str.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            if current: 
                entries.append(current)
            current = {'Model': line[2:]}  # remove '# '
        elif ':' in line:
            key, value = line.split(':', 1)
            current[key.strip()] = float(value.split()[0])
    if current:  # add last
        entries.append(current)

    return pd.DataFrame(entries)
