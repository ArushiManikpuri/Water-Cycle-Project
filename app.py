from flask import Flask, request
from water_cycle_SM import WaterCycleSM
from logger_config import setup_logger

# Get logger for this module
logger = setup_logger('flask_app')

app = Flask(__name__)
water_cycle = WaterCycleSM()

history = []

@app.route("/")
def index():
    logger.info(f"Index page accessed from {request.remote_addr}")
    return "Welcome to the Water Cycle Project"

@app.route("/state")
def state():
    current_state = water_cycle.state
    logger.info(f"State requested: {current_state}")
    return current_state

@app.route("/heat_up")
def heat_up():
    current_state = water_cycle.state
    logger.info(f"Heat up requested. Current state: {current_state}")
    
    message = ""
    if current_state == "liquid":
        message = water_cycle.evaporate()
    elif current_state == "solid":
        message = water_cycle.melt()
    elif current_state == "gaseous":
        message = water_cycle.remain_gaseous()
    
    water_cycle.heat_up()
    new_state = water_cycle.state
    logger.info(f"State changed from {current_state} to {new_state}")
    history.append(f"State changed from {current_state} to {new_state}")
    if len(history) > 5:
        history.pop(0)  # Keep only the last 5 entries
    return f"{message}<br>Temperature increased. New state: {new_state}"

@app.route("/cool_down")
def cool_down():
    current_state = water_cycle.state
    logger.info(f"Cool down requested. Current state: {current_state}")
    
    message = ""
    if current_state == "liquid":
        message = water_cycle.freeze()
    elif current_state == "gaseous":
        message = water_cycle.condense()
    elif current_state == "solid":
        message = water_cycle.remain_solid()
    
    water_cycle.cool_down()
    new_state = water_cycle.state
    logger.info(f"State changed from {current_state} to {new_state}")
    history.append(f"State changed from {current_state} to {new_state}")
    if len(history) > 5:
        history.pop(0)  # Keep only the last 5 entries
    return f"{message}<br>Temperature decreased. New state: {new_state}"

@app.route("/history")
def history_view():
    return "<br>".join(history[-5:])  # Return only the last 5 items

if __name__ == "__main__":
    water_cycle.start()
    logger.info("Water cycle started in liquid state")
    logger.info("Flask application starting")
    app.run(debug=True, host='0.0.0.0')