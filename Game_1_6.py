from game_objects import *


def main():
    game_over = True
    running = True
    player = None
    pygame.init()
    while running:
        if game_over:
            number_of_mobs, number_of_balloons, running = show_go_screen(player)
            game_over = False

            new_mine = Mine()
            mines.add(new_mine)
            all_sprites.add(new_mine)
            for i in range(number_of_mobs):
                new_mob(all_spr=all_sprites, mobs_=mobs)
            for i in range(number_of_balloons):
                create_balloon(all_spr=all_sprites, balloons_=balloons)
            player = Ship()
            Speed = Speedometer(player)
            all_sprites.add(player)
            all_sprites.add(Speed)
            score = 0

        if Mob.total + Balloon.total <= 0:
            game_over = True

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            key_state = pygame.key.get_pressed()
            if key_state[pygame.K_q]:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    stop_the_game()

        new_mine.event += 1
        if new_mine.event == FPS * 5 and new_mine.hidden:
            new_mine.move_up(player=player)
            new_mine.event = 0
            new_mine.hidden = False
        if new_mine.event == FPS * 10 and not new_mine.hidden:
            new_mine.move_down()
            new_mine.event = 0
            new_mine.hidden = True

        all_sprites.update()
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += int(Mob.POINTS / hit.size)
            play_animation_on_hit(hit.rect.center, 'small', all_spr=all_sprites)
            hit.die()
            Mob.total -= 1
            if random.random() > 0.6:
                new_pow = Pow(hit.rect.center)
                all_sprites.add(new_pow)
                powerups.add(new_pow)

        hits = pygame.sprite.groupcollide(balloons, bullets, True, True)
        for hit in hits:
            score += 100
            play_animation_on_hit(hit.rect.center, 'small', all_spr=all_sprites)
            new_bomb = Bomb(hit.rect.x, hit.rect.y)
            new_bomb.speed_y = -30
            all_sprites.add(new_bomb)
            bombs.add(new_bomb)
            Balloon.total -= 1

        hits = pygame.sprite.groupcollide(mobs, rockets, True, True)
        for hit in hits:
            score += int(Mob.POINTS / hit.size)*5
            play_animation_on_hit(hit.rect.center, 'large', all_spr=all_sprites)
            hit.kill()
            Mob.total -= 1

        hits = pygame.sprite.groupcollide(balloons, rockets, True, True)
        for hit in hits:
            score += 300
            play_animation_on_hit(hit.rect.center, 'large', all_spr=all_sprites)
            hit.kill()
            Balloon.total -= 1

        hits = pygame.sprite.spritecollide(player, bombs, True)
        for hit in hits:
            bomb_damage = random.randint(Bomb.min_damage, Bomb.max_damage)
            play_animation_on_hit(hit.rect.center, 'player', all_spr=all_sprites)
            player.receive_damage(bomb_damage)
            game_over = is_player_alive(player=player, hit=hit)

        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'health':
                player.health += random.randrange(30, 50)
                if player.health >= 100:
                    player.health = 100
            if hit.type == 'gun':
                player.powerup()
            if hit.type == 'rocket':
                player.count_rocket += 1

        hits = pygame.sprite.spritecollide(player, mines, True)
        for hit in hits:
            mine_damage = random.randint(Mine.min_damage, Mine.max_damage)
            play_animation_on_hit(hit.rect.center, 'player', all_spr=all_sprites)
            player.receive_damage(mine_damage)
            game_over = is_player_alive(player=player, hit=hit)
            new_mine.kill()
            if not game_over:
                new_mine = Mine()
                all_sprites.add(new_mine)
                mines.add(new_mine)

        screen.blit(background['game'], background_rect)
        all_sprites.draw(screen)
        draw_health_bar(screen, 5, 5, player.health)
        draw_text(screen, str(score), 28, WIDTH / 2, 20)
        draw_lives(screen, WIDTH - 100, 5, player.lives)
        draw_rockets(5, HEIGHT-20, player.count_rocket)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
