init -11 python:
    # Interactions (Girlsmeets Helper Functions):
    def rc(*args):
        """
        random choice function
        Wrapper to enable simpler girl_meets choices, returns whatever char_gm is set to along with a random line.
        """
        # https://github.com/Xela00/PyTFall/issues/37
        return char.say(choice(list(args)))
        
    def rts(girl, options):
        """
        Get a random string from a random trait that a girl has.
        girl = The girl to check the traits against.
        options = A dictionary of trait/eval -> (strings,).
        """
        default = options.pop("default", None)
        available = list()
        
        for trait in options.iterkeys():
            if trait in traits:
                if traits[trait] in girl.traits: available.append(options[trait])
            else:
                if eval(trait, globals(), locals()): available.append(options[trait])
        
        if not available: trait = default
        else: trait = choice(available)
        
        if isinstance(trait, (list, tuple)): return choice(trait)
        else: return trait
        
    def ec(d):
        # Not used atm.
        """
        Expects a dict of k/v pairs as argument. If key is a valid trait, the function will check if character has it.
        Else, the key will be evaluated and value added to the choices.
        This will return a single random choice from all that return true (traits and evals).
        """
        l = list()
        for key in d:
            if key in traits:
                if key in char.traits:
                    l.extend(d[key])
            else:
                if eval(key):
                    l.extend(d[key])
        # raise Error, l
        if l:
            g(choice(l))
            return True
        else:
            return False
        
    def ct(*args):
        """
        Check traits function.
        Checks is character in girl_meets has any trait in entered as an argument.
        """
        l = list(traits[i] for i in list(args))
        return any(i in l for i in char.traits)
        
    def co(*args):
        """
        Check occupation
        Checks if any of the occupations belong to the character.
        """
        return ct(*args)
        
    def cgo(*args):
        """
        Checks for General Occupation strings, such as "SIW", "Warrior", "Server", etc.
        """
        gen_occs = set()
        for occ in char.traits:
            if hasattr(occ, "occupations"):
                gen_occs = gen_occs.union(set(occ.occupations))
        return any(i for i in list(args) if i in gen_occs)
        
    def d(value):
        """
        Checks if disposition of the girl is any higher that value.
        """
        return char.disposition >= value
        
    # Relationships:
    def check_friends(*args):
        friends = list()
        for i in args:
            for z in args:
                if i != z:
                    friends.append(i.is_friend(z))
        return all(friends)
        
    def set_friends(*args):
        for i in args:
            for z in args:
                if i != z:
                    i.friends.add(z)

    def end_friends(*args):
        for i in args:
            for z in args:
                if i != z and z in i.friends:
                    i.friends.remove(z)
        
    def check_lovers(*args):
        lovers = list()
        for i in args:
            for z in args:
                if i != z:
                    lovers.append(i.is_lover(z))
        return all(lovers)

    def set_lovers(*args):
        for i in args:
            for z in args:
                if i != z:
                    i.lovers.add(z)

    def end_lovers(*args):
        for i in args:
            for z in args:
                if i != z and z in i.lovers:
                    i.lovers.remove(z)
                    
    # Other:
    def find_les_partners():
        """
        Returns a set with if any partner(s) is availible and willing at the location.
        (lesbian action)
        *We can move this to GM class and have this run once instead of twice! (menu + label)
        """
        # First get a set of all girls at the same location as the current character:
        partners = set()
        for i in chars.values():
            if i.location == char.location:
                partners.add(i)
                
        # Next figure out if disposition of possible partners towards MC is high enough for them to agree and/or they are lovers of char.
        willing_partners = set()
        for i in partners:
            if char != i: # @review: (Alex) make sure we do not pick the girl to fuck herself...
                # @review: (Alex) vitality is a fixed stat but it's best to check health as a percentage of it's max (60%+), 25 can feel like near death for some characters.
                if (check_lovers(i, hero) or check_lovers(char, i)) and not (i.vitality < 25 or i.health < i.get_max("health")*0.6) and not (i.disposition <= -50): # Last check is too make sure partner doesn't dislike the MC.
                    willing_partners.add(i)
        # @review: (Alex) renamed the function. We are returning all choices, nit just the one partner.
        return willing_partners
        
    def interactions_run_gm_anywhere(char, place, background):
        """           
        Runs (or doesn't) gm or interactions with the char based on her status
        """
        if chars[char].status == "slave" or not(chars[char].is_available):
            narrator("Nobody's here...")
            renpy.jump(place)
        elif chars[char] in hero.girls:
            gm.start("girl_interactions", chars[char], chars[char].get_vnsprite(), place, background)
        else:
            gm.start("girl_meets", chars[char], chars[char].get_vnsprite(), place, background)