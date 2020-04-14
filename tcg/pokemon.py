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

        ##### POKEMON STATS #####
        self.pokemon_id = tk.StringVar(self)
        self.pokemon_id.set('')

        self.pokemon_name = tk.StringVar(self)
        self.pokemon_name.set('')

        self.pokemon_speed = tk.StringVar(self)
        self.pokemon_speed.set('')

        self.pokemon_defense = tk.StringVar(self)
        self.pokemon_defense.set('')

        self.pokemon_special_defense = tk.StringVar(self)
        self.pokemon_special_defense.set('')

        self.pokemon_attack = tk.StringVar(self)
        self.pokemon_attack.set('')

        self.pokemon_special_attack = tk.StringVar(self)
        self.pokemon_special_attack.set('')

        self.pokemon_hp = tk.StringVar(self)
        self.pokemon_hp.set('')

        self.pokemon_height = tk.StringVar(self)
        self.pokemon_height.set('')

        self.pokemon_weight = tk.StringVar(self)
        self.pokemon_weight.set('')

        self.pokemon_type_list = tk.StringVar(self)
        ##### END OF POKEMON STATS #####

        ##### WIDGET SET UP #####
        self.id_lbl = tk.Label(self, text='ID')
        self.id_entry = tk.Entry(self, textvar=self.pokemon_id)

        self.name_lbl = tk.Label(self, text='Name')
        self.name_entry = tk.Entry(self, textvar=self.pokemon_name)

        self.hp_lbl = tk.Label(self, text='HP')
        self.hp_entry = tk.Entry(self, textvar=self.pokemon_hp)

        self.speed_lbl = tk.Label(self, text='Speed')
        self.speed_entry = tk.Entry(self, textvar=self.pokemon_speed)

        self.defense_lbl = tk.Label(self, text='Defense')
        self.defense_entry = tk.Entry(self, textvar=self.pokemon_defense)
        
        self.spc_defense_lbl = tk.Label(self, text='Special Defense')
        self.spc_defense_entry = tk.Entry(
            self, 
            textvar=self.pokemon_special_defense
        )

        self.type_lbl = tk.Label(self, text='Type(s)')

        self.rand_pokemon_btn = tk.Button(
            self,
            text='Random Pokemon',
            command=self.start_rando_pokemon_thread
        )

        self.search_pokemon_btn = tk.Button(
            self,
            text='Search Pokemon',
            command=self.search_pokemon
        )

        widget_list = [
            self.id_lbl, self.id_entry,
            self.name_lbl, self.name_entry,
            self.hp_lbl, self.hp_entry,
            self.speed_lbl, self.speed_entry,
            self.defense_lbl, self.defense_entry,
            self.spc_defense_lbl, self.spc_defense_entry,
            self.search_pokemon_btn,
            self.rand_pokemon_btn
        ]

        ##### GRIDS ##### 
        # HACK: Refactor this mess.
        w_count = 1
        column = {'count': 0, 'max': 0}
        row = {'count': 0, 'max': 0}

        for widget in widget_list:
            logger.debug(f'widget: {widget.widgetName}')

            if widget.widgetName == 'button':
                column['count'] = 0
                row['count'] = row['max'] + 1
                widget.grid(
                    column=column['count'], row=row['count'],
                    columnspan=column['max'], padx=3, pady=3, 
                    sticky=('N', 'S', 'E', 'W')
                )
            else:
                widget.grid(
                    column=column['count'], row=row['count'], padx=3, pady=3, 
                    sticky=('N', 'S', 'E', 'W')
                )

            logger.debug(f'column: {column}')
            logger.debug(f'row: {row}')

            if w_count != 0 and w_count % 4 == 0:
                column['count'] += 1
                row['count'] = 0
            else:
                row['count'] += 1
            w_count += 1

            if column['count'] > column['max']:
                column['max'] = column['count']

            if row['count'] > row['max']:
                row['max'] = row['count']

        # master.update()
        # print(master.winfo_width())

        # self.type_lbl.grid(column=0, row=4, pady=3, sticky=('S', 'W'))
        # self.type_listbox = tk.Listbox(
        #     self, height=3, width=int(master.winfo_width()/6), 
        #     listvariable=self.pokemon_type_list
        # )
        # self.type_listbox.grid(
        #     column=0, row=5, pady=3, columnspan=2, sticky=('S', 'W')
        # )

        
        # self.search_pokemon_btn.grid(
        #     column=0, row=6, pady=3, columnspan=2, sticky=('N', 'S', 'E', 'W')
        # )

        
        # self.rand_pokemon_btn.grid(
        #     column=0, row=7, pady=3, columnspan=2, sticky=('N', 'S', 'E', 'W')
        # )


    def search_pokemon(self):
        # TODO: ADD SEARCH LOGIC
        print(f'({self.pokemon_id.get()}) {self.pokemon_name.get()}')

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

        self.pokemon_type_list.set(
            [poke_type['type']['name'] for poke_type in self.pokemon.types]
        )

        for i in range(len(self.pokemon.stats)):  # HACK: Refactor
            if self.pokemon.stats[i]['stat']['name'] == 'speed':
                self.pokemon_speed.set(self.pokemon.stats[i]['base_stat'])
            elif self.pokemon.stats[i]['stat']['name'] == 'defense':
                self.pokemon_defense.set(self.pokemon.stats[i]['base_stat'])
            elif self.pokemon.stats[i]['stat']['name'] == 'special-defense':
                self.pokemon_special_defense.set(
                    self.pokemon.stats[i]['base_stat']
                )
            elif self.pokemon.stats[i]['stat']['name'] == 'attack':
                self.pokemon_attack.set(self.pokemon.stats[i]['base_stat'])
            elif self.pokemon.stats[i]['stat']['name'] == 'special-attack':
                self.pokemon_special_attack.set(
                    self.pokemon.stats[i]['base_stat']
                )
            elif self.pokemon.stats[i]['stat']['name'] == 'hp':
                self.pokemon_hp.set(self.pokemon.stats[i]['base_stat'])
            elif self.pokemon.stats[i]['stat']['name'] == 'height':
                self.pokemon_height.set(self.pokemon.stats[i]['base_stat'])
            elif self.pokemon.stats[i]['stat']['name'] == 'weight':
                self.pokemon_weight.set(self.pokemon.stats[i]['base_stat'])
            else:
                logger.debug(
                    f"forgotten stat: {self.pokemon.stats[i]['stat']['name']}"
                )


class Pokemon:
    def __init__(self, pokemon):
        self.__dict__.update(pokemon)
        self.store_last()

    def store_last(self):
        with open(tcg_last_pokemon_accessed, 'w') as f:
            json.dump(self.__dict__, f, indent=True)
