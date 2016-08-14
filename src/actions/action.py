from random import choice
import re

class Action:
    """
    Defines an action (how will a message be replied)
    """

    def __init__(self, name, keywords, action=None, multiple_answers=[], requires_admin=False):
        """
        Initializes this action
        :param name: The name of the action

        :param keywords: Which keywords trigger this action? They should be a valid regex

        :param action: The action to be triggered. This *must* return an enumerator (use yield)
                       If no action is provided, multiple_answers will be used

        :param multiple_answers: Returns one of the given multiple answers. This is mutually
                                 exclusive with action

        :param admin: Determines whether the command is an admin-only command
        """
        self.name = name

        # For each keyword, add word bounding (\b) and pre-compile the regex
        self.keywords = []
        for keyword in keywords:
            self.keywords.append(re.compile(r'\b{}\b'.format(keyword), re.IGNORECASE))

        self.action = action
        self.multiple_answers = multiple_answers
        self.requires_admin = requires_admin


    def should_trigger(self, user, msg):
        """
        Should the action trigger with the given message?

        :param msg: The message that will be checked
        :return: Returns the match which was triggered if it should trigger, None otherwise
        """
        if self.requires_admin and not user.is_admin:
            return None

        for keyword in self.keywords:
            match = keyword.search(msg)
            if match is not None:  # If we found a match, return it
                return match

        return None

    def act(self, user, msg, match):
        """
        Acts for the given user with the specified action.

        :param user: The user for who the action will be performed
        :param msg: The message that the user sent
        :return: An iterable
        """
        if self.action is not None:
            for a in self.action(user, msg, match):
                yield a  # TODO avoid iterating twice, maybe return a set
            return

        else:
            yield choice(self.multiple_answers)
            return

        return []