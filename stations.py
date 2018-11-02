radioStations = {   "Radio Gong"        : ["http://webstream.gong971.de/gong971",":/radiologos/radiologos/gong971.png"],
                    "StarFM"            : ["http://nbg.starfm.de/player/pls/nbg_pls_mp3.php.pls",":/radiologos/radiologos/starfm.jpg"],
                    "Antenne Bayern"    : ["http://www.antenne.de/webradio/antenne.m3u",":/radiologos/radiologos/antenne.png"],
                    "Rock Antenne"      : ["http://www.rockantenne.de/webradio/rockantenne.aac.pls",":/radiologos/radiologos/rockantenne.png"],
                    "Bayern 1"          : ["http://dg-br-http-fra-dtag-cdn.cast.addradio.de/br/br1/franken/mp3/128/stream.mp3?ar-distributor=f0a0",":/radiologos/radiologos/bayern1.png"],
                    "Bayern 2"          : ["http://dg-br-http-fra-dtag-cdn.cast.addradio.de/br/br2/nord/mp3/128/stream.mp3?ar-distributor=f0a0",":/radiologos/radiologos/bayern2.png"],
                    "BR Heimat"         : ["http://dg-br-http-fra-dtag-cdn.cast.addradio.de/br/brheimat/live/mp3/128/stream.mp3?ar-distributor=f0a0",":/radiologos/radiologos/br_heimat.png"],
                    "Audiophile Jazz"   : ["http://8.38.78.173:8210/stream/1/",":/radiologos/radiologos/audiophile_jazz.png"],
                    "Radio BUH"         : ["http://streaming.radio.co/saed08c46d/listen",":/radiologos/radiologos/radio-buh.png"],
                    "Jazztime Nürnberg" : ["http://webradio.radiof.de:8000/radiof",":/radiologos/radiologos/jazztime_nbg.png"]
}


if(__name__ == "__main__"):

    for key, value in radioStations.items():
        print(key, value[0], value[1])
