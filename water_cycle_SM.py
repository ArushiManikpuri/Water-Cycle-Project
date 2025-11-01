from transitions import Machine, State
from logger_config import setup_logger

# Get logger for this module
logger = setup_logger('water_cycle_sm')

class WaterCycleSM(Machine):
    
    def __init__(self):
        
        states = [
            State(name='liquid'),
            State(name='gaseous'),
            State(name='solid')
        ]
        
        transitions = [
            {'trigger':'start', 'source':'initial', 'dest':'liquid'},
            
            # transitions for liquid state
            {'trigger': 'heat_up', 'source': 'liquid', 'dest': 'gaseous','before':'evaporate'},
            {'trigger': 'cool_down', 'source': 'liquid', 'dest': 'solid', 'before':'freeze'},
            
            # transitions for gaseous state
            {'trigger': 'heat_up', 'source': 'gaseous', 'dest': '=', 'before': 'remain_gaseous'},
            {'trigger': 'cool_down', 'source': 'gaseous', 'dest': 'liquid', 'before': 'condense'},
            
            # transitions for solid state
            {'trigger': 'heat_up', 'source': 'solid', 'dest': 'liquid', 'before': 'melt'},           
            {'trigger': 'cool_down', 'source': 'solid', 'dest': '=', 'before': 'remain_solid'},
        ]
        
        Machine.__init__(self, states=states, transitions=transitions, initial='initial')
        logger.info("Water cycle state machine initialized")
    
    def evaporate(self):
        message = "Water is evaporating"
        logger.info(message)
        return message
    
    def freeze(self):
        message = "Water is freezing"
        logger.info(message)
        return message
    
    def melt(self):
        message = "Ice is melting"
        logger.info(message)
        return message
    
    def condense(self):
        message = "Vapour is condensing"
        logger.info(message)
        return message
        
    def remain_solid(self):
        message = "Ice is already at freezing point - cannot get any colder"
        logger.info(message)
        return message

    def remain_gaseous(self):
        message = "Vapor is already at boiling point - cannot get any hotter"
        logger.info(message)
        return message