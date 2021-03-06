import tkinter as tk
from tkinter import ttk

from pprint import pprint
import threading
import inspect
import secrets
import functools
import json

import tinydb
import pokebase
from loguru import logger

from tcg import tcg_pokemon_cache, tcg_path, tcg_last_pokemon_accessed

logger.add('./logs/debug.log', level='DEBUG')


class PokeCache:
    """The PokeCache class is designed to act as a decorator for functions
    or methods that call from the PokeAPI using Pokebase."""
    def __init__(self, func):
        """Initialization of the cache and the class field for the decorated
        function.

        Parameters
        ----------
        func : Class Method or a Function
            The function that is being decorated. This function should contain
            some information regarding a single Pokemon.
        """
        self.poke_cache = tinydb.TinyDB(tcg_pokemon_cache)
        self.func = func

    def __call__(self, *args, **kwargs):
        """When the decorator is called, it will check the original parameters
        passed to the function that it is decorating.
        """
        in_cache, pokemon_results = self.query_poke_id(kwargs['p_id'])
        logger.debug(f'`pokemon_results`: {pokemon_results}')
        logger.debug(f'`in_cache`: {in_cache}')
        if in_cache:
            self.func(
                p_id=pokemon_results[0].id,
                name=pokemon_results[0].name,
                pokemon=pokemon_results[0],
                *args
            )
        elif not in_cache:
            pokemon = self.cache_pokemon(*args, **kwargs)
            self.func(
                p_id=pokemon.id,
                name=pokemon.name,
                pokemon=pokemon,
                *args  # Necessary for passing the
            )

    def __get__(self, instance, owner):
        # Required to be used on class methods. Without it you will receive an
        # error stating that you are not satisfying `self` of that specific
        # class method that you are decorating.
        return functools.partial(self.__call__, instance)

    # TODO: CHANGE ARGS TO KWARGS
    # Doing this will support queries of names as well.
    # Example:
    # def query_poke(self, p_id=None, p_name=None):
    #     ...
    def query_poke_id(self, p_id):
        """Make a query on the cache using the Pokemon's id, ``p_id``.

        Parameters
        ----------
        p_id : int
            The id of the Pokemon that we are querying within the cache.

        Returns
        -------
        tuple
            The tuple contains a bool and a list. The bool acts as a flag if
            there was a positive hit within the cache. The list contains the
            results of the cache query.
        """
        p_id_query = tinydb.Query()
        query_results = self.poke_cache.search(p_id_query.id == p_id)
        if len(query_results) > 0:
            pokemon_results = []
            for result in query_results:
                pokemon_results.append(Pokemon(result))

            logger.info(f'Pokemon with id, {p_id}, in cache')
            return True, pokemon_results
        else:
            return False, []

    def cache_pokemon(self, *args, **kwargs):
        pokemon = Pokemon(
            pokebase.pokemon(kwargs['p_id'])._NamedAPIResource__data
        )
        logger.info(f'Caching ({pokemon.id}) {pokemon.name}')
        self.poke_cache.insert(pokemon.__dict__)
        return pokemon


class PokemonTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        logger.debug('>>> Setting up Pokemon Frame <<<')

        self.pokemon = None

        master.add(self, text='Pokemon')

        # TODO: ADD THE REST OF THE VARIABLES THAT THE ``POKEMON``
        #   CLASS CONTAINS.
        self.pokemon_id = tk.StringVar(self)
        self.pokemon_id.set('')

        self.pokemon_name = tk.StringVar(self)
        self.pokemon_name.set('')

        self.id_lbl = tk.Label(self, text='ID')
        self.id_entry = tk.Entry(self, textvar=self.pokemon_id)

        self.name_lbl = tk.Label(self, text='Name')
        self.name_entry = tk.Entry(self, textvar=self.pokemon_name)

        self.id_lbl.pack()
        self.id_entry.pack()

        self.name_lbl.pack()
        self.name_entry.pack()

        self.rand_pokemon_btn = tk.Button(
            self,
            text='Random Pokemon',
            command=self.start_rando_pokemon_thread
        )
        self.rand_pokemon_btn.pack(side='bottom', fill=tk.X)

    def start_rando_pokemon_thread(self):
        t1 = threading.Thread(target=self.get_random_pokemon)
        t1.start()

    def get_random_pokemon(self):
        cf = inspect.currentframe()
        logger.debug(f'btn command @ {__name__}:{cf.f_lineno}')

        pokemon_no = 807
        random_pokemon_no = secrets.choice(range(1, pokemon_no+1))

        logger.debug(f'pokemon_no: {random_pokemon_no}')

        self.call_api(p_id=random_pokemon_no)
        self.update_pokemon_frame()

    # HACK: HOW CAN I MAKE ``call_api`` NOT DEPENDENT ON THE ``@PokeCache``
    #   DECORATOR?

    # HACK: SHOULD I MAKE ``PokeCache`` A CLASS METHOD OF ``Pokemon`` INSTEAD?
    @PokeCache
    def call_api(self, p_id=None, name=None, pokemon=None):
        """Used to be decorated.

        The ``call_api`` method is used specifically to be decorated. Meaning,
        that it must have the ``@PokeCache`` decorator on it. If it doesn't then
        calling from the API will not work.
        """
        if pokemon is not None:
            self.pokemon = pokemon

    def update_pokemon_frame(self):
        logger.debug('Updating Pokemon information')

        self.pokemon_id.set(self.pokemon.id)
        logger.debug(self.pokemon_id)

        self.pokemon_name.set(self.pokemon.name)
        logger.debug(self.pokemon_name)


class Pokemon:
    def __init__(self, pokemon):
        self.__dict__.update(pokemon)
        self.store_last()

    def store_last(self):
        with open(tcg_last_pokemon_accessed, 'w') as f:
            json.dump(self.__dict__, f, indent=True)
