# Run
inputs = {
    "question": "How did the sales from finance compare to the total sales in the year 2024??","response" :None, "source" : None
}
from pprint import pprint
for output in app.stream(inputs):
    for key, value in output.items():
        # Node
        pprint(f"Node '{key}':")
        # Optional: print full state at each node
        # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
    pprint("\n---\n")


print(value['response'])
print("--")
print(value['source'])
