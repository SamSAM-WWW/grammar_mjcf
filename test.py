import re
target_node_name = 'body2996'
prefix = re.match(r'([a-zA-Z]+)', target_node_name).group(1)
print(prefix)

