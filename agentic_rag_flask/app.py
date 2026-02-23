from flask import render_template
from flask import Flask, request, jsonify
from ingestion import load_and_split
from vector_store import create_vector_store
from agents.planner_agent import planner_agent
from agents.execution_agent import execution_agent
from agents.validator_agent import validator_agent

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_pdf():

    file = request.files["file"]
    file.save("temp.pdf")

    chunks = load_and_split("temp.pdf")
    create_vector_store(chunks)

    return jsonify({"message":"PDF Processed Successfully"})

from flask import render_template
from flask import Flask, request, jsonify
from ingestion import load_and_split
from vector_store import create_vector_store
from agents.planner_agent import planner_agent
from agents.execution_agent import execution_agent
from agents.validator_agent import validator_agent

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_pdf():

    file = request.files["file"]
    file.save("temp.pdf")

    chunks = load_and_split("temp.pdf")
    create_vector_store(chunks)

    return jsonify({"message":"PDF Processed Successfully"})

@app.route("/rag", methods=["POST"])
def rag():

    try:
        data = request.get_json(force=True)

        print("Received Data:", data)

        if not data or "query" not in data:
            return jsonify({"error": "Query missing"}), 400

        query = data["query"]

        plan = planner_agent(query)
        answer = execution_agent(query, plan)

        if not answer:
            return jsonify({"response":"No documents found. Upload PDF first."})

        validation = validator_agent(answer)

        if validation == "UNSAFE":
            return jsonify({"response":"Blocked by Guardrails"})

        return jsonify({"response":answer})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(port=5000)