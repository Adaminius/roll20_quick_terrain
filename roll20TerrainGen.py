"""
Generate random outdoor maps for roll20. Requires map_generate.js to be running in your roll20 dev
game and the following images to be in your library and correctly addressed in map_generate.js:

PINE_IMAGE
STONE_IMAGE
"""

__author__ = 'Adam Mansfield'

import tkinter as tk
import random
import time

from copy import deepcopy
from tkinter import messagebox
from collections import OrderedDict
from collections import namedtuple
from collections import defaultdict

#################################
#                               #
#       --- Globals ---         #
#                               #
#################################


# todo: more sophisticated terrain generation alg
#   - connected regions labeling algorithm
#   - make maxobjects actually do something
# todo: add more terrain images/types
# todo: add a listbox? of presets
# todo: something for background texture/image
# todo: add some way to get back current state of map from roll20 and generate around what's already there? (sounds like too much trouble for now)


ANIMALS_LIST = "Aardvark	Albatross	Alligator	Alpaca	Ant	Anteater	Antelope	Ape	Armadillo	Ass	Baboon	Badger	Barracuda	Bat	Bear	Beaver	Bee	Bison	Boar	Buffalo	Galago	Butterfly	Camel	Caribou	Cat	Caterpillar	Cattle	Chamois	Cheetah	Chicken	Chimpanzee	Chinchilla	Chough	Clam	Cobra	Cod	Cormorant	Coyote	Crab	Crane	Crocodile	Crow	Curlew	Deer	Dinosaur	Dog	Dogfish	Dolphin	Donkey	Dotterel	Dove	Dragonfly	Duck	Dugong	Dunlin	Eagle	Echidna	Eel	Eland	Elephant	Elephant seal	Elk	Emu	Falcon	Ferret	Finch	Fish	Flamingo	Fly	Fox	Frog	Gaur	Gazelle	Gerbil	Giant Panda	Giraffe	Gnat	Gnu	Goat	Goose	Goldfinch	Goldfish	Gorilla	Goshawk	Grasshopper	Grouse	Guanaco	Guinea fowl	Guinea pig	Gull	Hamster	Hare	Hawk	Hedgehog	Heron	Herring	Hippopotamus	Hornet	Horse	Human	Hummingbird	Hyena	Jackal	Jaguar	Jay	Jay, Blue	Jellyfish	Kangaroo	Koala	Komodo dragon	Kouprey	Kudu	Lapwing	Lark	Lemur	Leopard	Lion	Llama	Lobster	Locust	Loris	Louse	Lyrebird	Magpie	Mallard	Manatee	Marten	Meerkat	Mink	Mole	Monkey	Moose	Mouse	Mosquito	Mule	Narwhal	Newt	Nightingale	Octopus	Okapi	Opossum	Oryx	Ostrich	Otter	Owl	Ox	Oyster	Panther	Parrot	Partridge	Peafowl	Pelican	Penguin	Pheasant	Pig	Pigeon	Pony	Porcupine	Porpoise	Prairie Dog	Quail	Quelea	Rabbit	Raccoon	Rail	Ram	Rat	Raven	Red deer	Red panda	Reindeer	Rhinoceros	Rook	Ruff	Salamander	Salmon	Sand Dollar	Sandpiper	Sardine	Scorpion	Sea lion	Sea Urchin	Seahorse	Seal	Shark	Sheep	Shrew	Shrimp	Skunk	Snail	Snake	Spider	Squid	Squirrel	Starling	Stingray	Stinkbug	Stork	Swallow	Swan	Tapir	Tarsier	Termite	Tiger	Toad	Trout	Turkey	Turtle	Vicuña	Viper	Vulture	Wallaby	Walrus	Wasp	Water buffalo	Weasel	Whale	Wolf	Wolverine	Wombat	Woodcock	Woodpecker	Worm	Wren	Yak	Zebra"
ANIMALS_LIST = [s.upper() for s in ANIMALS_LIST.split('\t')]
ADJECTIVES_LIST = "abandoned	able	absolute	academic	acceptable	acclaimed	accomplished	accurate	aching	acidic	acrobatic	adorable	adventurous	babyish	back	bad	baggy	bare	barren	basic	beautiful	belated	beloved	calculating	calm	candid	canine	capital	carefree	careful	careless	caring	cautious	cavernous	celebrated	charming	damaged	damp	dangerous	dapper	daring	dark	darling	dazzling	dead	deadly	deafening	dear	dearest	each	eager	early	earnest	easy	easygoing	ecstatic	edible	educated	fabulous	failing	faint	fair	faithful	fake	familiar	famous	fancy	fantastic	far	faraway	farflung	faroff	gargantuan	gaseous	general	generous	gentle	genuine	giant	giddy	gigantic	hairy	half	handmade	handsome	handy	happy	happygolucky	hard	icky	icy	ideal	idealistic	identical	idiotic	idle	idolized	ignorant	ill	illegal	jaded	jagged	jampacked	kaleidoscopic	keen	lame	lanky	large	last	lasting	late	lavish	lawful	mad	madeup	magnificent	majestic	major	male	mammoth	married	marvelous	naive	narrow	nasty	natural	naughty	obedient	obese	oblong	oblong	obvious	occasional	oily	palatable	pale	paltry	parallel	parched	partial	passionate	past	pastel	peaceful	peppery	perfect	perfumed	quaint	qualified	radiant	ragged	rapid	rare	rash	raw	recent	reckless	rectangular	sad	safe	salty	same	sandy	sane	sarcastic	sardonic	satisfied	scaly	scarce	scared	scary	scented	scholarly	scientific	scornful	scratchy	scrawny	second	secondary	secondhand	secret	selfassured	selfish	selfreliant	sentimental	talkative	tall	tame	tan	tangible	tart	tasty	tattered	taut	tedious	teeming	ugly	ultimate	unacceptable	unaware	uncomfortable	uncommon	unconscious	understated	unequaled	vacant	vague	vain	valid	wan	warlike	warm	warmhearted	warped	wary	wasteful	watchful	waterlogged	watery	wavy	yawning	yearly	zany	false	active	actual	adept	admirable	admired	adolescent	adorable	adored	advanced	affectionate	afraid	aged	aggravating	beneficial	best	better	bewitched	big	bighearted	biodegradable	bitesized	bitter	black	cheap	cheerful	cheery	chief	chilly	chubby	circular	classic	clean	clear	clearcut	clever	close	closed	decent	decimal	decisive	deep	defenseless	defensive	defiant	deficient	definite	definitive	delayed	delectable	delicious	elaborate	elastic	elated	elderly	electric	elegant	elementary	elliptical	embarrassed	fast	fat	fatal	fatherly	favorable	favorite	fearful	fearless	feisty	feline	female	feminine	few	fickle	gifted	giving	glamorous	glaring	glass	gleaming	gleeful	glistening	glittering	hardtofind	harmful	harmless	harmonious	harsh	hasty	hateful	haunting	illfated	illinformed	illiterate	illustrious	imaginary	imaginative	immaculate	immaterial	immediate	immense	impassioned	jaunty	jealous	jittery	key	kind	lazy	leading	leafy	lean	left	legal	legitimate	light	masculine	massive	mature	meager	mealy	mean	measly	meaty	medical	mediocre	nautical	near	neat	necessary	needy	odd	oddball	offbeat	offensive	official	old	periodic	perky	personal	pertinent	pesky	pessimistic	petty	phony	physical	piercing	pink	pitiful	plain	quarrelsome	quarterly	ready	real	realistic	reasonable	red	reflecting	regal	regular	separate	serene	serious	serpentine	several	severe	shabby	shadowy	shady	shallow	shameful	shameless	sharp	shimmering	shiny	shocked	shocking	shoddy	short	shortterm	showy	shrill	shy	sick	silent	silky	tempting	tender	tense	tepid	terrible	terrific	testy	thankful	that	these	uneven	unfinished	unfit	unfolded	unfortunate	unhappy	unhealthy	uniform	unimportant	unique	valuable	vapid	variable	vast	velvety	weak	wealthy	weary	webbed	wee	weekly	weepy	weighty	weird	welcome	welldocumented	yellow	zealous	aggressive	agile	agitated	agonizing	agreeable	ajar	alarmed	alarming	alert	alienated	alive	all	altruistic	blackandwhite	bland	blank	blaring	bleak	blind	blissful	blond	blue	blushing	cloudy	clueless	clumsy	cluttered	coarse	cold	colorful	colorless	colossal	comfortable	common	compassionate	competent	complete	delightful	delirious	demanding	dense	dental	dependable	dependent	descriptive	deserted	detailed	determined	devoted	different	embellished	eminent	emotional	empty	enchanted	enchanting	energetic	enlightened	enormous	filthy	fine	finished	firm	first	firsthand	fitting	fixed	flaky	flamboyant	flashy	flat	flawed	flawless	flickering	gloomy	glorious	glossy	glum	golden	good	goodnatured	gorgeous	graceful	healthy	heartfelt	hearty	heavenly	heavy	hefty	helpful	helpless	impartial	impeccable	imperfect	imperturbable	impish	impolite	important	impossible	impractical	impressionable	impressive	improbable	joint	jolly	jovial	kindhearted	kindly	lighthearted	likable	likely	limited	limp	limping	linear	lined	liquid	medium	meek	mellow	melodic	memorable	menacing	merry	messy	metallic	mild	negative	neglected	negligible	neighboring	nervous	new	oldfashioned	only	open	optimal	optimistic	opulent	plaintive	plastic	playful	pleasant	pleased	pleasing	plump	plush	pointed	pointless	poised	polished	polite	political	queasy	querulous	reliable	relieved	remarkable	remorseful	remote	repentant	required	respectful	responsible	silly	silver	similar	simple	simplistic	sinful	single	sizzling	skeletal	skinny	sleepy	slight	slim	slimy	slippery	slow	slushy	small	smart	smoggy	smooth	smug	snappy	snarling	sneaky	sniveling	snoopy	thick	thin	third	thirsty	this	thorny	thorough	those	thoughtful	threadbare	united	unkempt	unknown	unlawful	unlined	unlucky	unnatural	unpleasant	unrealistic	venerated	vengeful	verifiable	vibrant	vicious	wellgroomed	wellinformed	welllit	wellmade	welloff	welltodo	wellworn	wet	which	whimsical	whirlwind	whispered	yellowish	zesty	amazing	ambitious	ample	amused	amusing	anchored	ancient	angelic	angry	anguished	animated	annual	another	antique	bogus	boiling	bold	bony	boring	bossy	both	bouncy	bountiful	bowed	complex	complicated	composed	concerned	concrete	confused	conscious	considerate	constant	content	conventional	cooked	cool	cooperative	difficult	digital	diligent	dim	dimpled	dimwitted	direct	disastrous	discrete	disfigured	disgusting	disloyal	dismal	enraged	entire	envious	equal	equatorial	essential	esteemed	ethical	euphoric	flimsy	flippant	flowery	fluffy	fluid	flustered	focused	fond	foolhardy	foolish	forceful	forked	formal	forsaken	gracious	grand	grandiose	granular	grateful	grave	gray	great	greedy	green	hidden	hideous	high	highlevel	hilarious	hoarse	hollow	homely	impure	inborn	incomparable	incompatible	incomplete	inconsequential	incredible	indelible	indolent	inexperienced	infamous	infantile	joyful	joyous	jubilant	klutzy	knobby	little	live	lively	livid	loathsome	lone	lonely	long	milky	mindless	miniature	minor	minty	miserable	miserly	misguided	misty	mixed	next	nice	nifty	nimble	nippy	orange	orderly	ordinary	organic	ornate	ornery	poor	popular	portly	posh	positive	possible	potable	powerful	powerless	practical	precious	present	prestigious	questionable	quick	repulsive	revolving	rewarding	rich	right	rigid	ringed	ripe	sociable	soft	soggy	solid	somber	some	sophisticated	sore	sorrowful	soulful	soupy	sour	spanish	sparkling	sparse	specific	spectacular	speedy	spherical	spicy	spiffy	spirited	spiteful	splendid	spotless	spotted	spry	thrifty	thunderous	tidy	tight	timely	tinted	tiny	tired	torn	total	unripe	unruly	unselfish	unsightly	unsteady	unsung	untidy	untimely	untried	victorious	vigilant	vigorous	villainous	violet	white	whole	whopping	wicked	wide	wideeyed	wiggly	wild	willing	wilted	winding	windy	young	zigzag	anxious	any	apprehensive	appropriate	apt	arctic	arid	aromatic	artistic	ashamed	assured	astonishing	athletic	brave	breakable	brief	bright	brilliant	brisk	broken	bronze	brown	bruised	coordinated	corny	corrupt	costly	courageous	courteous	crafty	crazy	creamy	creative	creepy	criminal	crisp	dirty	disguised	dishonest	dismal	distant	distant	distinct	distorted	dizzy	dopey	downright	dreary	even	evergreen	everlasting	every	evil	exalted	excellent	excitable	exemplary	exhausted	forthright	fortunate	fragrant	frail	frank	frayed	free	french	frequent	fresh	friendly	frightened	frightening	frigid	gregarious	grim	grimy	gripping	grizzled	gross	grotesque	grouchy	grounded	honest	honorable	honored	hopeful	horrible	hospitable	hot	huge	infatuated	inferior	infinite	informal	innocent	insecure	insidious	insignificant	insistent	instructive	insubstantial	judicious	juicy	jumbo	knotty	knowing	knowledgeable	longterm	loose	lopsided	lost	loud	lovable	lovely	loving	modern	modest	moist	monstrous	monthly	monumental	moral	mortified	motherly	motionless	nocturnal	noisy	nonstop	normal	notable	noted	original	other	our	outgoing	outlandish	outlying	precious	pretty	previous	pricey	prickly	primary	prime	pristine	private	prize	probable	productive	profitable	quickwitted	quiet	quintessential	roasted	robust	rosy	rotating	rotten	rough	round	rowdy	square	squeaky	squiggly	stable	staid	stained	stale	standard	starchy	stark	starry	steel	steep	sticky	stiff	stimulating	stingy	stormy	straight	strange	strict	strident	striking	striped	strong	studious	stunning	tough	tragic	trained	traumatic	treasured	tremendous	tremendous	triangular	tricky	trifling	trim	untrue	unused	unusual	unwelcome	unwieldy	unwilling	unwitting	unwritten	upbeat	violent	virtual	virtuous	visible	winged	wiry	wise	witty	wobbly	woeful	wonderful	wooden	woozy	wordy	worldly	worn	youthful	attached	attentive	attractive	austere	authentic	authorized	automatic	avaricious	average	aware	awesome	awful	awkward	bubbly	bulky	bumpy	buoyant	burdensome	burly	bustling	busy	buttery	buzzing	critical	crooked	crowded	cruel	crushing	cuddly	cultivated	cultured	cumbersome	curly	curvy	cute	cylindrical	doting	double	downright	drab	drafty	dramatic	dreary	droopy	dry	dual	dull	dutiful	excited	exciting	exotic	expensive	experienced	expert	extralarge	extraneous	extrasmall	extroverted	frilly	frivolous	frizzy	front	frosty	frozen	frugal	fruitful	full	fumbling	functional	funny	fussy	fuzzy	growing	growling	grown	grubby	gruesome	grumpy	guilty	gullible	gummy	humble	humiliating	humming	humongous	hungry	hurtful	husky	intelligent	intent	intentional	interesting	internal	international	intrepid	ironclad	irresponsible	irritating	itchy	jumpy	junior	juvenile	known	kooky	kosher	low	loyal	lucky	lumbering	luminous	lumpy	lustrous	luxurious	mountainous	muddy	muffled	multicolored	mundane	murky	mushy	musty	muted	mysterious	noteworthy	novel	noxious	numb	nutritious	nutty	onerlooked	outrageous	outstanding	oval	overcooked	overdue	overjoyed	profuse	proper	proud	prudent	punctual	pungent	puny	pure	purple	pushy	putrid	puzzled	puzzling	quirky	quixotic	quizzical	royal	rubbery	ruddy	rude	rundown	runny	rural	rusty	stupendous	stupid	sturdy	stylish	subdued	submissive	substantial	subtle	suburban	sudden	sugary	sunny	super	superb	superficial	superior	supportive	surefooted	surprised	suspicious	svelte	sweaty	sweet	sweltering	swift	sympathetic	trivial	troubled	trusting	trustworthy	trusty	truthful	tubby	turbulent	twin	upright	upset	urban	usable	used	useful	useless	utilized	utter	vital	vivacious	vivid	voluminous	worried	worrisome	worse	worst	worthless	worthwhile	worthy	wrathful	wretched	writhing	wrong	wry	yummy	true	aliceblue	antiquewhite	aqua	aquamarine	azure	beige	bisque	black	blanchedalmond	blue	blueviolet	brown	burlywood	cadetblue	chartreuse	chocolate	coral	cornflowerblue	cornsilk	crimson	cyan	darkblue	darkcyan	darkgoldenrod	darkgray	darkgreen	darkgrey	darkkhaki	darkmagenta	darkolivegreen	darkorange	darkorchid	darkred	darksalmon	darkseagreen	darkslateblue	darkslategray	darkslategrey	darkturquoise	darkviolet	deeppink	deepskyblue	dimgray	dimgrey	dodgerblue	firebrick	floralwhite	forestgreen	fractal	fuchsia	gainsboro	ghostwhite	gold	goldenrod	gray	green	greenyellow	honeydew	hotpink	indianred	indigo	ivory	khaki	lavender	lavenderblush	lawngreen	lemonchiffon	lightblue	lightcoral	lightcyan	lightgoldenrod	lightgoldenrodyellow	lightgray	lightgreen	lightgrey	lightpink	lightsalmon	lightseagreen	lightskyblue	lightslateblue	lightslategray	lightsteelblue	lightyellow	lime	limegreen	linen	magenta	maroon	mediumaquamarine	mediumblue	mediumforestgreen	mediumgoldenrod	mediumorchid	mediumpurple	mediumseagreen	mediumslateblue	mediumspringgreen	mediumturquoise	mediumvioletred	midnightblue	mintcream	mistyrose	moccasin	navajowhite	navy	navyblue	oldlace	olive	olivedrab	opaque	orange	orangered	orchid	palegoldenrod	palegreen	paleturquoise	palevioletred	papayawhip	peachpuff	peru	pink	plum	powderblue	purple	red	rosybrown	royalblue	saddlebrown	salmon	sandybrown	seagreen	seashell	sienna	silver	skyblue	slateblue	slategray	slategrey	snow	springgreen	steelblue	tan	teal	thistle	tomato	transparent	turquoise	violet	violetred	wheat	white	whitesmoke	yellow	yellowgreen"          
ADJECTIVES_LIST = [s.upper() for s in ADJECTIVES_LIST.split('\t')]
COLORS_LIST = ["sky blue", "green yellow", "coral", "orchid", "DarkOliveGreen2", "plum3", "gray60", "wheat", "pale violet red", "salmon", "sienna", "lavender", "honeydew", "moccasin", "brown1", "green2", "OliveDrab1", "turquoise1", "tan1", "LightCyan2", "SeaGreen1", "PaleGreen2"]
           
MAX_TERRAIN_WIDGET_WIDTH = 6  # number of terrain widgets to be displayed horizontally before starting a new row
LABEL_FONT = ("Calibri", 10, "bold")
PREVIEW_SIZE = 8
   
default_settings = {    'map_width':    25,
                        'map_height':   25,
                   }
settings = deepcopy(default_settings)
   
root = tk.Tk()
output = ""
          
          
#################################
#                               #
#       --- Classes ---         #
#                               #
#################################


class TerrainType(object):
    def __init__(self, image, min_size=0, max_size=0, max_objects=None, name=None, color=None):
        self.image = image  # e.g. 'STONE_IMAGE' or 'PINE_IMAGE'
        # self._min_size = min_size
        # self._max_size = max_size        
        self.min_size = min_size
        self.max_size = max_size
        self.max_objects = max_objects
        self.name = name if name is not None else random.choice(ADJECTIVES_LIST) + " " + random.choice(ANIMALS_LIST)
        self.color = color if color is not None else random.choice(COLORS_LIST)
       

    # don't actually want to do this -- don't want to arbitrarily decide the order in which min_size and max_size are
    #   checked
    #
    # @property
    # def min_size(self):
        # return self._min_size
        
    # @min_size.setter
    # def min_size(self, min_size):
        # if min_size > self._max_size
        # self._min_size   


class TerrainObject(object):
    def __init__(self, terrain_type, x, y, size):
        self.terrain_type = terrain_type
        self.x = x
        self.y = y
        self.size = size
        
    def get_out_str(self):
        """Return the command string to create this TerrainObject in roll20."""
        return ",".join(["!makeMapToken", str(self.x), str(self.y), str(self.size), str(self.terrain_type.image)])
        
        
class BattleMap(object):
    def __init__(self, width, height):
        if width < 1 or height < 1:
            messagebox.showerror("Error", "Invalid map width and height. They will be set to the default values " 
                "width=%d, height=%d." % (default_settings["map_width"], default_settings["map_height"]))
            
            self._width = default_settings["map_width"]
            self._height = default_settings["map_height"]
        else:    
            self._width = width
            self._height = height
        
        self._rows = [[None for i in range(self._height)] for j in range(self._width)]  # 2D representation of the map
        self._terrain_objects = []  # all the objects added to the map
     
        
    def in_bounds(self, x, y, size=1):
        """Checks to see if the terrain object of given size with its top left corner at x,y could fit in the map. True
        if so, False if not."""
        left = x
        right = left + size - 1
        top = y
        bottom = top + size - 1
        
        if left < 0 or right > self._width - 1 or top < 0 or bottom > self._height - 1:
            return False
            
        return True
        
        
    def get(self, x, y):
        """Get TerrainObject at (x,y), or None if nothing is there or coordinates are out of bounds."""
        if not self.in_bounds(x, y):
            return None
            
        return self._rows[x][y]

        
    def check_collision(self, x, y, size=1):
        """Checks to see if there is a TerrainObject at (x,y). If size > 1, checks a square of that size with its top
        left corner at x,y. Returns True if there's anything there, False if not or if out of bounds."""
        if not self.in_bounds(x, y, size):
            return False
            
        for x_coord in range(x, x + size):  # these maps aren't very big, so efficiency doesn't matter much
            for y_coord in range(y, y + size):
                if self._rows[x_coord][y_coord] is not None:
                    return True
                    
        return False
        
 
    def add(self, terrain_object, collision=True):
        """Add a TerrainObject with top left corner at (terrain_object.x, terrain_object.y). If collision=True, will not 
        add the terrain object if there's one already there. Will not add a TerrainObject that is already in this
        BattleMap's list of TerrainObjects. Returns True if successful, False otherwise."""
        if not self.in_bounds(terrain_object.x, terrain_object.y, terrain_object.size):
            return False

        if terrain_object in self._terrain_objects:
            return False
            
        if collision and self.check_collision(terrain_object.x, terrain_object.y, terrain_object.size):
            return False
            
        self._terrain_objects.append(terrain_object)
        
        for x_coord in range(terrain_object.x, terrain_object.x + terrain_object.size):
            for y_coord in range(terrain_object.y, terrain_object.y + terrain_object.size):
                self._rows[x_coord][y_coord] = terrain_object
                
        return True
        
        
    def redraw(self):
        """Remove everything and add it back in the order in self._terrain_objects."""
        self._rows = [[None for i in range(height)] for j in range(width)]
        terrain_objects = self._terrain_objects
        self._terrain_objects = None
        
        for t_o in terrain_objects:
            self.add(t_o)     

            
    def delete(self, x, y):
        """Remove and return the TerrainObject at (x,y). Calls redraw to update the map's 2D representation."""
        terrain_object = self.get(x, y)
        self._terrain_objects.remove(terrain_object)
        self.redraw()
        return terrain_object
    

    def ensure_playable(self, empty_terrain_types=None):
        """Uses connected-component region labeling to ensure that all the empty spaces in a BattleMap are touching. Any
        TerrainObjects in the way are removed from the BattleMap, ruthlessly.
        
        Args:
            empty_terrain_types:    An iterable of TerrainTypes which are treated as 'empty', e.g. "shallow water", 
                                        "brick floor". Coordinates in battle_map which contain 'None' are also empty.
                                        
                                        todo: actually implement empty_terrain_types stuff
        """
        empty_terrain_types = (None,) if empty_terrain_types is None else empty_terrain_types
        
        
        class UndirectedGraph(object):
            """Undirected graph data structure, mostly a copy of a great SO answer here:
            http://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python
            """
            
            
            def __init__(self, connections):
                self._graph = defaultdict(set)
                
                
            def add_connections(self, connections):
                """Add connections (list of tuple pairs) to the graph."""
                for node1, node2 in connections:
                    self.add(node1, node2)
                    
                    
            def add(self, node1, node2):
                """Add a connection between node1 and node2."""
                self._graph[node1].add(node2)
                self._graph[node2].add(node1)
                
                
            def remove(self, node):
                """Remove all references to node."""
                for n, cxns in self._graph.iteritems():
                    try:
                        cxns.remove(node)
                    except KeyError:
                        pass
                
                try:
                    del self._graph[node]
                except KeyError:
                    pass
                    
                    
            def is_connected(self, node1, node):
                """Is node1 directly connected to node2"""
                return node1 in self._graph and node2 in self._graph[node1]
                
                
            def find_path(self, node1, node2, path=[]):
                """Find ANY path between node1 and node2 (may not be shortest)"""
                path = path + [node1]
                if node1 == node2:
                    return path
                    
                if node1 not in self._graph:
                    return None
                    
                for node in self._graph[node1]:
                    if node not in path:
                        new_path = self.find_path(node, node2, path)
                        if new_path:
                            return new_path
                return None
        
        
        # Find regions -----------------------------------------------
        labeled_map = [[0 for y in range(self._height)] for x in range(self._width)]

        for x in range(self._width):
            for y in range(self._height):
                if self.get(x,y) not in empty_terrain_types:
                    labeled_map[x][y] = 0
                else:
                    labeled_map[x][y] = 1
                    
        equivalences = defaultdict(set)
        labelcount = 1
        
        #first pass
        for y in range(self._height):
            for x in range(self._width):
                left = 0
                up = 0
                
                if labeled_map[x][y] == 0:
                    continue
                    
                if x - 1 >= 0:
                    left = labeled_map[x-1][y]
                if y - 1 >= 0:
                    up = labeled_map[x][y-1]
                    
                if left == up == 0:  # neighbors aren't labeled, so we make a new label and assign it to ourself
                    labelcount += 1
                    labeled_map[x][y] = labelcount
                else:
                    if left > 0 and up > 0:  # then our neighbors are connected, so we assign ourself one of their regions and make a note of their regions' equivalence
                        labeled_map[x][y] = min(left, up)
                        if left != up:
                            equivalences[max(left,up)].add(min(left,up))
                    elif left > 0:
                        labeled_map[x][y] = left
                    else:
                        labeled_map[x][y] = up
                    

                        
                
        for y in range(self._height):
            outstr = []
            for x in range(self._width):
                outstr += str(labeled_map[x][y])
            outstr = ' '.join(["%2s" % i for i in outstr])
            print(outstr)
            
        print()
        for k,v in equivalences.items():
            print(str(k) + "\t" + str(v))
                
        
        # Create region graph ----------------------------------------
        # If two blank regions are not connected, connect them -------
        
        # for x in range(self._width):
            # for y in range(self._height):
                # if self.get(x,y) not in empty_terrain_types:
        
        # for x in range(self._width):
            # for y in range(self._height):
                # if self.get(x,y) not in empty_terrain_types:
                    # labeled_map[x][y] = 1
        
        
        
        
    def get_out_str(self):
        """Returns the string of commands to create this BattleMap in Roll20."""
        out_commands = ["!setup"]
        for t_o in self._terrain_objects:
            out_commands.append(t_o.get_out_str())
        
        return "\n".join(out_commands)
        
        
Terrain_Widget = namedtuple("Terrain_Widget", "container, terrain_type, name_label, min_size_label, min_size_scale, \
                             max_size_label, max_size_scale, max_objects_label, max_objects_scale")
        
        
class TerrainWindow(tk.Frame):
    def __init__(self, master=None, terrain_types=None):
        super().__init__(master)
        # self.outtxt = outtxt
        self.terrain_types = terrain_types
        self.pack()
        self.terrain_widgets = []
        self.create_widgets()
        
        
    def create_terrain_widget(self, terrain_type, master):
        container = tk.Frame(master)
    
        name_label = tk.Label(container, text=terrain_type.name, bg=terrain_type.color, relief=tk.RIDGE, 
                              padx=4, font=LABEL_FONT)
        name_label.pack()
        
        min_size_label = tk.Label(container, text="Min " + terrain_type.name + " Size", font=LABEL_FONT)
        min_size_label.pack()
        min_size_scale = tk.Scale(container, from_=1, to=min(settings["map_width"], settings["map_height"]), 
                                  resolution=1, orient=tk.HORIZONTAL)
        min_size_scale.pack()
        
        max_size_label = tk.Label(container, text="Max " + terrain_type.name + " Size", font=LABEL_FONT)
        max_size_label.pack()
        max_size_scale = tk.Scale(container, from_=1, to=min(settings["map_width"], settings["map_height"]), 
                                  resolution=1, orient=tk.HORIZONTAL)
        max_size_scale.pack()
        
        max_objects_label = tk.Label(container, text="Max "  + terrain_type.name + " Objects", font=LABEL_FONT)
        max_objects_label.pack()
        max_objects_scale = tk.Scale(container, from_=0, to=(settings["map_width"] * settings["map_height"] // 8), 
                                     resolution=1, orient=tk.HORIZONTAL)
        max_objects_scale.pack()
        
        return Terrain_Widget(container, terrain_type, name_label, min_size_label, min_size_scale, max_size_label, 
                              max_size_scale, max_objects_label, max_objects_scale)        
        
        
    def create_widgets(self):  
        # -------- Draw the grid of sliders -------- #
        
        self.terrains_frame = tk.Frame(self)
        
        tcount = 0
        while tcount < len(self.terrain_types):
            for i in range(MAX_TERRAIN_WIDGET_WIDTH):
                if tcount >= len(self.terrain_types):
                    break
                    
                self.terrain_widgets.append(self.create_terrain_widget(self.terrain_types[tcount], self.terrains_frame))
                self.terrain_widgets[tcount].container.grid(row=tcount // MAX_TERRAIN_WIDGET_WIDTH, column=i, sticky=tk.W + tk.E)
                tcount += 1
            
        self.terrains_frame.pack(side="top")

        
        # ------------ Draw the output  ----------- #
        
        self.output_frame = tk.Frame(self)
        
        self.preview_frame = tk.Canvas(self.output_frame, width=settings["map_width"] * PREVIEW_SIZE + 1, height=settings["map_height"] * PREVIEW_SIZE + 1)
        self.preview_frame.pack(side="left")
        
        self.outtxt = tk.Text(self.output_frame, width=35, height=9)
        self.outtxt.insert(tk.END, "Paste me into Roll20!")
        self.outtxt.config(state=tk.DISABLED)
        self.outtxt.pack(side="left")

        self.output_frame.pack(side="bottom")
        

        # ------------ Draw the buttons ----------- #
        
        self.buttons_frame = tk.Frame(self.output_frame)
        
        self.generate_button = tk.Button(self.buttons_frame, text="GENERATE", bg="green", fg="white", 
                                         command=self.generate_terrain, font=LABEL_FONT)
        self.generate_button.pack(side="bottom")
        
        self.max_objects_frame = tk.Frame(self.buttons_frame)
        self.max_objects_label = tk.Label(self.max_objects_frame, text="Max Objects", font=LABEL_FONT)
        self.max_objects_scale = tk.Scale(self.max_objects_frame, from_=1, 
                                          to=settings["map_width"] * settings["map_height"] // 4, resolution=1, 
                                          orient=tk.HORIZONTAL)
        self.max_objects_label.pack(side="top")
        self.max_objects_scale.pack(side="top")
        self.max_objects_frame.pack(side="left")
              
        # self.quit = tk.Button(self.buttons_frame, text="QUIT", bg="red", command=root.destroy)
        # self.quit.pack(side="left")
        
        self.buttons_frame.pack(side="right")

  
    def update_terrain_types(self):
        for t_w in self.terrain_widgets:
            t_w.terrain_type.min_size = t_w.min_size_scale.get()
            
            if t_w.max_size_scale.get() < t_w.terrain_type.min_size:
                messagebox.showwarning("Invalid parameters", "Min size > max size for " + str(t_w.terrain_type.name) + 
                    ". Max size will be treated as equal to min size for this type.")
                t_w.terrain_type.max_size = t_w.terrain_type.min_size
            else:
                t_w.terrain_type.max_size = t_w.max_size_scale.get()
                
            t_w.terrain_type.max_objects = t_w.max_objects_scale.get()
            
        
    def generate_terrain(self):  # probably want to move actual terrain generation code somewhere else...some day
        self.update_terrain_types()
    
        bmap = BattleMap(settings["map_width"], settings["map_height"])
        for i in range(self.max_objects_scale.get()):  # just for testing -- sophisticated terrain gen is next goal
            ttype = random.choice(self.terrain_types)
            size = random.randrange(ttype.min_size, ttype.max_size + 1, 1)
            locx = random.randrange(0, settings["map_width"], 1)
            locy = random.randrange(0, settings["map_height"], 1)
            bmap.add(TerrainObject(ttype, locx, locy, size))

        bmap.ensure_playable()
            
        self.preview_frame.delete(tk.ALL)
        self.preview_frame.create_rectangle((0, 0, self.preview_frame.winfo_width() - 1, self.preview_frame.winfo_height() - 1),
                                            fill="black")
                                            
        for x in range(settings["map_width"]):
            for y in range(settings["map_height"]):
                terrain_object = bmap.get(x,y)
                color = terrain_object.terrain_type.color if terrain_object is not None else 'white'
                coords = x * PREVIEW_SIZE + 2, y * PREVIEW_SIZE + 2,\
                         x * PREVIEW_SIZE + PREVIEW_SIZE + 2, y * PREVIEW_SIZE + PREVIEW_SIZE + 2
                self.preview_frame.create_rectangle(coords, fill=color)
        
        
        self.outtxt.config(state=tk.NORMAL)
        self.outtxt.delete(1.0, tk.END)
        self.outtxt.insert(tk.END, bmap.get_out_str())
        self.outtxt.config(state=tk.DISABLED)
        
        
#################################
#                               #
#       --- Functions ---       #
#                               #
#################################
   

#################################
#                               #
#       --- Execution ---       #
#                               #
#################################
      # def __init__(self, image, min_size, max_size, max_objects=None, name=None):

  
def main():
    pine_type = TerrainType("PINE_IMAGE", 1, 10, 10, "PINE", "green")
    stone_type = TerrainType("STONE_IMAGE", 1, 10, 10, "STONE", "gray60")
    
    # gui = GUI(master=root, terrain_types=[TerrainType("fff") for i in range(15)])
    root.wm_title("Random Terrain by Adam Mansfield! if(D && D) ∩༼˵☯‿☯˵༽つ¤=[]:::::>")
    root.minsize(600, 0)

    # out_window = tk.Toplevel()
    # # out_window.minsize(400, 600)
    # out_window.title("Paste this in Roll20")
    # outtxt = tk.Text(out_window, width=40)
    # outtxt.insert(tk.END, "Paste me into Roll20!")
    # outtxt.config(state=tk.DISABLED)
    # outtxt.pack()
    
    # terrain_window = TerrainWindow(master=root, outtxt=outtxt, terrain_types=[pine_type, stone_type] + [TerrainType(str(i)) for i in range(10)])
    terrain_window = TerrainWindow(master=root, terrain_types=[pine_type, stone_type] + [TerrainType("PINE_IMAGE") for i in range(6)])
    
    root.mainloop()
    

if __name__ == '__main__':
    main()
    
    
# example output
#
# !setup
# !makeMapToken, 1, 1, 1, STONE_IMAGE
# !makeMapToken, 4, 4, 5, STONE_IMAGE

# !setup
# !makeMapToken, gridX, gridY, sizeMul, image 
# ...
# currently only images are STONE_IMAGE and PINE_IMAGE