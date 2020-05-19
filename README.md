[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="url"><img src="https://github.com/JonathanCourtois/Machine_Qlearning/blob/master/image/objects/submarineV3.PNG" align="center" height="48" width="60" ></a>
  
  <h3 align="center">Machine Qlearning</h3>

  <p align="center">
    Funny test application of Deep Qlearning on a Python Game!
  </p>
</p>
<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [The Game](#the-game)
* [Game rules](#game-rules)
* [The Network](#the-network)



<!-- ABOUT THE PROJECT -->
## About The Project

The project is juste a random initative of building a little game and train an IA on it. After few search, I had read that the Neuronal Network with reinforcement Qlearning was a good choice. 

<!-- THE GAME -->
## The Game

<p align="center">
<img width="300" src="https://github.com/JonathanCourtois/Machine_Qlearning/blob/master/image/Presentation/FirstBuild.PNG"/>
</p>

Underwater is an easy game. You are a submarine and you have to each a signal without dying. Beware of the naval mines !
<!-- GAME RULES -->
### Game rules.
You Start on left top corner 
<p align="center">
<img width="200" src="https://github.com/JonathanCourtois/Machine_Qlearning/blob/master/image/Presentation/FirstBuild.PNG"/>
</p>
Some naval mines are hidden. you have 5 actions possible:
- Move Up         : Go to the upper case
- Move Down       : Go to the lower case
- Move Left       : Go to the lefr case
- Move Right      : Go to the right case
<img width="100" src="https://github.com/JonathanCourtois/Machine_Qlearning/blob/master/image/Presentation/Direction.PNG"/>
- Use Your Sonar  : Scan a 5x5 box around you to seek naval mine

.You can use your sonar by pressing 'space' to detect naval mine
<p align="left">
<img width="200" src="https://github.com/JonathanCourtois/Machine_Qlearning/blob/master/image/Presentation/DetectMine.PNG"/>
<img width="200" src="https://github.com/JonathanCourtois/Machine_Qlearning/blob/master/image/Presentation/AllMines.PNG"/>
</p>
.Sonar range
<img width="100" src="https://github.com/JonathanCourtois/Machine_Qlearning/blob/master/image/Presentation/Sonar.PNG"/>

<!-- THE NETWORK -->
## The Network

Thanks to [Phil Tabor](https://github.com/philtabor) and his [video](https://www.youtube.com/watch?v=wc-FxNENg9U&t=2080s), on his youtube channel, I build a Deep_Q Network on [Python](https://www.python.org/) ([PyTorch coding](https://pytorch.org/)).
The newtork, in our case, is a 3 hidden layers Neuronal Network with Relu activation function.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/JonathanCourtois/Machine_Qlearning.svg?style=flat-square
[contributors-url]: https://github.com/JonathanCourtois/Machine_Qlearning/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/JonathanCourtois/Machine_Qlearning.svg?style=flat-square
[forks-url]: https://github.com/JonathanCourtois/Machine_Qlearning/network/members
[stars-shield]: https://img.shields.io/github/stars/JonathanCourtois/Machine_Qlearning.svg?style=flat-square
[stars-url]: https://github.com/JonathanCourtois/Machine_Qlearning/stargazers
[issues-shield]: https://img.shields.io/github/issues/JonathanCourtois/Machine_Qlearning.svg?style=flat-square
[issues-url]: https://github.com/JonathanCourtois/Machine_Qlearning/issues
[license-shield]: https://img.shields.io/github/license/JonathanCourtois/Machine_Qlearnin.svg?style=flat-square
[license-url]: https://github.com/JonathanCourtois/Machine_Qlearning/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/jonathan-courtois
[product-screenshot]: image/Presentation/FirstBuild.PNG
