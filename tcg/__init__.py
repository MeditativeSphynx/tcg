import os
from loguru import logger

tcg_path = os.path.abspath(os.path.dirname(__file__))
logger.debug(tcg_path)

tcg_pokemon_cache = f'{tcg_path}/data/pokecache.json'
tcg_last_pokemon_accessed = f'{tcg_path}/data/last_pokemon.json'
tcg_last_mtg_accessed = f'{tcg_path}/data/last_mtg.json'


# TODO: FIX THE INITIAL CREATION OF THE `./logs` dir and the `debug.log` file
if not os.path.exists(f'./logs/debug.log'):
    # with open(f'./logs/debug.log', 'w') as f:
    #     f.write('')
    logger.debug(f'{os.path.exists("./logs/debug.log")}')