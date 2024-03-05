import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path else None
from cli.ui import UI
from common.models import Database
from cli.controllers import IController, NavigationNode, UniversitySystem, NodeAddType
from typing import List
from common.services import RegisterService, LoginService, AdminOperationsLogic
import sys
import os



def main():
    db = Database()
    navigation_stack: List[NavigationNode] = [NavigationNode(0, NodeAddType.APPEND,  UniversitySystem(
        db, AdminOperationsLogic(db), LoginService(db), RegisterService(db)))]  
    try:
        ui = UI(0)
        while navigation_stack:
            current_node = navigation_stack[-1]  # Get the top controller
            nav_node = current_node.run()
            if nav_node is None or nav_node.node_add_type == NodeAddType.REPLACE:
                navigation_stack.pop()  # Pop the top controller if None
            if nav_node is not None:
                navigation_stack.append(nav_node)
        ui.info("Thank You")
    except OSError:
        ui.error(f"Encountered error: {e}")
    except EOFError:  # Ctrl+Z
        ui.info("Exiting...")
    except KeyboardInterrupt:  # Ctrl+C
        ui.info("Exiting...")
    except Exception as e:
        ui.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
