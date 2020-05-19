[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="url"><img src="https://github.com/JonathanCourtois/Machine_Qlearning/blob/master/image/objects/submarineV3.PNG" align="center" height="48" width="55" ></a>
  
  <h3 align="center">Machine Qlearning</h3>

  <p align="center">
    Funny test application of Deep Qlearning on a Python Game!
  </p>
</p>
<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)



<!-- ABOUT THE PROJECT -->
## About The Project

<p align="center">
<img width="300" src="https://github.com/JonathanCourtois/Machine_Qlearning/blob/master/image/Presentation/FirstBuild.PNG"/>
</p>
<p align="left">
  The project is juste a random initative of building a little game and train an IA on it. After few search, I had read that the Neuronal Network with reinforcement Qlearning was a good choice. Thanks to [Phil Tabor](https://github.com/philtabor) and his [video](https://www.youtube.com/watch?v=wc-FxNENg9U&t=2080s), on his youtube channel, I build a Deep_Q Network on [Python](https://www.python.org/) ([PyTorch coding](https://pytorch.org/)).
</p> 
  
This script generates a Mackey-Glass time series using the 4th 
order Runge-Kutta method. The code is a straighforward translation 
in Julia of Matlab code, available [here](https://ww2.mathworks.cn/matlabcentral/fileexchange/24390-mackey-glass-time-series-generator?s_tid=prof_contriblnk).                                           
 

## Exemple

```julia
 using MackeyGlass
 using Plots

 T,X = MGGenerator()
 plot(T, X, label = "Mackey Glass")
```
<p align="center">
<img width="400px" src="https://github.com/JonathanCourtois/MackeyGlass/blob/master/MGplot.png"/>
</p>

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
