import asyncio
import pygame

from game.game import WrestlingGame


async def main():
    game = WrestlingGame()

    while game.running:
        game.handle_events()
        game.update()
        game.draw()
        game.clock.tick(60)

        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
