from pokemon_card_game.effects import (
    heal_target,
    move_energy,
    switch_opponent_pokemon,
    flip_coins_until_tails,
    boost_attack_damage,
    play_as_pokemon,
    retrieve_to_hand,
    attach_energy_to_specific_pokemon
)

# Mapping Trainer cards to their corresponding effects
object_effects = {
    "Misty": lambda player, opponent, logger: flip_coins_until_tails(
        "attach_energy", "Water", player.active_pokemon, logger
    ),
    "Blaine": lambda player, opponent, logger: boost_attack_damage(
        [pokemon for pokemon in player.bench if pokemon.name in ["Ninetales", "Rapidash", "Magmar"]],
        30,
        logger
    ),
    "Giovanni": lambda player, opponent, logger: boost_attack_damage(
        player.bench, 10, logger
    ),
    "Erika": lambda player, opponent, logger: heal_target(
        player.active_pokemon, amount=50, logger=logger
    ),
    "Lt. Surge": lambda player, opponent, logger: move_energy(
        source=player.bench, target=player.active_pokemon, energy_type="Lightning", logger=logger
    ),
    "Dome Fossil": lambda player, opponent, logger: play_as_pokemon(
        card=player.active_pokemon, logger=logger
    ),
    "Koga": lambda player, opponent, logger: retrieve_to_hand(
        player=player, card_name="Muk" if player.active_pokemon.name == "Muk" else "Weezing", logger=logger
    ),
    "Sabrina": lambda player, opponent, logger: switch_opponent_pokemon(
        opponent, logger=logger
    ),
    "Brock": lambda player, opponent, logger: attach_energy_to_specific_pokemon(
        energy_zone=player.energy, pokemon=player.active_pokemon, energy_type="Fighting", logger=logger
    )
}
