import textwrap

alkutarina = ('Alkutarina on vielä tulossa.'
              )
wrapper1 = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
ensimmainen = wrapper1.wrap(text=alkutarina)
def johdanto():
    return ensimmainen



kirje_teksti = ('Rakas, ajattelin sinua tänään, kun keitin aamukahvit ja katselin ikkunasta, '
         'kuinka valo hiipi hiljaa pihan yli. Sinä tulit mieleeni niin kirkkaasti, että oli pakko tarttua kynään '
         'ja lähettää sinulle pieni tervehdys. Toivon, että muistat välillä pysähtyä. '
         'Elämä kulkee usein niin kovaa, että tärkeimmät hetket vilahtavat ohi, jos ei malta hengähtää. Minä olen oppinut, '
         'että kiire ei vie mihinkään, mutta rauha vie kaikkialle. Pidä siis huolta itsestäsi. Ja muista: '
         'elämä ei ole kilpailu, vaan matka, jossa jokainen askel on arvokas.Lämpimin ajatuksin, Mummo')
wrapper2 = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
toinen = wrapper2.wrap(text=kirje_teksti)
def kirje():
    return toinen



teelusikka = ('Vihdoin ja viimein löysin teelusikan. En ymmärrä miksi mummo halusi minun löytävän tämän, kun lusikka menee '
              'iha rihkamasta. Ehkä sillä on jotain suurempaa tunnearvoa, josta en vaan tiedä?')
wrapper3 = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
kolmas = wrapper3.wrap(text=teelusikka)
def teelusikka():
    return kolmas

kaulakoru = ('Mikä tuolla kiiltää. Ei voi olla, ei voi olla. Suvun perintökaulakoru. Tämähän on täyttä kultaa!'
             'Luulin aina äitini valehdelleen minulle kertoessaan tästä korusta ja kaikesta mitä se on vuosien '
             'aikana kokenut. Mutta miten mummo on saanut sen itselleen, kun sen pitäsi olla lukkojen takana '
             'pankissa? Nyt laitan tämän oikeen hyvään talteen!')
wrapper4 = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
neljäs = wrapper4.wrap(text=kaulakoru)
def kaulakoru():
    return neljäs

nahkahanskat = ('Niin lämpöiset. Niin mukavat. Miten mummon onkin voinut unohtaa hanskansa. Ja vielä nahkaiset sellaiset. '
                'Toivottavasti hän löysi loppumatkalleen toiset samanlaiset.')
wrapper5 = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
viides = wrapper5.wrap(text=nahkahanskat)
def nahkahanskat():
    return viides

taskukello = ('Oi löysin mummoni taskukellon, jonka hän oli saanut aikoinaan isältään. Sehän on jopa vielä ihan ajassa. '
              'Tämän avulla mummo onkin ollut aina ajoissa oli tilaisuus mikä tahansa. '
              'Ehkä hän susotuu joskus antamaan kellon minulle, niin opin itsekkin paremmaksi ajan hallitsijaksi.')
wrapper6 = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
kuudes = wrapper6.wrap(text=taskukello)
def taskukello():
    return kuudes