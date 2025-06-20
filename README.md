# traffic-time-heatmap

This is a question which has been on my mind, especially with the traffic surge the city has seen in the past year. Is there some method to solve this madness ? Well, here is my approach to this problem, it helped me and might help you as well.

First, we need to understand the time it takes to travel from your home to office if you were to leave at 8 am, 8:15 am, ....., 9:45 am, 10 am and so on, for every day of the week. Google comes to the rescue with its distance matrix APIs which help you get exactly this. So, now I can see what the travel times are for all the options I could choose from.

Next, which option is best for me, should I choose the fastest travel time? Or should I choose something closer to my routine travel time ( which probably is better if I don't want to change too much of my daily routine )?

One way to look at this is to get a return on investment style metric ( ROI ) which considers two factors for any given time slot. 

Minutes saved by travelling early and Minutes you have to leave earlier 
Lets say my ideal travel time is currently 10:30 am where I will take 40 minutes to reach office, a slot at 9:30 am would take 30 minutes. So the ROI, in this case becomes minutes saved ( 10 minutes) divided by minutes you have to leave early ( 60 minutes) ~ 0.17

What you see above is a heatmap of just this ROI. Dark spots are something to avoid and Yellow spots are something to strive for. 

For me personally as with most of us, Friday's look to be the best day where even leaving closer to my routine time will not effect my travel much, leaving early on Thursday make sense as I get the best bang for my buck at 9:15, some days are just bad like Monday where you either leave super early or leave later.

Will I now breeze through traffic with this new-found understanding? Absolutely NOT! But it did help me get a hang of things. If you find this useful, see for yourself, access the python script in my github repo. You can change the travel source, destination, preferred slot to customize the script and get your own personal heatmap, which can help you answer the question - "When should I leave for office in Bengaluru traffic ?"
