
The application was created to help in the accurate identification
of species of the genus _Eurygaster_ Laporte (Hemiptera, Scutelleridae), common in Russia and neighboring
countries (within the former USSR).

_Eurygaster integriceps_ (sunn pest, corn bug) – the main pest of wheat in Eastern Europe,
West Asia (Near and Middle East) and
Central Asia (Пучков, 1972; Paulian & Popov 1980, 1980; Нейморовец, 2006; Павлюшин и др., 2008, 2010, 2015;
Гричанов&Овсянникова 2003–2009).
This species is included in the "List of harmful organisms especially dangerous for plant products"
for the territory of Russia (Working Group of the VIZR, 2010).
The corn bug is morphologically very similar to _E. maura and E. testudinaria_ (Виноградова, 1959, Пучков, 1961, Кержнер, Ячевский, 1964,
Batzakis, 1972, Нейморовец, 2008, Сыромятников и др., 2017).

These three species are often found together in the wheat-growing area in the European part of the country.
Moreover, _E. maura_ is a pest (Пучков, 1972), but its number on wheat crops is much lower
than _E. integriceps. E. testudinaria_ has the widest distribution in the Palearctic,
and sometimes also occurs on wheat crops.
However, this species has not yet been registered as a pest of wheat (Пучков, 1961, 1972).
Even plant protection specialists cannot always distinguish between _E. integriceps, E. maura_ and _E. testudinaria_,
which sometimes leads to incorrect information about the pest population size during monitoring of
the _E. integriceps_ population on wheat crops. 
This affects the cost and efficiency of protective measures (Neimorovets, 2020).
In Russia there are also three species of the genus _Eurygaster_:
_E. austriaca_ (marked as a pest (Пучков, 1972), but currently is less common),
_E. dilaticollis_ and _E. laeviuscula_ (these two species are quite rare (Кужугет, 2010) and have no commercial value).

The recognition of species in the application is carried out using the convolutional neural network
[MobileNet V2](https://pytorch.org/hub/pytorch_vision_mobilenet_v2/).
The first model performs binary classification and seeks to identify the presence of _Eurygaster_ in the image.
The second model classifies _Eurygaster_ on a species level. The output of each model is
the distribution of the [confidence](https://en.wikipedia.org/wiki/Softmax_function) values that the image submitted to the input of the
model belongs to each of the possible types of _Eurygaster_.
It should be noted that one of the disadvantages of modern neural networks from the user point of view is
"overconfidence". 
Formally, this means that the models are not initially calibrated, i.e. the values of the model's confidence cannot
be directly associated with the concept of the probability of belonging
to one of the recognized species. To smooth out this problem, the models were calibrated using the 
[temperature scaling](https://arxiv.org/abs/1706.04599 ) method.

To train models, the authors of the project took specimens images from the collection of the Zoological Institute and
open databases [iNaturalist](www.inaturalist.org) and [MacroID](www.macroid.ru ).
The images were taken with a professional photosystem as well as a smartphone and a compact camera.


<left>
Copyright:<br/>
© The Zoological Institute RAS (ZISP)<br/>
© Designed by A. Popkov<br/>
© Text V. Neimorovets</left>


