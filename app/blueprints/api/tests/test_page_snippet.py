import unittest
from page_snippet import SearchQuerySnippet

text = """
In the space of a few short years, we’ve become surrounded by computers. 
They used to be safely hidden away in military research centers and university
laboratories, but now they’re everywhere: on our desks, in our pockets, under 
the hoods of our cars, implanted inside our bodies. As programmers, we work
with sophisticated computing devices every day, but how well do we understand
the way they work?

The power of modern computers comes with a lot of complexity. It’s difficult to 
understand every detail of a computer’s many subsystems, and more difficult still to 
understand how those subsystems interact to create the system as a whole. This 
complexity makes it impractical to reason directly about the capabilities and behavior
of real computers, so it’s useful to have simplified models of computers that share 
interesting features with real machines but that can still be understood in their entirety.
In this chapter, we’ll strip back the idea of a computing machine to its barest essentials,
see what it can be used for, and explore the limits of what such a simple computer can do.
"""

class TestSearchQuerySnippet(unittest.TestCase):

    def setUp(self):
        pass
