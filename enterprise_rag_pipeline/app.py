from flask import Flask, request, jsonify, render_template
from ingestion import load_all_pdfs
from vector_store import create_vector_store
from agents.planner_agent import planner_agent
from agents.execution_agent import execution_agent
from agents.validator_agent import validator_agent

app = Flask(__name__)

print("Loading all PDFs from data directory...")

chunks = load_all_pdfs("data")
create_vector_store(chunks)

print("Vector Store Ready!")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/rag", methods=["POST"])
def rag():

    data = request.get_json(force=True)
    query = data["query"]

    plan = planner_agent(query)
    answer = execution_agent(query, plan)
    validation = validator_agent(answer)

    if validation == "UNSAFE":
        return jsonify({"response":"Blocked"})

    return jsonify({"response":answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)