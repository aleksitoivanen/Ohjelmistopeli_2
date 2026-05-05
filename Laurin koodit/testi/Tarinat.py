import textwrap

alkutarina = ('Peli alkaa. Olet saanut mummoltasi pyynnön käydä etsimässä hänen kadottamansa esineet Euroopasta, jotka hän '
              'on hävittänyt lomareissullaan. Mummosi on myös huolissaan uusista EU-direktiiveistä ja hän on asettanut sinulle '
              'rajoitteet lentämisessä. Jos ylität asetetun rajan, peli päättyy ja et saa hoidettua annettua tehtävää loppuun. Mummo '
              'on kuitenkin sen verran arvoituksellineen, ettei hän suoraan kertonut missä esineet sijaitsevat vaan hän on antanut sinulle '
              'vihjeitä, ehkä hän haluaa opettaa sinulle jotakin. Onnea matkaan.'
              )
wrapper1 = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
ensimmainen = wrapper1.wrap(text=alkutarina)
def johdanto():
    return ensimmainen



kirje_teksti = ('Nyt on kummallista, pelkkä kirje. Kehtaanko avata tätä? Kai se on pakko, kun ei tässä kuoressa lue mitään. "Rakas, ajattelin sinua tänään, kun keitin aamukahvit ja katselin ikkunasta, '
         'kuinka valo hiipi hiljaa pihan yli. Sinä tulit mieleeni niin kirkkaasti, että oli pakko tarttua kynään '
         'ja lähettää sinulle pieni tervehdys. Toivon, että muistat välillä pysähtyä. '
         'Elämä kulkee usein niin kovaa, että tärkeimmät hetket vilahtavat ohi, jos ei malta pysähtyä ja hengähtää. Minä olen oppinut, '
         'että kiire ei vie mihinkään, mutta rauha vie kaikkialle. Pidä siis huolta itsestäsi. Ja muista, että  '
         'elämä ei ole kilpailu, vaan matka, jonka me jokainen koemme vain kerran. Lämpimin ajatuksin, Mummo." '
        'Tiesin, että mummo on hyvä kirjoittamaan, mutta tämä meni syvälle tunteisiin. Nyt voin hyvillä mielillä palata mummon luokse.')
wrapper2 = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
toinen = wrapper2.wrap(text=kirje_teksti)
def kirje():
    return toinen



teelusikka = ('Vihdoin ja viimein löysin teelusikan. En ymmärrä miksi mummo halusi minun löytävän tämän, kun lusikka menee '
              'ihan rihkamasta. Ehkä sillä on jotain suurempaa tunnearvoa, jota en vain ymmärrä? Ja kappas, lusikassa on seuraava vihje toisen esineen luokse.')
wrapper3 = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
kolmas = wrapper3.wrap(text=teelusikka)
def teelusikka():
    return kolmas

kaulakoru = ('Mikä tuolla kiiltää. Ei voi olla, ei voi olla. Suvun perintökaulakoru. Tämähän on täyttä kultaa!'
             'Luulin aina mummoni valehdelleen minulle kertoessaan tästä korusta ja kaikesta mitä se on vuosien '
             'aikana kokenut. Mutta miten mummo on saanut sen itselleen, kun sen pitäsi olla lukkojen takana '
             'pankissa? Nyt laitan tämän oikeen hyvään talteen! Onneksi koru ja uusi vihje eivät olleet päätyneet vääriin käsiin.')
wrapper4 = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
neljäs = wrapper4.wrap(text=kaulakoru)
def kaulakoru():
    return neljäs

nahkahanskat = ('Niin lämpöiset. Niin mukavat. Miten mummon onkin voinut unohtaa hanskansa. Ja vielä nahkaiset sellaiset. '
                'Toivottavasti hän löysi loppumatkalleen toiset samanlaiset. Mutta mitä ihmettä sisälle on tungettu. Paperilappu, no onpa rypyssä. '
                'Hädin tuskin saan luettua tekstiä, mutta yritetään silti.')
wrapper5 = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
viides = wrapper5.wrap(text=nahkahanskat)
def nahkahanskat():
    return viides

taskukello = ('Oi löysin mummoni taskukellon, jonka hän oli saanut aikoinaan isältään. Sehän on jopa vielä ihan ajassa. '
              'Tämän avulla mummo onkin ollut aina ajoissa oli tilaisuus mikä tahansa. '
              'Ehkä hän suostuu joskus antamaan kellon minulle, niin opin itsekkin paremmaksi ajan hallitsijaksi. Mutta mitä ihmettä, kello pysähtyi! '
              'Kellon viisarit pysähtyivät juuri sopivasti, että näen kello tauluun kirjoitetun tekstin. Tässähän alkaa olla ihan '
              'James Bond meininkiä. Ehkä se on uusi vihje?')
wrapper6 = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
kuudes = wrapper6.wrap(text=taskukello)
def taskukello():
    return kuudes