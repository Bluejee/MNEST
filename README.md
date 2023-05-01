# MNEST

MNEST (Multi-agent Neuro Evolution Simulation Toolkit) is a software framework designed to model and study emergent
behavior in complex systems. The toolkit enables researchers to simulate and analyze multi-agent systems and study their
collective behavior, with a particular focus on neuro-evolutionary algorithms, including but not limited to
Reinforcement Learning, Q-Learning, Deep-Q, and Genetic Algorithms. The system allows agents to learn from their
experiences and evolve over time using Brains that can be configured to be as simple as Q-Tables or as complex as Deep
Neural Networks. MNEST provides a visualization tool to help researchers understand the emergent phenomena that arise
from the interactions among agents. To improve the research experience, the system also has a Command Line Interface
where visualization is disabled to improve speed. The toolkit's modular design and customizable components allow for
flexibility and extensibility, making it a versatile tool for exploring the dynamics of complex systems and developing
new insights into the behavior of multi-agent systems. The Toolkit is built using OOPs concepts, and hence can be
extended to create agents whose limitations lie only in the minds of the creator. Overall, MNEST is an ideal platform
for researchers and practitioners seeking to explore the potential of neuro-evolutionary algorithms in the study of
emergent behavior in complex systems.

# About

# Installation.

```commandline
pip install mnest
```

# Thank you for your patience

This project is under development, I will soon be adding proper documentation and other usage details.

# Notes

This was earlier planned to be released as SEAN (A Simulation Environment for Agent-based Neuro-evolution) is a Python package
for building and simulating artificial intelligence in multi agent-based models.

## Help with MNEST

If you need help regarding MNEST, then please open an issue or reach out to me through any of the contacts you can find in my [GitHub Profile](https://github.com/Bluejee)

If you would like to submit a bug report or feature request, please [open an issue](https://github.com/Bluejee/MNEST/issues).

## Contributing

Contributions to this project are always welcome.
Please see the [Contribution Guidelines](https://github.com/Bluejee/MNEST/blob/main/CONTRIBUTING.md) to see how to help.

## Code of Conduct

I value a positive and respectful community, and I kindly ask that you follow our code of conduct in all interactions with other members. 
Please take a moment to review the [Code of Conduct](https://github.com/Bluejee/MNEST/blob/main/CODE_OF_CONDUCT.md).

## License
Please refer the [License](https://github.com/Bluejee/MNEST/blob/main/LICENSE.txt) of this project to understand about your rights.

# Scratch Story.

Everything starts with nothingness. The first thing to be created is the world. The world by its name has no meaning, It
still is nothingness. something arives as the first rule for the world is set. Its shape[Rows x Columns].But what good
is the shape if it stillhas nothing which is where things start to exist in the world. There are many ways to catagorise
the world. here i go with the following structure the world is made of different layers each layer serves a "class" of
purpose. E.g. One layer holds the agent , another holds food, etc... The only purpose of the world is to hold the
classes of things and five it existance. hence it need not provide the tools for visualisation or calculations. In order
to prevent confusions, each cell of a layer can hold only one element. E.g. If ther exist a scanario where say 2 agents
can occupy a single position, then each agent is to be given a separate layer.

Now, even before the creation of "thing" or "Agents" which have their own rules and can interact, there must exist 2
more things. Since we(Creators) are playing "GOD", we need a (Gods Perspecitve) method of viusualising the world we
created. (Unfotunately in this version of the universe we do not have the ability to reverse time or alter the world
once it is set in motion. these are functionalities not too complex to add to the system in other Universes(Versions).
even these functionalities are accessible through the gods perspective.) Once we can see what the world looks like, the
next thing that needs to exist is a universal clock. One which none of the Universes beings/entities have the ability to
control. This clock marches forward one step at a time. the unit of time is irrelavent and can be chosen to please the
visualisation and necessities. Thus we have time evolution.

The collection of the clock, the world and the Gods perspective is together called "The Environment"
