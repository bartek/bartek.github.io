title: weeknotes WK9
date: 02-17-2024
---

This week has been another one filled with disruptions due to a proper Nor'easter hitting Nova Scotia. Two weeks in a row of lots of snow!

Those disruptions mean more home time, and although it can be difficult to juggle the needs of both a 7 and 3 year old, the wife and I make it work. Often that is family time, but as the needs of the children are quite different, that means dedicated 1:1 time with each child. Some of that 1:1 time this week was spent in front of the computer building a new game!

Previously, H (7yo) and I tinkered with a few games. Our most "complete" project was pong in PICO-8, with a theme of "Canada vs. USA" hockey match. This was a simple game but it introduced H to high level concepts, improved his patience, X/Y coordinates, and allowed him to use PICO-8's built in editor to design the simple graphics.

What H enjoys most is the design aspect. As expected, he's full of ideas and he can surprise me with what he comes up with! It was on Monday (or maybe Tuesday?) this week before the snow storm that he came home with a drawing of a video game scene:

![H's Endless Runner Concept](/static/weeknotes/henry-endlessrunner.png)

In this scene, H described that you are _"always running, bad guys are throwing hammers and spikes at you, causing fire hydrants to explode, holes in the sidewalk, and oh also your lives are soda cans. Each hit is one soda can lost"_

On that snow storm evening we decided to sit down and explore how we'd build this game. I wanted something more rich than PICO-8, especially as the low fidelity can be difficult to work with. I decided to revisit the [LÖVE](https://love2d.org) framework, which allows one to write 2D games in Lua. I particularly enjoy writing Lua as it's a lean and simple language, doesn't get in my way, and the warts are minimal enough that I can dodge them fairly consistently.

However, simply coding the physics, building maps from scratch, and so forth would result in H sitting there twiddling his thumbs. I wanted to ensure we could have this cadence of dad coding and son designing, exploring ideas, and truly contributing to the effort.

Things began clicking when I found a YouTube channel by a fellow named [@Challacde](https://www.youtube.com/@Challacade). He has a collection of detailed but succint videos on developing games in love2d using a variety of existing plugins and tools:

* [windfield](https://github.com/a327ex/windfield) a physics module for love2d. This project is archived but it seems to be in a relatively strong place and not having to worry about the physics as much is nice!
* [hump](https://github.com/vrld/hump) is another collection of small game-making utilities. We used the camera module to handle the problem of “follow the player around a map”
* Finally, we used [Tiled](https://www.mapeditor.org) to make the actual maps/levels for the game. This is the “fun” part for my kiddo as he can basically be a game designer with very little friction.

This resulted in a flow of watching these videos while coding in parallel (picture in picture!), allowing me to get the basics in place and then layering on H's levels and ideas into the game. With physics, camera, and other nuance mostly out of the way we were able to get a very simple implementation going quite quickly! For H, it's just as fun to tinker with the game in its early implementation to see how things react to the variables we've placed on gravity, player speed, etc.

![H testing our early game](/static/weeknotes/henry-endlessrunner-test.png)

A screenshot from a video I took when H was tinkering with the game. We can see a little bit of the code and the level editing H had accomplished in view.

There is of course, much work to do! Teaching a young child scope and setting goals for a single night is a fun exercise for both of us. We'll hopefully have a few more hacking sessions next week. As well, I'll need to push this into my GitHub!
