init python:

    def get_act(character, tags): # copypaste from jobs without the self part, allows to randomly select one of existing tags sets
            acts = list()
            for t in tags:
                if isinstance(t, tuple):
                    if character.has_image(*t):
                        acts.append(t)
                elif isinstance(t, dict):
                    if character.has_image(*t.get("tags", []), exclude=t.get("exclude", [])) and dice(t.get("dice", 100)):
                        acts.append(t)
                
            if acts:
                act = choice(acts)
            else:
                act = None
                
            return act
# lines for the future male libido
# You're a little out of juice at the moment, you might want to wait a bit.
# The spirit is willing, but the flesh is spongy and bruised.
screen int_libido_level(libido):
    hbox:
        xpos 5
        ypos 55
        vbox:
            fixed:
                xysize (150, 25)
                yfill True
                bar:
                    yalign 1.0
                    left_bar ProportionalScale("content/gfx/interface/bars/hp1.png", 150, 20)
                    right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                    value libido
                    range max_sex_scene_libido
                    thumb None
                    xysize (150, 20)
                text "Libido" size 14 color ivory bold True yalign 0.2 xpos 7
label interactions_hireforsex: # we go to this label from GM menu hire for sex. it's impossible to hire lovers, however they never refuse to do it for free, unless too tired or something like that
    "You propose to pay her for sex."
    $ interactions_check_for_bad_stuff(char)
    if char.flag("quest_cannot_be_fucked") == True:
        call int_sex_nope
        jump girl_interactions
    if char.disposition<0: # for negative disposition
        if dice(abs(char.disposition)-200): # if it's low enough to make the dice work she refuses, 100% chance at -300 disposition
            call int_sex_nope
            $ char.disposition -= randint(15, 35)
            jump girl_interactions
    elif char.vitality < 60: # no sex with low vitality
        call int_refused_because_tired
        jump girl_interactions
    $ price = 100 #a placeholder, the price should be close to whore job prices, which are calculated weirdly atm
    if price <= 0:
        "You managed to charm her and get free service."
        jump interactions_sex_scene_select_place
    else:
        if check_friends(char, hero):
            $ price = round(price * 0.7)
        if ct("Lesbian"):
            $ price = round(price * 1.5)
        if ct("Nymphomaniac"):
            $ price = round(price * 0.9)
        elif ct("Frigid"):
            $ price = round(price * 1.1)
           
    if ct("Impersonal"): 
        $rc("Affirmative. It will be %d G." % price, "Calculations completed. %d G to proceed." % price)
    elif ct("Shy") and dice(50):
        $rc("S-sure. %d G, please." % price, "*blushes* I-i-it will be %d G..." % price)
    elif ct("Imouto"):
        $rc("Mmm, I think it should be %d G... No, wait, it will be %d G. I'm not very good with this stuff, hehe ♪" % (abs(price-randint(15,35)), price), "Ooh, you want to do 'it' with me, don't you? Ok, but it will cost you %d G." % price) 
    elif ct("Dandere"):
        $rc("I see. I shall do it for %d G." % price, "*she nods* %d G." % price)
    elif ct("Tsundere"):
        $rc("I'll do it for %d G. You better be thankful for my low prices." % price, "Fine, fine. I hope you have %d G then." % price)
    elif ct("Kuudere"):
        $rc("It will be %d. And no funny business, understood?" % price, "It will cost you %d G. Do you have so much money?" % price)
    elif ct("Kamidere"):
        $rc("What's that? You want to hire me? I want %d G then, money up front." % price, "Hm? You want my body? Well of course you do. %d G, and you can have it." % price)
    elif ct("Bokukko"):
        $rc("Sure thing. That will cost ya %d G." % price, "What'ya wanna? Ohoh, you wanna me, don't you? ♪ Alrighty, %d G and we good to go.")
    elif ct("Ane"):
        $rc("Let's see... How about %d G? Can you afford me? ♪" % price, "Hm? What's the matter? Need some... special service? For you my price is %d G ♪" % price)
    elif ct("Yandere"):
        $rc("Fine, I want %d G. No bargaining." % price, "Well, I suppose we can, if you want to... It will cost %d G." % price)
    else:
        $rc("You want to hire me? Very well, it will be %d G." % price, "Of course. For you my body costs %d G." % price)
    if hero.gold < price:
        "You don't have that much money."
        call int_girl_dissapointed
        $ del price
        jump girl_interactions
    else:
        menu:
            "She wants [price] G. Do you want to pay her?"
            
            "Yes":
                if hero.take_money(price):
                    $ char.add_money(price)
                else:
                    "You don't have that much money."
                    call int_girl_dissapointed
                    $ del price
                    jump girl_interactions
            "No":
                "You changed your mind."
                $ char.disposition -= randint(1, 3)
                call int_girl_dissapointed
                $ del price
                jump girl_interactions
    $ del price
    
label intro_story:
    $ m = 800/300
    "[m]"
    $ m = 300/800
    "[m]"
    $ m = 800//300
    "[m]"
    $ m = (800*1.0)/300
    "[m]"
    $ m = (800*1.0)/(300*1.0)
    "[m]"
    $ m = 800/(300*1.0)
    "[m]"
    $ m = (800*1.0)//300
    "[m]"
    $ m = (800*1.0)//(300*1.0)
    "[m]"
    $ m = 800//(300*1.0)
    "[m]"
    $ del m
    jump dev_testing_menu
label interactions_sex_scene_select_place: # we go here if price for hiring is less than 0, ie no money checks and dialogues required; or after money check was successful
    if ct("Shy") or ct("Dandere"):
        "[char.name] is too shy to do it anywhere. You go to her room."
        show bg girl_room with fade
        $ sex_scene_location="room"
    else:
        menu:
            "Where would you like to do it?"
            
            "Beach":
                show bg city_beach with fade
                "You are going to the beach, to one of the secluded places away from people."
                $ sex_scene_location=="beach"
            "Park":
                show bg city_park with fade
                "You are going to the park, to the thick bushes away from people."
                $ sex_scene_location=="park"
            "Room":
                show bg girl_room with fade
                "You are going to her room."
                $ sex_scene_location=="room"
    $ sex_scene_libido = 0
    jump interactions_sex_scene_begins
                    
label interactions_sex: # we go to this label from GM menu propose sex
    "You propose [char.name] to have sex."
    $ interactions_check_for_bad_stuff(char)
    $ interactions_check_for_minor_bad_stuff(char)
    if char.flag("quest_cannot_be_fucked") == True: # a special flag for chars we don't want to be accessible unless a quest will be finished
        call int_sex_nope
        jump girl_interactions
    if ct("Lesbian"):
        call lesbian_refuse_because_of_gender # you can hire them, but they will never do it for free with wrong orientation
        jump girl_interactions
    if char.vitality < 60:
        call int_refused_because_tired
        jump girl_interactions
        
    $ sub = check_submissivity(char)
    $ sex_scene_libido = 0 # local, internal libido stat, based on traits and flags
    if check_lovers(char, hero): # a clear way to calculate how much disposition is needed to make her agree
        $ disposition_level_for_sex = randint(0, 100) + sub*200 # probably a placeholder until it becomes more difficult to keep lover status
    else:
        $ disposition_level_for_sex = randint(600, 700) + sub*200 # thus weak willed characters will need from 400 to 500 disposition, strong willed ones from 800 to 900, if there are no other traits that change it
        
    if ct("Frigid"):
        $ disposition_level_for_sex += randint(100, 200) # and it's totally possible that with some traits and high character stat the character will never agree, unless lover status is involved
    elif ct("Nymphomaniac"):
        $ disposition_level_for_sex -= randint(100, 200)
    
    if char.status == "slave":
        $ disposition_level_for_sex -= randint(50, 100)
    
    if char.flag("quest_sex_anytime"): # special flag for cases when we don't want character to refuse unless disposition is ridiculously low
        $ disposition_level_for_sex -= 1000
        
    if cgo("SIW"): # SIWs won't be against it if they know MC well, but at the same time would prefer to be paid if they don't
        if char.disposition >= 400:
            $ disposition_level_for_sex += randint(50, 100)
        else:
            $ disposition_level_for_sex -= randint(50, 100)
    # so normal (without flag) required level of disposition could be from 200 to 1200 for non lovers
    if disposition_level_for_sex < 100:
        $ disposition_level_for_sex = 100 # normalisation, no free sex with too low disposition no matter the character
    if char.disposition < disposition_level_for_sex:
        call int_sex_nope
        $ dif = disposition_level_for_sex - char.disposition # the difference between required for sex and current disposition
        if dif < 40:
            $ char.disposition -= randint(1, dif+1) # if it's low, then disposition penalty will be low too
        else:
            $ char.disposition -= randint(15, (45+15*sub)) # otherwise it will be significant
        $ del dif
        $ del disposition_level_for_sex
        jump girl_interactions
    else:
        $ dif = (char.disposition - disposition_level_for_sex) // 300
        $ sex_scene_libido += dif # the positive difference might give a bit of additional libido, 1 point per 300
    $ del disposition_level_for_sex
    $ del dif
    if check_friends(char, hero) or ct("Nymphomaniac") or check_lovers(char, hero) or char.disposition >= 600:
        menu:
            "Where would you like to do it?"
            
            "Beach":
                show bg city_beach with fade
                "You are going to the beach, to one of the secluded places away from people."
                $ sex_scene_location = "beach"
            "Park":
                show bg city_park with fade
                "You are going to the park, to the thick bushes away from people."
                $ sex_scene_location = "park"
            "Room":
                show bg girl_room with fade
                "You are going to her room."
                $ sex_scene_location = "room"
    elif (char.status == "slave") and (ct("Shy") or ct("Dandere")):
        "She is too shy to do it anywhere. You can force her nevertheless, but she prefers her room."
        menu:
            "Where would you like to do it?"
            "Beach":
                show bg city_beach with fade
                "You are going to the beach, to one of the secluded places away from people."
                $ sex_scene_location="beach"
                if ct("Masochist"):
                    $ sex_scene_libido += 1
                else:
                    $ sex_scene_libido -= 2
            "Park":
                show bg city_park with fade
                "You are going to the park, to the thick bushes away from people."
                $ sex_scene_location=="park"
                if ct("Masochist"):
                    $ sex_scene_libido += 1
                else:
                    $ sex_scene_libido -= 2
            "Room":
                show bg girl_room with fade
                "You are going to her room."
                $ sex_scene_location=="room"
    elif ct("Shy") or ct("Dandere"):
        "She's too shy to do it anywhere. You go to her room."
        show bg girl_room with fade
        $ sex_scene_location="room"
    elif ct("Homebody"):
        "She doesn't want to do it outdoors, so you go to her room."
        show bg girl_room with fade
        $ sex_scene_location="room"
    else:
        "She wants to do it in her room."
        show bg girl_room with fade
        $ sex_scene_location="room"

label interactions_sex_scene_begins: # here we set initial picture before the scene and set local variables
    $ scene_picked = 1
    $ sub = check_submissivity(char)
    if sex_scene_location == "beach": # here we make sure that all suitable pics with swimsuit have a chance to be shown
        $ tags = ({"tags": ["beach", "swimsuit"], "exclude": ["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"]}, {"tags": ["simple bg", "swimsuit"], "exclude": ["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"]}, {"tags": ["no bg", "swimsuit"], "exclude": ["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"]})
        $ result = get_act(char, tags)
        if result == tags[0]:
            $ gm.generate_img("beach", "swimsuit", "nude", exclude=["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"], type="reduce")
        elif result == tags[1]:
            $ gm.generate_img("swimsuit", "simple bg", "nude", exclude=["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"], type="reduce")
        elif result == tags[2]:
            $ gm.generate_img("swimsuit", "no bg", "nude", exclude=["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"], type="reduce")
        else:
            $ gm.generate_img("swimsuit", "nude", exclude=["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"], type="reduce")
    elif sex_scene_location == "park":
        if char.has_image("nature", exclude=["sex", "sleeping", "angry", "in pain", "sad", "scared", "indoors", "beach", "onsen", "pool", "stage", "dungeon", "bathing"]):
            $ gm.generate_img("nature", "nude", "urban", exclude=["sex", "sleeping", "angry", "in pain", "sad", "scared", "indoors", "beach", "onsen", "pool", "stage", "dungeon", "bathing"], type="reduce")
        else:
            $ gm.generate_img("nude", "simple bg", exclude=["sex", "sleeping", "angry", "in pain", "sad", "scared", "indoors", "beach", "onsen", "pool", "stage", "dungeon"], type="reduce")
    else: # it's a living room
        $ tags = ({"tags": ["living", "nude"], "exclude": ["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"]}, {"tags": ["living", "lingerie"], "exclude": ["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"]})
        $ result = get_act(char, tags)
        if result: # we prefer to show living pics
            if result == tags[0]:
                $ gm.generate_img("living", "nude", exclude=["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"], type="reduce")
            else:
                $ gm.generate_img("living", "lingerie", exclude=["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"], type="reduce")
        else: # no living pics, proceed to no bgs
            $ tags = ({"tags": ["no bg", "nude"], "exclude": ["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"]}, {"tags": ["no bg", "lingerie"], "exclude": ["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"]}, {"tags": ["simple bg", "lingerie"], "exclude": ["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"]}, {"tags": ["simple", "lingerie"], "exclude": ["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.generate_img("no bg", "nude", exclude=["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"], type="reduce")
                elif result == tags[1]:
                    $ gm.generate_img("no bg", "lingerie", exclude=["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"], type="reduce")
                elif result == tags[2]:
                    $ gm.generate_img("simple bg", "nude", exclude=["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"], type="reduce")
                else:
                    $ gm.generate_img("simple bg", "lingerie", exclude=["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"], type="reduce")
            else: # screw it, show the closest possible of remained ones
                $ gm.generate_img("indoors", "living", "indoor", "nude", exclude=["sex", "sleeping", "angry", "in pain", "outdoors", "beach", "onsen", "pool", "stage", "dungeon", "public", "bathing"], type="reduce")

    $ sex_count = guy_count = girl_count = together_count = cum_count = 0 # these variable will decide the outcome of sex scene
    if ct("Nymphomaniac"): # let's begin to modify libido based on traits
        $ sex_scene_libido += randint(5, 6)
    elif ct("Frigid"):
        $ sex_scene_libido += randint(1, 2)
    else:
        $ sex_scene_libido += randint(3, 4)
    if ct ("Messy") and dice(60):
        $ sex_scene_libido += 1
    if check_lovers(hero, char):
        $ sex_scene_libido += randint(1, 2)
    elif cgo("SIW"):
        $ sex_scene_libido += 1
    if ct("Extremely Jealous")and dice(40):
        $ sex_scene_libido += 1
    if ct("Virgin"):
        $ sex_scene_libido -= 1
    elif ct("MILF") and dice(70):
        $ sex_scene_libido += 1
    if ct("Undead"):
        $ sex_scene_libido -= 1
    elif ct("Furry"):
        $ sex_scene_libido += 1
    elif ct("Demonic Creature"):
        $ sex_scene_libido += 1
    if ct("Indifferent"):
        $ sex_scene_libido -= randint(0, 1)
    if ct("Impersonal"):
        $ sex_scene_libido -= 1
    if sex_scene_libido < 2:
        $ sex_scene_libido = 2 # normalization, at worst you will do it 2 times
    $ max_sex_scene_libido = sex_scene_libido
    # max is 12, min is 2
    call int_sex_ok
    jump interaction_scene_choice

    
label interaction_scene_choice: # here we select specific scene, show needed image, jump to scene logic and return here after every scene
    show screen int_libido_level(sex_scene_libido)
    if char.vitality <=10:
        jump interaction_scene_finish_sex
    if hero.vitality <= 30:
        "You are too tired to continue."
        jump interaction_scene_finish_sex
    if char.status == "slave":
        if sex_scene_libido <= 0:
            "[char.name] doesn't want to do it any longer. You can force her, but it will not be without consequences."
            jump interaction_sex_scene_choice
        if char.joy <= 20:
            "[char.name] looks upset. Not the best mood for sex. You can force her, but it will not be without consequences."
            jump interaction_sex_scene_choice
        if char.vitality <= 30:
            "[char.name] looks very tired. You can force her, but it's probably for the best to let her rest."
            jump interaction_sex_scene_choice
    else:
        if sex_scene_libido <= 0:
            "[char.name] doesn't want to do it any longer."
            jump interaction_scene_finish_sex
        elif char.joy <= 20:
            "[char.name] looks upset. Not the best mood for sex."
            jump interaction_scene_finish_sex
        if char.vitality < 30:
            "[char.name] is too tired to continue."
            jump interaction_scene_finish_sex
    if scene_picked == 0:
        $ scene_picked = 1
        if dice(sex_scene_libido*10 + 50*sub): # strong willed and/or very horny characters may pick action on their own from time to time
            $ available = list() # let's form a list of available actions
            if sex_scene_libido > 1:
                if (not(ct("Virgin")) or check_lovers(hero, char)) and current_action != "vag":
                    $ available.append("vag")
                if (char.has_image("2c anal", exclude=["rape", "angry", "scared", "in pain", "gay", "restrained"])) or (char.has_image("after sex", exclude=["angry", "in pain", "sad", "scared", "restrained"])) and current_action != "anal":
                    $ available.append("anal")
            if (char.has_image("bc blowjob", exclude=["rape", "in pain", "restrained"]) or (char.has_image("after sex", exclude=["angry", "in pain", "sad", "scared", "restrained"]))) and current_action != "blow":
                $ available.append("blow")
            if (char.has_image("bc titsjob", exclude=["rape", "in pain", "restrained"]) or (char.has_image("after sex", exclude=["angry", "in pain", "sad", "scared", "restrained"]))) and current_action != "tits":
                $ available.append("tits")
            if (char.has_image("bc handjob", exclude=["rape", "in pain", "restrained"])) or (char.has_image("after sex", exclude=["angry", "in pain", "sad", "scared", "restrained"])) and current_action != "hand":
                $ available.append("hand")
            if (char.has_image("bc handjob", exclude=["rape", "in pain", "restrained"])) or (char.has_image("after sex", exclude=["angry", "in pain", "sad", "scared", "restrained"])) and current_action != "foot":
                $ available.append("foot")
            if not(available):
                jump interaction_sex_scene_choice
            $ current_action = choice(available)
            if sub < 0:
                "She is so horny she cannot cannot control herself."
            elif sub == 0:
                "She wants to try out with you something else."
            else:
                "She wants to do something else with you."
            if current_action == "vag":
                if ct("Virgin"):
                    jump interaction_check_for_virginity
            jump interactions_sex_scene_logic_part
label interaction_sex_scene_choice:
    $ scene_picked = 0
    menu:
        "What would you like to do now?"
        
        "Ask for striptease": 
            $ current_action = "strip"
            jump interactions_sex_scene_logic_part
            
        "Ask her to play with herself" if char.has_image("masturbation", exclude=["forced", "normalsex", "group", "bdsm"]):
            $ current_action = "mast"
            jump interactions_sex_scene_logic_part
            
        "Ask for a blowjob" if (char.has_image("bc blowjob", exclude=["rape", "in pain", "restrained"]) or (char.has_image("after sex", exclude=["angry", "in pain", "sad", "scared", "restrained"]))): 
            $ current_action = "blow"
            jump interactions_sex_scene_logic_part
            
        "Ask for paizuri" if (char.has_image("bc titsjob", exclude=["rape", "in pain", "restrained"]) or (char.has_image("after sex", exclude=["angry", "in pain", "sad", "scared", "restrained"]))):
            $ current_action = "tits"
            jump interactions_sex_scene_logic_part
            
        "Ask for a handjob" if (char.has_image("bc handjob", exclude=["rape", "in pain", "restrained"])) or (char.has_image("after sex", exclude=["angry", "in pain", "sad", "scared", "restrained"])):
            $ current_action = "hand"
            jump interactions_sex_scene_logic_part
            
        "Ask for a footjob" if (char.has_image("bc footjob", exclude=["rape", "angry", "in pain", "restrained"], type="first_default")) or (char.has_image("after sex", exclude=["angry", "in pain", "sad", "scared", "restrained"])):
            $ current_action = "foot"
            jump interactions_sex_scene_logic_part
            
        "Ask for sex" if (char.has_image("2c vaginal", exclude=["rape", "angry", "scared", "in pain", "gay", "restrained"])) or (char.has_image("after sex", exclude=["angry", "in pain", "sad", "scared", "restrained"])):
            if ct("Virgin"):
                jump interaction_check_for_virginity
            else:
                call interaction_scene_vaginal
                $ current_action = "vag"
                jump interactions_sex_scene_logic_part
                
        "Ask for anal sex" if (char.has_image("2c anal", exclude=["rape", "angry", "scared", "in pain", "gay", "restrained"])) or (char.has_image("after sex", exclude=["angry", "in pain", "sad", "scared", "restrained"])):
            call interaction_scene_anal
            $ current_action = "anal"
            jump interactions_sex_scene_logic_part
            
        "That's all.":
            $ del current_action
            "You decided to finish."

            
label interaction_scene_finish_sex:
    hide screen int_libido_level
    if sex_scene_libido > 3 and char.vitality >= 70:
        call interaction_scene_mast
        "[char.name] is not satisfied yet, so she quickly masturbates to decrease libido."
        $ char.disposition -= round(sex_scene_libido*2)
    if (together_count > 0 and sex_count >=1) or (sex_count >=2 and girl_count >=1 and guy_count >= 1):
        if sex_scene_location == "beach":
            if char.has_image("profile", "beach", exclude=["angry", "sad", "scared", "in pain"]):
                $ gm.set_img("profile", "beach", "happy", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "happy", "beach", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
        elif sex_scene_location == "park":
            if char.has_image("profile", "nature", exclude=["angry", "sad", "scared", "in pain"]):
                $ gm.set_img("profile", "nature", "happy", "urban", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "happy", "nature", "urban", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
        else:
            if char.has_image("profile", "living", exclude=["angry", "sad", "scared", "in pain"]):
                $ gm.set_img("profile", "living", "happy", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "happy", "indoors", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
        call after_good_sex
        $ char.disposition += randint(20, 40)
        $ char.vitality -= randint(5, 10)
    elif girl_count < 1 and guy_count > 0:
        if sex_scene_location == "beach":
            if char.has_image("profile", "beach", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"]):
                $ gm.set_img("profile", "beach", "angry", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"])
            else:
                $ gm.set_img("girlmeets", "angry", "beach", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
        elif sex_scene_location == "park":
            if char.has_image("profile", "nature", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"]):
                $ gm.set_img("profile", "nature", "angry", "urban", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "angry", "nature", "urban", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
        else:
            if char.has_image("profile", "living", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"]):
                $ gm.set_img("profile", "living", "angry", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "angry", "indoors", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
            "She's not satisfied at all."
            call girl_never_come
            $ char.disposition -= randint(20, 50)
            $ char.joy -= randint(2, 5)
            $ char.vitality -= randint(5, 10)
    elif girl_count > 0 and guy_count < 1 and cum_count < 1 and sex_count > 0:
        if sex_scene_location == "beach":
            if char.has_image("profile", "beach", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"]):
                $ gm.set_img("profile", "beach", "sad", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"])
            else:
                $ gm.set_img("girlmeets", "sad", "beach", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
        elif sex_scene_location == "park":
            if char.has_image("profile", "nature", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"]):
                $ gm.set_img("profile", "nature", "sad", "urban", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "sad", "nature", "urban", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
        else:
            if char.has_image("profile", "living", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"]):
                $ gm.set_img("profile", "living", "sad", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "sad", "indoors", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
        "She was unable to satisfy you."
        call guy_never_came
        $ char.disposition += randint(10, 20)
        $ char.joy -= randint(10, 15)
        $ char.vitality -= randint(5, 15)
    elif (cum_count >=5) and (cum_count > girl_count):
        if sex_scene_location == "beach":
            if char.has_image("profile", "beach", exclude=["angry", "sad", "scared", "in pain"]):
                $ gm.set_img("profile", "beach", "shy", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "shy", "beach", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
        elif sex_scene_location == "park":
            if char.has_image("profile", "nature", exclude=["angry", "sad", "scared", "in pain"]):
                $ gm.set_img("profile", "nature", "shy", "urban", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "shy", "nature", "urban", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
        else:
            if char.has_image("profile", "living", exclude=["angry", "sad", "scared", "in pain"]):
                $ gm.set_img("profile", "living", "shy", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "shy", "indoors", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
        call guy_cum_alot
        $ char.disposition += randint(10, 20)
        $ char.vitality -= randint(5, 10)
    elif sex_count < 1:
        if sex_scene_location == "beach":
            if char.has_image("profile", "beach", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"]):
                $ gm.set_img("profile", "beach", "angry", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"])
            else:
                $ gm.set_img("girlmeets", "angry", "beach", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
        elif sex_scene_location == "park":
            if char.has_image("profile", "nature", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"]):
                $ gm.set_img("profile", "nature", "angry", "urban", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "angry", "nature", "urban", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
        else:
            if char.has_image("profile", "living", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"]):
                $ gm.set_img("profile", "living", "angry", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "angry", "indoors", exclude=["happy", "scared", "in pain", "ecstatic", "suggestive"], type="reduce")
        if char.status == "slave":
            "She is puzzled and confused by the fact that you didn't do anything. She quickly leaves, probably thinking that you teased her."
        else:
            "She is quite upset and irritated because you didn't do anything. She quickly leaves, probably thinking that you teased her."
            $ char.disposition -= randint(20, 50)
            $ char.joy -= randint(15, 30)
            $ char.vitality -= 5
    elif girl_count > 0 and sex_count < 1:
        if sex_scene_location == "beach":
            if char.has_image("profile", "beach", exclude=["angry", "sad", "scared", "in pain"]):
                $ gm.set_img("profile", "beach", "shy", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "shy", "beach", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
        elif sex_scene_location == "park":
            if char.has_image("profile", "nature", exclude=["angry", "sad", "scared", "in pain"]):
                $ gm.set_img("profile", "nature", "shy", "urban", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "shy", "nature", "urban", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
        else:
            if char.has_image("profile", "living", exclude=["angry", "sad", "scared", "in pain"]):
                $ gm.set_img("profile", "living", "shy", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "shy", "indoors", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
        "She did nothing but masturbated in front of you. Probably better than nothing, but be prepared for rumours about your impotence or orientation."
        $ char.disposition -= randint(10, 15)
        $ char.vitality -= 5
    else:
        if sex_scene_location == "beach":
            if char.has_image("profile", "beach", exclude=["angry", "sad", "scared", "in pain"]):
                $ gm.set_img("profile", "beach", "happy", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "happy", "beach", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
        elif sex_scene_location == "park":
            if char.has_image("profile", "nature", exclude=["angry", "sad", "scared", "in pain"]):
                $ gm.set_img("profile", "nature", "happy", "urban", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "happy", "nature", "urban", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
        else:
            if char.has_image("profile", "living", exclude=["angry", "sad", "scared", "in pain"]):
                $ gm.set_img("profile", "living", "happy", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
            else:
                $ gm.set_img("girlmeets", "happy", "indoors", exclude=["angry", "sad", "scared", "in pain"], type="reduce")
        "It was pretty good, and she looks quite pleased and satisfied. But there is room for improvement."
        $ char.disposition += randint(10, 20)
        $ char.vitality -= randint(5, 10)
    $ gm.restore_img()
    jump girl_interactions_end
            
label interactions_lesbian_choice:
    # The interactions itself.
    # Since we called a function, we need to do so again (Consider making this func a method so it can be called just once)...
    if ct("Lesbian") or ct("Bisexual"):
        if char.disposition <= 500 or not(check_friends(hero, char) or check_lovers(hero, char)):
            "Unfortunately she does not want to do it."
            jump interaction_scene_choice
        elif check_lovers(hero, char):
            "She gladly agrees to make a show for you."
        elif check_friends(hero, char) or char.disposition > 600:
            "A bit hesitant, she agrees to do it for you."
    else:
        if char.disposition <= 600 or not(check_friends(hero, char) or check_lovers(hero, char)) or not(cgo("SIW")): 
            "Unfortunately she does not like girls in this way."
            jump interaction_scene_choice
        elif check_lovers(hero, char):
                "She gladly agrees to make a show for you if there will be some straight sex as well today."
        elif (check_friends(hero, char) or char.disposition > 600) and cgo("SIW"):
                "She prefers men, but agrees to make a show for you if there will be some straight sex as well today."
    $ willing_partners = find_les_partners()
    
    # Single out one partner randomly from a set:
    $ char2 = random.sample(willing_partners, 1)[0]
    
    # We plainly hide the interactions screen to get rid of the image and gradient:
    hide screen pyt_girl_interactions
    
    $ char_sprite = char.get_vnsprite()
    $ char_sprite2 = char2.get_vnsprite()
    "[char.nickname] decided to call [char2.nickname] for the lesbo action!"
    
    show expression char_sprite at mid_left with dissolve
    char.say "We are going to do 'it'."
    show expression char_sprite at mid_right as char_sprite with move
    show expression char_sprite2 at mid_left as char_sprite2 with dissolve
    char2.say "And..."
    extend "(*looking at you*) Are you planning to watch?"
    
    hide char_sprite
    hide char_sprite2
    with dissolve
    
    # Resize images to be slightly smaller than half a screen in width and the screen in height. ProportionalScale will do the rest.
    $ resize = (config.screen_width/2 - 75, config.screen_height - 75)
    
    
    show expression char.show("nude", "simple bg", resize=resize, exclude=["sex", "sleeping", "angry", "in pain", "beach", "onsen", "pool", "stage", "dungeon", "bathing"], type="first_default") as xxx at Transform(align=(0, 0.5)) with moveinright
    show expression char2.show("nude", "simple bg", resize=resize, exclude=["sex", "sleeping", "angry", "in pain", "beach", "onsen", "pool", "stage", "dungeon", "bathing"], type="first_default") as xxx2 at Transform(align=(1.0, 0.5)) with moveinleft
    
    # Wait for 0.25 secs and add soundbyte:
    pause 0.25
    play events "female/orgasm.mp3"
    $ renpy.pause(5.0)
    hide xxx
    hide xxx2
    

    show expression char2.get_vnsprite() at left as char_sprite2 with dissolve
    show expression char.get_vnsprite() at right as char_sprite with dissolve
    if sex_scene_libido <= 0:
        $ char.vitality -= 20
        $ char.joy -= 5
    if char.joy <= 10:
        $ char.disposition -= 5
    if char.vitality <= 15 and char.health >= 50:
        $ char.health -= 2
    if char.oral < 100 and char.sex < 100 and char2.oral < 100 and char2.sex < 100:
        "They both were not skilled enough to give each other enough pleasure, no matter how they tried. That was quite awkward."
        $ char.oral += randint (0,1)
        $ char2.oral += randint (0,1)
        $ char.sex += randint (0,1)
        $ char2.sex += randint (0,1)
        $ char.vitality -= 20
        $ char2.vitality -= 20
        $ sex_scene_libido -= 5
        char2.say "..."
        char.say "Sorry..."
    elif char.oral < 100 and char.sex < 100:
        "[char.nickname] was not skilled enough to make her partner come. On the bright side, [char2.nickname] made her come a lot."
        $ char.oral += randint (2,4)
        $ char2.oral += randint (2,4)
        $ char.sex += randint (0,1)
        $ char2.sex += randint (0,1)
        $ char.vitality -= 20
        $ char2.vitality -= 15
        $ sex_scene_libido -= 10
        char.say "Sorry..."
        char2.say "Don't worry. You'll become better in time."
    elif char2.oral < 100 and char2.sex < 100:
        "[char2.nickname] was not skilled enough to make her partner come. On the bright side, [char.nickname] made her come a lot."
        $ char.oral += randint (2,4)
        $ char2.oral += randint (2,4)
        $ char.sex += randint (0,1)
        $ char2.sex += randint (0,1)
        $ char.vitality -= 20
        $ char2.vitality -= 15
        $ sex_scene_libido -= 10
        char2.say "I'm sorry..."
        char.say "Don't be. We had our fun (*looking at you*)."
    else:
        "They both come a lot. What a beautiful sight."
        $ char.oral += randint (2,4)
        $ char2.oral += randint (2,4)
        $ char.sex += randint (2,4)
        $ char2.sex += randint (2,4)
        $ char.vitality -= 15
        $ char2.vitality -= 15
        $ sex_scene_libido -= 10
        $ char.joy += 5
        $ char2.joy += 5
        char2.say "That... wasn't so bad."
        char2.say "We should do that again sometime ♪"
    hide char_sprite2 with dissolve
    hide char_sprite with dissolve
    
    # Restore the gm image:
    
    # Show the screen again:
    show screen pyt_girl_interactions
    
    # And finally clear all the variables for global scope:
    python:
        del resize
        del char2
        del willing_partners
        
    stop events
        
    # And we're all done!:
    jump interaction_scene_choice
    
    
label interactions_sex_scene_logic_part: # here we resolve all logic for changing stats and showing lines after picking a sex scene
    if sex_scene_libido <= 0:
        $ char.vitality -= randint(5, 25)
        $ char.joy -= randint(3, 6)
    if char.joy <= 10:
        $ char.disposition -= randint(5, 10)
    if char.vitality <= 15 and char.health >= 50:
        $ char.health -= 2
    $ sex_count += 1
    if current_action == "mast":
        call interaction_scene_mast
        "She masturbates in front of you." 
        if max_sex_scene_libido > sex_scene_libido and dice(40):
            extend " She is more aroused now."
            $ sex_scene_libido += 1
        $ char.vitality -= randint(5, 10)
        $ girl_count +=1
    elif current_action == "strip":
        call interaction_scene_strip
        "You ask her to show you a striptease."
        $ skill_for_checking = char.get_skill("strip")
        $ male_skill_for_checking = char.get_skill("strip")
        if skill_for_checking >= 2000:
            "She looks unbearably hot and sexy. After a short time you cannot withstand it anymore and begin to masturbate, quickly coming. She looks at you with a smile and superiority in her eyes."
        elif skill_for_checking >= 1000:
            "Her movements are so fascinating that you cannot look away from her. She looks proud and pleased."
        elif skill_for_checking >= 500:
            "It's nice to look at her graceful and elegant moves."
        elif skill_for_checking >= 200:
            "She did her best to show you her body, but her skills could definitely be improved."
        elif skill_for_checking >= 50:
            "She tried her best, but the moves were quite clumsy and unnatural. At least she learned something new today."
        else:
            "Looks like [char.name] barely knows what she's doing. Even just standing still without clothes would made a better impression..."
        if dice(20):
            $ char.strip += 1
        if dice(10):
            $ hero.strip += 1
        if (skill_for_checking - male_skill_for_checking) > 250 and dice(50):
            $ hero.strip += 1
        if (male_skill_for_checking - skill_for_checking) > 250 and dice(75):
            $ char.strip += 1
    elif current_action == "blow":
        call interaction_scene_blowjob
        $ image_tags = gm.img.get_image_tags()
        if ct("Lesbian"):
            $ skill_for_checking = round(char.get_skill("oral")*0.65 + char.get_skill("sex")*0.1)
        else:
            $ skill_for_checking = round(char.get_skill("oral")*0.8 + char.get_skill("sex")*0.2)
        $ male_skill_for_checking = round(hero.get_skill("oral")*0.8 + hero.get_skill("sex")*0.2)
        if sub > 0:
            "[char.name] licks her lips, defiantly looking at your crotch."
            if "bc deepthroat" in image_tags:
                extend " She shoves it all the way into her throat."
            elif "after sex" in image_tags:
                extend " She enthusiastically begins to lick and suck it."
            else:
                extend " She enthusiastically begins to lick and suck it."
        elif sub < 0:
            "Glancing at your crotch, [char.name] is patiently waiting for your orders."
            if "bc deepthroat" in image_tags:
                extend " You told her to take your dick inside her mouth as deeply as she can, and she diligently obeyed."
            elif "after sex" in image_tags:
                extend " You told her to lick and suck your dick."
            else:
                extend " You told her to lick and suck your dick, and she immediately obeyed."
        else:
            "[char.name] slowly approached your crotch."
            if "bc deepthroat" in image_tags:
                extend " You shove your dick deeply into her throat."
            elif "after sex" in image_tags:
                extend " She begins to lick and suck your dick."
            else:
                extend " She begins to lick and suck your dick."
        call interaction_sex_scene_check_skill_jobs
        if dice(20):
            $ char.oral += 1
        if dice(10):
            $ hero.oral += 1
        if (skill_for_checking - male_skill_for_checking) > 250 and dice(50):
            $ hero.oral += 1
        if (male_skill_for_checking - skill_for_checking) > 250 and dice(75):
            $ char.oral += 1
        if dice(10):
            $ char.sex += 1
        if dice(5):
            $ hero.sex += 1
    elif current_action == "tits":
        call interaction_scene_titsjob
        $ image_tags = gm.img.get_image_tags()
        if sub > 0:
            "[char.name] massages her boobs, defiantly looking at your crotch."
        elif sub < 0:
            "Holding her boobs, [char.name] meekly approaches you."
        else:
            "[char.name] playfully grabs her boobs, looking at you."
        if ct("Big Boobs"):
            extend " She warps her soft big breasts around you."
        elif ct("Abnormally Large Boobs"):
            extend " You almost lost yourself in her enormous breasts as they envelop you."
        elif ct("Small Boobs"):
            extend " She begins to assiduously rub her small breasts around you."
        else:
            extend " She squeezes you between her soft breasts."
        if ct("Lesbian"):
            $ skill_for_checking = round(char.get_skill("oral")*0.6 + char.get_skill("sex")*0.1)
        else:
            $ skill_for_checking = round(char.get_skill("oral")*0.75 + char.get_skill("sex")*0.25)
        $ male_skill_for_checking = round(hero.get_skill("oral")*0.75 + hero.get_skill("sex")*0.25)
        if dice(20):
            $ char.oral += 1
        if dice(10):
            $ hero.oral += 1
        if (skill_for_checking - male_skill_for_checking) > 250 and dice(50):
            $ hero.oral += 1
        if (male_skill_for_checking - skill_for_checking) > 250 and dice(75):
            $ char.oral += 1
        if dice(10):
            $ char.sex += 1
        if dice(5):
            $ hero.sex += 1
        call interaction_sex_scene_check_skill_jobs
    elif current_action == "hand":
        call interaction_scene_handjob
        $ image_tags = gm.img.get_image_tags()
        if sub > 0:
            "[char.name] grabs you with her soft hands."
        elif sub < 0:
            "[char.name] wraps her soft hands around your dick."
        else:
            "[char.name] takes your dick in her soft hands."
        if ct("Lesbian"):
            $ skill_for_checking = round(char.get_skill("oral")*0.1 + char.get_skill("sex")*0.6)
        else:
            $ skill_for_checking = round(char.get_skill("oral")*0.25 + char.get_skill("sex")*0.75)
        $ male_skill_for_checking = round(hero.get_skill("oral")*0.25 + hero.get_skill("sex")*0.75)
        if dice(20):
            $ char.sex += 1
        if dice(10):
            $ hero.sex += 1
        if (skill_for_checking - male_skill_for_checking) > 250 and dice(50):
            $ hero.sex += 1
        if (male_skill_for_checking - skill_for_checking) > 250 and dice(75):
            $ char.sex += 1
        if dice(10):
            $ char.oral += 1
        if dice(5):
            $ hero.oral += 1
        call interaction_sex_scene_check_skill_jobs
    elif current_action == "foot":
        call interaction_scene_footjob
        $ image_tags = gm.img.get_image_tags()
        if sub > 0:
            "With a sly smile [char.name] gets closer to you."
        elif sub < 0:
            "You asked [char.name] to use her feet."
        else:
            "[char.name] sits next to you."
        if ct("Athletic"):
            if ct("Long Legs"):
                "She squeezes your dick her between her long muscular legs and stimulates it until you come."
            else:
                "She squeezes your dick her between her muscular legs and stimulates it until you come."
        elif ct("Slim"):
            if ct("Long Legs"):
                "She squeezes your dick her between her long slim legs and stimulates it until you come."
            else:
                "She squeezes your dick her between her slim legs and stimulates it until you come."
        elif ct("Lolita"):
            if ct("Long Legs"):
                "She squeezes your dick her between her long thin legs and stimulates it until you come."
            else:
                "She squeezes your dick her between her thin legs and stimulates it until you come."
        else:
            if ct("Long Legs"):
                "She squeezes your dick her between her long legs and stimulates it until you come."
            else:
                "She squeezes your dick her between her legs and stimulates it until you come."
        if "after sex" in image_tags:
            extend " You generously cover her body with your thick liquid."
        if ct("Lesbian"):
            $ skill_for_checking = round(char.get_skill("oral")*0.1 + char.get_skill("sex")*0.6)
        else:
            $ skill_for_checking = round(char.get_skill("oral")*0.25 + char.get_skill("sex")*0.75)
        $ male_skill_for_checking = round(hero.get_skill("oral")*0.25 + hero.get_skill("sex")*0.75)
        if dice(20):
            $ char.sex += 1
        if dice(10):
            $ hero.sex += 1
        if (skill_for_checking - male_skill_for_checking) > 250 and dice(50):
            $ hero.sex += 1
        if (male_skill_for_checking - skill_for_checking) > 250 and dice(75):
            $ char.sex += 1
        if dice(10):
            $ char.oral += 1
        if dice(5):
            $ hero.oral += 1
        call interaction_sex_scene_check_skill_jobs
    elif current_action == "vag":
        if ct("Lesbian"):
            $ skill_for_checking = round(char.get_skill("vaginal")*0.6 + char.get_skill("sex")*0.15)
        else:
            $ skill_for_checking = round(char.get_skill("vaginal")*0.75 + char.get_skill("sex")*0.25)
        $ male_skill_for_checking = round(hero.get_skill("vaginal")*0.75 + hero.get_skill("sex")*0.25)
        if dice(20):
            $ char.vaginal += 1
        if dice(10):
            $ hero.vaginal += 1
        if (skill_for_checking - male_skill_for_checking) > 250 and dice(50):
            $ hero.vaginal += 1
        if (male_skill_for_checking - skill_for_checking) > 250 and dice(75):
            $ char.vaginal += 1
        if dice(10):
            $ char.sex += 1
        if dice(5):
            $ hero.sex += 1
        call interaction_scene_vaginal
        $ image_tags = gm.img.get_image_tags()
        if sub > 0:
            "[char.name] looking forward to something big inside her pussy."
            if "ontop" in image_tags:
                extend " She sits on top of you, immersing your dick inside."
            elif "doggy" in image_tags:
                extend " She bent over, pushing her crotch toward your dick."
            elif "missionary" in image_tags:
                extend " She lay on her back spreading her legs, awaiting for your dick."
            elif "onside" in image_tags:
                extend " She lay down on her side, waiting for you to join her."
            elif "standing" in image_tags:
                extend " She spreads her legs waiting for you, not even bothering to lay down."
            elif "spooning" in image_tags:
                extend " She snuggled to you, being in a mood for some spooning."
            elif "sitting" in image_tags:
                extend " She sat upon you knees, immersing your dick inside."
            else:
                extend " She confidently pushes your dick inside and starts to move."
        elif sub < 0:
            "[char.name] prepares herself, awaiting for further orders."
            if "ontop" in image_tags:
                extend " You ask her to sit on top of you, immersing your dick inside."
            elif "doggy" in image_tags:
                extend " You ask her to bent over, allowing you to take her from behind."
            elif "missionary" in image_tags:
                extend " You ask her to lay on her back and spread legs, allowing you to shove your dick inside."
            elif "onside" in image_tags:
                extend "  You asked her to lay down on her side, allowing you to get inside."
            elif "standing" in image_tags:
                extend " You asked her to spread her legs while standing, and pushed your dick inside."
            elif "spooning" in image_tags:
                extend " You asked her to snuggle to you, spooning her in the process."
            elif "sitting" in image_tags:
                extend " You asked her to sit upon you knees, immersing your dick inside."
            else:
                extend " You entered her and asked to start moving."
        else:
            "[char.name] doesn't mind you to do her pussy."
            if "ontop" in image_tags:
                extend " You invite her to sit on top of you, preparing your dick for some penetration."
            elif "doggy" in image_tags:
                extend " She bent over, welcoming your dick from behind."
            elif "missionary" in image_tags:
                extend " She lays on her back and spreads legs, inviting you to enter inside."
            elif "onside" in image_tags:
                extend " She lays down on her side, inviting you to enter inside."
            elif "standing" in image_tags:
                extend " You proceed to penetrate her not even bothering to lay down."
            elif "spooning" in image_tags:
                extend " You two snuggle to each other, trying out spooning."
            elif "sitting" in image_tags:
                extend " She sits upon you knees while you prepare your dick for going inside her."
            else:
                extend " You enter her pussy and you two begin to move."
        call interaction_sex_scene_check_skill_acts
        
    elif current_action == "anal":
        if ct("Lesbian"):
            $ skill_for_checking = round(char.get_skill("anal")*0.6 + char.get_skill("sex")*0.15)
        else:
            $ skill_for_checking = round(char.get_skill("anal")*0.75 + char.get_skill("sex")*0.25)
        $ male_skill_for_checking = round(hero.get_skill("anal")*0.75 + hero.get_skill("sex")*0.25)
        if dice(20):
            $ char.anal += 1
        if dice(10):
            $ hero.anal += 1
        if (skill_for_checking - male_skill_for_checking) > 250 and dice(50):
            $ hero.anal += 1
        if (male_skill_for_checking - skill_for_checking) > 250 and dice(75):
            $ char.anal += 1
        if dice(10):
            $ char.sex += 1
        if dice(5):
            $ hero.sex += 1
        call interaction_scene_anal
        $ image_tags = gm.img.get_image_tags()
        if sub > 0:
            "[char.name] looking forward to something big inside her ass."
            if "ontop" in image_tags:
                extend " She sits on top of you, immersing your dick inside."
            elif "doggy" in image_tags:
                extend " She bent over, pushing her anus toward your dick."
            elif "missionary" in image_tags:
                extend " She lay on her back spreading her legs, awaiting for your dick."
            elif "onside" in image_tags:
                extend " She lay down on her side, waiting for you to join her."
            elif "standing" in image_tags:
                extend " She spreads her legs waiting for you, not even bothering to lay down."
            elif "spooning" in image_tags:
                extend " She snuggled to you, being in a mood for some spooning."
            elif "sitting" in image_tags:
                extend " She sat upon you knees, immersing your dick inside."
            else:
                extend " She confidently pushes your dick inside and starts to move."
        elif sub < 0:
            "[char.name] prepares herself, awaiting for further orders."
            if "ontop" in image_tags:
                extend " You ask her to sit on top of you, immersing your dick inside."
            elif "doggy" in image_tags:
                extend " You ask her to bent over, allowing you to take her from behind."
            elif "missionary" in image_tags:
                extend " You ask her to lay on her back and spread legs, allowing you to shove your dick inside."
            elif "onside" in image_tags:
                extend "  You asked her to lay down on her side, allowing you to get inside."
            elif "standing" in image_tags:
                extend " You asked her to spread her legs while standing, and pushed your dick inside."
            elif "spooning" in image_tags:
                extend " You asked her to snuggle to you, spooning her in the process."
            elif "sitting" in image_tags:
                extend " You asked her to sit upon you knees, immersing your dick inside."
            else:
                extend " You entered her and asked to start moving."
        else:
            "[char.name] doesn't mind you to do her ass."
            if "ontop" in image_tags:
                extend " You invite her to sit on top of you, preparing your dick for some penetration."
            elif "doggy" in image_tags:
                extend " She bent over, welcoming your dick from behind."
            elif "missionary" in image_tags:
                extend " She lays on her back and spreads legs, inviting you to enter inside."
            elif "onside" in image_tags:
                extend " She lays down on her side, inviting you to enter inside."
            elif "standing" in image_tags:
                extend " You proceed to penetrate her not even bothering to lay down."
            elif "spooning" in image_tags:
                extend " You two snuggle to each other, trying out spooning."
            elif "sitting" in image_tags:
                extend " She sits upon you knees while you prepare your dick for going inside her."
            else:
                extend " You enter her anus and you two begin to move."
        call interaction_sex_scene_check_skill_acts
    jump interaction_scene_choice
    
label interaction_sex_scene_check_skill_jobs: # skill level check for one side actions

    if current_action == "hand":
        if skill_for_checking <= 200:
            if sub > 0:
                $ narrator(choice(["She strokes you a bit too quickly, the friction is a bit uncomfortable.", "She begins to stroke you very quickly. But because of the speed your cock often slips out of her hand."]))
            elif sub < 0:
                $ narrator(choice(["She strokes you gently. She isn't quite sure however what to make of the balls.", "She makes up for her inexperience with determination, carefully stroking your cock."]))
            else:
                $ narrator(choice(["She squeezes one of your balls too tightly, but stops when you wince.", "She has a firm grip, and she's not letting go."]))
        elif skill_for_checking < 1000:
            if sub > 0:
                $ narrator(choice(["Her fingers cause tingles as they caress the shaft.", "She quickly strokes you, with a very deft pressure."]))
            elif sub < 0:
                $ narrator(choice(["She gently caresses the shaft, and cups the balls in her other hand, giving them a warm massage.", "She moves very smoothly, stroking casually and very gently."]))
            else:
                $ narrator(choice(["Her hands glide smoothly across it.", "She moves her hands up and down. She's a little rough at this, but at she tries her best."]))
        else:
            if sub > 0:
                $ narrator(choice(["Her movements are masterful, her slightest touch starts you twitching.", "Her expert strokes will have you boiling over in seconds."]))
            elif sub < 0:
                $ narrator(choice(["She gently blows across the tip as her finger dance along the shaft.", "She slowly caresses you in a way that makes your blood boil, then pulls back at the last second."]))
            else:
                $ narrator(choice(["She knows what to do now, and rubs you with smooth strokes, focusing occasionally on the head.", "You can't tell where her hand is at any moment, all you know is that it works."]))
        if "after sex" in image_tags:
            "Soon you generously cover her body with your thick liquid."
    elif current_action == "tits":
        if skill_for_checking <= 200:
            if sub > 0:
                $ narrator(choice(["She kind of bounces her tits around your cock.", "She tries to quickly slide the cock up and down between her cleavage, but it tends to slide out."]))
            elif sub < 0:
                $ narrator(choice(["She slides the cock up and down between her cleavage.", "She squeezes her cleavage as tight as she can and rubs up and down."]))
            else:
                $ narrator(choice(["She sort of squishes her breasts back and forth around your cock.", "She slaps her tits against your dick, bouncing her whole body up and down."]))
        elif skill_for_checking < 1000:
            if sub > 0:
                $ narrator(choice(["She juggles her breasts up and down around your cock.", "She moves her boobs up and down in a fluid rocking motion."]))
            elif sub < 0:
                $ narrator(choice(["She gently caresses the shaft between her tits.", "She lightly brushes the head with her chin as it pops up between her tits."]))
            else:
                $ narrator(choice(["Sometimes she pauses to rub her nipples across the shaft.", "She rapidly slides the shaft between her tits"]))
        else:
            if sub > 0:
                $ narrator(choice(["She rapidly rocks her breasts up and down around your cock, covering them with drool to keep things well lubed.", "In as she strokes faster and faster, she bends down to suck on the head."]))
            elif sub < 0:
                $ narrator(choice(["In between strokes she gently sucks on the head.", "She drips some spittle down to make sure you're properly lubed."]))
            else:
                $ narrator(choice(["She licks away at the head every time it pops up between her tits.", "She dancers her nipples across the shaft."]))
        if "after sex" in image_tags:
            if sub > 0:
                "At the last moment she pulls away, covering herself with your thick liquid."
            elif sub < 0:
                "At the last moment you take it away from her chest, covering her body with your thick liquid."
            else:
                "At the last moment she asked you to take it away from her chest to cover her body with your thick liquid."
    elif current_action == "blow":
        if skill_for_checking <= 200:
            if sub > 0:
                $ narrator(choice(["Her head bobs rapidly, until she goes a bit too deep and starts to gag.", "She begins to suck very quickly. But because of the speed your cock often pops out of her mouth."]))
            elif sub < 0:
                $ narrator(choice(["She tentatively kisses and licks around the head.", "She licks all over your dick, but she doesn't really have a handle on it."]))
            else:
                $ narrator(choice(["She bobs quickly on your cock, but clamps down a bit too tight.", "She puts the tip in her mouth and starts suck in as hard as she can. She's a little rough at this, but at least she tries her best."]))
        elif skill_for_checking < 1000:
            if sub > 0:
                $ narrator(choice(["She licks her way down the shaft, and gently teases the balls.", "Her mouth envelopes the head, then she quickly draws it in and draws back with a pop."]))
            elif sub < 0:
                $ narrator(choice(["She gently caresses the shaft, and cups the balls in her other hand, giving them a warm massage.", "She moves her tongue very smoothly and very gently, keeping her teeth well clear, aside from a playful nip."]))
            else:
                $ narrator(choice(["She's settled into a gentle licking pace that washes over you like a warm bath.", "She licks up and down the shaft. A little rough, but at least she tries her best."]))
        else:
            if sub > 0:
                $ narrator(choice(["She rapidly bobs up and down on your cock, a frenzy of motion.", "She puts the tip into her mouth and her tongue swirls rapidly around it."]))
            elif sub < 0:
                $ narrator(choice(["She gently blows across the head as she covers your cock in smooth licks.", "She moves very smoothly, tongue dancing casually and very gently."]))
            else:
                $ narrator(choice(["Her deft licks are masterful, your cock twitches with each stroke.", "She's really good at this, alternating between deep suction and gentle licks."]))
        if "after sex" in image_tags:
            if sub > 0:
                "At the last moment she pulls it out, covering herself with your thick liquid."
            elif sub < 0:
                "At the last moment you pull it out from her mouth, covering her body with your thick liquid."
            else:
                "She asked you to pull it out from her mouth at the last moment to cover her body with your thick liquid."
    if skill_for_checking >= 4000:
        "She was so good that you profusely came after a few seconds. Pretty impressive."
        $ char.joy += randint(3, 5)
    elif skill_for_checking >= 2000:
        "You barely managed to hold out for half a minute in the face of her amazing skills."
        $ char.joy += randint(2, 4)
    elif skill_for_checking >= 1000:
        "It was very fast and very satisfying."
        $ char.joy += randint(1, 2)
    elif skill_for_checking >= 500:
        "Nothing extraordinary, but it wasn't half bad either."
        $ char.joy += randint(0, 1)
    elif skill_for_checking >= 200:
        "It took some time and effort on her part, her skills could definitely be improved."
    elif skill_for_checking >= 50:
        "Looks like [char.name] barely knows what she's doing. Still, she somewhat managed to get the job done."
        $ char.vitality -= randint(5, 10)
    else:
        $ char.vitality -= randint(10, 15)
        "Her moves were clumsy and untimely. By the time she finished the moment had passed, bringing you no satisfaction."
        $ char.joy -= randint(2, 4)
    $ sex_count += 1
    if skill_for_checking >= 50:
        $ guy_count +=1
        $ cum_count += 1
    return

label interaction_sex_scene_check_skill_acts: # skill level check for two sides actions
    if current_action == "vag":
        if skill_for_checking >= 4000:
            "Her technique is brought to perfection, her body moves in perfect synchronisation with yours, and her pussy felt like velvet."
            $ char.joy += randint(3, 5)
        elif skill_for_checking >= 2000:
            "Her refined skills, rhythmic movements, and wet hot pussy quickly brought you to the finish."
            $ char.joy += randint(2, 4)
        elif skill_for_checking >= 1000:
            "Her pussy felt very good, her movement patterns and amazing skills quickly exhausted your ability to hold back."
            $ char.joy += randint(1, 2)
        elif skill_for_checking >= 500:
            "Her movements were pretty good. Nothing extraordinary, but it wasn't half bad either."
            $ char.joy += randint(0, 1)
        elif skill_for_checking >= 200:
            "It took some time and effort on her part, her pussy could use some training."
            $ char.vitality -= randint(5, 10)
        elif skill_for_checking >= 50:
            "Looks like [char.name] barely knows what she's doing. Still, it's hard to screw up such a basic thing, so eventually she managed to get the job done."
            $ char.vitality -= randint(10, 15)
        else:
            "Her moves were clumsy and untimely, and her pussy was too dry. Sadly, she was unable to properly satisfy you."
            $ char.joy -= randint(2, 4)
            $ char.vitality -= randint(10, 15)
    elif current_action == "anal":
        if skill_for_checking >= 4000:
            "Her technique is brought to perfection, her body moves in perfect synchronisation with yours, and her anus was fit and tight."
            $ char.joy += randint(3, 5)
        elif skill_for_checking >= 2000:
            "Her refined skills, rhythmic movements, and tight hot ass quickly brought you to the finish."
            $ char.joy += randint(2, 4)
        elif skill_for_checking >= 1000:
            "Her anus felt very good, her movement patterns and amazing skills quickly exhausted your ability to hold back."
            $ char.joy += randint(1, 2)
        elif skill_for_checking >= 500:
            "Her movements were pretty good. Nothing extraordinary, but it wasn't half bad either."
            $ char.joy += randint(0, 1)
        elif skill_for_checking >= 200:
            "It took some time and effort on her part, her anus could use some training."
            $ char.vitality -= randint(5, 10)
        elif skill_for_checking >= 50:
            "Looks like [char.name] barely knows what she's doing. Still, it's hard to screw up such a basic thing, so eventually she managed to get the job done."
            $ char.vitality -= randint(10, 15)
        else:
            "Her moves were clumsy and untimely, and her anus wasn't quite ready for that. Sadly, she was unable to properly satisfy you."
            $ char.vitality -= randint(10, 15)

    if male_skill_for_checking >= 4000:
        extend " Your bodies merged into a single entity, filling each other with pleasure and satisfaction."
        $ char.joy += randint(3, 5)
    elif male_skill_for_checking >= 2000:
        extend " In the end you both simultaneously come multiple times."
        $ char.joy += randint(2, 4)
    elif male_skill_for_checking >= 1000:
        extend " In the end you both simultaneously come."
        $ char.joy += randint(1, 2)
    elif male_skill_for_checking >= 500:
        extend " You fucked her until you both come. It was pretty good."
        $ char.joy += randint(0, 1)
    elif male_skill_for_checking >= 200:
        extend " You fucked her until you both come."
        $ hero.vitality -= randint(5, 10)
    elif male_skill_for_checking >= 50:
        extend " You had some difficulties with bringing her to orgasm, but managed to overcome them in the end."
        $ hero.vitality -= randint(10, 15)
    else:
        extend " Unfortunately you didn't have enough skill to properly satisfy her as well. [char.name] looks disappointed."
        $ hero.vitality -= randint(10, 15)
        
    if "after sex" in image_tags:
        $ cum_count += 1
        if sub > 0:
            "At the last moment she pulls it out, covering herself with your thick liquid."
        elif sub < 0:
            "At the last moment you pull it out from her, covering her body with your thick liquid."
        else:
            "She asked you to pull it out from her at the last moment to cover her body with your thick liquid."
    if (male_skill_for_checking) >= 1000 and (skill_for_checking >= 1000):
        $ together_count += 1
    $ sex_count += 1
    if male_skill_for_checking >= 50:
        $ girl_count += 1
    if skill_for_checking >= 50:
        $ guy_count += 1
    return

label int_sex_ok: # the character agrees to do it
    $ char.override_portrait("portrait", "shy")
    if ct("Half-Sister") and dice(40):
        if ct("Impersonal"):
            $rc("I'll take in all your cum, brother.", "Sex with my brother, initiation.", "Let's have incest.", "Even though we're siblings... it's fine to do this, right?", "Let's deepen our bond as siblings.")
        elif ct("Shy") and dice(40):
            $rc("Umm... anything is fine as long as it's you... brother.", "I-if it's you, b-brother, then anything you do makes me feel good.")
        elif ct("Masochist") and dice(40):
            $rc("Are you going to violate me now, brother? Please?", "I'll be your slut any time you wish, brother.", "Hehe, would you prefer your sister to be to be an obedient girl?")
        elif ct("Imouto"):
            $rc("Teach me more things, brother!", "Brother, teach me how to feel good!", "Sis... will try her best.", "Sister's gonna show you her skills as a woman.")
        elif ct("Dandere"):
            $rc("Ah... actually, your sister has been feeling sexually frustrated lately...", "Brother, please do me.", "Even though we're related, we can have sex if we love each other.", "I'm only doing this because you're my brother.", "I'll do whatever you want, brother.", "Brother can do anything with me...", "I-is it alright to do something like that with my brother?")
        elif ct("Kuudere"):
            $rc("I... I can't believe I'm doing it with my brother...", "Y-you're lusting for your sister? O-okay, you can be my sex partner.", "I... I don't mind doing it even though we're siblings, but...")
        elif ct("Tsundere"):
            $rc("Ugh... I... I have such a lewd brother!", "O... only you are allowed to touch me, brother.", "I... I'm only doing this because you're hard, brother.", "Doing something like this... with my brother... But... truth be told...")
        elif ct("Kamidere"):
            $rc("B...brother...it's... it's wrong to do this...!", "E...even though we're siblings...", "Doing such a thing to my brother. Am I a bad big sister?")
        elif ct("Yandere"):
            $rc("Make love to me, brother. Drive me mad.", "I'm looking forward to see your face writhing in mad ecstacy, bro.", "Shut up and yield yourself to your sister.", "Bro, you're a perv. It runs in the family though.", "Man, who'd have thought that my brother is as perverted as I am...", "My brother is in heat.  That's wonderful.", "As long as the pervy brother has a pervy sis as well, all is right with the world.", "Damn... The thought of incest gets me all excited now...")
        elif ct("Ane"):
            $rc("This is how you've always wanted to claim me, isn't it?", "Doing such things to your sister... Well, it can't be helped...", "Sis will do her best.", "Let sis display her womanly skills.")
        elif ct("Bokukko"):
            $rc("You wanted to have sex with your sister so bad, huh?", "Have you been planning to do this? Man, what a hopeless brother you are...", "I'm gonna show you that I'm a woman too, bro.", "Right on, brother.  Better you just shut up and don't move.", "Leave this to me, you can rely on sis.", "As long as it's for my brother a couple of indecent things is nothing.")
        else:
            $rc("It's alright for siblings to do something like this.", "Make your sister feel good.", "Just for now, we're not siblings... we're just... a man and a woman.", "We're brother and sister. What we're doing now must remain an absolute secret.", "I'll do my best. I want you to feel good, brother.", "I bet our parents would be so mad.")
       
    elif ct("Impersonal"):
        $rc("...Please insert to continue.", "You are authorized so long as it does not hurt.", "You can do me if you want.", "So, I'll begin the sexual interaction...", "Understood. I will... service you…", "I dedicate this body to you.", "Understood. Please demonstrate your abilities.")
    elif ct("Shy") and dice(40):
        $rc("D-do you mean…  Ah, y-yes…  If I'm good enough…", "Eeh?! Th-that's... uh... W- well... I do... want to...", "O...okay. I'll do my best.", "I-I was thinking… That I wanted to be one with you…", "If it's you, I'm fine with anything...", "I too... wanted to be touched by you... ","I want my feelings…  To reach you…", "It's... it's... o-okay to... have... s--s-sex... with me...", "Uh... I... h...how should I say this... It... it'll be great if you could do it gently...", "Aah... p... please... I... I want it... I... I can't think of anything else now!", "I-I'll do my best... for your sake!", "Uhm... I want you... to be gentle...", "Um, I-I want to do it… Please treat me well…", "Uh, uhm, how should I...? Eh? You want it like this...? O-okay! Then, h-here I go…", "Eeh, i-is it ok with someone like me...?", "Sorry if I'm no good at this...", "Uh... p... please... d...do it for me... my whole body's aching right now...", "Umm... anything is fine as long as it's you...", "Umm… please do perverted things to me…", "I don't know how well I will do...")
    elif ct("Nymphomaniac") and dice(40):
        $rc("Come on, I'll do the same for you, so please hurry and do me.", "Ahh, I can't wait anymore... quickly... please do me fast…", "I've been waiting for you all this time, so hurry up.", "Ready anytime you are.", "Please fill my naughty holes with your hot shaft.", " Let's do it all night long, okay? ...What, I'm just a dirty-minded girl~ ♪", "I don't mind. I really loooove to have sex. ♪", "Just watching is boring, right?  So… ♪", "...Shit! Now I'm horny as hell! ...Hey? You up for a go?", "Whenever, wherever…", "If you'd made me wait any longer I would have violated you myself.", "You know, had you kept me waiting any longer I would probably have jumped you myself.", "I hope you know how to handle a pussy...", "Man, who'd have thought that you are as perverted as I am...", "Ah... actually, I have been feeling sexually frustrated lately...", "Aah~~ Geez, I can't hold it anymore! Let's fuck!", "Hyauh…  Geez, do you have any idea how long I've been wet?", "Finally!", "You can ask me as much as you like... We can do it again... and again...", "...These perverted feelings... You can make them go away, can't you...?", "Umm, I-I'm always ready for it, so...!", "Turn me into a sloppy mess...!", "Let's do it! Right now! Take off your clothes! Hurry!", "Hmmm, what should I do～? ...Do you wanna do it THAT much～? I guess there's no stopping it～", "eah, it's okay. If that's what you want. Besides... I kinda like this stuff.", "What, you want to do it too... Sure, let's do it♪", "Mm, I might be able to learn some new tricks... Okay, fine by me!")
    elif ct("Masochist") and dice (25):
        $rc("Feel free to make me your personal bitch slave!", "Geez～, you could have just taken me by force～...", "Kya~... I - am - being - molested -... Oh come on, at least play along a little bit...")
    elif ct("Sadist") and dice(25):
            $rc("Become my... sex slave ♪", "Just shut up and surrender yourself to me. Good boy.", "Stay still and let me violate you.", "Come. I'll be gentle with you.")
    elif ct("Tsundere"):
        $rc("*gulp*… W-well... since you're begging to do it with me, I suppose we can…", "It...it can't be helped, right? It... it's not that I like you or anything!", "I-it's not like I want to do it! It's just that you seem to want to do it so much…", "I'll punish you if I don't feel good, got it?", "Hhmph... if...if you wanna do it... uh... go all the way with it!", "Hm hmm! Be amazed at my fabulous technique!", "If you're asking, then I'll listen… B-but it's not like I actually want to do it, too!", "I-I'm actually really good at sex! So... I-I'd like to show you…", "I...I'm only doing it because of your happy face.", "Humph! I'll show you I can do it!", "If-if you say that you really, really want it… Then I won't turn you down…", "L.... leave it to me... you idiot...", "If you want to do it now, it's okay… I just don't want to do anything weird in front of other people.", "Th-things like that should only happen after marriage… but… fine, I'll do it…", "God, people like you… Are way too honest about what they want…", "T...that can't be helped, right? B...but that doesn't mean you can do anything you like!", "You're hopeless.... Well, fine then....", "...Yes, yes, I'll do it, I'll do it so…  geez, stop making that stupid face…", "Geez, you take anything you can get...")
    elif ct("Dandere"):
        $rc("...Very well then. Please go ahead and do as you like.", "I... want you inside me.", "You're welcome to... do that.", "You can do whatever you want to me.", "I'm going to make you cum. You had better prepare yourself.", "I will not go easy on you.", "I... I'm ready for sex.", "Make me feel good...", "...If you do it, be gentle.", "I will handle... all of your urges...", "Then…  I will do it with you…", "...If you want, do it now.", "...I want to do it, too.", "...How do you want it?  ...Okay, I can do it…", "Now is your chance...")
    elif ct("Kuudere"):
        $rc("...I don't particularly mind.", "Heh. I'm just a girl too, you know. Let's do it.", "...V-Very well. I will neither run nor hide.", "Don't forget that I'm a woman after all...", "What a bothersome guy... Alright, I get it.", "...Fine, just don't use the puppy-dog eyes.", "*sigh* ...Fine, fine! I'll do it as many times as you want!", "Fine with me… Wh-what? ...Even I have times when I want to do it…", "I-I'll make sure to satisfy you...!", "If you wanna do it just do what you want.")
    elif ct("Imouto"):
        $rc("Ehehe... It's ok? Doing it...", "Ehehe, I'm going to move a lot for you... ♪", "[char.name] will show you the power of love♪", "I can do naughty stuff, you know? ...Want to see?", "Uhuhu, Well then, I'll be really nice to you, ok? ♪", "Uhuhu, Well then, what should I tease first~ ♪", "Okayyy! Let's love each other a lot. ♪", "Hey? You want to? You do, don't you? We can do it, if you waaaaant~", "Aah... I want you… To love me lots…", "Ehehe♪ Prepare to receive loads and loads of my love! ♪", "Hold me really tight, kiss me really hard, and make me feel really good. ♪", "Aha, When I am with a certain someone, I do only naughty things~… Uhuhu ♪", "Yeah, let's make lots of love♪", "I-is it okay for me to climb onto you? I'm sorry if I'm heavy...", "I-I'll do my best to pleasure you!", "Yes. I'm happy that I can help make you feel good.", "I don't know how well I will do...", "Geez, you're so forceful...♪")
    elif ct("Ane"):
        $rc("Hmhm, what is going to happen to me, I wonder?", "Come on, show me what you've got...", "This looks like it will be enjoyable.", "If you can do this properly... I'll give you a nice pat on the head.", "Seems like you can't help it, huh...", "Fufufu, please don't overdo it, okay?", "Go ahead and do it as you like, it's okay.", "Very well, I can show you a few things... Hmhm.")
    elif ct("Bokukko"):
        $rc("Right, yeah... As long as you don't just cum on your own, sure, let's do it", "Y-yeah… I sort of want to do it, too... ehehe…", "Wha!? C-can you read my mind...?", "Ah, eh, right now?", "Okay... but I'll do it like I want, kay?" ,"...Okay, that's it! I can't stand it! I've gotta fuck ya!", "S-sure… Ehehe, I'm, uh, kind of interested, too…", "Hey, let's do it while we got some time to kill...?", "Hehee, just leave it all to me! I'll make this awesome!", "Gotcha, sounds like a plan!", "Hey, maybe… The two of us could have an anatomy lesson?", "Is that ok? Ehehe... I wanted to do it too…", "Huhu… I want to do it with a pervert like you.", "Ehehe… In that case, let's go hog wild~", "Ehehe… So... let's do it. ♪", "Hmph... if you'd like, I'll give ya' some lovin'. ♪", "Got'cha. Hehe. Now I won't go easy on you.", "Y-yeah... if we're going to do it, we should do it now...", "Huhuh, I sort of want to do it now...", "Hey, er…  Wanna try doing it with me...?", "Well, I s'pose once in a while wouldn't hurt♪")
    elif ct("Yandere"):
        $rc("Yes, let's have passionate sex, locked together♪", "Hehe. How should I make you feel good?", "If we have sex you will never forget me, right?♪", "Please do your best... if it's you, it'll be okay.", "Heh heh... You're going to feel a lot of pleasure. Try not to break on me.", "Alright, I'll just kill some time playing around with your body...", "Feel grateful for even having the opportunity to touch my body.", "Huhuh, I'll kill you with my tightness...", "You're lewd～♪")
    elif ct("Kamidere"):
        $rc("*giggle* I'll give you a feeling you'll never get from anyone else…", "Oh? You seem quite confident. I'm looking forward to this. ♪", "You're raring to go, aren't you? Very well, let's see what you've got.", "Now then, show me sex appropriate to someone qualified to be my lover...", "Hhmn... My, my... you love my body so much? Of course you do, it can't be helped.", "Oh, you seem to understand what I want from you,.. Good doggy, good doggy ♪", "Be sure to make me feel good, got it?", "Then you're bored, too.", "Feel grateful for even having the opportunity to touch my body.", "You won't be able to think about anybody else besides me after I'm done with you.", "Huhuhu, having sex with me… pretty cheeky for a pet dog~ ♪", "Hmph, Entertain me the best you can…", "Hmph, I'll prove that I'm the greatest you'll ever have...", "...For now, I'm open to the idea.", "Huhuh, I'll be using you until I'm satisfied...", "Huhu, you can't cum until I give you permission, okay? So, get ready to endure it~ ♪", "I don't really want to, but since you look so miserable I'll allow it.", "For me to get in this state... I can't believe it...", "Haa, in the end, it turned out like this…  Fine then, do as you like…")
    else:
        $rc("Oh... I guess if you like me it's ok.", "Fufu… I hope you are looking forward to this…!", "For you, I'll do my best today as well, okay?", "If it's with you... I'd do it, you know...?", "If you're so fascinated with me, let's do it.", "Hn, I want you to feel really good, okay...", "If we're going to do it, then let's make it the best performance possible. Promise?", "Now, let us discover the shape of our love. ♪", "Let's... feel good together...", "Huhn, if you do it, then… please make sure it feels good…", "Huhu, so here we are…  you can't hold it anymore, right?", "Then… Let's do it? ♪", "Sex... O-okay, let's do it...", "I don't mind. Now get yourself ready before I change my mind.", "Please let me make you feel good...", "What do you think about me, let your body answer for you…", "If you feel like it, do what you want, with my body…", "Ok, I'll serve you! ♪", "Now, [char.name] shall give you some pleasure ~ !", "Want to become one with me? …ok", "You're this horny...? Fine, then…", "If that's what you desire...", "Oh? You've already become like this? Heh, heh... ♪", "Okay… I'd like to.", "That expression on your face... Hehe, do you wanna fuck me that much?", "You insist, hm? Right away, then!", "Heh, how can I say no?", "Hum, What should we do? ...That, there? ..hmm", "I want to do so many dirty things... I can't hold it back...", "Huhuhu, I'll give you a really. Good. Time. ♪", "You can't you think of anything else beside having sex? You're such a perv~", "So you want to do it. Right. Now? Huhu... I very much approve. ♪", "You mean, like, have sex and stuff? ...Hmm~?  Meh, you pass!", "What? You want to do it? Geez, you're so hopeless... ♪", "Come on, I can tell that you're horny… Feel free to partake of me.", "Huhn, fine, do me to your heart's content.", "Um, if you'd like, I can do it for you… I'll do my best!", "I know you wanna feel good too. ...huhu, come here…", "I can't wait any more… Huhu, look how wet I am just thinking about you... ♪", "S-shut up and... entrust your body to me… Okay?", "You've got good intuition. That was just what I had in mind, Huhuh. ♪", "Haa, your lust knows no bounds...", "Huhu, ok then… Surrender yourself to me…", "Now... show me the dirty side of you…", "You really like it, don't you… Huhuh, okay, let's go.", "Y-yes… I don't mind letting you do as you please…", "I want to do it with you...", "Hn…  Looking at you... makes me want to do it…", "If the one corrupting my body is you, then I'll have no regrets.", "Yes. Go ahead and let my body overwhelm you.", "... Leave it to me...", "I'll do it. You better be prepared.", "I wanna do all kinds of dirty things to you. Just let yourself go, okay?", " Leave it to me... I'll make you cum so much.", "All right. Do as you like.", "Let's deepen our love for each other.", "Please, go ahead and do it.", "Are we going... All the way?", "Yup. That's the way. You need more love.", "Not good... I want to do perverted things so badly, I can't stand it...", "Sure, if you want", "Hey... do me...", "I-if it's with you... I'd go skin to skin...") 
    $ char.restore_portrait()
    return


label int_sex_nope: # the character disagrees to do it
    $ char.override_portrait("portrait", "angry")
    if ct("Half-Sister") and dice(60):
        if ct("Impersonal"):
            $rc("No... no incest please...")
        elif ct("Yandere"):
            $rc("Wait! We're siblings damnit.", "Hey, ummm... Siblings together... Is that really okay?")
        elif ct("Dandere"):
            $rc("We're siblings. We shouldn't do things like this.", "Do you have sexual desires for your sister...?")
        elif ct("Bokukko"):
            $rc("B... brother! P... please don't say things like that!")
        elif ct("Tsundere"):
            $rc("It's... it's wrong to have sexual desire among siblings, isn't it?", "Brother, you idiot! Lecher! Pervert!")
        elif ct("Kuudere"):
            $rc("...You want your sister's body that much? Pathetic.", "How hopeless can you be to do it with a sibling!")
        elif ct("Ane"):
            $rc("What? But... I'm your sister.", "Don't you know how to behave yourself, as siblings?")
        elif ct("Kamidere"):
            $rc("It's unacceptable for siblings to have sex!", "I can't believe... you do that... with your siblings!", "Having sex with a blood relative? That's wrong!")
        elif ct("Bokukko"):
            $rc("Man, you are weird.", "I'm your sis... Are you really okay with that?")
        else:
            $rc("No! Brother! We can't do this!",  "Don't you think that siblings shouldn't be doings things like that?")
    elif ct("Impersonal"):
        $rc("I see no possible benefit in doing that with you so I will have to decline.", "No.", "So, let's have you explain in full detail why you decided to do that today, hmm?")
    elif ct("Shy") and dice(40):
        $rc("I... I don't want that! ","W-we can't do that. ","I-I don't want to. ...sorry.")
    elif ct("Imouto"):
        $rc("Noooo way!", "I, I think perverted things are bad!", "That only happens after you've made your vows to be together forever, right?", "...I-I'm gonna get mad if you say that stuff, you know? Jeez!", "Y-you dummy! You should be talking about stuff like s-s-sex!") 
    elif ct("Dandere"):
        $rc("Keep sexual advances to a minimum.", "No.", "...pathetic.", "...you're no good.")
    elif ct("Tsundere"):
        $rc("I'm afraid I must inform you of your utter lack of common sense. Hmph!", "You are so... disgusting!!", "You pervy little scamp! Not in a million years!", "Hmph! Unfortunately for you, I'm not that cheap!")
    elif ct("Kuudere"):
        $rc("...Perv.", "...Looks like I'll have to teach you about this little thing called reality.", "O-of course the answer is no!", "Hmph, how unromantic!", "Don't even suggest something that awful.")
    elif ct("Kamidere"):
        $rc("Wh-who do you think you are!?", "W-what are you talking about… Of course I'm against that!", "What?! How could you think that I... NO!", "What? Asking that out of the blue? Know some shame!", "You should really settle down.", "What? Dying wish? You want to die?", "The meaning of 'not knowing your place' must be referring to this, eh...?", "I don't know how anyone so despicable as you could exist outside of hell.")
    elif ct("Bokukko"):
        $rc("He- Hey, Settle down a bit, okay?", "You should keep it in your pants, okay?", "Y-you're talking crazy...", "Hmph! Well no duh!")
    elif ct("Ane"):
        $rc("If I was interested in that sort of thing I might, but unfortunately...", "Sorry... I'm not ready for that...", "Oh my, can't you think of a better way to seduce me?", "No. I have decided that it would not be appropriate.", "I'm sorry, it's too early for that.", "I don't think our relationship has progressed to that point yet.", "I think that you are being way too aggressive.", "I'm not attracted to you in ‘that’ way.")
    elif ct("Yandere"):
        $rc("I've never met someone who knew so little about how pathetic they are.", "...I'll thank you to turn those despicable eyes away from me.")
    else:
        $rc("No! Absolutely NOT!", "With you? Don't make me laugh.", "Yeah right, dickhead.", "Yeah, get the fuck away from me, you disgusting perv.", "Get lost, pervert!", "Woah, hold on there, killer. Maybe after we get to know each other better.", "Don't tell me that you thought I was a slut...?", "I'm just really tired... ok?", "How about you fix that 'anytime's fine' attitude of yours, hmm?")  
    $ char.restore_portrait()
    return

   

# further goes logic which shows needed sex picture, they require sex_scene_location variable to work as intended
# since these algorithms are universal, might as well make unique labels for them and call when needed from anywhere
label interaction_scene_strip: # for striptease at first we try to get stripping or nude picture with needed bg
    if sex_scene_location == "beach":
        if char.has_image("stripping", "beach", exclude=["in pain", "scared"]):
            $ gm.set_img("stripping", "beach", exclude=["in pain", "scared"])
        elif char.has_image("nude", "beach", exclude=["in pain", "scared", "bathing", "sleeping"]):
            $ gm.set_img("nude", "beach", exclude=["in pain", "scared", "bathing", "sleeping"])
        elif char.has_image("lingerie", "beach", exclude=["in pain", "scared", "bathing", "sleeping"]):
            $ gm.set_img("lingerie", "beach", exclude=["in pain", "scared", "bathing", "sleeping"])
        else: # if it fails, we go for bgless
            $ tags = ({"tags": ["simple bg", "stripping"], "exclude": ["stage", "in pain", "scared"]}, {"tags": ["no bg", "stripping"], "exclude": ["stage", "in pain", "scared"]}, {"tags": ["simple bg", "nude"], "exclude": ["sleeping", "stage", "in pain", "scared", "bathing"]}, {"tags": ["no bg", "nude"], "exclude": ["sleeping", "stage", "in pain", "scared", "bathing"]}, {"tags": ["no bg", "lingerie"], "exclude": ["sleeping", "stage", "in pain", "scared", "bathing"]}, {"tags": ["simple bg", "lingerie"], "exclude": ["sleeping", "stage", "in pain", "scared", "bathing"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("simple bg", "stripping", exclude=["stage", "in pain", "scared"])
                elif result == tags[1]:
                    $ gm.set_img("no bg", "stripping", exclude=["stage", "in pain", "scared"])
                elif result == tags[2]:
                    $ gm.set_img("simple bg", "nude", exclude=["stage", "in pain", "scared"])
                elif result == tags[3]:
                    $ gm.set_img("no bg", "nude", exclude=["stage", "in pain", "scared"])
                elif result == tags[4]:
                    $ gm.set_img("no bg", "lingerie", exclude=["stage", "in pain", "scared"])
                else:
                    $ gm.set_img("simple bg", "lingerie", exclude=["stage", "in pain", "scared"])
            else: # so we don't have anything, and just show any strip
                if char.has_image ("stripping"):
                    $ gm.set_img("stripping", exclude=["stage", "in pain", "scared"])
                else: # or any nude
                    $ gm.set_img("nude", exclude=["stage", "in pain", "scared", "dungeon"])
    elif sex_scene_location == "park": # for pack we will try to show nature picture, preferably with urban
        if char.has_image("stripping", "nature", exclude=["in pain", "scared"]):
            $ gm.set_img("stripping", "nature", "urban", exclude=["in pain", "scared"], type="reduce")
        elif char.has_image("nude", "nature", exclude=["in pain", "scared", "bathing", "sleeping"]):
            $ gm.set_img("nude", "nature", "urban", exclude=["in pain", "scared", "bathing", "sleeping"])
        elif char.has_image("lingerie", "nature", "urban", exclude=["in pain", "scared", "bathing", "sleeping"]):
            $ gm.set_img("lingerie", "nature", "urban", exclude=["in pain", "scared", "bathing", "sleeping"])
        else: # if it fails, we go for bgless
            $ tags = ({"tags": ["simple bg", "stripping"], "exclude": ["stage", "in pain", "scared"]}, {"tags": ["no bg", "stripping"], "exclude": ["stage", "in pain", "scared"]}, {"tags": ["simple bg", "nude"], "exclude": ["sleeping", "stage", "in pain", "scared", "bathing"]}, {"tags": ["no bg", "nude"], "exclude": ["sleeping", "stage", "in pain", "scared", "bathing"]}, {"tags": ["no bg", "lingerie"], "exclude": ["sleeping", "stage", "in pain", "scared", "bathing"]}, {"tags": ["simple bg", "lingerie"], "exclude": ["sleeping", "stage", "in pain", "scared", "bathing"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("simple bg", "stripping", exclude=["stage", "in pain", "scared"])
                elif result == tags[1]:
                    $ gm.set_img("no bg", "stripping", exclude=["stage", "in pain", "scared"])
                elif result == tags[2]:
                    $ gm.set_img("simple bg", "nude", exclude=["stage", "in pain", "scared"])
                elif result == tags[3]:
                    $ gm.set_img("no bg", "nude", exclude=["stage", "in pain", "scared"])
                elif result == tags[4]:
                    $ gm.set_img("no bg", "lingerie", exclude=["stage", "in pain", "scared"])
                else:
                    $ gm.set_img("simple bg", "lingerie", exclude=["stage", "in pain", "scared"])
            else: # so we don't have anything, and just show any strip
                if char.has_image ("stripping"):
                    $ gm.set_img("stripping", exclude=["stage", "in pain", "scared"])
                else: # or any nude
                    $ gm.set_img("nude", exclude=["stage", "in pain", "scared", "dungeon"])
    else: # living room, we try to get a room bg
        if char.has_image("stripping", "living", exclude=["in pain", "scared"]):
            $ gm.set_img("stripping", "living", exclude=["in pain", "scared"], type="reduce")
        elif char.has_image("nude", "living", exclude=["in pain", "scared", "bathing", "sleeping"]):
            $ gm.set_img("nude", "living", exclude=["in pain", "scared", "bathing", "sleeping"])
        elif char.has_image("lingerie", "living", exclude=["in pain", "scared", "bathing", "sleeping"]):
            $ gm.set_img("lingerie", "nature", "urban", exclude=["in pain", "scared", "bathing", "sleeping"])
        else: # if it fails, we go for bgless
            $ tags = ({"tags": ["simple bg", "stripping"], "exclude": ["stage", "in pain", "scared"]}, {"tags": ["no bg", "stripping"], "exclude": ["stage", "in pain", "scared"]}, {"tags": ["simple bg", "nude"], "exclude": ["sleeping", "stage", "in pain", "scared", "bathing"]}, {"tags": ["no bg", "nude"], "exclude": ["sleeping", "stage", "in pain", "scared", "bathing"]}, {"tags": ["no bg", "lingerie"], "exclude": ["sleeping", "stage", "in pain", "scared", "bathing"]}, {"tags": ["simple bg", "lingerie"], "exclude": ["sleeping", "stage", "in pain", "scared", "bathing"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("simple bg", "stripping", exclude=["stage", "in pain", "scared"])
                elif result == tags[1]:
                    $ gm.set_img("no bg", "stripping", exclude=["stage", "in pain", "scared"])
                elif result == tags[2]:
                    $ gm.set_img("simple bg", "nude", exclude=["stage", "in pain", "scared"])
                elif result == tags[3]:
                    $ gm.set_img("no bg", "nude", exclude=["stage", "in pain", "scared"])
                elif result == tags[4]:
                    $ gm.set_img("no bg", "lingerie", exclude=["stage", "in pain", "scared"])
                else:
                    $ gm.set_img("simple bg", "lingerie", exclude=["stage", "in pain", "scared"])
            else: # so we don't have anything, and just show any strip, preferably indoors
                if char.has_image ("stripping"):
                    $ gm.set_img("stripping", "indoors", exclude=["stage", "in pain", "scared"], type="reduce")
                else: # or any nude
                    $ gm.set_img("nude", "indoors", exclude=["stage", "in pain", "scared", "dungeon"], type="reduce")
    return
    
label interaction_scene_mast:
    if sex_scene_location == "beach": # for mast we try to show mast+needed location, then bgless, then simply mast
        if char.has_image("masturbation", "beach", exclude=["forced", "normalsex", "group", "bdsm"]):
            $ gm.set_img("masturbation", "beach", exclude=["forced", "normalsex", "group", "bdsm"])
        else:
            $ tags = ({"tags": ["simple bg", "masturbation"], "exclude": ["forced", "normalsex", "group", "bdsm"]}, {"tags": ["no bg", "masturbation"], "exclude": ["forced", "normalsex", "group", "bdsm"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm"])
                else:
                    $ gm.set_img("masturbation", "no bg", exclude=["forced", "normalsex", "group", "bdsm"])
            else:
                $ gm.set_img("masturbation", "outdoors", exclude=["forced", "normalsex", "group", "bdsm"], type="reduce")
    elif sex_scene_location == "park":
        if char.has_image("masturbation", "nature", exclude=["forced", "normalsex", "group", "bdsm"]):
            $ gm.set_img("masturbation", "nature", "urban", exclude=["forced", "normalsex", "group", "bdsm"], type="reduce")
        else:
            $ tags = ({"tags": ["simple bg", "masturbation"], "exclude": ["forced", "normalsex", "group", "bdsm"]}, {"tags": ["no bg", "masturbation"], "exclude": ["forced", "normalsex", "group", "bdsm"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm"])
                else:
                    $ gm.set_img("masturbation", "no bg", exclude=["forced", "normalsex", "group", "bdsm"])
            else:
                $ gm.set_img("masturbation", "outdoors", exclude=["forced", "normalsex", "group", "bdsm"], type="reduce")
    else:
        if char.has_image("masturbation", "living", exclude=["forced", "normalsex", "group", "bdsm"]):
            $ gm.set_img("masturbation", "living", exclude=["forced", "normalsex", "group", "bdsm"])
        elif char.has_image("masturbation", "indoors", exclude=["forced", "normalsex", "group", "bdsm", "outdoors", "public", "dungeon"]):
            $ gm.set_img("masturbation", "indoors", exclude=["forced", "normalsex", "group", "bdsm", "outdoors", "public", "dungeon"])
        else:
            $ tags = ({"tags": ["simple bg", "masturbation"], "exclude": ["forced", "normalsex", "group", "bdsm"]}, {"tags": ["no bg", "masturbation"], "exclude": ["forced", "normalsex", "group", "bdsm"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm"])
                else:
                    $ gm.set_img("masturbation", "no bg", exclude=["forced", "normalsex", "group", "bdsm"])
            else:
                $ gm.set_img("masturbation", "indoors", exclude=["forced", "normalsex", "group", "bdsm"], type="reduce")
    return
    
label interaction_scene_blowjob:
    # for bj we use after_sex tag if needed, and partnerhidden is an optional tag, since it's quite rare in some packs
    if sex_scene_location == "beach":
        if char.has_image("bc blowjob", "beach", exclude=["rape", "in pain", "restrained"]):
            $ gm.set_img("bc blowjob", "beach", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
        elif char.has_image("after sex", "beach", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "beach", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["bc blowjob", "simple bg"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "bc blowjob"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]}, {"tags": ["simple bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("bc blowjob", "simple bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[1]:
                    $ gm.set_img("bc blowjob", "no bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[2]:
                    $ gm.set_img("after sex", "no bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
                else:
                    $ gm.set_img("after sex", "simple bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
            else:
                $ gm.set_img("bc blowjob", "outdoors", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
    elif sex_scene_location == "park":
        if char.has_image("bc blowjob", "nature", exclude=["rape", "in pain", "restrained"]):
            $ gm.set_img("bc blowjob", "nature", "partnerhidden", "urban", exclude=["rape", "in pain", "restrained"], type="reduce")
        elif char.has_image("after sex", "nature", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "nature", "urban", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["bc blowjob", "simple bg"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "bc blowjob"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]}, {"tags": ["simple bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("bc blowjob", "simple bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[1]:
                    $ gm.set_img("bc blowjob", "no bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[2]:
                    $ gm.set_img("after sex", "no bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
                else:
                    $ gm.set_img("after sex", "simple bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
            else:
                $ gm.set_img("bc blowjob", "outdoors", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
    else:
        if char.has_image("bc blowjob", "living", exclude=["rape", "in pain", "restrained"]):
            $ gm.set_img("bc blowjob", "living", "partnerhidden", "urban", exclude=["rape", "in pain", "restrained"], type="reduce")
        elif char.has_image("bc blowjob", "indoors", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"]):
            $ gm.set_img("bc blowjob", "indoors", "partnerhidden", "urban", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"], type="reduce")
        elif char.has_image("after sex", "living", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "living", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        elif char.has_image("after sex", "indoors", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"]):
            $ gm.set_img("after sex", "indoors", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["bc blowjob", "simple bg"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "bc blowjob"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]}, {"tags": ["simple bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("bc blowjob", "simple bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[1]:
                    $ gm.set_img("bc blowjob", "no bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[2]:
                    $ gm.set_img("after sex", "no bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
                else:
                    $ gm.set_img("after sex", "simple bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
            else:
                $ gm.set_img("bc blowjob", "indoors", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
    return
    
label interaction_scene_titsjob:
    if sex_scene_location == "beach":
        if char.has_image("bc titsjob", "beach", exclude=["rape", "in pain", "restrained"]):
            $ gm.set_img("bc titsjob", "beach", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
        elif char.has_image("after sex", "beach", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "beach", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["bc titsjob", "simple bg"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "bc titsjob"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]}, {"tags": ["simple bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("bc titsjob", "simple bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[1]:
                    $ gm.set_img("bc titsjob", "no bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[2]:
                    $ gm.set_img("after sex", "no bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
                else:
                    $ gm.set_img("after sex", "simple bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
            else:
                $ gm.set_img("bc titsjob", "outdoors", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
    elif sex_scene_location == "park":
        if char.has_image("bc titsjob", "nature", exclude=["rape", "in pain", "restrained"]):
            $ gm.set_img("bc titsjob", "nature", "partnerhidden", "urban", exclude=["rape", "in pain", "restrained"], type="reduce")
        elif char.has_image("after sex", "nature", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "nature", "urban", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["bc titsjob", "simple bg"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "bc titsjob"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]}, {"tags": ["simple bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("bc titsjob", "simple bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[1]:
                    $ gm.set_img("bc titsjob", "no bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[2]:
                    $ gm.set_img("after sex", "no bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
                else:
                    $ gm.set_img("after sex", "simple bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
            else:
                $ gm.set_img("bc titsjob", "outdoors", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
    else:
        if char.has_image("bc titsjob", "living", exclude=["rape", "in pain", "restrained"]):
            $ gm.set_img("bc titsjob", "living", "partnerhidden", "urban", exclude=["rape", "in pain", "restrained"], type="reduce")
        elif char.has_image("bc titsjob", "indoors", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"]):
            $ gm.set_img("bc titsjob", "indoors", "partnerhidden", "urban", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"], type="reduce")
        elif char.has_image("after sex", "living", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "living", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        elif char.has_image("after sex", "indoors", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"]):
            $ gm.set_img("after sex", "indoors", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["bc titsjob", "simple bg"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "bc titsjob"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]}, {"tags": ["simple bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("bc titsjob", "simple bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[1]:
                    $ gm.set_img("bc titsjob", "no bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[2]:
                    $ gm.set_img("after sex", "no bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
                else:
                    $ gm.set_img("after sex", "simple bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
            else:
                $ gm.set_img("bc titsjob", "indoors", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
    return
    
label interaction_scene_handjob:
    if sex_scene_location == "beach":
        if char.has_image("bc handjob", "beach", exclude=["rape", "in pain", "restrained"]):
            $ gm.set_img("bc handjob", "beach", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
        elif char.has_image("after sex", "beach", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "beach", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["bc handjob", "simple bg"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "bc handjob"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]}, {"tags": ["simple bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("bc handjob", "simple bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[1]:
                    $ gm.set_img("bc handjob", "no bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[2]:
                    $ gm.set_img("after sex", "no bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
                else:
                    $ gm.set_img("after sex", "simple bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
            else:
                $ gm.set_img("bc handjob", "outdoors", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
    elif sex_scene_location == "park":
        if char.has_image("bc handjob", "nature", exclude=["rape", "in pain", "restrained"]):
            $ gm.set_img("bc handjob", "nature", "partnerhidden", "urban", exclude=["rape", "in pain", "restrained"], type="reduce")
        elif char.has_image("after sex", "nature", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "nature", "urban", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["bc handjob", "simple bg"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "bc handjob"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]}, {"tags": ["simple bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("bc handjob", "simple bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[1]:
                    $ gm.set_img("bc handjob", "no bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[2]:
                    $ gm.set_img("after sex", "no bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
                else:
                    $ gm.set_img("after sex", "simple bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
            else:
                $ gm.set_img("bc handjob", "outdoors", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
    else:
        if char.has_image("bc handjob", "living", exclude=["rape", "in pain", "restrained"]):
            $ gm.set_img("bc handjob", "living", "partnerhidden", "urban", exclude=["rape", "in pain", "restrained"], type="reduce")
        elif char.has_image("bc handjob", "indoors", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"]):
            $ gm.set_img("bc handjob", "indoors", "partnerhidden", "urban", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"], type="reduce")
        elif char.has_image("after sex", "living", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "living", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        elif char.has_image("after sex", "indoors", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"]):
            $ gm.set_img("after sex", "indoors", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["bc handjob", "simple bg"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "bc handjob"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]}, {"tags": ["simple bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("bc handjob", "simple bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[1]:
                    $ gm.set_img("bc handjob", "no bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[2]:
                    $ gm.set_img("after sex", "no bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
                else:
                    $ gm.set_img("after sex", "simple bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
            else:
                $ gm.set_img("bc handjob", "indoors", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
    return
               
label interaction_scene_footjob:
    if sex_scene_location == "beach":
        if char.has_image("bc footjob", "beach", exclude=["rape", "in pain", "restrained"]):
            $ gm.set_img("bc footjob", "beach", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
        elif char.has_image("after sex", "beach", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "beach", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["bc footjob", "simple bg"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "bc footjob"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]}, {"tags": ["simple bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("bc footjob", "simple bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[1]:
                    $ gm.set_img("bc footjob", "no bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[2]:
                    $ gm.set_img("after sex", "no bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
                else:
                    $ gm.set_img("after sex", "simple bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
            else:
                $ gm.set_img("bc footjob", "outdoors", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
    elif sex_scene_location == "park":
        if char.has_image("bc footjob", "nature", exclude=["rape", "in pain", "restrained"]):
            $ gm.set_img("bc footjob", "nature", "partnerhidden", "urban", exclude=["rape", "in pain", "restrained"], type="reduce")
        elif char.has_image("after sex", "nature", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "nature", "urban", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["bc footjob", "simple bg"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "bc footjob"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]}, {"tags": ["simple bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("bc footjob", "simple bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[1]:
                    $ gm.set_img("bc footjob", "no bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[2]:
                    $ gm.set_img("after sex", "no bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
                else:
                    $ gm.set_img("after sex", "simple bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
            else:
                $ gm.set_img("bc footjob", "outdoors", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
    else:
        if char.has_image("bc footjob", "living", exclude=["rape", "in pain", "restrained"]):
            $ gm.set_img("bc footjob", "living", "partnerhidden", "urban", exclude=["rape", "in pain", "restrained"], type="reduce")
        elif char.has_image("bc footjob", "indoors", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"]):
            $ gm.set_img("bc footjob", "indoors", "partnerhidden", "urban", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"], type="reduce")
        elif char.has_image("after sex", "living", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "living", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        elif char.has_image("after sex", "indoors", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"]):
            $ gm.set_img("after sex", "indoors", exclude=["angry", "in pain", "sad", "scared", "public", "dungeon", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["bc footjob", "simple bg"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "bc footjob"], "exclude": ["rape", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]}, {"tags": ["simple bg", "after sex"], "exclude": ["angry", "in pain", "sad", "scared", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("bc footjob", "simple bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[1]:
                    $ gm.set_img("bc footjob", "no bg", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
                elif result == tags[2]:
                    $ gm.set_img("after sex", "no bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
                else:
                    $ gm.set_img("after sex", "simple bg", exclude=["angry", "in pain", "sad", "scared", "restrained"])
            else:
                $ gm.set_img("bc footjob", "indoors", "partnerhidden", exclude=["rape", "in pain", "restrained"], type="reduce")
    return
            
label interaction_scene_anal:
    if sex_scene_location == "beach":
        if char.has_image("2c anal", "beach", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]):
            $ gm.set_img("2c anal", "beach", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
        elif char.has_image("after sex", "beach", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "beach", exclude=["angry", "in pain", "sad", "scared", "restrained"])
        else:
            $ tags = ({"tags": ["2c anal", "simple bg"], "exclude": ["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]}, {"tags": ["no bg", "2c anal"], "exclude": ["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("2c anal", "simple bg", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
                else:
                    $ gm.set_img("2c anal", "no bg", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
            else:
                $ tags = ({"tags": ["after sex", "simple bg"], "exclude": ["angry", "sad", "scared", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "sad", "scared", "in pain", "restrained"]})
                $ result = get_act(char, tags)
                if result:
                    if result == tags[0]:
                        $ gm.set_img("after sex", "simple bg", exclude=["angry", "sad", "scared", "in pain", "restrained"])
                    else:
                        $ gm.set_img("no bg", "after sex", exclude=["angry", "sad", "scared", "in pain", "restrained"])
                else:
                    $ gm.set_img("2c anal", "outdoors", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
    elif sex_scene_location == "park":
        if char.has_image("2c anal", "nature", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]):
            $ gm.set_img("2c anal", "nature", "partnerhidden", "urban", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
        elif char.has_image("after sex", "nature", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "nature", "urban", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["2c anal", "simple bg"], "exclude": ["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]}, {"tags": ["no bg", "2c anal"], "exclude": ["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("2c anal", "simple bg", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
                else:
                    $ gm.set_img("2c anal", "no bg", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
            else:
                $ tags = ({"tags": ["after sex", "simple bg"], "exclude": ["angry", "sad", "scared", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "sad", "scared", "in pain", "restrained"]})
                $ result = get_act(char, tags)
                if result:
                    if result == tags[0]:
                        $ gm.set_img("after sex", "simple bg", exclude=["angry", "sad", "scared", "in pain", "restrained"])
                    else:
                        $ gm.set_img("no bg", "after sex", exclude=["angry", "sad", "scared", "in pain", "restrained"])
                else:
                    $ gm.set_img("2c anal", "outdoors", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
    else:
        if char.has_image("2c anal", "living", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]):
            $ gm.set_img("2c anal", "living", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
        elif char.has_image("after sex", "living", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "living", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["2c anal", "simple bg"], "exclude": ["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]}, {"tags": ["no bg", "2c anal"], "exclude": ["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("2c anal", "simple bg", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
                else:
                    $ gm.set_img("2c anal", "no bg", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
            else:
                $ tags = ({"tags": ["after sex", "simple bg"], "exclude": ["angry", "sad", "scared", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "sad", "scared", "in pain", "restrained"]})
                $ result = get_act(char, tags)
                if result:
                    if result == tags[0]:
                        $ gm.set_img("after sex", "simple bg", exclude=["angry", "sad", "scared", "in pain", "restrained"])
                    else:
                        $ gm.set_img("no bg", "after sex", exclude=["angry", "sad", "scared", "in pain", "restrained"])
                else:
                    $ gm.set_img("2c anal", "indoors", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
    return

label interaction_check_for_virginity: # here we do all checks and actions with virgin trait when needed
    if ct("Virgin"):
        if char.status == "slave":
            if ((cgo("SIW") or ct("Nymphomaniac")) and char.disposition >= 200) or (char.disposition >= 300) or (check_lovers(hero, char)) or (check_friends(hero, char)):
                menu:
                    "She warns you that this is her first time. She does not mind, but her value at the market might decrease. Do you want to continue?"
                    "Yes":
                        call girl_virgin
                    "No":
                        if check_lovers(hero, char) or check_friends(hero, char) or char.disposition >= 600:
                            "You changed your mind. She looks a bit disappointed."
                        else:
                            "You changed your mind."
                        jump interaction_scene_choice
            else:
                menu: 
                    "She tells you that this is her first time, and asks plaintively to do something else instead. You can force her, but it will not be without consequences. Do you want to use force?"
                    "Yes":
                        "You violated her."
                        if char.health >=20:
                            $ char.health -= 10
                        else:
                            $ char.vitality -= 20
                        if ct("Masochist"):
                            $ sex_scene_libido += 1
                            $ char.disposition -= 50
                        else:
                            $ char.disposition -= 150
                            $ char.joy -= 50
                            $ sex_scene_libido -= 2
                    "No":
                        "You agreed to do something else instead. She sighs with relief."
                        jump interaction_scene_choice
        else:
            if (check_lovers(hero, char)) or (check_friends(hero, char) and char.disposition >= 600) or ((cgo("SIW") or ct("Nymphomaniac")) and char.disposition >= 400):
                menu:
                    "Looks like this is her first time, and she does not mind. Do you want to continue?"
                    "Yes":
                        call girl_virgin
                    "No":
                        "You changed your mind. She looks a bit disappointed."
                        jump interaction_scene_choice
            else:
                "Unfortunately she's still a virgin, and is not ready to pop her cherry yet."
                jump interaction_scene_choice
        $ char.disposition += 50
        $ char.remove_trait(traits["Virgin"])
        if char.health >=15:
            $ char.health -= 10
        else:
            $ char.vitality -= 20      
    $ current_action = "vag"
    jump interactions_sex_scene_logic_part
    
label interaction_scene_vaginal:
    if sex_scene_location == "beach":
        if char.has_image("2c vaginal", "beach", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]):
            $ gm.set_img("2c vaginal", "beach", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
        elif char.has_image("after sex", "beach", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "beach", exclude=["angry", "in pain", "sad", "scared", "restrained"])
        else:
            $ tags = ({"tags": ["2c vaginal", "simple bg"], "exclude": ["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]}, {"tags": ["no bg", "2c vaginal"], "exclude": ["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("2c vaginal", "simple bg", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
                else:
                    $ gm.set_img("2c vaginal", "no bg", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
            else:
                $ tags = ({"tags": ["after sex", "simple bg"], "exclude": ["angry", "sad", "scared", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "sad", "scared", "in pain", "restrained"]})
                $ result = get_act(char, tags)
                if result:
                    if result == tags[0]:
                        $ gm.set_img("after sex", "simple bg", exclude=["angry", "sad", "scared", "in pain", "restrained"])
                    else:
                        $ gm.set_img("no bg", "after sex", exclude=["angry", "sad", "scared", "in pain", "restrained"])
                else:
                    $ gm.set_img("2c vaginal", "outdoors", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
    elif sex_scene_location == "park":
        if char.has_image("2c vaginal", "nature", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]):
            $ gm.set_img("2c vaginal", "nature", "partnerhidden", "urban", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
        elif char.has_image("after sex", "nature", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "nature", "urban", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["2c vaginal", "simple bg"], "exclude": ["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]}, {"tags": ["no bg", "2c vaginal"], "exclude": ["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("2c vaginal", "simple bg", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
                else:
                    $ gm.set_img("2c vaginal", "no bg", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
            else:
                $ tags = ({"tags": ["after sex", "simple bg"], "exclude": ["angry", "sad", "scared", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "sad", "scared", "in pain", "restrained"]})
                $ result = get_act(char, tags)
                if result:
                    if result == tags[0]:
                        $ gm.set_img("after sex", "simple bg", exclude=["angry", "sad", "scared", "in pain", "restrained"])
                    else:
                        $ gm.set_img("no bg", "after sex", exclude=["angry", "sad", "scared", "in pain", "restrained"])
                else:
                    $ gm.set_img("2c vaginal", "outdoors", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
    else:
        if char.has_image("2c vaginal", "living", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]):
            $ gm.set_img("2c vaginal", "living", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
        elif char.has_image("after sex", "living", exclude=["angry", "in pain", "sad", "scared", "restrained"]):
            $ gm.set_img("after sex", "living", exclude=["angry", "in pain", "sad", "scared", "restrained"], type="reduce")
        else:
            $ tags = ({"tags": ["2c vaginal", "simple bg"], "exclude": ["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]}, {"tags": ["no bg", "2c vaginal"], "exclude": ["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"]})
            $ result = get_act(char, tags)
            if result:
                if result == tags[0]:
                    $ gm.set_img("2c vaginal", "simple bg", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
                else:
                    $ gm.set_img("2c vaginal", "no bg", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
            else:
                $ tags = ({"tags": ["after sex", "simple bg"], "exclude": ["angry", "sad", "scared", "in pain", "restrained"]}, {"tags": ["no bg", "after sex"], "exclude": ["angry", "sad", "scared", "in pain", "restrained"]})
                $ result = get_act(char, tags)
                if result:
                    if result == tags[0]:
                        $ gm.set_img("after sex", "simple bg", exclude=["angry", "sad", "scared", "in pain", "restrained"])
                    else:
                        $ gm.set_img("no bg", "after sex", exclude=["angry", "sad", "scared", "in pain", "restrained"])
                else:
                    $ gm.set_img("2c vaginal", "indoors", "partnerhidden", exclude=["rape", "angry", "sad", "scared", "in pain", "gay", "restrained"], type="reduce")
    return