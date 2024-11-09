# importing libraries
import pygame
import time
import random


# Window size
window_x = 700
window_y = 700
game_x = 500
game_y = 500
game_border_x = game_x + 20
game_border_y = game_y + 20

# defining colors
beige = pygame.Color(250, 235, 215)
mud = pygame.Color(139, 131, 120)
khaki = pygame.Color(205, 192, 176)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Catch The Treats')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# set up elements
dog_size = 90
dog_rect = pygame.Rect(0, 0, dog_size, dog_size)

heart_size = 70
hearts = 3

treat_size = [30, 15]
treat1_rect = pygame.Rect(0, 0, treat_size[0], treat_size[1])
treat2_rect = pygame.Rect(0, 0, treat_size[0], treat_size[1])
heart_treat_rect = pygame.Rect(0, 0, heart_size, heart_size)

point_size = 50
point_rect = pygame.Rect(0, 0, point_size, point_size)

# load dog frames
dog_sitting1 = pygame.image.load('nini-sitting1.png').convert_alpha()
dog_sitting2 = pygame.image.load('nini-sitting2.png').convert_alpha()
dog_walking1 = pygame.image.load('nini-walking1.png').convert_alpha()
dog_walking2 = pygame.image.load('nini-walking2.png').convert_alpha()

# load heart frames
heart_full = pygame.image.load('heart-full.png').convert_alpha()
heart_empty = pygame.image.load('heart-empty.png').convert_alpha()

# load treat frame
treat = pygame.image.load('treat.png').convert_alpha()

# resize frames
dog_sitting1 = pygame.transform.scale(dog_sitting1, dog_rect.size)
dog_sitting2 = pygame.transform.scale(dog_sitting2, dog_rect.size)
dog_walking_right1 = pygame.transform.scale(dog_walking1, dog_rect.size)
dog_walking_right2 = pygame.transform.scale(dog_walking2, dog_rect.size)
dog_walking_left1 = pygame.transform.flip(dog_walking_right1, True, False)
dog_walking_left2 = pygame.transform.flip(dog_walking_right2, True, False)

heart_full = pygame.transform.scale(heart_full, (heart_size, heart_size))
heart_empty = pygame.transform.scale(heart_empty, (heart_size, heart_size))

treat = pygame.transform.scale(treat, (treat_size[0], treat_size[1]))

# animation list
# action 0 = sitting
# action 1 = walking right
# action 2 = walking left
dog = [ [dog_sitting1, dog_sitting2], 
					[dog_walking_right1, dog_walking_right2], 
					[dog_walking_left1, dog_walking_left2] ]

health = [heart_full, heart_empty]
							
# initiate starting frame for each action
frame = 0

update_time = time.time()
frame_rate = 0.3

# set default values
dog_rect.midbottom = (window_x // 2, window_y - 10)
direction = 'IDLE'
action = 0
hit = 0
score = 0
game_speed = 9
treat1_drop_speed = random.randrange(7, 11, 1)
treat2_drop_speed = random.randrange(7, 11, 1)
heart_drop_speed = random.randrange(7, 11, 1)
hit_bottom1 = False
hit_bottom2 = False
hit_bottom_heart = False
spawn_second = False
heart_treat = False
point_font_size = 30
opacity = 255


treat1_rect.midbottom = (random.randrange((window_x - game_x) // 2 + dog_size // 2, 
																		(window_x - game_x) // 2 + game_x - dog_size // 2, treat_size[0]), 
																	 	window_y - game_border_y + 10)
treat2_rect.midbottom = (random.randrange((window_x - game_x) // 2 + dog_size // 2, 
																		(window_x - game_x) // 2 + game_x - dog_size // 2, treat_size[0]), 
																	 	window_y - game_border_y +10)
heart_treat_rect.midbottom = (random.randrange((window_x - game_x) // 2 + dog_size // 2, 
																		(window_x - game_x) // 2 + game_x - dog_size // 2, heart_size), 
																	 	window_y - game_border_y +10)


running = True



# displaying Score function
def show_score(color, font, size):
  
    # creating font object score_font 
    score_font = pygame.font.SysFont(font, size, bold = True)
    
    # create the display surface object
    # score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)
    
    # create a rectangular object for the 
    # text surface object
    score_rect = score_surface.get_rect()
    score_rect = ((window_x - game_border_x) // 2, 
											 window_y - game_border_y - size - 10)
    # displaying text
    game_window.blit(score_surface, score_rect)
	


# display effect when catched a treat
def get_point(color, font, size, opacity, point_box, point):
	
	# creating font object score_font 
    point_font = pygame.font.SysFont(font, size, bold = True)
    
    # create the display surface object
    point_surface = point_font.render('+' + str(point), True, color)
    font_rect = point_surface.get_rect()
    point_surface.set_alpha(opacity)
    
    # displaying text
    if opacity >= 30:
    	opacity -= 30
    	size += 7
    	point_surface.set_alpha(opacity)
    	point_box.y -= 11
    	font_rect.center = point_box.center
    	game_window.blit(point_surface, font_rect)
    else:
    	size += 7
    	point_surface.set_alpha(0)
    	point_box.y -= 11
    	font_rect.center = point_box.center
    	game_window.blit(point_surface, font_rect)
    	
    return opacity, size, point_box



# display current health
def health_check(max_health, damage):
	
	full_heart = max_health
	for i in range(max_health):
		heart_rect = pygame.Rect((window_x - game_border_x) // 2 + game_border_x - heart_size * (i + 1), 
																			  		window_y - game_border_y - heart_size + 10, 
																			  		heart_size, heart_size)
		if full_heart - damage > 0:
			game_window.blit(health[0], heart_rect)
			full_heart -= 1
		else:
			game_window.blit(health[1], heart_rect)



# show branding
def branding(color, font, size):
  
    # creating font object branding_font 
    branding_font = pygame.font.SysFont(font, size, bold = True)
    
    # create the display surface object
    branding_surface = branding_font.render('VaLeHo', True, color)
    branding_surface = pygame.transform.rotate(branding_surface, 90)
    
    # create a rectangular object for the 
    # text surface object
    branding_rect = branding_surface.get_rect()
    branding_rect.right = (window_x - game_border_x) // 2
    branding_rect.bottom = window_y
    # displaying text
    game_window.blit(branding_surface, branding_rect)



# display dog animation based on action
def dog_animation(action, frame, update_time):
  	
  	current_time = time.time()
  	if current_time - update_time >= frame_rate:
  		frame = (frame + 1) % len(dog[action])
  		update_time = current_time
  	
  	game_window.blit(dog[action][frame], dog_rect)
  	
  	return frame, update_time
 
 
 
# control treat drop
def treat_drop(type, treat_rect, top, bottom, speed, hit_bottom):
	
	hit_bottom = False
	
	# treat won't show until they enter the game window	
	if treat_rect.top < top:	
		clip_rect = treat_rect.clip(game_rect)
		display_area = (0, treat_rect.height - clip_rect.height, clip_rect.width, clip_rect.height)	
		game_window.blit(type, clip_rect, display_area)
	else:
		game_window.blit(type, treat_rect)
		
	# treat will drop until it hit the floor
	if treat_rect.bottom < bottom:
		treat_rect.bottom += speed
	else:
		hit_bottom = True
		
	return hit_bottom, treat_rect
 
 

# game reset function
def game_reset():
    
    global direction, dog_rect
    global action
    global hit
    global score
    global hit_bottom1, hit_bottom2, hit_bottom_heart
    global spawn_second, heart_treat
    global opacity, point_font_size
    
    direction = 'IDLE'
    action = 0
    hit = 0
    score = 0
    hit_bottom1 = False
    hit_bottom2 = False
    hit_bottom_heart = False
    spawn_second = False 
    heart_treat = False
    opacity = 255
    point_font_size = 30
    
    dog_rect.midbottom = (window_x // 2, window_y - 10)
    
    treat1_rect.midbottom = (random.randrange((window_x - game_x) // 2 + dog_size // 2, (window_x - game_x) // 2 + game_x - dog_size // 2, treat_size[0]), window_y - game_border_y + 10)
    treat2_rect.midbottom = (random.randrange((window_x - game_x) // 2 + dog_size // 2, (window_x - game_x) // 2 + game_x - dog_size // 2, treat_size[0]), window_y - game_border_y + 10)
    heart_treat_rect.midbottom = (random.randrange((window_x - game_x) // 2 + dog_size // 2, (window_x - game_x) // 2 + game_x - dog_size // 2, heart_size), window_y - game_border_y + 10)
    

  
   
# game over function
def game_over(game_box):
    count_down = 10
    # creating font
    game_over_font = pygame.font.SysFont('Roboto', 50, bold = True)
    game_reset_font = pygame.font.SysFont('Roboto', 27)
    count_down_font = pygame.font.SysFont('Roboto', 170, bold = True)
    
    # creating a text surface on which text will be drawn
    game_over_surface = game_over_font.render('Your Score is : ' + str(score), True, mud)
    game_reset_surface = game_reset_font.render('Continue ? (press any key) ', True, mud)
    
    
    # create a rectangular object for the text surface object
    game_over_rect = game_over_surface.get_rect()
    game_reset_rect = game_reset_surface.get_rect()
    
    # setting position of the text
    game_over_rect.midtop = game_box.midtop
    game_over_rect.y += 50
    game_reset_rect.midtop = game_box.midtop
    game_reset_rect.y += 110
    
    # the game will close after 10 seconds
    while count_down >= 0 :
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
        # update count down surface
        count_down_surface = count_down_font.render(str(count_down), True, mud)
        count_down_rect = count_down_surface.get_rect()
        count_down_rect.midtop = game_box.midtop
        count_down_rect.y += 170
        
        
        pygame.draw.rect(game_window, beige, game_box)
        game_window.blit(game_over_surface, game_over_rect)
        game_window.blit(game_reset_surface, game_reset_rect)
        game_window.blit(count_down_surface, count_down_rect)
        
        # Update display and decrease countdown
        pygame.display.update()
        count_down -= 1
        
        time.sleep(1)
        
    pygame.quit()
    quit()        
       
        
                  
        
while True:
 	
 	# fill backgound and draw game window
 	game_window.fill(beige)
 	
 	game_border = pygame.Rect(0, 0, game_border_x, game_border_y)
 	game_border.midbottom = (window_x // 2, window_y)
 	pygame.draw.rect(game_window, mud, game_border)
 	
 	game_rect = pygame.Rect(0, 0, game_x, game_y)
 	game_rect.center = game_border.center
 	pygame.draw.rect(game_window, beige, game_rect)
 	
 	
 	# display score
 	show_score(mud, 'Roboto', 40)
 	
 	# display branding
 	branding(mud, 'Roboto', 50)
 	
 	for event in pygame.event.get():
 		if event.type == pygame.QUIT:
 				running = False
 		
 	# check key state for continuous movement
 	keys = pygame.key.get_pressed()		
 	
 	if keys[pygame.K_RIGHT]:
 		direction = 'RIGHT'
 		action = 1
 		dog_rect.x += 10
 	elif keys[pygame.K_LEFT]:
 		direction = 'LEFT'
 		action = 2
 		dog_rect.x -= 10	
 	else: 
 		direction = 'IDLE'
 		action = 0
 		
 	# limit dog movement inside game frame
 	if dog_rect.x <= game_rect.x :
 		direction = 'IDLE'
 		action = 0
 		dog_rect.x += 10
 	elif dog_rect.x + dog_size >= game_rect.x + game_x:
 		direction = 'IDLE'
 		action = 0
 		dog_rect.x -= 10
 	 
 	# dog animation
 	frame, update_time = dog_animation(action, frame, update_time)
 	
 	# there is a chance to spawn heart treat
 	if not heart_treat and random.randrange(1, 77, 1) == 7:
 			heart_treat = True
 	
 	# heart treat drop
 	if heart_treat:		
 		hit_bottom_heart, heart_treat_rect = treat_drop(heart_full, heart_treat_rect, game_rect.top, game_rect.bottom, heart_drop_speed, hit_bottom_heart)
 	
 	# drop heart treat doesn't cause damage
 	if hit_bottom_heart:
 		heart_treat = False
 		heart_treat_drop_speed = random.randrange(7, 11, 1)
 		heart_treat_rect.midbottom = (random.randrange((window_x - game_x) // 2 + dog_size // 2, 
																		(window_x - game_x) // 2 + game_x - dog_size // 2, heart_size), 
																	 	window_y - game_border_y + 10)

 	# getting health for heart treat
 	overlap_heart = dog_rect.clip(heart_treat_rect)	
 	if overlap_heart.height >= 15 and overlap_heart.width >= 15:
 		heart_treat_drop_speed = random.randrange(7, 11, 1)
 		heart_treat_rect.midbottom = (random.randrange((window_x - game_x) // 2 + dog_size // 2, 
 																			(window_x - game_x) // 2 + game_x - dog_size // 2, heart_size), 
 																			  window_y - game_border_y + 10)
 		if hit >=1:
	 		hit -= 1
	 	elif hit == 0:
	 		score += 30
	 		opacity = 255
	 		point_font_size = 30
	 		point_rect.midbottom = dog_rect.midtop
 			point3_float_time = time.time()
	 	heart_treat = False
	 	
	 # floating point after catched heart				
 	try:
 		if time.time() - point3_float_time < 0.7:	
 			opacity, point_font_size, point_rect = get_point(mud, 'Roboto', point_font_size, opacity, point_rect, 30)
 	except: pass
 	
 	# treat 1 drop
 	hit_bottom1, treat1_rect = treat_drop(treat, treat1_rect, game_rect.top, game_rect.bottom, treat1_drop_speed, hit_bottom1)
 	
 	if hit_bottom1:
 		hit += 1
 		treat1_drop_speed = random.randrange(7, 11, 1)
 		treat1_rect.midbottom = (random.randrange((window_x - game_x) // 2 + dog_size // 2, 
																			 (window_x - game_x) // 2 + game_x - dog_size // 2, treat_size[0]), 
																	 		  window_y - game_border_y +10)
 	
 	
	 	
 	# getting points for treat 1
 	overlap1 = dog_rect.clip(treat1_rect)	
 	if overlap1.height >= 15 and overlap1.width >= 15:
 		treat1_drop_speed = random.randrange(7, 11, 1)
 		treat1_rect.midbottom = (random.randrange((window_x - game_x) // 2 + dog_size // 2, 
 																			(window_x - game_x) // 2 + game_x - dog_size // 2, treat_size[0]), 
 																			  window_y - game_border_y +10)
 		score += 10
 		# set up position for point to appear
 		opacity = 255
 		point_font_size = 30
 		point_rect.midbottom = dog_rect.midtop
 		point1_float_time = time.time()
 		
 	# start delay time at a certain point 
 	if score >= 50 and not spawn_second:
 		spawn_time = time.time()
 		spawn_second = True
 	
 	# floating point after catched treat
 	try:				
 		if time.time() - point1_float_time < 0.7:	
 			opacity, point_font_size, point_rect = get_point(mud, 'Roboto', point_font_size, opacity, point_rect, 10)
 	except: pass
 	
 	# spawn second treat after a delay
 	if spawn_second and time.time() - spawn_time >= 3.0:
 		hit_bottom2, treat2_rect = treat_drop(treat, treat2_rect, game_rect.top, game_rect.bottom, treat2_drop_speed, hit_bottom2)
 	if hit_bottom2:
 		hit += 1
 		treat2_drop_speed = random.randrange(7, 11, 1)
 		treat2_rect.midbottom = (random.randrange((window_x - game_x) // 2 + dog_size // 2, 
																			 (window_x - game_x) // 2 + game_x - dog_size // 2, treat_size[0]), 
																	 		  window_y - game_border_y +10)
 	
 	# getting points for treat 2
 	overlap2 = dog_rect.clip(treat2_rect)
 	if overlap2.height >= 15 and overlap2.width >= 15:
 		treat2_drop_speed = random.randrange(7, 11, 1)
 		treat2_rect.midbottom = (random.randrange((window_x - game_x) // 2 + dog_size // 2, 
 																			(window_x - game_x) // 2 + game_x - dog_size // 2, treat_size[0]), 
 																			  window_y - game_border_y +10)
 		score += 10
 		# set up position for point to appear
 		opacity = 255
 		point_font_size = 30
 		point_rect.midbottom = dog_rect.midtop
 		point2_float_time = time.time()
 	
 	# floating point after catched treat 2
 	try:				
 		if time.time() - point2_float_time < 0.7:	
 			opacity, point_font_size, point_rect = get_point(mud, 'Roboto', point_font_size, opacity, point_rect, 10)
 	except: pass
 	
 	# display health
 	health_check(hearts, hit)	
 	# game ends if take more than 3 hits
 	if hit >= 3:
 		game_over(game_rect)
 		game_reset()
 						
 	pygame.display.update()
 	fps.tick(game_speed)

pygame.quit()