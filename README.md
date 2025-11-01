# Water Cycle Simulation Project
This project simulates the water cycle using a state machine to model transitions between the three states of water: solid (ice), liquid (water), and gaseous (vapor). It provides a web interface to interact with these state transitions.

## Overview
The Water Cycle Simulation demonstrates how water changes between different states based on temperature changes. The project uses:

- Python Transitions Library: For state machine implementation
- Flask: For web API endpoints
- Logging: For tracking state changes and API requests

## States and Transitions
The water cycle has three main states:

- Solid (Ice)
- Liquid (Water)
- Gaseous (Vapor)

Transitions between states:

- Heat up:
  - Solid → Liquid (Melting)
  - Liquid → Gaseous (Evaporation)
  - Gaseous → Gaseous (Remain gaseous)
- Cool down:
  - Gaseous → Liquid (Condensation)
  - Liquid → Solid (Freezing)
  - Solid → Solid (Remain solid)

## Project Structure

```
Water-Cycle-Project/ │ 
                     ├── app.py # Flask web application 
                     ├── water_cycle_SM.py # State machine implementation 
                     ├── logger_config.py # Centralized logging configuration 
                     ├── logs/ # Log files directory 
                     │ ├── flask_app.log # Application logs 
                     │ └── water_cycle_sm.log # State machine logs 
                     └── README.md # This file
```


## API Endpoints
- GET / - Welcome page
- GET /state - Get the current state of water
- GET /heat_up - Increase temperature and trigger state transitions
- GET /cool_down - Decrease temperature and trigger state transitions

## Installation
1. Clone the repository:

```sh
git clone https://github.com/yourusername/Water-Cycle-Project.git 
cd Water-Cycle-Project
```


2. Install dependencies:

```sh
pip install -r requirements.txt
```


3. Run the application:

```sh   
python app.py
```



4. Access the application at: http://localhost:5000

## Usage Examples
Check the current state:

```sh
curl http://localhost:5000/state
```

Heat up the water cycle:

```sh
curl http://localhost:5000/heat_up
```

Cool down the water cycle:

```sh  
curl http://localhost:5000/cool_down
```


## Logging
The application logs all state transitions and API requests to:

- Console output
- Log files in the logs directory

You can monitor these logs to track the simulation's behavior.

## Future Enhancements
- Add a graphical UI to visualize the water cycle
- Implement temperature values instead of simple up/down commands
- Add more complex transitions and edge cases
- Create a Docker container for easy deployment

## License
This project is licensed under the MIT License - see the LICENSE file for details