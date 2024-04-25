
import pygame
import time
import os
import sys
from gtts import gTTS
from playsound import playsound
import pyttsx3

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
fontColor = BLACK
bgColor = GREY
generic = pygame.image.load("AIPIC.png")
buttonColor = (80,80,80)



class TextScroll:
    def __init__(self, area, font, fg_color, bk_color, text, ms_per_line=800):
        """object to display lines of text scrolled in with a delay between each line
        in font and fg_color with background o fk_color with in the area rect"""

        super().__init__()
        self.rect = area.copy()
        self.fg_color = fg_color
        self.bk_color = bk_color
        self.size = area.size
        self.surface = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        self.surface.fill(bk_color)
        self.font = font
        self.lines = text.split('\n')
        self.ms_per_line = ms_per_line
        self.y = 0
        self.y_delta = self.font.size("M")[1]
        self.next_time = None
        self.dirty = False

    def _update_line(self, line):  # render next line if it's time
        if self.y + self.y_delta > self.size[1]:  # line does not fit in remaining space
            self.surface.blit(self.surface, (0, -self.y_delta))  # scroll up
            self.y += -self.y_delta  # backup a line
            pygame.draw.rect(self.surface, self.bk_color,
                             (0, self.y, self.size[0], self.size[1] - self.y))

        text = self.font.render(line, True, self.fg_color)
        # pygame.draw.rect(text, GREY, text.get_rect(), 1)  # for demo show render area
        self.surface.blit(text, (0, self.y))
        

        self.y += self.y_delta

    # call update from pygame main loop
    def update(self):

        time_now = time.time()
        if (self.next_time is None or self.next_time < time_now) and self.lines:
            self.next_time = time_now + self.ms_per_line / 1000
            line = self.lines.pop(0)
            self._update_line(line)
            self.dirty = True
            self.update()  # do it again to catch more than one event per tick

    # call draw from pygam main loop after update
    def draw(self, screen):
        if self.dirty:
            screen.blit(self.surface, self.rect)
            self.dirty = False


STORY2 = """Strong Son of God, immortal Love,
   Whom we, that have not seen thy face,
   By faith, and faith alone, embrace,
   Believing where we cannot prove;
 
Thine are these orbs of light and shade;
   Thou madest Life in man and brute;
   Thou madest Death; and lo, thy foot
Is on the skull which thou hast made.
 
Thou wilt not leave us in the dust:
Thou madest man, he knows not why,
He thinks he was not made to die;
And thou hast made him: thou art just.
 
Thou seemest human and divine,
   The highest, holiest manhood, thou.
   Our wills are ours, we know not how;
Our wills are ours, to make them thine.
 
Our little systems have their day;
   They have their day and cease to be:
   They are but broken lights of thee,
And thou, O Lord, art more than they.
 
We have but faith: we cannot know;
   For knowledge is of things we see
   And yet we trust it comes from thee,
A beam in darkness: let it grow.
 
Let knowledge grow from more to more,
   But more of reverence in us dwell;
   That mind and soul, according well,
May make one music as before,
 
But vaster. We are fools and slight;
   We mock thee when we do not fear:
   But help thy foolish ones to bear;
Help thy vain worlds to bear thy light.
 
Forgive what seem'd my sin in me;
   What seem'd my worth since I began;
   For merit lives from man to man,
And not from man, O Lord, to thee.
 
Forgive my grief for one removed,
   Thy creature, whom I found so fair.
   I trust he lives in thee, and there
I find him worthier to be loved.
 
Forgive these wild and wandering cries,
   Confusions of a wasted youth;
   Forgive them where they fail in truth,
And in thy wisdom make me wise.
 
I
I held it truth, with him who sings
   To one clear harp in divers tones,
   That men may rise on stepping-stones
Of their dead selves to higher things.
 
But who shall so forecast the years
   And find in loss a gain to match?
   Or reach a hand thro' time to catch
The far-off interest of tears?
 
Let Love clasp Grief lest both be drown'd,
   Let darkness keep her raven gloss:
   Ah, sweeter to be drunk with loss,
To dance with death, to beat the ground,
 
Than that the victor Hours should scorn
   The long result of love, and boast,
   `Behold the man that loved and lost,
But all he was is overworn.'
 
II
Old Yew, which graspest at the stones
   That name the under-lying dead,
   Thy fibres net the dreamless head,
Thy roots are wrapt about the bones.
 
The seasons bring the flower again,
   And bring the firstling to the flock;
   And in the dusk of thee, the clock
Beats out the little lives of men.
 
O, not for thee the glow, the bloom,
   Who changest not in any gale,
   Nor branding summer suns avail
To touch thy thousand years of gloom:
 
And gazing on thee, sullen tree,
   Sick for thy stubborn hardihood,
   I seem to fail from out my blood
And grow incorporate into thee.
 
III
O Sorrow, cruel fellowship,
   O Priestess in the vaults of Death,
   O sweet and bitter in a breath,
What whispers from thy lying lip?
 
'The stars,' she whispers, `blindly run;
   A web is wov'n across the sky;
   From out waste places comes a cry,
And murmurs from the dying sun:
 
'And all the phantom, Nature, stands—
   With all the music in her tone,
   A hollow echo of my own,—
A hollow form with empty hands.'
 
And shall I take a thing so blind,
   Embrace her as my natural good;
   Or crush her, like a vice of blood,
Upon the threshold of the mind?
 
IV
To Sleep I give my powers away;
   My will is bondsman to the dark;
   I sit within a helmless bark,
And with my heart I muse and say:
 
O heart, how fares it with thee now,
   That thou should'st fail from thy desire,
   Who scarcely darest to inquire,
'What is it makes me beat so low?'
 
Something it is which thou hast lost,
   Some pleasure from thine early years.
   Break, thou deep vase of chilling tears,
That grief hath shaken into frost!
 
Such clouds of nameless trouble cross
   All night below the darken'd eyes;
   With morning wakes the will, and cries, 
'Thou shalt not be the fool of loss.'
 
V
I sometimes hold it half a sin
   To put in words the grief I feel;
   For words, like Nature, half reveal
And half conceal the Soul within.
 
But, for the unquiet heart and brain,
   A use in measured language lies;
   The sad mechanic exercise,
Like dull narcotics, numbing pain.
 
In words, like weeds, I'll wrap me o'er,
   Like coarsest clothes against the cold:
   But that large grief which these enfold
Is given in outline and no more.
 
VI
One writes, that `Other friends remain,'
   That `Loss is common to the race'—
   And common is the commonplace,
And vacant chaff well meant for grain.
 
That loss is common would not make
   My own less bitter, rather more:
   Too common! Never morning wore
To evening, but some heart did break.
 
O father, wheresoe'er thou be,
   Who pledgest now thy gallant son;
   A shot, ere half thy draught be done,
Hath still'd the life that beat from thee.
 
O mother, praying God will save
   Thy sailor,—while thy head is bow'd,
   His heavy-shotted hammock-shroud
Drops in his vast and wandering grave.
 
Ye know no more than I who wrought
   At that last hour to please him well;
   Who mused on all I had to tell,
And something written, something thought;
 
Expecting still his advent home;
   And ever met him on his way
   With wishes, thinking, `here to-day,'
Or `here to-morrow will he come.'
 
O somewhere, meek, unconscious dove,
   That sittest ranging golden hair;
   And glad to find thyself so fair,
Poor child, that waitest for thy love!
 
For now her father's chimney glows
   In expectation of a guest;
   And thinking `this will please him best,'
She takes a riband or a rose;
 
For he will see them on to-night;
   And with the thought her colour burns;
   And, having left the glass, she turns
Once more to set a ringlet right;
 
And, even when she turn'd, the curse
   Had fallen, and her future Lord
   Was drown'd in passing thro' the ford,
Or kill'd in falling from his horse.
 
O what to her shall be the end?
   And what to me remains of good?
   To her, perpetual maidenhood,
And unto me no second friend.
 
VII
Dark house, by which once more I stand
   Here in the long unlovely street,
   Doors, where my heart was used to beat
So quickly, waiting for a hand,
 
A hand that can be clasp'd no more—
   Behold me, for I cannot sleep,
   And like a guilty thing I creep
At earliest morning to the door.
 
He is not here; but far away
   The noise of life begins again,
   And ghastly thro' the drizzling rain
On the bald street breaks the blank day.
 
VIII
A happy lover who has come
   To look on her that loves him well,
   Who 'lights and rings the gateway bell,
And learns her gone and far from home;
 
He saddens, all the magic light
   Dies off at once from bower and hall,
   And all the place is dark, and all
The chambers emptied of delight:
 
So find I every pleasant spot
   In which we two were wont to meet,
   The field, the chamber, and the street,
For all is dark where thou art not.
 
Yet as that other, wandering there
   In those deserted walks, may find
   A flower beat with rain and wind,
Which once she foster'd up with care;
 
So seems it in my deep regret,
   O my forsaken heart, with thee
   And this poor flower of poesy
Which little cared for fades not yet.
 
But since it pleased a vanish'd eye,
   I go to plant it on his tomb,
   That if it can it there may bloom,
Or, dying, there at least may die.
 
IX
Fair ship, that from the Italian shore
   Sailest the placid ocean-plains
   With my lost Arthur's loved remains,
Spread thy full wings, and waft him o'er.
 
So draw him home to those that mourn
   In vain; a favourable speed
   Ruffle thy mirror'd mast, and lead
Thro' prosperous floods his holy urn.
 
All night no ruder air perplex
   Thy sliding keel, till Phosphor, bright
   As our pure love, thro' early light
Shall glimmer on the dewy decks.
 
Sphere all your lights around, above;
   Sleep, gentle heavens, before the prow;
   Sleep, gentle winds, as he sleeps now,
My friend, the brother of my love;
 
My Arthur, whom I shall not see
   Till all my widow'd race be run;
   Dear as the mother to the son,
More than my brothers are to me.
 
X
I hear the noise about thy keel;
   I hear the bell struck in the night:
   I see the cabin-window bright;
I see the sailor at the wheel.
 
Thou bring'st the sailor to his wife,
   And travell'd men from foreign lands;
   And letters unto trembling hands;
And, thy dark freight, a vanish'd life.
 
So bring him; we have idle dreams:
   This look of quiet flatters thus
   Our home-bred fancies. O to us,
The fools of habit, sweeter seems
 
To rest beneath the clover sod,
   That takes the sunshine and the rains,
   Or where the kneeling hamlet drains
The chalice of the grapes of God;
 
Than if with thee the roaring wells
   Should gulf him fathom-deep in brine;
   And hands so often clasp'd in mine,
Should toss with tangle and with shells.
 
XI
Calm is the morn without a sound,
   Calm as to suit a calmer grief,
   And only thro' the faded leaf
The chestnut pattering to the ground:
 
Calm and deep peace on this high world,
   And on these dews that drench the furze,
   And all the silvery gossamers
That twinkle into green and gold:
 
Calm and still light on yon great plain
   That sweeps with all its autumn bowers,
   And crowded farms and lessening towers,
To mingle with the bounding main:
 
Calm and deep peace in this wide air,
   These leaves that redden to the fall;
   And in my heart, if calm at all,
If any calm, a calm despair:
 
Calm on the seas, and silver sleep,
   And waves that sway themselves in rest,
   And dead calm in that noble breast
Which heaves but with the heaving deep.
 
XII
Lo, as a dove when up she springs
   To bear thro' Heaven a tale of woe,
   Some dolorous message knit below
The wild pulsation of her wings;
 
Like her I go; I cannot stay;
   I leave this mortal ark behind,
   A weight of nerves without a mind,
And leave the cliffs, and haste away
 
O'er ocean-mirrors rounded large,
   And reach the glow of southern skies,
   And see the sails at distance rise,
And linger weeping on the marge,
 
And saying; `Comes he thus, my friend?
   Is this the end of all my care?'
   And circle moaning in the air:
'Is this the end? Is this the end?'
 
And forward dart again, and play
   About the prow, and back return
   To where the body sits, and learn
That I have been an hour away.
 
XIII
Tears of the widower, when he sees
   A late-lost form that sleep reveals,
   And moves his doubtful arms, and feels
Her place is empty, fall like these;
 
Which weep a loss for ever new,
   A void where heart on heart reposed;
   And, where warm hands have prest and closed,
Silence, till I be silent too.
 
Which weep the comrade of my choice,
   An awful thought, a life removed,
   The human-hearted man I loved,
A Spirit, not a breathing voice.
 
Come, Time, and teach me, many years,
   I do not suffer in a dream;
   For now so strange do these things seem,
Mine eyes have leisure for their tears;
 
My fancies time to rise on wing,
   And glance about the approaching sails,
   As tho' they brought but merchants' bales,
And not the burthen that they bring.
 
XIV
If one should bring me this report,
   That thou hadst touch'd the land to-day,
   And I went down unto the quay,
And found thee lying in the port;
 
And standing, muffled round with woe,
   Should see thy passengers in rank
   Come stepping lightly down the plank,
And beckoning unto those they know;
 
And if along with these should come
   The man I held as half-divine;
   Should strike a sudden hand in mine,
And ask a thousand things of home;
 
And I should tell him all my pain,
   And how my life had droop'd of late,
   And he should sorrow o'er my state
And marvel what possess'd my brain;
 
And I perceived no touch of change,
   No hint of death in all his frame,
   But found him all in all the same,
I should not feel it to be strange.
 
XV
To-night the winds begin to rise
   And roar from yonder dropping day:
   The last red leaf is whirl'd away,
The rooks are blown about the skies;
 
The forest crack'd, the waters curl'd,
   The cattle huddled on the lea;
   And wildly dash'd on tower and tree
The sunbeam strikes along the world:
 
And but for fancies, which aver
   That all thy motions gently pass
   Athwart a plane of molten glass,
I scarce could brook the strain and stir
 
That makes the barren branches loud;
   And but for fear it is not so,
   The wild unrest that lives in woe
Would dote and pore on yonder cloud
 
That rises upward always higher,
   And onward drags a labouring breast,
   And topples round the dreary west,
A looming bastion fringed with fire.
 
XVI
What words are these have falle'n from me?
   Can calm despair and wild unrest
   Be tenants of a single breast,
Or sorrow such a changeling be?
 
Or cloth she only seem to take
   The touch of change in calm or storm;
   But knows no more of transient form
In her deep self, than some dead lake
 
That holds the shadow of a lark
   Hung in the shadow of a heaven?
   Or has the shock, so harshly given,
Confused me like the unhappy bark
 
That strikes by night a craggy shelf,
   And staggers blindly ere she sink?
   And stunn'd me from my power to think
And all my knowledge of myself;
 
And made me that delirious man
   Whose fancy fuses old and new,
   And flashes into false and true,
And mingles all without a plan?
 
XVII
Thou comest, much wept for: such a breeze
   Compell'd thy canvas, and my prayer
   Was as the whisper of an air
To breathe thee over lonely seas.
 
For I in spirit saw thee move
   Thro' circles of the bounding sky,
   Week after week: the days go by:
Come quick, thou bringest all I love.
 
Henceforth, wherever thou may'st roam,
   My blessing, like a line of light,
   Is on the waters day and night,
And like a beacon guards thee home.
 
So may whatever tempest mars
   Mid-ocean, spare thee, sacred bark;
   And balmy drops in summer dark
Slide from the bosom of the stars.
 
So kind an office hath been done,
   Such precious relics brought by thee;
   The dust of him I shall not see
Till all my widow'd race be run.
 
XVIII
'Tis well; 'tis something; we may stand
   Where he in English earth is laid,
   And from his ashes may be made
The violet of his native land.
 
'Tis little; but it looks in truth
   As if the quiet bones were blest
   Among familiar names to rest
And in the places of his youth.
 
Come then, pure hands, and bear the head
   That sleeps or wears the mask of sleep,
   And come, whatever loves to weep,
And hear the ritual of the dead.
 
Ah yet, ev'n yet, if this might be,
   I, falling on his faithful heart,
   Would breathing thro' his lips impart
The life that almost dies in me;
 
That dies not, but endures with pain,
   And slowly forms the firmer mind,
   Treasuring the look it cannot find,
The words that are not heard again.
 
XIX
The Danube to the Severn gave
   The darken'd heart that beat no more;
   They laid him by the pleasant shore,
And in the hearing of the wave.
 
There twice a day the Severn fills;
   The salt sea-water passes by,
   And hushes half the babbling Wye,
And makes a silence in the hills.
 
The Wye is hush'd nor moved along,
   And hush'd my deepest grief of all,
   When fill'd with tears that cannot fall,
I brim with sorrow drowning song.
 
The tide flows down, the wave again
   Is vocal in its wooded walls;
   My deeper anguish also falls,
And I can speak a little then.
 
XX
The lesser griefs that may be said,
   That breathe a thousand tender vows,
   Are but as servants in a house
Where lies the master newly dead;
 
Who speak their feeling as it is,
   And weep the fulness from the mind:
   `It will be hard,' they say, `to find
Another service such as this.'
 
My lighter moods are like to these,
   That out of words a comfort win;
   But there are other griefs within,
And tears that at their fountain freeze;
 
For by the hearth the children sit
   Cold in that atmosphere of Death,
   And scarce endure to draw the breath,
Or like to noiseless phantoms flit;
 
But open converse is there none,
   So much the vital spirits sink
   To see the vacant chair, and think,
'How good! how kind! and he is gone.'
 
XXI
I sing to him that rests below,
   And, since the grasses round me wave,
   I take the grasses of the grave,
And make them pipes whereon to blow.
 
The traveller hears me now and then,
   And sometimes harshly will he speak:
   `This fellow would make weakness weak,
And melt the waxen hearts of men.'
 
Another answers, `Let him be,
   He loves to make parade of pain
   That with his piping he may gain
The praise that comes to constancy.'
 
A third is wroth: `Is this an hour
   For private sorrow's barren song,
   When more and more the people throng
The chairs and thrones of civil power?
 
'A time to sicken and to swoon,
   When Science reaches forth her arms
   To feel from world to world, and charms
Her secret from the latest moon?'
 
Behold, ye speak an idle thing:
   Ye never knew the sacred dust:
   I do but sing because I must,
And pipe but as the linnets sing:
 
And one is glad; her note is gay,
   For now her little ones have ranged;
   And one is sad; her note is changed,
Because her brood is stol'n away.
 
XXII
The path by which we twain did go,
   Which led by tracts that pleased us well,
   Thro' four sweet years arose and fell,
From flower to flower, from snow to snow:
 
And we with singing cheer'd the way,
   And, crown'd with all the season lent,
   From April on to April went,
And glad at heart from May to May:
 
But where the path we walk'd began
   To slant the fifth autumnal slope,
   As we descended following Hope,
There sat the Shadow fear'd of man;
 
Who broke our fair companionship,
   And spread his mantle dark and cold,
   And wrapt thee formless in the fold,
And dull'd the murmur on thy lip,
 
And bore thee where I could not see
   Nor follow, tho' I walk in haste,
   And think, that somewhere in the waste
The Shadow sits and waits for me.
 
XXIII
Now, sometimes in my sorrow shut,
   Or breaking into song by fits,
   Alone, alone, to where he sits,
The Shadow cloak'd from head to foot,
 
Who keeps the keys of all the creeds,
   I wander, often falling lame,
   And looking back to whence I came,
Or on to where the pathway leads;
 
And crying, How changed from where it ran
   Thro' lands where not a leaf was dumb;
   But all the lavish hills would hum
The murmur of a happy Pan:
 
When each by turns was guide to each,
   And Fancy light from Fancy caught,
   And Thought leapt out to wed with Thought
Ere Thought could wed itself with Speech;
 
And all we met was fair and good,
   And all was good that Time could bring,
   And all the secret of the Spring
Moved in the chambers of the blood;
 
And many an old philosophy
   On Argive heights divinely sang,
   And round us all the thicket rang
To many a flute of Arcady.
 
XXIV
And was the day of my delight
   As pure and perfect as I say?
   The very source and fount of Day
Is dash'd with wandering isles of night.
 
If all was good and fair we met,
   This earth had been the Paradise
   It never look'd to human eyes
Since our first Sun arose and set.
 
And is it that the haze of grief
   Makes former gladness loom so great?
   The lowness of the present state,
That sets the past in this relief?
 
Or that the past will always win
   A glory from its being far;
   And orb into the perfect star
We saw not, when we moved therein?
 
XXV
I know that this was Life,—the track
   Whereon with equal feet we fared;
   And then, as now, the day prepared
The daily burden for the back.
 
But this it was that made me move
   As light as carrier-birds in air;
   I loved the weight I had to bear,
Because it needed help of Love:
 
Nor could I weary, heart or limb,
   When mighty Love would cleave in twain
   The lading of a single pain,
And part it, giving half to him.
 
XXVI
Still onward winds the dreary way;
   I with it; for I long to prove
   No lapse of moons can canker Love,
Whatever fickle tongues may say.
 
And if that eye which watches guilt
   And goodness, and hath power to see
   Within the green the moulder'd tree,
And towers fall'n as soon as built—
 
Oh, if indeed that eye foresee
   Or see (in Him is no before)
   In more of life true life no more
And Love the indifference to be,
 
Then might I find, ere yet the morn
   Breaks hither over Indian seas,
   That Shadow waiting with the keys,
To shroud me from my proper scorn.
 
XXVII
I envy not in any moods
   The captive void of noble rage,
   The linnet born within the cage,
That never knew the summer woods:
 
I envy not the beast that takes
   His license in the field of time,
   Unfetter'd by the sense of crime,
To whom a conscience never wakes;
 
Nor, what may count itself as blest,
   The heart that never plighted troth
   But stagnates in the weeds of sloth;
Nor any want-begotten rest.
 
I hold it true, whate'er befall;
   I feel it, when I sorrow most;
   'Tis better to have loved and lost
Than never to have loved at all.
"""
language = 'en'

pygame.init()
pygame.mixer.init()
engine = pyttsx3.init()

# Set up the drawing window
screen = pygame.display.set_mode([1500, 800])
clock = pygame.time.Clock()


#vars
x,y = size = screen.get_width(), screen.get_height()

varX = x/10
varY = y/10

fLeft = varX
mLeft = ((x/2)-(2*varX))
mRight = ((x/2)+(2*varX))
fRight = (x-varX)

fTop = varY
mTop = (y/2)-varY
mBottom = (y/2)+varY
fBottom = (y-varY)

recH = ((y/2)-(2*varY))
recW = ((x/2)-(2*varX))

fontsize = x/70
font = pygame.font.SysFont("Liberation Sans", int(fontsize))
fontsize2 = x/50
font2 = pygame.font.SysFont("Liberation Sans", int(fontsize2))
fontsize3 = x/50
font3 = pygame.font.SysFont("Liberation Sans", int(fontsize3))

topTextW = x/4
topTextY = (x/2)-(topTextW/2)

buttonW = x/10
buttonH = y/10
buttonX = (x/2)-(buttonW/2)
buttonY = (3*y/4) - (buttonH/2)

imgSX = x/8
imgSY = x/8
imgX = (x/2)-(imgSX/2)
imgY = (y/2)-(imgSY/2)
imgSize = (imgSX, imgSY)
imgPst = (imgX, imgY)

generic = pygame.transform.scale(generic, imgSize)

message = TextScroll(pygame.Rect(fLeft, fTop, recW, recH), font, fontColor, bgColor, STORY2, ms_per_line=1000)
message2 = TextScroll(pygame.Rect(mRight, fTop, recW, recH), font, fontColor, bgColor, STORY2, ms_per_line=1000)
message3 = TextScroll(pygame.Rect(fLeft, mBottom, recW, recH), font, fontColor, bgColor, STORY2, ms_per_line=1000)
message4 = TextScroll(pygame.Rect(mRight, mBottom, recW, recH), font, fontColor, bgColor, STORY2, ms_per_line=1000)
messageTop = TextScroll(pygame.Rect(topTextY, fTop, topTextW, int((fontsize2*3))), font2, WHITE, bgColor, STORY2, ms_per_line=1000)

release = font3.render('RELEASE' , True , BLACK) 

screen.fill((128, 128, 128))


# Run until the user asks to quit
running = True
        
playsound('audiobook.mp3', False)


while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    else:
    # Fill the background with white
    # Draw a solid blue circle in the center
    #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    #pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,x/2,y/2))
        pygame.draw.line(screen, (0,0,0), (0,y/2),(x,y/2),(4))
        message.update()
        message2.update()
        message3.update()
        message4.update()
        messageTop.update()
        message.draw(screen)
        message2.draw(screen)
        message3.draw(screen)
        message4.draw(screen)
        messageTop.draw(screen)
        #button outlines
        pygame.draw.rect(screen,BLACK,[buttonX*.99, buttonY*.99, buttonW*1.088, buttonH*1.15]) 
        pygame.draw.rect(screen,buttonColor,[buttonX, buttonY, buttonW, buttonH]) 
        screen.blit(release, (buttonX, buttonY))

        screen.blit(generic, imgPst)
        pygame.display.flip()

        

        clock.tick(60)
        

pygame.quit()