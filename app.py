from flask import Flask, jsonify, render_template, request

import lottery_engine as engine

app = Flask(__name__)

MIN_BUDGET = engine.TICKET_COST
MAX_BUDGET = 5_000_000  # 1,000,000 draws


@app.route("/")
def index():
    return render_template("index.html", max_budget=MAX_BUDGET)


@app.route("/api/simulate")
def simulate():
    budget = request.args.get("budget", type=int)
    if budget is None or budget < MIN_BUDGET or budget > MAX_BUDGET:
        return jsonify({"error": f"Budget must be between ${MIN_BUDGET:,} and ${MAX_BUDGET:,}."}), 400
    return jsonify(engine.run_simulation(budget))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
