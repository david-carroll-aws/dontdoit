# Don't Do It !
Don't Do It - Mega Millions simulator that spends a million dollars so you don't have to. Spoiler: you lose. : Watch 200,000 lottery tickets turn $1,000,000 into about $50,000 and a flash. Python, Flask + Plotly + AWS EC2.

Pick a budget from $5 to $5,000,000, buy tickets at $5 a pop, and watch the counters tick up while your balance goes the other direction. The big red number at the top is the whole point.

<img width="1108" height="569" alt="image" src="https://github.com/user-attachments/assets/7bb9c7ef-d448-4df5-b960-54648ce5dc27" />


## What it does

- Simulates Mega Millions draws: 5 numbers from 1-70 plus a Mega Ball from 1-24
- Checks every ticket against your preset numbers using the real base prize table
- Animates the run live: draws, spent, won back, % lost, and a net loss that gets uglier as it goes
- Plots spent vs. won over time with Plotly
- Shows a frequency chart of every number drawn, so you can see the randomness for yourself
- For small runs (1,000 draws or fewer), lists every individual draw with your matches highlighted

A typical $1,000,000 run (200,000 tickets) gets back somewhere around 3-5 cents on the dollar.

## Stack

- **Python + Flask** for the simulation engine and API
- **Plotly.js** for charts
- **Vanilla JavaScript/HTML/CSS** for the front end
- **AWS EC2** for hosting, with a systemd service to keep it running

## Run it

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

Then open http://localhost:8080.

## Project layout

```
app.py              Flask app: serves the page and the /api/simulate endpoint
lottery_engine.py   Draw logic, payout table, simulation loop
templates/
  index.html        The UI: live counters, Plotly charts, draw list
requirements.txt
```

To change your numbers, edit `MY_MAIN` and `MY_BONUS` at the top of `lottery_engine.py`.

## API

`GET /api/simulate?budget=<dollars>`

Runs the simulation and returns totals, a sampled timeline for the live chart, number frequencies, and (for small runs) every draw. Budgets must be between $5 and $5,000,000.

## Roadmap

- Log every draw to DynamoDB for deeper analysis
- Compare observed number frequencies against what true randomness predicts

## Disclaimer

This is a simulation for fun and education. It uses Python's pseudo-random number generator, not the real lottery's draw machinery, and it applies the base prize amounts without the multiplier. The jackpot is fixed at its $50 million starting value. It's not affiliated with Mega Millions. If anything, it's here to talk you out of it.
