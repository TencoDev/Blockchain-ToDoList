from flask import Flask, request, jsonify, render_template
import hashlib
import json
from time import time

app = Flask(__name__)

class Block:
    def __init__(self, index, previous_hash, timestamp, task, hash, completed=False):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.task = task
        self.hash = hash
        self.completed = completed

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4)

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", time(), "Genesis Block", self.calculate_hash(0, "0", time(), "Genesis Block"))

    def add_task(self, task):
        previous_block = self.chain[-1]
        index = len(self.chain)
        timestamp = time()
        previous_hash = previous_block.hash
        hash = self.calculate_hash(index, previous_hash, timestamp, task)
        new_block = Block(index, previous_hash, timestamp, task, hash)
        self.chain.append(new_block)

    def mark_task_completed(self, index):
        self.chain[index].completed = True

    def remove_task(self, index):
        self.chain.pop(index)

    def calculate_hash(self, index, previous_hash, timestamp, task):
        block_string = f"{index}{previous_hash}{timestamp}{task}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != self.calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.task):
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def display_chain(self):
        return [block.__dict__ for block in self.chain]

# Create a new blockchain-based to-do list
todo_list_blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    todo_list_blockchain.add_task(task)
    return jsonify(todo_list_blockchain.display_chain()), 201

@app.route('/complete_task', methods=['POST'])
def complete_task():
    index = int(request.form['index'])
    todo_list_blockchain.mark_task_completed(index)
    return jsonify(todo_list_blockchain.display_chain()), 200

@app.route('/remove_task', methods=['POST'])
def remove_task():
    index = int(request.form['index'])
    todo_list_blockchain.remove_task(index)
    return jsonify(todo_list_blockchain.display_chain()), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify(todo_list_blockchain.display_chain()), 200

@app.route('/view_chain')
def view_chain():
    return render_template('chain.html')

if __name__ == '__main__':
    app.run(debug=True)
