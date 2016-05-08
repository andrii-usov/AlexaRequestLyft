## "I need a Lyft"

## Inspiration

We were inspired by capabilities of voice control system of Amazon Echo (Alexa) and decided to implement a new feature for it. We liked the idea of existing Uber application that allows people to call a cab however it has the very basic and limited functionality. So we took the idea and implemented a new, more informative Skill with richer functionality. Also, to provide a better service Uber has to have a competitor and Lyft is a worthy opponent !

## What it does

A new Skill allows Alexa to accept a ride requests using Lyft. After you tell Alexa your destination it will calculate approximate cost and duration of a ride and request a Lyft if you agree with conditions.

## How I built it

We used Amazon AWS Alexa Toolkit together with AWS Lamda to create a new Skill. Also, we used ESRI API for translation physical address to coordinated (geocoding) and Lyft API to perform requests to cab service. To train Alexa for address recognition we build a custom Slot Address Type with about 30k physical addressess and most popular touristic destinations of NYC.

## Challenges I ran into

It was challanging to train Alexa to understand the address information. Using a Slot was not obvious and took a time to implement. Also it was challanging to lync Lyft user accounts and handle tokens.

## Accomplishments that I'm proud of

We're proud to present a system with configured interaction between all its services. Although it has a space for enhancements we believe this is a pretty good start.

## What I learned

We learned how to create Alexa SKills, use Alexa Voice Services, Amazon WebServices API, manage sessions and tokens. 

## What's next for A ride with Lyft

To create ride status updates and create a wrapper for both - Uber and Lyft services to choose best available option to ride.
