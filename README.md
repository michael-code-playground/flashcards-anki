# flashcards-anki


As a foreign languages enthusiast and programming self-learner, I like to come up with ideas to merge those two fields. I've been working on my self-awareness and every time I spot some problem/weakness, I try to find the cause and address it. I set myself a goal to regularly, once a week, create flashcards containing words I looked up in a dictionary and export them to AnkiDroid so I could comfortably review them later on. I managed to stick to that plan for 2 weeks at best. I used to manually go through my Google search history once a week, pick up the words and save them. It became too tedious though and I started to neglect it. That's when it occurred to me that I could export my search history, create a Python script to do the work for me and save everything to a .csv file. I could then tailor those documents to my needs and put them into AnkiDroid (in case someone wonders, there's an option in the desktop app to import .csv files and specify which columns will be at the front/back). 

The code is pretty simple and adaptable, in my case I use cambridgedictionary as a source, that's why I extract records containing that particular title, but it can be replaced by anything. I name my files "pronunciation_date.csv", because I target my pronunciation, which also corresponds to the category name I defined in AnkiDroid - it helps me keep an organised and neat structure. I implemented a few functions featured in Pandas framework to remove duplicates and sort the rows descending by date. It's also possible to define how far the program should go back in the search history. 

Even though it may be "my case-specific", I think there's room to extend the program, make it more versatile and adapt it to one's requirements. The idea is simple, yet helpful :) I'm open to any suggestions on what I could incorporate and would be happy to join forces with someone and work together on it. 

The only flaw is that google doesn't provide any feature to have the takeout data automatically exported (or maybe I just haven't found it) which means it's necessary to head to the website manually and export Google search history. To introduce jus
t a tiny bit of automation, I created a simple batch script to unzip the file and copy it to the location where I store my Python script. 




