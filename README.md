# Metar Map

WARNING: This project is still a work in progress so documentation may be incomplete!!!

There are a lot of different metar maps that display flight conditions but most
of them use a Raspberry Pi. I did not want to use a raspberry pi, instead I am
using an esp32 (an esp8266 should work as well) which are cheaper than a
Raspberry Pi, don't require an SD card and handles power-on/power-offs much
better than a Raspberry Pi because you don't need an sd card. It also boots
up much quicker.

## Getting Started

Things you'll need:
- NeoPixel lights or similar
- Something that will run micropython (I'm using an esp32)
- Wires and some solder
- a map and frame of some sort

To get started, you'll need to wire up your lights to your microcontroller.
A lot of people use the [WS2811 string lights](https://www.amazon.com/ALITOVE-LED-Individually-Addressable-Waterproof/dp/B01AG923GI/)
but these will stick out pretty far behind the back of the map and you'll need
something like a shadowbox frame. I am using the strip lights which are similar
to [these](https://www.amazon.com/ALITOVE-Individual-Addressable-Programmable-Non-Waterproof/dp/B01MG49QKD/)
(note: these aren't the exact ones I had but they should work)

So on your microcontroller, you'll want to wire up the 3v3 pin to the power of
the lights, and the GND to the ground of the lights. Then you need to pick a
pin to use to control the data line. I used GPIO15 which was right next to the
GND pin on my board to make wiring a little easier. This corresponds to the line:
```
pin = 15
```
in main.py at the top of the file. If you use a different pin, you'll need to
change this.

There are some other options but the next thing you'll want to change is the
airports dictionary. This is the `airports.json` file. The first part is the
airport identifier, the 2nd is the location of the pixel (0 based) in the chain.
So for example:
```
{
    "KEEN": 0,
    "KCON": 1
}
```
Defines 2 airports, the first is `KEEN` which is the first light, the second
is `KCON` which is the 2nd light. The order in the dict doesn't matter but
the number value does. Also this needs to be valid JSON.

I would suggest wiring up just one pixel first and make sure everything is working.
