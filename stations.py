radioStations = {   "Radio Gong"        : ["http://webstream.gong971.de/gong971",":/radiologos/radiologos/gong971.png"],
                    "StarFM"            : ["https://starfm-4.explodio.com/nuernberg.mp3",":/radiologos/radiologos/starfm.jpg"],
                    "Antenne Bayern"    : ["https://www.antenne.de/webradio/antenne.m3u",":/radiologos/radiologos/antenne.png"],
                    "Rock Antenne"      : ["http://www.rockantenne.de/webradio/rockantenne.aac.pls",":/radiologos/radiologos/rockantenne.png"],
                    "Bayern 1"          : ["https://br-br1-franken.cast.addradio.de/br/br1/franken/mp3/mid",":/radiologos/radiologos/bayern1.png"],
                    "Bayern 2"          : ["https://addrad.io/444y2ph",":/radiologos/radiologos/bayern2.png"],
                    "Bayern 3"          : ["https://br-edge-200b-fra-lg-cdn.cast.addradio.de/br/br3/live/mp3/mid",":/radiologos/radiologos/bayern3.png"],
                    "BR Heimat"         : ["https://br-brheimat-live.cast.addradio.de/br/brheimat/live/mp3/mid",":/radiologos/radiologos/br_heimat.png"],
                    "Audiophile Jazz"   : ["http://8.38.78.173:8210/stream/1/",":/radiologos/radiologos/audiophile_jazz.png"],
                    "Radio BUH"         : ["http://streaming.radio.co/saed08c46d/listen",":/radiologos/radiologos/radio-buh.png"],
                    "Afk max"           : ["http://stream.afkmax.de/afkmax-hq.mp3",":/radiologos/radiologos/afkmax.png"],
                    "Jazztime Nürnberg" : ["http://webradio.radiof.de:8000/radiof",":/radiologos/radiologos/jazztime_nbg.png"],
                    "Allzic Blues"      : ["http://allzic09.ice.infomaniak.ch/allzic09.mp3",":/radiologos/radiologos/allzicblues.png"],
                    "Allzic Jazz & Soul": ["http://jazzradio.ice.infomaniak.ch/jazzradio-high.mp3",":/radiologos/radiologos/allzicjazzsoul.png"]

}


if(__name__ == "__main__"):

    for key, value in radioStations.items():
        print(key, value[0], value[1])


