"""
A Trading Card Game or Collector Card Game API interaction application.
Basically, if there it an API for a particular TCG or CCG (or a variation of
these types of concepts) you will be able to use this to view information on
the cards/characters.

Not all data included is considered to be from a TCG or CCG but may be inspired
from it. For example, the PokeAPI that is being used to pull data about Pokemon
isn't based on the TCG itself but the games. Those games were inspired by the
TCG and are included within this application.

It's for fun. Let's have fun interacting with different APIs, Python GUI
programming, and data!
"""

from loguru import logger

from tcg.tkroot import Root

from tcg.pokemon import PokemonTab


if __name__ == '__main__':
    logger.info('>>> STARTING <<<')

    root = Root()

    pokemon_frame = PokemonTab(root.notebook)

    root.mainloop()

    logger.info('>>> STOPPING <<<')
