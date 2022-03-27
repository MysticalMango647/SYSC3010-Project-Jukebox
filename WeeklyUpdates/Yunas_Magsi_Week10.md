## Weekly Individual Project Update Report
### Group number: L3-G6
### Student name: Yunas Magsi
### Week: 8 (Give week number and also dates covered, where a week is Mon-Sun)_
___
1. **How many hours did you spend on the project this week? (0-10)**
  This week included 
  - Monday 2 hours
  - Tuesday 3.5 hours
  - Wednesday 4 hours

2. **Give rough breakdown of hours spent on 1-3 of the following:***
   (meetings, information gathering, design, research, brainstorming, evaluating options, prototyping options, writing/documenting, refactoring, testing, software implementation, hardware implementation)
   1. Setup all the code in one area and merging to have components working without interfrence. (5 hours)
   2. Prepare Code script for unit test demo (3 hours)
   3. Reset all wiring after my arduino mega got blown up (1.5 hour)
   
3. ***What did you accomplish this week?*** _(Be specific)_
  - This week i was able to succesfully merge a lot of the code to work together, right now the button, motor, and microphone work synchoniusly.
  - I set up the RGb library, switched from fastLed Arduino library to Neopixel, it offers better software for programming the rgb lights
  - I prepared an automated script for unit testing that is hardsfree and is good I might just keep it on the jukebox as a start up feature


4. ***How do you feel about your progress?*** _(brief, free-form reflection)_
  - Overall very good, there is a lot of good progress, The pyserial library started acting up so I am going to have to debug a bit more.

5. ***What are you planning to do next week***? _(give specific goals)_
  -  Setupt a code pattern going for the rgb leds, currently if i run the led lighting synchonous there is a bit of delay with the rest of the code as it takes too much processing
  -  implement a function that will calculate the percent change in the sound detector and the rgb lights change according to the percent change for the rgb lighting speed
  -  fix the pyserial communication issue that just started happening this week

6. ***Is anything blocking you that you need from others?*** _(What do you need from whom)_
  - not really, my system is pretty standalone
