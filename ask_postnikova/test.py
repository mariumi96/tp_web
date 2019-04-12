from random import choice
from pyknow import *
from ask.models import Question,Answer,Tag,Profile,Like, TestAnswer,TestQuestion, Animal
class MyFact(Fact):
    pass


@Rule(MyFact())  # This is the LHS
def match_with_every_myfact():
    """This rule will match with every instance of `MyFact`."""
    # This is the RHS
    print("MyFact()")
    pass


@Rule(Fact('animal', family='felinae'))
def match_with_cats():
    """
    Match with every `Fact` which:

      * f[0] == 'animal'
      * f['family'] == 'felinae'

    """
    print("Meow!")


class Light(Fact):
    """Info about the traffic light."""
    pass

class RobotCrossStreet(KnowledgeEngine):
    @Rule(Light(color='green'))
    def green_light(self):
        print("Walk")

    @Rule(Light(color='red'))
    def red_light(self):
        print("Don't walk")

    @Rule(AS.light << Light(color=L('yellow') | L('blinking-yellow')))
    def cautious(self, light):
        print("Be cautious because light is", light["color"])


engine = RobotCrossStreet()
engine.reset()
engine.declare(Light(color=choice(['green', 'yellow', 'blinking-yellow', 'red']))) # значение
engine.run()

a = Animal.objects.all()
print(a)
'''
class Pet(Fact):
    """Info about the traffic light."""
    pass

class RobotChoosingPet(KnowledgeEngine):
    @Rule(Pet(wool='long'))
    def fluffy_pet(self):
        print("A lot of fur")

    @Rule(Pet(wool='medium'))
    def medium_fluffy_pet(self):
        print("Some fur")
    
    @Rule(AS.light << Light(color=L('yellow') | L('blinking-yellow')))
    def cautious(self, light):
        print("Be cautious because light is", light["color"])
    


engine = RobotChoosingPet()
engine.reset()
#engine.declare(Light(color=choice(['green', 'yellow', 'blinking-yellow', 'red']))) # значение
engine.run()


'''


'''
@Rule(
    AND(
        OR(MyFact('admin'),
           MyFact('root')),
        NOT(Fact('drop-privileges'))
    )
)
'''
@DefFacts()
def needed_data():
    yield Fact(best_color="red")
    yield Fact(best_body="medium")
    yield Fact(best_sweetness="dry")

#All DefFacts inside a KnowledgeEngine will be called every time the reset method is called.


class Greetings(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="greet")

    @Rule(Fact(action='greet'),
          NOT(Fact(name=W())))
    def ask_name(self):
        self.declare(Fact(name=input("What's your name? ")))

    @Rule(Fact(action='greet'),
          NOT(Fact(location=W())))
    def ask_location(self):
        self.declare(Fact(location=input("Where are you? ")))

    @Rule(Fact(action='greet'),
          Fact(name=MATCH.name),
          Fact(location=MATCH.location))
    def greet(self, name, location):
        print("Hi %s! How is the weather in %s?" % (name, location))

engine = Greetings()
engine.reset()  # Prepare the engine for the execution.
engine.run()  # Run it!
