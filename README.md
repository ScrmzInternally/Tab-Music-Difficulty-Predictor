# Tab-Music-Difficulty-Predictor
The aim of this project is to create a piece of software to read in a piece of music in tab form and output a difficulty level of the music. There are a massive amount of music files without any difficulty assigned to them, which oftentimes makes it difficult for musicians to decide on an appropriate music piece to play. Many who go through formal tuition will be given appropriate pieces of music by their teacher, but many who are self taught do not have this luxury
 
It uses Wayne Cripps TAB file, analysing the various features such as stretch required, note density, chord length, chord width and tempo change to create a model to test difficulty and train a Naive Bayes algorithm.

The end result is a predicted grade, followed by an accuracy statistic, followed by an optional confusion table displaying the distribution of the training set
