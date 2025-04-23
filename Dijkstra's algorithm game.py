import sys
import heapq as hq
import tkinter as tk
from tkinter import messagebox, simpledialog

def dijsktra(graph, src, dest):
    inf = sys.maxsize
    node_data = {node: {'dist': inf, 'pred': []} for node in graph}
    node_data[src]['dist'] = 0
    
    visited = []
    temp = src

    for _ in range(len(graph)-1):  
        if temp not in visited:
            visited.append(temp)  
            min_heap = []

            for j in graph[temp]:
                if j not in visited:  
                    dist = node_data[temp]['dist'] + graph[temp][j]
                    if dist < node_data[j]['dist']:
                        node_data[j]['dist'] = dist 
                        node_data[j]['pred'] = node_data[temp]['pred'] + [temp]  
                    hq.heappush(min_heap, (node_data[j]['dist'], j))

            if min_heap:
                hq.heapify(min_heap)
                temp = min_heap[0][1]
            else:
                break

    return node_data[dest]['pred'] + [dest], node_data[dest]['dist']

# Graphs
graph1 = {
    'A': {'B': 2, 'C': 4},
    'B': {'A': 2, 'C': 3, 'D': 8},
    'C': {'A': 4, 'B': 3, 'E': 5, 'D': 2},
    'D': {'B': 8, 'C': 2, 'E': 11, 'F': 22},
    'E': {'C': 5, 'D': 11, 'F': 1},
    'F': {'D': 22, 'E': 1}
}

graph2 = {
    'A': {'B': 7, 'C': 3},
    'B': {'A': 7, 'C': 1, 'D': 2},
    'C': {'A': 3, 'B': 1, 'D': 5},
    'D': {'B': 2, 'C': 5, 'E': 4},
    'E': {'D': 4}
}

graph3 = {
    'A': {'B': 10, 'D': 5},
    'B': {'A': 10, 'C': 1},
    'C': {'B': 1, 'D': 2},
    'D': {'A': 5, 'C': 2, 'E': 3},
    'E': {'D': 3}
}

graph4 = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'E': 3},
    'D': {'B': 5, 'E': 7},
    'E': {'C': 3, 'D': 7}
}

graph5 = {
    'A': {'B': 6, 'F': 3},
    'B': {'A': 6, 'C': 1},
    'C': {'B': 1, 'D': 4},
    'D': {'C': 4, 'E': 2},
    'E': {'D': 2, 'F': 5},
    'F': {'A': 3, 'E': 5}
}

graphs = [
    (graph1, 'F', "Graph 1:\nA to B(2), C(4)\nB to A(2), C(3), D(8)\nC to A(4), B(3), D(2), E(5)\nD to B(8), C(2), E(11), F(22)\nE to C(5), D(11), F(1)\nF to D(22), E(1)"),
    (graph2, 'E', "Graph 2:\nA to B(7), C(3)\nB to A(7), C(1), D(2)\nC to A(3), B(1), D(5)\nD to B(2), C(5), E(4)\nE to D(4)"),
    (graph3, 'E', "Graph 3:\nA to B(10), D(5)\nB to A(10), C(1)\nC to B(1), D(2)\nD to A(5), C(2), E(3)\nE to D(3)"),
    (graph4, 'E', "Graph 4:\nA to B(1), C(4)\nB to A(1), C(2), D(5)\nC to A(4), B(2), E(3)\nD to B(5), E(7)\nE to C(3), D(7)"),
    (graph5, 'F', "Graph 5:\nA to B(6), F(3)\nB to A(6), C(1)\nC to B(1), D(4)\nD to C(4), E(2)\nE to D(2), F(5)\nF to A(3), E(5)")
]

class DijkstraGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra's Shortest Path Challenge!")
        self.root.geometry("600x400")
        self.root.configure(bg="#f7f7f7")

        self.index = 0
        self.score = 0

        self.title = tk.Label(root, text="🧠 Dijkstra Path Quiz 🧠", font=("Helvetica", 20, "bold"), bg="#f7f7f7", fg="#4a4a4a")
        self.title.pack(pady=10)

        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 14), bg="#f7f7f7", fg="#333")
        self.score_label.pack()

        self.graph_text = tk.Label(root, text="", justify='left', font=("Courier", 11), bg="#f7f7f7")
        self.graph_text.pack(pady=10)

        self.entry_label = tk.Label(root, text="🔡 Enter path from A to target (space separated):", font=("Arial", 11), bg="#f7f7f7")
        self.entry_label.pack()

        self.entry = tk.Entry(root, width=40, font=("Arial", 12))
        self.entry.pack(pady=5)

        self.submit_btn = tk.Button(root, text="Check Path ✅", command=self.check_answer, bg="#5cb85c", fg="white", font=("Arial", 11, "bold"))
        self.submit_btn.pack(pady=10)

        self.feedback = tk.Label(root, text="", font=("Arial", 12, "italic"), bg="#f7f7f7")
        self.feedback.pack()

        self.next_question()

    def next_question(self):
        if self.index < len(graphs):
            graph, dst, description = graphs[self.index]
            self.graph_text.config(text=description + f"\n\n🎯 Goal: Find the shortest path from A to {dst}")
            self.entry.delete(0, tk.END)
            self.feedback.config(text="", fg="#333")
        else:
            self.end_game()

    def check_answer(self):
        user_input = self.entry.get().strip().upper().split()
        graph, dst, _ = graphs[self.index]
        correct_path, dist = dijsktra(graph, 'A', dst)

        if user_input == correct_path:
            self.feedback.config(text="✅ You nailed it!", fg="green")
            self.score += 2
            self.score_label.config(text=f"Score: {self.score}")
        else:
            correct_str = " → ".join(correct_path)
            self.feedback.config(text=f"❌ Oops! Correct path: {correct_str}", fg="red")

        self.index += 1
        self.root.after(2500, self.next_question)

    def end_game(self):
        again = messagebox.askyesno("Game Over", f"🎉 Final Score: {self.score} / {len(graphs)*2}\n\nDo you want to play again?")
        if again:
            self.index = 0
            self.score = 0
            self.score_label.config(text=f"Score: {self.score}")
            self.next_question()
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = DijkstraGame(root)
    root.mainloop()
