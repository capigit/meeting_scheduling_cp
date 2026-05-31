def parse_text_instance(instance_text):
    data = {
        "NumberOfMeetings": 0,
        "NumberOfAgents": 0,
        "DomainSize": 0,
        "AgentMeetings": [],
        "Distances": [],
    }
    mode = None

    for line in instance_text.split('\n'):
        line = line.strip()
        if not line:
            continue

        if '=' in line and mode is None:
            key, value = line.split('=')
            data[key.strip()] = int(value.strip())
        elif line.startswith("Agents Meetings:"):
            mode = "agents"
            continue
        elif line.startswith("Between Meetings Distance:"):
            mode = "distances"
            continue
        elif line.startswith("Estimated"):
            break

        if mode == "agents" and line.startswith("Agents"):
            parts = line.split(':')
            if len(parts) == 2:
                data["AgentMeetings"].append([int(x) for x in parts[1].split()])
        elif mode == "distances" and ':' in line:
            parts = line.split(':')
            if len(parts) == 2:
                data["Distances"].append([int(x) for x in parts[1].split()])

    return data
