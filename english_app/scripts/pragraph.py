
from main_app.models import Paragraph

paragraphs = [
    "The sun was setting behind the mountains, casting a golden glow across the landscape. The air was still and quiet, with only the sound of crickets chirping in the distance.",
    "The city was bustling with activity, as people rushed to and fro in the busy streets. Cars honked their horns, and pedestrians jostled for space on the sidewalks.",
    "The ocean was calm and serene, with waves gently lapping at the shore. Seagulls cried out overhead, and a salty breeze filled the air.",
    "The forest was dense and verdant, with towering trees reaching up to the sky. The rustling of leaves and the chirping of birds filled the air.",
    "The desert was hot and barren, with nothing but sand and rocks stretching out for miles in every direction. The sun beat down mercilessly, and the air was dry and dusty.",
    "The mountains loomed in the distance, their jagged peaks piercing the sky. Snow capped their summits, and a cold wind blew down from their heights.",
    "The city skyline stretched out before me, a sea of towering skyscrapers and flashing lights. The sound of traffic filled the air, and the night was alive with energy.",
    "The river flowed gently through the countryside, winding its way through green fields and pastures. The water was clear and sparkling, and fish darted to and fro beneath its surface.",
    "The jungle was thick and wild, with vines and branches criss-crossing overhead. The air was humid and heavy, and the sounds of exotic birds and animals filled the air.",
    "The meadow was filled with wildflowers, their colorful petals swaying in the breeze. The sun was shining brightly overhead, and the sky was a deep shade of blue.",
    "The snow was falling softly, blanketing the world in a layer of white. The air was cold and crisp, and the only sound was the crunching of snow beneath my feet.",
    "The beach was dotted with umbrellas and sunbathers, enjoying the warmth of the sun and the cool breeze off the ocean. The sand was soft and warm beneath my feet.",
    "The city park was filled with people enjoying the beautiful day. Children played on swings and slides, and dogs ran and barked with excitement.",
    "The countryside was peaceful and quiet, with rolling hills and fields of wheat and corn. The sun was shining down, and a light breeze rustled through the crops.",
    "The old town was full of historic buildings and narrow streets, lined with quaint shops and cafes. The air was filled with the smells of fresh-baked bread and roasting coffee.",
    "The city square was bustling with activity, with street performers and vendors selling their wares. The sound of music and laughter filled the air.",
    "The bridge stretched out before me, spanning the wide river below. The water rushed by far below, and the wind whipped through my hair.",
    "The farm was busy with activity, with cows mooing and chickens clucking. The sun was shining down, and the air was filled with the smell of freshly-mowed hay.",
    "The trail wound its way up the mountain, switchbacking through thick forests and rocky outcroppings. The air grew colder as I climbed higher, and the views became more spectacular.",
    "The city skyline at night was a sea of twinkling lights, with the tallest buildings rising up like stars. The air was cool and crisp, and the sounds of the city were muted.",
     "The garden was a riot of color, with flowers of everyhue and variety blooming in profusion. Bees buzzed from blossom to blossom, and the air was heavy with the scent of roses and lilies.",
    "The amusement park was a riot of noise and activity, with roller coasters and carnival games vying for attention. The smell of popcorn and cotton candy filled the air, and children laughed and shouted with delight.",
    "The airport was a hub of activity, with planes taking off and landing every few minutes. The sound of jet engines filled the air, and travelers rushed to catch their flights.",
    "The concert hall was filled with music lovers, listening intently to the strains of a symphony orchestra. The acoustics were perfect, and the music filled the air with a beautiful melody.",
    "The train station was bustling with travelers, rushing to catch their trains or saying goodbye to loved ones. The sound of train whistles and announcements echoed through the air.",
    "The university campus was a hive of activity, with students hurrying to class and professors discussing academic topics. The air was filled with the scent of freshly-cut grass and the sound of ringing bells.",
]


for paragraph in paragraphs:
    p = Paragraph(paratext=paragraph)
    p.save()
