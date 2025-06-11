def handle_split(parts):
 result = list(get_value(parts[1]))
 result.reverse()
 for i in range(len(result)):
  stacks[curstack].append(result[i])

instruction_handlers["SPLIT"] = handle_split
