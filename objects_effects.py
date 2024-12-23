from effects import heal_target, shuffle_hand_and_draw

object_effects = {
    "Potion": lambda player, opponent, logger: heal_target(player.active_pokemon, amount=20, logger=logger),
    "Red Card": lambda player, opponent, logger: shuffle_hand_and_draw(opponent, draw_count=3, logger=logger),
}
