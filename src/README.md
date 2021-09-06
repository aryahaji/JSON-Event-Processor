#Webflow Coding Challenge

Overall this was a very interesting coding challenge. I really enjoyed working 
on it as it strays away from the traditional interview questions and gears more towards 
the type of work that I could be doing at Webflow. 

After reading through the README and looking through the JSON file my thought was
to load the file and parse through each line (as each line in that file is one json object) 
and add it to a list. Initially I added each JSON object to the list and then started 
parsing the JSON based on the requirements, but then I realized it would be more optimal if
I did a check while reading the file to see if the `topic == SITE_EVENT`'. This way I only
add the JSON objects I want to parse into that list instead of all of them.

For the action type output I spent some time thinking about how I would implement that and read
a little bit about it through the link provided and determined that I would create
a default list with 0's for each type specified. Then I would do a series of checks to check
what the type is and based on that update the list with a 1 in the respective position.

Next came the hashing, I decided to go with SHA256 as it is more secure due to the 
larger bit size making it less susceptible to attacks. 

As far as the API call went I used the `requests` library to make the call and decided
to also use the `dotenv` library that way the API key isn't in the code. I also decided
to add the input path, output path, as well as the API URL in the .env file as well. Normally I would
not include the .env in the github but for the sake of this project I did just to showcase what I did.

Originally, in my `processData()` function I would create a new dictionary and set all the values
from parsing the JSON and then append that dictionary to a list. I had a loop to go through each object
and do that. When I ran it originally it took about 30-35 minutes to run due to the API calls. I wasn't
happy with how long it was taking to run so instead I decided to bring in the process of MultiThreading
so that I can have a bunch of API calls being made in parallel to make the program run faster. I figured 
this would work because order didn't really matter since the Data Science team requested the parsed json for analysis 
and to feed to their machine learning models. I went through a series of trial and error with the ThreadPool size due to getting a too many requests error and 
found that the ThreadPool size of 2 was able to not cause that to happen but still cut down the runtime by
about half. 

Finally, when it came down to the testing I wrote some tests and found out my code wasn't fully written
to handle edge cases I came up with, so I went back into the code and made the necessary changes.

To run the program navigate to the directory in which the files are located and
run `pip install -r requirements.txt` in order to ensure all the dependencies are installed. Navigate 
to the .env file and change the input path and output path variables to reflect your system.
Then through the command line navigate to `src` folder with `cd src/` command and run
`python3 main.py` and the program should start running :)



