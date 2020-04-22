import os

from loguru import logger

# TODO: RENAME—REMOVE 'tcg'
tcg_path = os.path.abspath(os.path.dirname(__file__))

# TODO: RENAME—REMOVE 'tcg'
# TODO: 
tcg_pokemon_cache = f'{tcg_path}/data/pokecache.json'
tcg_last_pokemon_accessed = f'{tcg_path}/data/last_pokemon.json'
tcg_last_mtg_accessed = f'{tcg_path}/data/last_mtg.json'

log_path = f'{tcg_path}/logs/debug.log'
if not os.path.exists(log_path):
    # with open(f'./logs/debug.log', 'w') as f:
    #     f.write('')
    logger.debug(f'{os.path.exists(log_path)}')

logger.add(log_path, level='DEBUG')