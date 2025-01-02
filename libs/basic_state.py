import logging

logger = logging.getLogger(__name__)

# the user provides a list of state names
# the idea is the the system moves from one state to the next or back with next/prev states
# it is also possible to jump to another state by providing the state value or the state name

# TODO:
# pushState(newstate) - save state to stack and move to new state
# popState() - restore previous saved state


class BasicStateMachine:

    def __init__(self) -> None:
        self.state = None
        self.state_table = ["uninitialised"]
        self.stack = []


    # ----------------------------------------------------------------------------
    def addStateTable(self, items):
        """add a list of strings

        Args:
            items : list of state name strings, must be more than one item in the list
            the list should be the normal flow of the statemachine, from element 0 to element x-1
        Returns:
            True if the list was added, false if not a list, not enough items, or elements not being a string
        """

        if not list:
            logger.error("items table is not defined")
            return False

        if type(items) != list[str]:
            logger.error("items table is not a list")
            return False

        if len(items) < 2:
            logger.error("not enough items in the table")
            return False

        # may not need this if the type(items) check works
        newtable = []
        for ele in items:
            if type(ele) != str:
                logger.error("each element needs to be a string")
                return False
            # lowercase and remove spaces
            newele = self.cleanState( ele)
            # check that we have not see this element before
            if newele in newtable:
                raise Exception( "REPEATED ELEMENT")

            newtable.append( newele)

        # only create the new table when there are no issues
        self.state_table = newtable

        # as we are creating a new table, we need a new stack
        self.stack = []



    # ----------------------------------------------------------------------------
    def getState(self):
        """get the string the current state represents

        Returns:
        the curent state string
        """
        return self.state_table[self.state]

    # ----------------------------------------------------------------------------
    def getStateValue(self):
        """get the value current state

        Returns:
        the curent state value
        """
        return self.state

    # ----------------------------------------------------------------------------
    def setState(self, new_state):
        """set the state

        Args:
        new_state: the state we want to move to, either state value or the name
        of a state in the state table


        Returns:
        the (new) curent state

        Raises:
            NO_STATE exception
        """

        if type(new_state) == int:
            if new_state > len(self.state_list) + 1:
                raise Exception("NO STATE")
            self.state = new_state
        elif type(new_state) == str:
            try:
                offset = self.state_table.index( self.cleanState(new_state))
                self.state = offset
            except ValueError:
                raise Exception("NO STATE")

        else:
            raise Exception("INVALID STATE")

        return self.state

    # ----------------------------------------------------------------------------
    def nextState(self):
        """transition to the next state

        Returns:
        the new curent state

        Raises:
            NO_STATE exception
        """

        if self.state + 1 > len(self.state_list) + 1:
            raise Exception("NO STATE")

        self.state = self.state + 1

    # ----------------------------------------------------------------------------
    def prevState(self):
        """transition to the previous state

        Returns:
        the new state

        Raises:
            "NO STATE" exception
        """

        if self.state - 1 < 1:
            raise Exception("NO STATE")

        self.state = self.state - 1


    # ----------------------------------------------------------------------------
    def pushState(self):
        """save the state to the internal stack, does not alter current state"""
        self.stack.append( self.state)

    # ----------------------------------------------------------------------------
    def popState(self):
        """retrieve the state from the internal stack, alters the current state
        Returns:
            the new state value
        """
        self.state = self.stack.pop()

        return self.state

    # ----------------------------------------------------------------------------
    def pushAndSetState( self, newstate):
        """push the current state onto a stack and switch to a new state

        Args:
        newstate: the state we wish to switch to either as the value or the name string

        Returns:
            the new state value

        Raises:
            "NO STATE" or "INVALID STATE" same as setState method
        """

        self.pushState()
        self.setState( newstate)

        return self.state


    # ----------------------------------------------------------------------------
    def cleanState( statename):
        """class function to clean a statename into a consistent form, as lower case and no spaces

        Args:
            statename : (string) the name to transform
        Returns:
            (string) the cleaned name
        """
        return statename.lower().replace( ' ', '')
